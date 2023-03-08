"""DTOs para la capa de infrastructura del dominio de rutas

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de rutas

"""

from alpesonline.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla ordenes y productos
ordenes_productos = db.Table(
    "ordenes_productos",
)

class Producto(db.Model):
    __tablename__ = "productos"


class Orden(db.Model):
    __tablename__ = "ordenes"

class EventosOrden(db.Model):
    __tablename__ = "eventos_orden"
