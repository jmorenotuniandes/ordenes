""" Excepciones del dominio de ordenes

En este archivo usted encontrará los Excepciones relacionadas
al dominio de ordenes

"""

from alpesonline.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioOrdenesExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de ordenes'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)