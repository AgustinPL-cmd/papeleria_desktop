from papeleria_app.models.producto import Producto
from papeleria_app.database.connection import get_connection

def insert_productos(nombre_producto, descripcion, precio_unitario_venta,
                     precio_unitario_compra, stock_actual, stock_minimo, id_categoria):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = (
            "INSERT INTO Productos (nombre_producto, descripcion, precio_unitario_venta, "
            "precio_unitario_compra, stock_actual, stock_minimo, id_categoria) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )

        #
        cursor.execute(query, (
            nombre_producto, descripcion, float(precio_unitario_venta),
            float(precio_unitario_compra), int(stock_actual), int(stock_minimo), int(id_categoria)
        ))

        conn.commit()
        return True, "Producto insertado correctamente."

    except Exception as e:
        print(f"Error al insertar producto: {e}")
        return False, f"Error al insertar producto: {e}"

    finally:
        if 'conn' in locals():
            conn.close()


def buscar_coincidencias(producto):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT * FROM Productos 
            WHERE nombre_producto LIKE %s;
        """
        # Agregamos % al inicio y final del término de búsqueda
        parametro_busqueda = f"%{producto}%"

        cursor.execute(query, (parametro_busqueda,))
        resultados = cursor.fetchall()

        return resultados

    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return []  # Devuelve lista vacía en caso de error

    finally:
        if conn and conn.is_connected():
            conn.close()


def producto_popular_semana_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT SUM(v.cantidad) as Cantidad, p.nombre_producto 
        From productos as P 
        Inner Join ventas as v On p.id_producto = v.productoId
        Where WEEK(v.fecha_venta,1) = WEEK(current_date(),1)
        Group By p.nombre_producto 
        Order By Cantidad Desc
        Limit 5
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return []

    finally:
        if conn and conn.is_connected():
            conn.close()

def producto_popular_semana_pasada():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT SUM(v.cantidad) AS Cantidad, p.nombre_producto 
        FROM productos AS p
        INNER JOIN ventas AS v ON p.id_producto = v.productoId
        WHERE WEEK(v.fecha_venta, 1) = WEEK(CURRENT_DATE(), 1) - 1
        GROUP BY p.nombre_producto 
        ORDER BY Cantidad DESC
        LIMIT 5
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar productos semana pasada: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()

def producto_popular_mes_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT SUM(v.cantidad) AS Cantidad, p.nombre_producto 
        FROM productos AS p
        INNER JOIN ventas AS v ON p.id_producto = v.productoId
        WHERE MONTH(v.fecha_venta) = MONTH(CURRENT_DATE())
          AND YEAR(v.fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY p.nombre_producto 
        ORDER BY Cantidad DESC
        LIMIT 5
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar productos mes actual: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def producto_popular_trimestre_actual():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT SUM(v.cantidad) AS Cantidad, p.nombre_producto 
        FROM productos AS p
        INNER JOIN ventas AS v ON p.id_producto = v.productoId
        WHERE QUARTER(v.fecha_venta) = QUARTER(CURRENT_DATE())
          AND YEAR(v.fecha_venta) = YEAR(CURRENT_DATE())
        GROUP BY p.nombre_producto 
        ORDER BY Cantidad DESC
        LIMIT 5
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar productos trimestre actual: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def obtener_todos_productos() -> list:
    """Obtiene todos los productos con información de categoría"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT p.*, c.nombre_categoria 
        FROM Productos as p
        INNER JOIN categorias as c ON c.id_categoria = p.id_categoria
        ORDER BY p.precio_unitario_venta, p.stock_actual
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Exception as err:
        print(f"Error al obtener productos: {err}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def aumentar_stock_producto(id_producto: int, cantidad: int) -> tuple:
    """
    Aumenta el stock de un producto en la cantidad especificada

    Args:
        id_producto: ID del producto a actualizar
        cantidad: Cantidad a agregar al stock (debe ser un número positivo)

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Validar que la cantidad sea positiva
        if cantidad <= 0:
            return False, "La cantidad debe ser un número positivo"

        conn = get_connection()
        cursor = conn.cursor()

        # Primero verificamos que el producto exista
        cursor.execute("SELECT id_producto FROM Productos WHERE id_producto = %s", (id_producto,))
        if not cursor.fetchone():
            return False, "El producto no existe"

        # Actualizamos el stock
        query = """
        UPDATE Productos 
        SET stock_actual = stock_actual + %s 
        WHERE id_producto = %s
        """
        cursor.execute(query, (cantidad, id_producto))
        conn.commit()

        # Verificamos si el stock actual supera el mínimo después del aumento
        cursor.execute("""
        SELECT stock_actual, stock_minimo 
        FROM Productos 
        WHERE id_producto = %s
        """, (id_producto,))
        stock_actual, stock_minimo = cursor.fetchone()

        # Si había una alerta pendiente y ahora el stock es suficiente, la marcamos como resuelta
        if stock_actual >= stock_minimo:
            cursor.execute("""
            UPDATE AlertasInventario 
            SET estado = 'resuelto' 
            WHERE productoId = %s AND estado = 'pendiente'
            """, (id_producto,))
            conn.commit()

        return True, f"Stock actualizado correctamente. Nuevo stock: {stock_actual}"

    except Exception as e:
        print(f"Error al aumentar stock del producto: {e}")
        conn.rollback()
        return False, f"Error al aumentar stock: {e}"

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()