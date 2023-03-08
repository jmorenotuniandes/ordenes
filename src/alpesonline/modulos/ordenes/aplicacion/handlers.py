from alpesonline.modulos.ordenes.dominio.eventos import OrdenCreada
from alpesonline.seedwork.aplicacion.handlers import Handler
from alpesonline.modulos.ordenes.infraestructura.despachadores import Despachador

class HandlerRutaIntegracion(Handler):

    @staticmethod
    def handle_ruta_programada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ruta')
