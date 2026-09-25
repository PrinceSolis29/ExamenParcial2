--Obtener todos los tickets con estado 'open' junto con el nombre de su solicitante
SELECT t.id, t.title, t.status, u.name AS requester_name
FROM tickets t
JOIN users u ON t.requester_id = u.id
WHERE t.status = 'open';

--Contar cuántos tickets tiene asignados cada técnico (excluyendo ceros, orden descendente)
SELECT u.id, u.name, COUNT(t.id) AS total_tickets
FROM users u
JOIN tickets t ON t.assignee_id = u.id
GROUP BY u.id, u.name
HAVING COUNT(t.id) > 0
ORDER BY total_tickets DESC;

--Encontrar todos los tickets que no tienen comentarios asociados
SELECT t.id, t.title
FROM tickets t
WHERE NOT EXISTS (
    SELECT 1 
    FROM comments c 
    WHERE c.ticket_id = t.id
);

--Demostración del comportamiento de ON DELETE CASCADE usando una transacción segura
BEGIN;
-- 1. Contar cuántos registros de historial existen asociados al ticket 1 antes de eliminarlo
SELECT COUNT(*) AS historial_antes_borrado FROM history_events WHERE ticket_id = 1;

-- 2. Eliminar el ticket con id = 1
DELETE FROM tickets WHERE id = 1;

-- 3. Comprobar que los registros hijos de historial se eliminaron automáticamente (debe dar 0)
SELECT COUNT(*) AS historial_despues_borrado FROM history_events WHERE ticket_id = 1;

-- 4. Aplicar ROLLBACK para que la base de datos cancele la eliminación y mantenga los datos originales intactos
ROLLBACK;
