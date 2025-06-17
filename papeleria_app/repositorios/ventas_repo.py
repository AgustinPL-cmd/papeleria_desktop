from os.path import curdir

from oauthlib.uri_validate import query

from papeleria_app.models.venta import Venta
from papeleria_app.database.connection import get_connection

from datetime import datetime, timedelta

def obtener_filtro_fecha(valor_dropdown):
    hoy = datetime.now().date()

    if valor_dropdown == "hoy":
        return hoy, hoy
    elif valor_dropdown == "ayer":
        ayer = hoy - timedelta(days=1)
        return ayer, ayer
    elif valor_dropdown == "semana":
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
        return inicio_semana, hoy
    elif valor_dropdown == "mes":
        inicio_mes = hoy.replace(day=1)
        return inicio_mes, hoy
    else:
        return None, None

def consultar_ventas_por_fecha_empleado(opcion_fecha, id_user):
    fecha_inicio, fecha_fin = obtener_filtro_fecha(opcion_fecha)
    try:
        conn =  get_connection()
        cursor = conn.cursor()

        query = """
            Select MAX(v.fecha_venta) as Fecha, v.numVenta as Venta, SUM(p.precio_unitario_venta*v.cantidad) as Total
            From Ventas as v
            INNER JOIN productos as p On v.productoId = p.id_producto
            WHERE DATE(v.fecha_venta) BETWEEN %s AND %s AND v.usuarioId = %s
            GROUP BY v.numVenta
            ORDER BY Fecha DESC
        """

        cursor.execute(query, (fecha_inicio, fecha_fin, id_user))
        resultados = cursor.fetchall()

        conn.close()
        return resultados
    except Exception as e:
        mensaje = f'Ha ocurrido un error inesperado {e}'
        return None, mensaje

    finally:
        if 'conn' in locals():
            conn.close()

def obtener_ventas_por_dia_empleado(usuario_id):
    try:

        conn = get_connection()
        cursor = conn.cursor()
        query="""
        SELECT 
            DAYNAME(v.fecha_venta) AS dia_semana,
            SUM(v.cantidad*p.precio_unitario_venta) AS total_vendido
        FROM Ventas v
        INNER JOIN productos as p On p.id_producto = v.productoId
        WHERE  v.usuarioId = %s
            AND YEARWEEK(v.fecha_venta, 1) = YEARWEEK(CURDATE(), 1)
        GROUP BY  dia_semana;
        """

        cursor.execute(query, (usuario_id,))
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        dias_ordenados = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dias_es = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        ventas_por_dia = {dias_es[d]: 0 for d in dias_ordenados}
        for dia, total in resultados:
            if dia in dias_es:
                ventas_por_dia[dias_es[dia]] = total

        return ventas_por_dia
    except Exception as e:
        mensaje = f'Ha ocurrido un error inesperado {e}'
        return None, mensaje

    finally:
        if 'conn' in locals():
            conn.close()


def obtener_venta_by_numVenta(numVenta):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT v.fecha_venta, v.cantidad, (v.cantidad*p.precio_unitario_venta) as Subtotal, 
            p.nombre_producto, p.precio_unitario_venta 
            FROM Ventas as v
            INNER JOIN productos as p On p.id_producto = v.productoId
            WHERE numVenta = %s
            ORDER BY p.precio_unitario_venta
        """


        cursor.execute(query, (numVenta,))
        resultados = cursor.fetchall()

        return resultados

    except Exception as e:
        print(f"Error en obtener_venta_by_numVenta: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def insertar_venta(fecha, cantidad, subtotal, numVenta, idProducto, idUsuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO VENTAS(fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId)
        values (%s, %s, %s, %s,%s, %s)
        """
        cursor.execute(query, (fecha, cantidad,subtotal, numVenta, idProducto, idUsuario))
        conn.commit()
        return True, "Venta insertado correctamente."
    except Exception as e:
        print(f"Error al insertar la venta: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def obtener_num_venta_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query="""
            SELECT MAX(numVenta) AS ultimo_numero_venta FROM Ventas
        """
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado

    except Exception as e:
        print(f"Error al obtener la venta actual: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()
