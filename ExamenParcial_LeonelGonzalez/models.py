from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empleados(db.Model):
    __tablename__ = 'Empleados'
    Empleado_ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Rol = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(255), nullable = False)
    # Relación con la tabla Asistencia
    Asistencia = db.relationship('Asistencia', backref='Empleado', lazy=True)


class Asistencia(db.Model):
    __tablename__ = 'Asistencia'
    Asistencia_ID = db.Column(db.Integer, primary_key=True)
    Empleado_ID = db.Column(db.Integer, db.ForeignKey('Empleados.Empleado_ID'), nullable=False)
    Fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Hora_Entrada = db.Column(db.Time, nullable=False)
    Hora_Salida = db.Column(db.Time, nullable=False)

    