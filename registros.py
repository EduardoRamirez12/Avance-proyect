from db import obtener_conexion


def insertar_citas(nombre, apellido_paterno,apellido_materno,email,tipo_sangre,numero, direccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(nombre, apellido_paterno, apellido_materno,email,tipo_sangre,numero,direccion) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                        (nombre, apellido_paterno, apellido_materno,email,tipo_sangre,numero,direccion))
    conexion.commit()
    conexion.close()


def obtener_citas():
    conexion = obtener_conexion()
    citas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, apellido_paterno, apellido_materno,email,tipo_sangre,numero,direccion FROM usuarios")
        citas = cursor.fetchall()
    conexion.close()
    return citas


def eliminar_cita(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_citas_por_id(id):
    conexion = obtener_conexion()
    cita = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT  id, nombre, apellido_paterno, apellido_materno,email,tipo_sangre,numero,direccion FROM usuarios WHERE id = %s", (id,))
        cita = cursor.fetchone()
    conexion.close()
    return cita


def actualizar_cita(nombre, apellido_paterno,apellido_materno,email,tipo_sangre,numero,direccion, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, email = %s, tipo_sangre = %s, numero = %s, direccion = %s WHERE id = %s",
                        (nombre, apellido_paterno,apellido_materno, email,tipo_sangre,numero,direccion, id))
    conexion.commit()
    conexion.close()