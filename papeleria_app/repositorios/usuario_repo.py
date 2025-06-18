from papeleria_app.database.connection import get_connection
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



def ventas_empleado_semana():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        Select Sum(v.cantidad), u.nombre
        From ventas as v
        Inner Join usuarios as u On v.usuarioId = u.id_usuario
        Where WEEK(v.fecha_venta,1) = WEEK(current_date(),1)
        group by u.nombre
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar usuarios: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def ventas_empleado_semana_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            u.nombre AS empleado,
            DAYNAME(v.fecha_venta) AS dia_semana,
            Sum(v.cantidad) AS total_ventas,
            SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas v
        INNER JOIN Productos p ON p.id_producto = v.productoId
        INNER JOIN Usuarios u ON u.id_usuario = v.usuarioId
        WHERE WEEK(v.fecha_venta, 1) = WEEK(CURRENT_DATE(), 1)
          AND YEAR(v.fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY u.nombre, dia_semana
        ORDER BY u.nombre, FIELD(dia_semana, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar usuarios : {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()

def ventas_empleado_semana_pasada():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            u.nombre AS empleado,
            DAYNAME(v.fecha_venta) AS dia_semana,
            Sum(v.cantidad) AS total_ventas,
            SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas v
        INNER JOIN Productos p ON p.id_producto = v.productoId
        INNER JOIN Usuarios u ON u.id_usuario = v.usuarioId
        WHERE WEEK(v.fecha_venta, 1) = WEEK(CURRENT_DATE(), 1) - 1
          AND YEAR(v.fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY u.nombre, dia_semana
        ORDER BY u.nombre, FIELD(dia_semana, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar usuarios: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def ventas_empleado_mes_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            u.nombre AS empleado,
            WEEK(v.fecha_venta, 1) AS semana,
            COUNT(*) AS total_ventas,
            SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas v
        INNER JOIN Productos p ON p.id_producto = v.productoId
        INNER JOIN Usuarios u ON u.id_usuario = v.usuarioId
        WHERE MONTH(v.fecha_venta) = MONTH(CURRENT_DATE())
          AND YEAR(v.fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY u.nombre, semana
        ORDER BY u.nombre, semana;
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar usuarios: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def ventas_empleado_trimestre_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            u.nombre AS empleado,
            MONTH(v.fecha_venta) AS mes,
            COUNT(*) AS total_ventas,
            SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas v
        INNER JOIN Productos p ON p.id_producto = v.productoId
        INNER JOIN Usuarios u ON u.id_usuario = v.usuarioId
        WHERE QUARTER(v.fecha_venta) = QUARTER(CURRENT_DATE())
          AND YEAR(v.fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY u.nombre, mes
        ORDER BY u.nombre, mes;
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar usuarios: {e}")
        return []
    finally:
        if conn and conn.is_connected():
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