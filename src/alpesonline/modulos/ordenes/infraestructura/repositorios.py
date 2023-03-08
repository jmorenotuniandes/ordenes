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
        raise NotImplementedError

    def obtener_todos(self) -> list[Orden]:
        raise NotImplementedError

    def agregar(self, evento):
        raise NotImplementedError

    def actualizar(self, orden: Orden):
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        raise NotImplementedError
