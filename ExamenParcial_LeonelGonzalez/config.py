import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://Leonel:Leonel@PC-DEV14/Gestion_Empleados?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)