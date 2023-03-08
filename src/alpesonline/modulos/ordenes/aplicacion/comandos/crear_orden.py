from alpesonline.seedwork.aplicacion.comandos import Comando
from alpesonline.modulos.ordenes.aplicacion.dto import ProductoDTO, OrdenDTO, UbicacionDTO
from .base import CrearOrdenBaseHandler
from dataclasses import dataclass
from alpesonline.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpesonline.modulos.ordenes.aplicacion.mapeadores import MapeadorOrden
from alpesonline.modulos.ordenes.infraestructura.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes

@dataclass
class CrearOrden(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    client_id: str
    origen: UbicacionDTO 
    destino: UbicacionDTO 
    tipo: str 
    productos: list[ProductoDTO]

class CrearOrdenHandler(CrearOrdenBaseHandler):
    
    def handle(self, comando: CrearOrden):
        orden_dto = OrdenDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   client_id=comando.client_id
            ,   origen=comando.origen
            ,   destino=comando.destino
            ,   tipo=comando.tipo
            ,   productos=comando.productos)

        orden: Orden = self.fabrica_ordenes.crear_objeto(orden_dto, MapeadorOrden())
        orden.crear_orden(orden)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CrearOrden)
def ejecutar_comando_crear_orden(comando: CrearOrden):
    handler = CrearOrdenHandler()
    handler.handle(comando)
    