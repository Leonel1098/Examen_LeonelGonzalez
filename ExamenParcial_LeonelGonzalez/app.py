from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Empleados,Asistencia
from config import Config
from datetime import datetime, timedelta


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#Inicializa la ruta del Login 
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password'] 
        
        # Busca el usuario por email y valida su existencia
        user = Empleados.query.filter_by(Email=email).first()
        
        #Agrega el parametro del campo ROl 
        if user:  
            session['user_id'] = user.Empleado_ID
            session['user_role'] = user.Rol 
            
            if user.Rol == 'Administrador':
                return redirect(url_for('admin_dashboard'))
            elif user.Rol == 'Empleado':
                return redirect(url_for('dashboard_empleado'))
            else:
                flash('Rol desconocido', 'danger')
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('login.html')

#Metodo para la eleccion del formulario dependiendo el rol del empleado
#Formulario para el empleado Administrador
@app.route('/admin')
def admin_dashboard():
    if 'user_role' in session and session['user_role'] == 'Administrador':
        # Mostrar dashboard para el administrador
        return render_template('index.html')
    else:
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('login'))
    
#Formulario para el Empleado Normal
@app.route('/empleado')
def dashboard_empleado():
    if 'user_role' in session and session['user_role'] == 'Empleado':
        # Mostrar dashboard para el empleado
        return render_template('index_Empleado.html')
    else:
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('login'))



#CRUD Empleados
#Crear Metodo Para Ingresar Empleados
@app.route('/empleados', methods=['GET', 'POST'])
def crear_Empleado():
    if request.method == 'POST':
        #Aqui creamos un nuevo Empleado
        new_empleado = Empleados(
            Nombre=request.form['Nombre'],
            Apellido=request.form['Apellido'],
            Email=request.form['Email'],
            Rol=request.form['Rol'],
            Password=request.form['Password'],
        )
        db.session.add(new_empleado)
        db.session.commit()
        return redirect(url_for('login'))
    
    empleados = Empleados.query.all()
    return render_template('Registrar_Empleado.html', empleados = empleados)


#Crear Metodo Para Listar Empleados
@app.route("/empleados/lista")
def listar_Empleados():
    nombre = request.args.get('Nombre')
    rol = request.args.get("Rol")

    query = Empleados.query

    if nombre:
        query = query.filter(Empleados.Nombre.ilike(f'%{nombre}%'))
    if rol:
        query = query.filter(Empleados.Rol.ilike(f'%{rol}%'))
    
    empleados = query.all()
    return render_template('Lista_Empleados.html', empleados = empleados)


#Actualizar Empleado
@app.route('/empleados/actualizar/<int:Empleado_ID>', methods=['GET', 'POST'])
def actualizar_Empleado(Empleado_ID):
    empleado = Empleados.query.get_or_404(Empleado_ID)

    if request.method == 'POST':
        empleado.Nombre = request.form.get('Nombre', empleado.Nombre)
        empleado.Apellido = request.form.get('Apellido', empleado.Apellido)
        empleado.Email = request.form.get('Email', empleado.Email)
        empleado.Rol = request.form.get('Rol', empleado.Rol)
        empleado.Password = request.form.get('Password', empleado.Password)
        try:
            db.session.commit()
            flash('Empleado Actualizado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar empleado: {e}', 'error')
        
        return redirect(url_for('listar_Empleados'))

    return render_template('Actualizar_Empleado.html', empleado = empleado)



#Metodo para Eliminar Empleado
@app.route('/empleados/eliminar/<int:Empleado_ID>', methods=['POST'])
def eliminar_Empleado(Empleado_ID):
    empleado = Empleados.query.get_or_404(Empleado_ID)
    db.session.delete(empleado)
    db.session.commit()
    return redirect(url_for('listar_Empleados'))



#Metodos Para Asistencia
@app.route('/empleado/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        empleado_id = request.form['Empleado_ID']
        tipo_registro = request.form['Tipo_Registro']  
        empleado = Empleados.query.filter_by(Empleado_ID=empleado_id).first()
        
        if empleado:
            ahora = datetime.utcnow()
            if tipo_registro == 'entrada':
                # Registrar la hora de  entrada del empleado 
                nueva_asistencia = Asistencia(
                    Empleado_ID=empleado_id,
                    Fecha=ahora,
                    Hora_Entrada=ahora.time(),
                    #La salida obtiene valor cuando el empleado vuelve a registrar su asistencia pero con la opcion de salida
                    Hora_Salida=None 
                )
                db.session.add(nueva_asistencia)
                db.session.commit()
                flash('Entrada registrada correctamente', 'success')
            elif tipo_registro == 'salida':
                # Registrar la salida
                asistencia = Asistencia.query.filter_by(Empleado_ID=empleado_id, Hora_Salida=None).first()
                if asistencia:
                    asistencia.Hora_Salida = ahora.time()
                    db.session.commit()
                    flash('Salida registrada correctamente', 'success')
                else:
                    flash('No se encontró una entrada sin salida registrada', 'danger')
            else:
                flash('Tipo de registro no válido', 'danger')
        else:
            flash('Empleado no encontrado', 'danger')
        
        return redirect(url_for('registro'))

    return render_template('Asistencia_Empleado.html')

#Crear Metodo Para Listar Registros de Asistencia de los Empleados
@app.route("/empleado/registro/lista")
def listar_Registros():
    query = Asistencia.query
    asistencias = query.all()
    return render_template('Lista_Registros.html', asistencias = asistencias)




#Metodo parar Crear los reportes de Asistencia de los Empleados
@app.route('/reportes', methods=['GET', 'POST'])
def reportes():
    if request.method == 'POST':
        # Obtener los parámetros del formulario
        empleado_id = request.form.get('Empleado_ID')
        fecha_inicio = request.form.get('Fecha_Inicio')
        fecha_fin = request.form.get('Fecha_Fin')
        tipo_reporte = request.form.get('Tipo_Reporte')

        # Construir el filtro de fecha basado en el tipo de reporte, diario, semanal o mensual
        if tipo_reporte == 'diario':
            fecha_inicio = fecha_fin = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        elif tipo_reporte == 'semanal':
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = fecha_inicio + timedelta(weeks=1)
        elif tipo_reporte == 'mensual':
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = (fecha_inicio.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        else:
            flash('Tipo de reporte no válido', 'danger')
            return redirect(url_for('reportes'))

        # Consultar la base de datos
        query = Asistencia.query
        if empleado_id:
            query = query.filter_by(Empleado_ID=empleado_id)
        if fecha_inicio and fecha_fin:
            query = query.filter(Asistencia.Fecha.between(fecha_inicio, fecha_fin))
        
        reportes = query.all()

        return render_template('Reporte_Empleado.html', reportes=reportes, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, tipo_reporte=tipo_reporte)

    return render_template('Reporte_Empleado.html')


if __name__ == '__main__':
    app.run(debug=True)