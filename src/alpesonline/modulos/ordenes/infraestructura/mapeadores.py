""" Mapeadores para la capa de infrastructura del dominio de rutas

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from alpesonline.seedwork.dominio.repositorios import Mapeador
from alpesonline.seedwork.infraestructura.utils import unix_time_millis
from alpesonline.modulos.ordenes.dominio.entidades import Orden, Producto
from alpesonline.modulos.ordenes.dominio.eventos import OrdenCreada, EventoOrden

from .dto import Orden as OrdenDTO
from .dto import Producto as ProductoDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosOrden(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            OrdenCreada: self._entidad_a_orden_creada
        }

    def obtener_tipo(self) -> type:
        return EventoOrden.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_orden_creada(self, entidad: OrdenCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import OrdenCreadaPayload, EventoOrdenCreada

            payload = OrdenCreadaPayload(
                id_orden=str(evento.id_orden),
                id_cliente=str(evento.id_cliente),
                tipo =str(evento.tipo),
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoOrdenCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'OrdenCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpesonline'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)

    def entidad_a_dto(self, entidad: EventoOrden, version=LATEST_VERSION) -> OrdenDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: OrdenDTO, version=LATEST_VERSION) -> Orden:
        raise NotImplementedError


class MapeadorOrden(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_producto_dto(self, productos_dto: list) -> list[Producto]:
        productos = list()
        
        for producto_dto in productos_dto:
            producto = Producto()
            producto.id = producto_dto.id
            productos.append(producto)


        return [Producto(productos)]

    def _procesar_producto(self, producto: any) -> ProductoDTO:
        producto_dto = ProductoDTO()
        producto_dto.id = producto.id
        producto_dto.nombre = producto.nombre

        return producto_dto

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        
        orden_dto = OrdenDTO()
        orden_dto.fecha_creacion = entidad.fecha_creacion
        orden_dto.fecha_actualizacion = entidad.fecha_actualizacion
        orden_dto.id = str(entidad.id)

        productos_dto = list()
        
        for producto in entidad.productos:
            productos_dto.extend(self._procesar_producto(producto))

        orden_dto.ordenes = productos_dto

        return orden_dto

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        orden.productos = list()

        ordenes_dto: list[ProductoDTO] = dto.productos

        orden.productos.extend(self._procesar_producto_dto(ordenes_dto))
        
        return orden