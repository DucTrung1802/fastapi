from typing import ClassVar

from pydantic import EmailStr
from neontology import BaseNode, BaseRelationship


# NODES with validation
class User(BaseNode):
    __primarylabel__: ClassVar[str] = "User"
    __primaryproperty__: ClassVar[str] = "email"

    full_name: str
    email: EmailStr
    password: str


class Profile(BaseNode):
    __primarylabel__: ClassVar[str] = "Profile"


class Name(BaseNode):
    __primarylabel__: ClassVar[str] = "Name"
    value: str


# RELATIONSHIPS
class HasProfile(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "HasProfile"
    source: User
    target: Profile


class HasName(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "HasName"
    source: Profile
    target: Name
