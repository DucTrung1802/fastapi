from typing import ClassVar
from neontology import BaseNode, BaseRelationship


# NODES
class Patient(BaseNode):
    __primarylabel__: ClassVar[str] = "Patient"
    __primaryproperty__: ClassVar[str] = "username"
    username: str
    password: str
    email: str


class Profile(BaseNode):
    __primarylabel__: ClassVar[str] = "Profile"


class Name(BaseNode):
    __primarylabel__: ClassVar[str] = "Name"
    value: str


# RELATIONSHIPS
class HasProfile(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "HasProfile"
    source: Patient
    target: Profile


class HasName(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "HasName"
    source: Profile
    target: Name
