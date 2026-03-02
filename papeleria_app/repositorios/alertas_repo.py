from papeleria_app.database.connection import get_connection

def obtener_alertas_inventario():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                p.nombre_producto,
                p.stock_actual,
                p.stock_minimo,
                a.estado,
                a.fecha_alerta
            FROM alertasinventario a
            INNER JOIN productos p ON a.productoId = p.id_producto
            WHERE a.estado = 'pendiente'
            ORDER BY a.fecha_alerta DESC
        """

        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados  # Lista de diccionarios

    except Exception as e:
        print(f"Error al obtener alertas: {e}")
        return []

    finally:
        if conn is not None:
            conn.close()