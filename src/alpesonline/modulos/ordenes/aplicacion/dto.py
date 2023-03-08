from dataclasses import dataclass, field
from alpesonline.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class UbicacionDTO(DTO):
    longitud: str
    latitud: str

@dataclass(frozen=True)
class ProductoDTO(DTO):
    id: str
    nombre: str

@dataclass(frozen=True)
class OrdenDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    client_id: str = field(default_factory=str)
    origen: UbicacionDTO = None
    destino: UbicacionDTO = None
    tipo: str = field(default_factory=str)
    productos: list[ProductoDTO] = field(default_factory=list)
