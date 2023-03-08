from alpesonline.seedwork.aplicacion.comandos import ComandoHandler
from alpesonline.modulos.ordenes.infraestructura.fabricas import FabricaRepositorio
from alpesonline.modulos.ordenes.dominio.fabricas import FabricaOrdenes

class CrearOrdenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ordenes: FabricaOrdenes = FabricaOrdenes()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_ordenes(self):
        return self._fabrica_ordenes    
    