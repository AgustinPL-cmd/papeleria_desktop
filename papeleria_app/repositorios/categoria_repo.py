from papeleria_app.database.connection import get_connection
from papeleria_app.models.categoria import Categoria


def get_categorias():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(buffered=True)  # Usar cursor buffered
        query = "SELECT id_categoria, nombre_categoria FROM Categorias"
        cursor.execute(query)

        # Consumir todos los resultados inmediatamente
        categorias = [Categoria(row[0], row[1]) for row in cursor.fetchall()]
        return categorias
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_categoria_by_name(categoria_nombre):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(buffered=True)  # Usar cursor buffered
        query = "SELECT id_categoria, nombre_categoria FROM Categorias WHERE nombre_categoria = %s"
        cursor.execute(query, (categoria_nombre,))

        # Consumir el resultado inmediatamente
        fila = cursor.fetchone()

        if fila:
            return Categoria(id_categoria=fila[0], nombre_categoria=fila[1])
        return None
    except Exception as e:
        print(f"Error al obtener categoría por nombre: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()