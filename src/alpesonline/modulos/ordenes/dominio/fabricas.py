""" Fábricas para la creación de objetos del dominio de rutas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de rutas

"""

from .entidades import Orden
from .excepciones import TipoObjetoNoExisteEnDominioOrdenesExcepcion
from alpesonline.seedwork.dominio.repositorios import Mapeador
from alpesonline.seedwork.dominio.fabricas import Fabrica
from alpesonline.seedwork.dominio.entidades import Entidad
from alpesonline.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaOrden(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            return mapeador.dto_a_entidad(obj)

@dataclass
class FabricaOrdenes(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Orden.__class__:
            fabrica_orden = _FabricaOrden()
            return fabrica_orden.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioOrdenesExcepcion()

