/*Tabla Empleados (empleados)
empleado_id (PK)
nombre
apellido
email
rol (admin/empleado)
password

Tabla Asistencia (asistencia)
• asistencia_id (PK)
• empleado_id (FK)
• fecha
• hora_entrada
• hora_salida*/

CREATE DATABASE Gestion_Empleados
USE Gestion_Empleados


Create Table Empleados(
Empleado_ID int Primary Key Identity (1,1),
Nombre NVarchar (50),
Apellido Nvarchar (50),
Email NVarchar (100),
Rol NVarchar (20),
Password NVarchar (255)
);


Create Table Asistencia(
Asistencia_ID Int Primary Key Identity(1,1),
Empleado_ID Int,
Fecha Date,
Hora_Entrada Time,
Hora_Salida Time,
Constraint FK_Empleados Foreign Key (Empleado_ID) References Empleados(Empleado_ID));


select * from Empleados
select * from Asistencia