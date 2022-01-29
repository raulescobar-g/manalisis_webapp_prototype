from .. import db
from datetime import datetime
from flask_login import UserMixin


class manalisis_Users(db.Model, UserMixin):
    __tablename__ = 'MANALISIS_USERS'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(40),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(50),nullable = False)
    phone = db.Column(db.String(20),nullable = False)

    user_receipt = db.relationship('Receipt',backref='user')

    def __repr__(self):
        return '<Task %r>' % self.id


class Receipt(db.Model):
    __tablename__ = 'RECEIPT'
    receipt_id = db.Column(db.Integer, primary_key = True)
    place = db.Column(db.String(50),nullable=True)
    time = db.Column(db.String(20),nullable=True)
    total = db.Column(db.Float(2) ,nullable=False)
    iva = db.Column(db.Float(2),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    file_loc = db.Column(db.String(100),nullable=True)
    cost = db.Column(db.String(20),nullable=False)
    rfc = db.Column(db.String(20),nullable=True)
    address = db.Column(db.String(100),nullable=True)
    phonee = db.Column(db.String(20),nullable=True)
    project_id = db.Column(db.String(20))
    user_id = db.Column(db.Integer,db.ForeignKey('MANALISIS_USERS.id'))
    
    xml = db.relationship('XML',backref='receipt',uselist=False)

    def __repr__(self):
        return '<Task %r>' % self.receipt_id


class XML(db.Model):
    __tablename__ = 'XML'
    id = db.Column(db.Integer, primary_key = True)
    rfc = db.Column(db.String(20), nullable = False)
    date = db.Column(db.String(20), nullable = False)
    total = db.Column(db.Float(2),nullable = False)
    iva = db.Column(db.Float(2), nullable=False)
    file_loc = db.Column(db.String(50), nullable = False)

    receipt_id_xml = db.Column(db.Integer,db.ForeignKey('RECEIPT.receipt_id'))

    def __repr__(self):
        return '<Task %r>' % self.id


class Ordenes_Muestreo_2(db.Model):
    __tablename__ = "ORDENES_MUESTREO_2"
    id = db.Column(db.Integer, primary_key=True)
    clave_empresa_muestreo = db.Column(db.String(4))
    fecha_registro_orden = db.Column(db.Date)
    numero_cliente = db.Column(db.Integer)
    numero_planta = db.Column(db.Integer)
    numero_contacto = db.Column(db.Integer)
    numero_solicitud_orden = db.Column(db.Integer)
    clave_empresa_administracion = db.Column(db.String(4))
    importe = db.Column(db.Float(2))
    fecha_inicio = db.Column(db.DateTime)
    clave_empresa_factura = db.Column(db.String(4))
    observaciones = db.Column(db.String(256))
    fecha_envio = db.Column(db.Date)
    envio_electronico = db.Column(db.String(1))
    paqueteria = db.Column(db.String(80))
    numero_guia = db.Column(db.String(32))
    ajuste = db.Column(db.Float(2))
    fecha_ajuste = db.Column(db.Date)
    elaboro = db.Column(db.Integer)
    terminada = db.Column(db.Date)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
    ot = db.Column(db.Integer)
    cot = db.Column(db.Integer)
    expincompleto = db.Column(db.String(1))

    def __repr__(self):
        return '<Task %r>' % self.id


class Gastos_Solicitudes_Viaticos(db.Model):
    __tablename__ = "GASTOS_SOLICITUDES_VIATICOS"
    numero_solicitud_viatico = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime)
    numero_orden = db.Column(db.String(14))
    numero_orden_1 = db.Column(db.String(14))
    empresa_gasto = db.Column(db.String(8))
    empresa_emisora = db.Column(db.String(14))
    numero_proveedor = db.Column(db.Integer)
    fecha_hora_aplicacion = db.Column(db.DateTime)
    fecha_hora_salida = db.Column(db.DateTime)
    fecha_hora_regreso = db.Column(db.DateTime)
    numero_ciudad_origen = db.Column(db.Integer)
    numero_ciudad_destino = db.Column(db.Integer)
    destino = db.Column(db.String(64))
    vale_azul = db.Column(db.Float(3))
    vale_azul_descripcion = db.Column(db.String(128))
    devolucion = db.Column(db.Float(3))
    otros_descripcion = db.Column(db.String(128))
    observaciones = db.Column(db.String(256))
    solicitante = db.Column(db.String(256))
    pagado = db.Column(db.DateTime)
    complemento = db.Column(db.DateTime)
    compl_pagado = db.Column(db.DateTime)
    comprobado = db.Column(db.DateTime)
    enviada = db.Column(db.DateTime)
    bloqueada = db.Column(db.DateTime)
    obs_admin = db.Column(db.String(256))
    deleted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    poliza_pagado = db.Column(db.Integer)
    poliza_compl = db.Column(db.Integer)
    poliza_ajuste = db.Column(db.Integer)
    mensajes = db.Column(db.String(256))
    pernocta = db.Column(db.Boolean)

    def __repr__(self):
        return '<Task %r>' % self.numero_solicitud_viatico


class Gastos_Solicitudes_2(db.Model):
    __tablename__ = "GASTOS_SOLICITUDES_2"
    numero_solicitud_gastos = db.Column(db.Integer, primary_key=True)
    fecha_solicitud = db.Column(db.DateTime) 
    numero_orden = db.Column(db.String(14))
    desciprcion = db.Column(db.String(256))
    numero_proveedor = db.Column(db.Integer)
    fecha_hora_aplicacion = db.Column(db.DateTime)
    centro_costo = db.Column(db.String(8))
    empresa_gasto = db.Column(db.String(8))
    numero_cuenta = db.Column(db.Integer)
    importe = db.Column(db.Float(2))
    iva = db.Column(db.Float(2))
    isr = db.Column(db.Float(2))
    retencion_iva = db.Column(db.Float(2))
    solicitante = db.Column(db.String(24))

    def __repr__(self):
        return '<Task %r>' % self.numero_solicitud_viatico


class Gastos_Viaticos_Desgloza(db.Model):
    __tablename__ = "GASTOS_VIATICOS_DESGLOZA"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    importe = db.Column(db.Float(3))
    complemento = db.Column(db.Float(3))
    comprobado = db.Column(db.Float(3))
    viaticosidfk = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at =db.Column(db.DateTime)

    def __repr__(self):
        return '<Task %r>' % self.id


class Beneficiarios(db.Model):
    __tablename__ = "BENEFICIARIOS"
    numero_beneficiario = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(128))
    rfc = db.Column(db.String(32))
    anadio = db.Column(db.Integer)
    deleted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    lg = db.Column(db.Boolean)
    evt = db.Column(db.Boolean)
    mi = db.Column(db.Boolean)
    viejo = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r>' % self.numero_beneficiario
