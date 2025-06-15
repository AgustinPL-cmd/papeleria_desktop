
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

def buscar_productos_por_nombre(nombre_busqueda):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id_producto, nombre_producto, descripcion, 
               precio_unitario_venta, precio_unitario_compra, 
               stock_actual, stock_minimo, id_categoria
        FROM Productos
        WHERE nombre_producto LIKE %s
        """

        cursor.execute(query, (f"%{nombre_busqueda}%",))

        resultados = cursor.fetchall()

        productos = []
        for r in resultados:
            producto = Producto(
                id_producto=r[0],
                nombre=r[1],
                descripcion=r[2],
                precio_venta=r[3],
                precio_compra=r[4],
                stock=r[5],
                stock_min=r[6],
                id_categoria=r[7]
            )
            productos.append(producto)

        return productos

    except Exception as e:
        print(f"Error al buscar productos: {e}")
        return []

    finally:
        if conn:
            conn.close()


def actualizar_producto(producto: Producto):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE Productos 
        SET nombre_producto = %s,
            descripcion = %s,
            precio_unitario_venta = %s,
            precio_unitario_compra = %s,
            stock_actual = %s,
            stock_minimo = %s,
            id_categoria = %s
        WHERE id_producto = %s
        """

        cursor.execute(query, (
            producto.nombre,
            producto.descripcion,
            producto.precio_venta,
            producto.precio_compra,
            producto.stock,
            producto.stock_min,
            producto.id_categoria,
            producto.id_producto
        ))

        conn.commit()
        return True, "Producto actualizado correctamente."

    except Exception as e:
        return False, f"Error al actualizar producto: {e}"

    finally:
        if conn:
            conn.close()