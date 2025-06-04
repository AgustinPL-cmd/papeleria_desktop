from papeleria_app.database.connection import get_connection
from papeleria_app.models.categoria import  Categoria

def get_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    query = "Select id_categoria, nombre_categoria From Categorias"
    cursor.execute(query)
    categorias = []
    for (id_categoria, nombre_categoria) in cursor:
        categorias.append(Categoria(id_categoria, nombre_categoria))
    cursor.close()
    conn.close()
    return categorias


def get_categoria_by_name(categoria_nombre):
    conexion = get_connection()
    cursor = conexion.cursor()
    query = "SELECT * FROM Categorias WHERE nombre_categoria = %s"
    cursor.execute(query, (categoria_nombre,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()

    if fila:
        return Categoria(id_categoria=fila[0], nombre_categoria=fila[1])
    else:
        return None

