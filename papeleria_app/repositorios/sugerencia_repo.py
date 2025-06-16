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
