from enum import StrEnum
import uuid


class ChatRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatSession:
    def __init__(self, session_id: str | None = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.history = []

    def add_message(self, role: ChatRole, content: str):
        self.history.append({"role": role, "content": content})

    def get_history(self) -> list[dict[str, str]]:
        return self.history

    def __repr__(self):
        return f"ChatSession(session_id='{self.session_id}', history={self.history})"


class ChatManager:
    def __init__(self):
        self.sessions: dict[str, ChatSession] = {}

    def create_session(self) -> str:
        session = ChatSession()
        self.sessions[session.session_id] = session
        return session.session_id

    def get_session(self, session_id: str) -> ChatSession | None:
        return self.sessions.get(session_id)

    def add_message(self, *, session_id: str, role: ChatRole, content: str) -> bool:
        session = self.get_session(session_id)
        if session:
            session.add_message(role, content)
            return True
        return False

    def get_history(self, session_id: str) -> list[dict[str, str]] | None:
        session = self.get_session(session_id)
        return session.get_history() if session else None

    def remove_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        else:
            return False

    def clear_sessions(self):
        self.sessions.clear()
