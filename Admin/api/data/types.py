from dataclasses import dataclass


@dataclass
class action:
    type: str
    member_id: int


@dataclass
class reply_message:
    date: int
    from_id: int
    text: str
    attachments: list
    conversation_message_id: int
    id: int
    peer_id: int


@dataclass
class Message:
    date: int
    from_id: int
    id: int
    out: int
    attachments: list
    conversation_message_id: int
    fwd_messages: list
    important: bool
    is_hidden: bool
    peer_id: int
    random_id: int
    text: str
    args: list = None
    reply_message: reply_message = None
    action: action = None


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    can_access_closed: bool
    is_closed: bool

