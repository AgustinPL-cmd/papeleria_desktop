
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
        return False, f"Error al insertar la venta: {e}"
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


def ventas_semana_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
        DAYNAME(fecha_venta) AS dia_semana,
        COUNT(*) AS total_ventas,
        SUM(v.cantidad*p.precio_unitario_venta) AS total_ingresos,
        Sum(v.cantidad*p.precio_unitario_venta) - Sum(v.cantidad*p.precio_unitario_compra) as ganancia_neta
        FROM Ventas as v
        Inner Join productos as p On p.id_producto = v.productoId
        WHERE WEEK(fecha_venta, 1) = WEEK(CURRENT_DATE(), 1)
        AND YEAR(fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY dia_semana
        ORDER BY FIELD(dia_semana, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def ventas_semana_pasada():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
        DAYNAME(fecha_venta) AS dia_semana,
        COUNT(*) AS total_ventas,
        SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
        SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas AS v
        INNER JOIN productos AS p ON p.id_producto = v.productoId
        WHERE WEEK(fecha_venta, 1) = WEEK(CURRENT_DATE(), 1) - 1
          AND YEAR(fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY dia_semana
        ORDER BY FIELD(dia_semana, 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def ventas_mes_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            CEIL(DAY(fecha_venta) / 7) AS semana_del_mes,
            COUNT(*) AS total_ventas,
            SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas AS v
        INNER JOIN productos AS p ON p.id_producto = v.productoId
        WHERE MONTH(fecha_venta) = MONTH(CURRENT_DATE())
          AND YEAR(fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY semana_del_mes
        ORDER BY semana_del_mes;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def ventas_trimestre_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT 
            MONTH(fecha_venta) AS mes,
            COUNT(*) AS total_ventas,
            SUM(v.cantidad * p.precio_unitario_venta) AS total_ingresos,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
        FROM Ventas AS v
        INNER JOIN productos AS p ON p.id_producto = v.productoId
        WHERE fecha_venta >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)
          AND MONTH(fecha_venta) <= MONTH(CURRENT_DATE())
          AND YEAR(fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY mes
        ORDER BY mes;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def consultar_ventas_por_fecha(opcion_fecha):
    fecha_inicio, fecha_fin = obtener_filtro_fecha(opcion_fecha)
    try:
        conn =  get_connection()
        cursor = conn.cursor()

        query = """
            Select MAX(v.fecha_venta) as Fecha, v.numVenta as Venta, SUM(p.precio_unitario_venta*v.cantidad) as Total,
            SUM(v.cantidad * p.precio_unitario_venta) - SUM(v.cantidad * p.precio_unitario_compra) AS ganancia_neta
            From Ventas as v
            INNER JOIN productos as p On v.productoId = p.id_producto
            WHERE DATE(v.fecha_venta) BETWEEN %s AND %s
            GROUP BY v.numVenta
            ORDER BY Fecha DESC
        """

        cursor.execute(query, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()

        conn.close()
        return resultados
    except Exception as e:
        mensaje = f'Ha ocurrido un error inesperado {e}'
        return None, mensaje

    finally:
        if 'conn' in locals():
            conn.close()
