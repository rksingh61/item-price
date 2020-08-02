from typing import Dict
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
import requests
import uuid
import re
from models.model import Model


@dataclass(eq=False)
# This will prevent us from doing two alert objects
class Item(Model):
    # collection = "items" i.e. name of the Table in DB
    # collection string is converted into a data class.
    # It is not going to be included in Init Method and default is going to be "items".
    collection: str = field(init=False, default="items")
    item_name: str
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    #now we no longer require post_init method,
    # also this parameter is available as init method.
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        s_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d+\.\d+)")
        match = pattern.search(s_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        return self.price

    # Convert a Python Object to JSON to be stored in MongoDB.
    def json(self) -> Dict:
        return {
            "_id": self._id,
            "item_name": self.item_name,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, iname: str) -> "Item":
        return cls.find_one_by("item_name", iname)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Item":
        url_regex = {"$regex": '^{}'.format(url_prefix)}  # make sure it starts with URL Prefix.
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Item":
        """
        Return a store from a url like "http://www.johnlewis.com/item/sdfj4h5g4g21k.html"
        :param url: The item's URL
        :return: a Store
        """
        pattern = re.compile(r"(https?://.*?/)")  # ?: Match both http or https://something/
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)

    """
    @classmethod
    def all(cls) -> List["Item"]:
        #items_from_db = Database.find("items", {})
        items_from_db = Database.find(cls.collection, {})
        # cls is current class i.e. Item ** passes respective 4 arguments to the constructor
        # Converts list of item dictionaries to list of item objects.
        # Returns a list of item object and not list/cursor dictionaries.
        return [cls(**item) for item in items_from_db]
   """

    # Defined in Model
    # @classmethod
    # def all(cls) -> List["Item"]:
    # def get_by_id(cls, _id) -> "Item":
    # def save_to_mongodb(self):

