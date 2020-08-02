from typing import Dict
import uuid
from dataclasses import dataclass, field
from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors


# NOTE: We don't use ==> from models.user import User, UserErrors
# the above definition creates all class objects defined in errors.py into an object UserErrors

@dataclass(eq=False)
class User(Model):
    collection: str = field(init=False, default="users")
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this e-mail was not found.')

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        my_user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, my_user.password):
            raise UserErrors.IncorrectPasswordError('Password Entered was incorrect.')
        return True


    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        """
        This method registers a user using e-mail and password.
        :param email: user's e-mail (might be invalid)
        :param password: password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail does not have the right format.')

        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('The e-mail you used to register already exists.')
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }
