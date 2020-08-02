from typing import List, TypeVar, Type, Dict, Union
from abc import ABCMeta, abstractmethod
from common.database import Database

Typ = TypeVar('Typ', bound='Model')


class Model(metaclass=ABCMeta):
    # remove the warnings and force child class to define Collection & _id.
    collection: str
    _id: str

    # remove the warnings
    def __init__(self, *args, **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def get_by_id(cls: Type[Typ], _id: str) -> Typ:
        # return cls(**Database.find_one(cls.collection, {"_id": _id}))
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls: Type[Typ]) -> List[Typ]:
        element_from_db = Database.find(cls.collection, {})
        # Sub class has Collection defined and hence warning is OK
        # However you cannot construct the Model object as there is no construtor in this class.
        # also it has an abstract method and hence it can't be constructed.
        return [cls(**elem) for elem in element_from_db]

    @classmethod
    def find_one_by(cls: Type[Typ], attribute: str, value: Union[str, Dict]) -> Typ:
        if Database.find_one(cls.collection, {attribute: value}) is None:
            return None
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[Typ], attribute: str, value: Union[str, Dict]) -> List[Typ]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]
