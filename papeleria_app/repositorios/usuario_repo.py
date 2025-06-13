from papeleria_app.database.connection import get_connection
import papeleria_app.models.usuario
from papeleria_app.models.usuario import Usuario


def verificar_usuario(user, password):
    mensaje = ''
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = (
            "SELECT * FROM usuarios "
            "WHERE nombre = %s AND contrasena = %s"
        )

        cursor.execute(query, (user, password))

        result = cursor.fetchone()

        if result:
            if result[4]:
                usuario = Usuario(result[0], result[1],result[2], result[3], result[4])
                mensaje = "LOGIN EXITOSO!"
                return usuario, mensaje
            else:
                mensaje = f'El usuario {result[1]} ya no está activo.'
                return None, mensaje
        else:
            mensaje = f'El usuario o contraseña son incorrectos'
            return None, mensaje

    except Exception as e:
        mensaje = f'Ha ocurrido un error inesperado {e}'
        return None, mensaje

    finally:
        if 'conn' in locals():
            conn.close()


def insert_empleado(usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = (
            "INSERT INTO Usuarios (nombre, contrasena, rol, activo) "
            "VALUES (%s, %s, %s, %s)"
        )

        cursor.execute(query, (
            usuario.nombre,
            usuario.contrasena,        # aquí va la contraseña tal cual
            usuario.rol,
            usuario.activo
        ))

        conn.commit()
        return True, "Empleado insertado correctamente."

    except Exception as e:
        print(f"Error al insertar empleado: {e}")
        return False, f"Error al insertar empleado: {e}"

    finally:
        if 'conn' in locals():
            conn.close()
