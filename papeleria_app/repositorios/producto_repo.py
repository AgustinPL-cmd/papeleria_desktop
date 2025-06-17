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