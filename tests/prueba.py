from app.models.entities import Ticket
from app.models.enums import TicketStatus
from app.repositories.memory import InMemoryTicketRepository

def test_count_by_status_report():
    # 1. Instanciar el repositorio que modificamos
    repo = InMemoryTicketRepository()
    
    # 2. Crear y agregar tickets dummy con diferentes estados
    t1 = Ticket(id=1, title="T1", description="D1", category="C1", priority="P1", requester_id=10, status=TicketStatus.OPEN)
    t2 = Ticket(id=2, title="T2", description="D2", category="C2", priority="P2", requester_id=20, status=TicketStatus.OPEN)
    t3 = Ticket(id=3, title="T3", description="D3", category="C3", priority="P3", requester_id=30, status=TicketStatus.CLOSED)
    
    repo.add(t1)
    repo.add(t2)
    repo.add(t3)
    
    # 3. Invocar el nuevo método del Ejercicio 5
    reporte = repo.count_by_status()
    
    # 4. Validar que cuente de forma exacta usando texto plano como pide el examen
    assert reporte.get("open") == 2
    assert reporte.get("closed") == 1
