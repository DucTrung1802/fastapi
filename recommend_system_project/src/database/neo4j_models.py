from typing import ClassVar
from neontology import BaseNode, BaseRelationship


# class TeamNode(BaseNode):
#     __primaryproperty__: ClassVar[str] = "teamname"
#     __primarylabel__: ClassVar[str] = "Team"
#     teamname: str
#     slogan: str = "Better than the rest!"


# class TeamMemberNode(BaseNode):
#     __primaryproperty__: ClassVar[str] = "nickname"
#     __primarylabel__: ClassVar[str] = "TeamMember"
#     nickname: str


# class BelongsTo(BaseRelationship):
#     __relationshiptype__: ClassVar[str] = "BELONGS_TO"
#     source: TeamMemberNode
#     target: TeamNode


# NODES
class Patient(BaseNode):
    __primarylabel__: ClassVar[str] = "Patient"
    __primaryproperty__: ClassVar[str] = "username"
    username: str
    password: str


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
