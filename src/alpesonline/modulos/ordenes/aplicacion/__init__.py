from pydispatch import dispatcher

from .handlers import HandlerOrdenIntegracion

from alpesonline.modulos.ordenes.dominio.eventos import OrdenCreada

dispatcher.connect(HandlerOrdenIntegracion.handle_orden_creada, signal=f'{OrdenCreada.__name__}Integracion')