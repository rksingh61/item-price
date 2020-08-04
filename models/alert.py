from typing import Dict
import uuid
from dataclasses import dataclass, field
from models.item import Item
from models.user import User
from models.model import Model
from libs.mailgun import Mailgun


@dataclass(eq=False)
# This will prevent us from doing two alert objects
class Alert(Model):
    # collection = "alerts"
    # collection string is converted into a data class.
    # It is not going to be included in Init Method and default is going to be "Alerts".
    collection: str = field(init=False, default="alerts")
    alert_name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    # But the data class can't take care of self.item which is not passed as a parameter
    # Also, the lamda methods can return a value, but can't access the parameter values.
    # to solve this there is __post_init__ method
    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "alert_name": self.alert_name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self) -> None:
        print(f"NOTIFY : {self}")
        if self.item.price < self.price_limit:
            print(f"Item ID: {self.item._id} Name: {self.item.item_name} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")
            resp = Mailgun.send_email(
                email=[self.user_email],
                subject=f"Notification for {self.item.item_name}",
                text=f"Your alert {self.item.item_name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.alert_name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}. Click <a href="{self.item.url}>here</a> to purchase your item.</p>'
            )
            print(f"Mail Sent Successfully {resp}")
