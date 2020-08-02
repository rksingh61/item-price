from typing import Dict
from dataclasses import dataclass, field
import uuid
import re
from models.model import Model


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="stores")
    store_name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.price = None

    # Convert a Python Object to JSON to be stored in MongoDB.
    def json(self) -> Dict:
        return {
            "_id": self._id,
            "store_name": self.store_name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, sname: str) -> "Store":
        return cls.find_one_by("store_name", sname)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": '^{}'.format(url_prefix)}  # make sure it starts with URL Prefix.
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return a store from a url like "http://www.johnlewis.com/item/sdfj4h5g4g21k.html"
        :param url: The item's URL
        :return: a Store
        """
        pattern = re.compile(r"(https?://.*?/)")  # ?: Match both http or https://something/
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
