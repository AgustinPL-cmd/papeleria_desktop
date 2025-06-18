import flet as ft

def alert_usuario_info(page):
    try:
        # Obtener datos del usuario desde el almacenamiento local
        usuario_data = page.client_storage.get("usuario")
        user = usuario_data["user"]

        # Preparar datos
        nombre = user["nombre"]
        rol = user["rol"]
        estado = "Activo ✅" if user["activo"] else "Inactivo ❌"
        id_usuario = user["id_usuario"]

        # Construir contenido del diálogo
        content_list = [
            ft.Text(f"👤 ID de Usuario: {id_usuario}", size=16),
            ft.Text(f"🧑 Nombre: {nombre}", size=16),
            ft.Text(f"🔐 Rol: {rol.upper()}", size=16),
            ft.Text(f"📌 Estado: {estado}", size=16, color=ft.Colors.GREEN if user["activo"] else ft.Colors.RED),

        ]

        # Crear diálogo
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Información del Usuario", text_align=ft.TextAlign.CENTER),
            content=ft.Column(content_list, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor="#0B1D51"
        )

        return dlg

    except Exception as ex:
        print(f"Error creando diálogo de usuario: {ex}")
        return ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(f"No se pudo cargar la información del usuario: {str(ex)}"),
            actions=[ft.TextButton("Cerrar")]
        )

def cerrar_dialogo(page):
    if page.dialog:
        page.dialog.open = False
        page.update()




