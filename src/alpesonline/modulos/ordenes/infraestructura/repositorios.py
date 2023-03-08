""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de rutas

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de rutas

"""

from alpesonline.config.db import db
from alpesonline.modulos.ordenes.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes
from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.modulos.ordenes.dominio.fabricas import FabricaOrdenes
from .dto import Orden as OrdenDTO
from .dto import EventosOrden
from .mapeadores import MapeadorOrden, MapadeadorEventosOrden
from uuid import UUID
from pulsar.schema import *

class RepositorioOrdenesSQLAlchemy(RepositorioOrdenes):

    def __init__(self):
        self._fabrica_ordenes: FabricaOrdenes = FabricaOrdenes()

    @property
    def fabrica_ordenes(self):
        return self._fabrica_ordenes

    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_ordenes.crear_objeto(orden_dto, MapeadorOrden())

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, orden: Orden):
        orden_dto = self.fabrica_ordenes.crear_objeto(orden, MapeadorOrden())

        db.session.add(orden_dto)

    def actualizar(self, orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosOrdenSQLAlchemy(RepositorioEventosOrdenes):

    def __init__(self):
        self._fabrica_ordenes: FabricaOrdenes = FabricaOrdenes()

    @property
    def fabrica_ordenes(self):
        return self._fabrica_ordenes

    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_ordenes.crear_objeto(orden_dto, MapadeadorEventosOrden())
        
    def obtener_todos(self) -> list[Orden]:
        raise NotImplementedError

    def agregar(self, evento):
        orden_evento = self.fabrica_ordenes.crear_objeto(evento, MapadeadorEventosOrden())
        parser_payload = JsonSchema(orden_evento.data.__class__)
        json_str = parser_payload.encode(orden_evento.data)
        evento_dto = EventosOrden()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_orden)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(orden_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(orden_evento.service_name)
        evento_dto.contenido = json_str
        db.session.add(evento_dto)

    def actualizar(self, orden: Orden):
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        raise NotImplementedError
