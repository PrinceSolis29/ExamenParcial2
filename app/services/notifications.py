from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    user_id: int
    title: str
    message: str

    @property
    def to_user_id(self) -> int:
        return self.user_id


class Notifier(ABC):
    @abstractmethod
    def notify(self, user_id: int, title: str, message: str) -> None:
        raise NotImplementedError


class NullNotifier(Notifier):
    def notify(self, user_id: int, title: str, message: str) -> None:
        return None


class ConsoleNotifier(Notifier):
    def notify(self, user_id: int, title: str, message: str) -> None:
        print(f"[{title}] user={user_id}: {message}")


class RecordingNotifier(Notifier):
    def __init__(self) -> None:
        self.sent: list[Notification] = []

    @property
    def notifications(self) -> list[Notification]:
        return list(self.sent)

    def notify(self, user_id: int, title: str, message: str) -> None:
        self.sent.append(Notification(user_id=user_id, title=title, message=message))
        
class WebhookNotifier(Notifier):
    def __init__(self) -> None:
        self.sent_payloads: list[dict] = []

    def notify(self, user_id: int, title: str, message: str) -> None:
        # Almacena de forma polimórfica los datos en un diccionario dentro de la lista
        self.sent_payloads.append({
            "user_id": user_id,
            "title": title,
            "message": message
        })
        
