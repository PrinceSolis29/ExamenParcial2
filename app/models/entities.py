from dataclasses import dataclass, field
from datetime import datetime
from app.domain.errors import ValidationError
from app.models.comments import Comment
from app.models.enums import Role, TicketStatus


@dataclass
class HistoryEvent:
    id: int
    ticket_id: int
    actor_id: int
    event_type: str
    detail: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    @property
    def action(self) -> str:
        return self.event_type

    @property
    def details(self) -> str:
        return self.detail


@dataclass
class User:
    id: int
    name: str
    email: str
    role: Role = Role.REQUESTER

    @property
    def is_staff(self) -> bool:
        return Role(self.role) in {
            Role.TECHNICIAN,
            Role.SUPERVISOR,
            Role.ADMINISTRATOR,
        }


@dataclass
class Ticket:
    id: int
    title: str
    description: str
    category: str
    priority: str
    requester_id: int
    status: TicketStatus = TicketStatus.OPEN
    assignee_id: int | None = None
    comments: list[Comment] = field(default_factory=list)
    history: list[HistoryEvent] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now().astimezone()
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now().astimezone()
    )
    # Requisito: Lista interna por instancia protegida, fuera del constructor e ignorada en el repr
    _tags: list[str] = field(default_factory=list, init=False, repr=False)

    @property
    def is_open(self) -> bool:
        return self.status not in (TicketStatus.CLOSED, TicketStatus.CANCELLED)

    @property
    def is_assigned(self) -> bool:
        return self.assignee_id is not None

    # Requisito: Propiedad de solo lectura que devuelve una tupla
    @property
    def tags(self) -> tuple[str, ...]:
        return tuple(self._tags)

    # Requisito: Método seguro con validaciones, normalización en minúsculas y eliminación de duplicados
    def add_tag(self, tag: str) -> None:
        if not tag:
            raise ValidationError("La etiqueta no puede estar vacía.")
        
        normalized_tag = tag.strip().lower()
        if not normalized_tag:
            raise ValidationError("La etiqueta no puede contener únicamente espacios en blanco.")
            
        if normalized_tag not in self._tags:
            self._tags.append(normalized_tag)