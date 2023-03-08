from alpesonline.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from alpesonline.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from alpesonline.modulos.ordenes.infraestructura.fabricas import FabricaRepositorio
from alpesonline.modulos.ordenes.infraestructura.repositorios import RepositorioOrdenes
from alpesonline.modulos.ordenes.dominio.entidades import Orden
from alpesonline.modulos.ordenes.dominio.objetos_valor import Ubicacion
from alpesonline.modulos.ordenes.infraestructura.dto import Orden as OrdenDTO

from alpesonline.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class ProyeccionOrden(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionOrdenesLista(ProyeccionOrden):
    #TODO: agregar los demas campos para guardar en BD
    def __init__(self, id_ruta):
        self.id_ruta = id_ruta
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        
        repositorio.agregar(
            Orden(id=str(self.id_ruta), origen=Ubicacion("123","123"), destino=Ubicacion("123","123")))
        
        db.session.commit()

class ProyeccionOrdenHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionOrden):
        from alpesonline.config.db import db
        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionOrdenesLista)
def ejecutar_proyeccion_orden(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionOrdenHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    