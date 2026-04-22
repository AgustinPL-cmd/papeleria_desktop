from papeleria_app.database.connection import get_connection

from papeleria_app.models.sugerencia_cliente import SugerenciaCliente

def obtener_sugerencias():
    sugerencias = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SugerenciasClientes")
        for row in cursor.fetchall():
            sugerencias.append(SugerenciaCliente(*row))
    except Exception as e:
        print(f"❌ Error al obtener sugerencias: {e}")
    finally:
        if conn:
            conn.close()
    return sugerencias

def eliminar_sugerencia(id_sugerencia):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SugerenciasClientes WHERE id_sugerencia = %s", (id_sugerencia,))
        conn.commit()
    except Exception as e:
        print(f"❌ Error al eliminar sugerencia: {e}")
    finally:
        if conn:
            conn.close()

def insert_sugerencia(sugerencia: SugerenciaCliente):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = (
            "INSERT INTO SugerenciasClientes (producto_sugerido, comentario) "
            "VALUES (%s, %s)"
        )
        cursor.execute(query, (sugerencia.producto_sugerido, sugerencia.comentario))
        conn.commit()
        return True, "Sugerencia guardada correctamente"
    except Exception as e:
        print(f"❌ Error al insertar sugerencia: {e}")
        return False, f"Error: {e}"
    finally:
        if 'conn' in locals():
            conn.close()

