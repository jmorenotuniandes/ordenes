from pydispatch import dispatcher

from .handlers import HandlerRutaIntegracion

from alpesonline.modulos.ordenes.dominio.eventos import OrdenCreada

dispatcher.connect(HandlerRutaIntegracion.handle_ruta_programada, signal=f'{OrdenCreada.__name__}Integracion')