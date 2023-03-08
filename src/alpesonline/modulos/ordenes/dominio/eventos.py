from __future__ import annotations
from dataclasses import dataclass, field
from alpesonline.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoOrden(EventoDominio):
    ...

@dataclass
class OrdenCreada(EventoOrden):
    id_orden: uuid.UUID = None
    id_cliente: uuid.UUID = None
    tipo: str = None
    productos: list = None
    fecha_creacion: datetime = None
    