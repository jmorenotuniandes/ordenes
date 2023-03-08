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
    'ordenes_productos',
    db.Model.metadata,
    db.Column('orden_id', db.String(40), db.ForeignKey('ordenes.id')),
    db.Column('producto_id', db.String(40)),
    db.Column('nombre', db.String(20)),
    db.ForeignKeyConstraint(
        ['producto_id', 'nombre'],
        ['productos.id', 'productos.nombre']
    )
)


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.String(40), primary_key=True)
    nombre = db.Column(db.String(20), primary_key=True, nullable=True)


class Orden(db.Model):
    __tablename__ = 'ordenes'
    id = db.Column(db.String(40), primary_key=True)
    id_cliente = db.Column(db.String(40), nullable=True)
    tipo = db.Column(db.String(40), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    productos = db.relationship(
        'Producto', secondary=ordenes_productos, backref='ordenes')


class EventosOrden(db.Model):
    __tablename__ = 'eventos_orden'
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
