from alpesonline.seedwork.aplicacion.dto import Mapeador as AppMap
from alpesonline.seedwork.dominio.repositorios import Mapeador as RepMap
from alpesonline.modulos.ordenes.dominio.entidades import Producto, Orden
from alpesonline.modulos.ordenes.dominio.objetos_valor import Ubicacion
from .dto import OrdenDTO, ProductoDTO, UbicacionDTO

from datetime import datetime

class MapeadorOrdenDTOJson(AppMap):
    def _procesar_ubicacion(self, ubicacion: dict) -> UbicacionDTO:
        return UbicacionDTO(ubicacion.get('longitud'), ubicacion.get('latitud'))
    
    def _procesar_producto(self, orden: dict) -> ProductoDTO:                
        return ProductoDTO(orden.get('id'), orden.get('nombre')) 
    
    def externo_a_dto(self, externo: dict) -> OrdenDTO:
        orden_dto = OrdenDTO("","","",externo.get('client_id'), 
        self._procesar_ubicacion(externo.get('origen')), 
        self._procesar_ubicacion(externo.get('destino')), externo.get('tipo'))

        for producto in externo.get('productos', list()):
            orden_dto.productos.append(self._procesar_producto(producto))

        return orden_dto

    def dto_a_externo(self, dto: OrdenDTO) -> dict:
        return dto.__dict__

class MapeadorOrden(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_producto(self, producto_dto: ProductoDTO) -> Producto:
        return Producto(id=producto_dto.id, nombre=producto_dto.nombre)

    def _procesar_ubicacion(self, ubicacion_dto: UbicacionDTO) -> Ubicacion:
        return Ubicacion(longitud=ubicacion_dto.longitud, latitud=ubicacion_dto.latitud)

    def obtener_tipo(self) -> type:
        return Orden.__class__
    
    def entidad_a_dto(self, entidad: Orden) -> OrdenDTO:
        return OrdenDTO("","","",[])

    def dto_a_entidad(self, dto: OrdenDTO) -> Orden:
        orden = Orden(origen = self._procesar_ubicacion(dto.origen), destino = self._procesar_ubicacion(dto.destino))
        orden.client_id = dto.client_id
        orden.tipo = dto.tipo
        orden.productos = list()

        ordenes_dto: list[ProductoDTO] = dto.productos

        for orden_dto in ordenes_dto:
            orden.productos.append(self._procesar_producto(orden_dto))
        
        return orden
