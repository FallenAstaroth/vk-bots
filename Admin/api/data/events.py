from dataclasses import dataclass


@dataclass
class Actions:

    ChatInviteNewUser: str = "chat_invite_user"
    ChatInviteUserByLink: str = "chat_invite_user_by_link"
    ChatKickUser: str = "chat_kick_user"
