import flet as ft
from papeleria_app.models.usuario import Usuario
from papeleria_app.repositorios.usuario_repo import insert_empleado
from papeleria_app.ui.components.logo_header import Logo_header


def alta_empleado_view(page: ft.Page):
    header = Logo_header("papeleria_app/images/logo_blanco.jpg").getHeader()

    nombre_input = ft.TextField(
        label="NOMBRE",
        width=300,
        bgcolor="#ffffff",
        border_color="#90a4ae",
        focused_border_color="#5c6bc0",
        label_style=ft.TextStyle(color="black"),
        color="black"
    )
    rol_input = ft.TextField(
        value="Empleado",
        label="ROL",
        width=300,
        disabled=True,
        bgcolor="#f0f0f0",
        border_color="#b0bec5",
        label_style=ft.TextStyle(color="black"),
        color="black"
    )
    estado_input = ft.TextField(
        value="ACTIVO",
        label="ESTADO",
        width=300,
        disabled=True,
        bgcolor="#f0f0f0",
        border_color="#b0bec5",
        label_style=ft.TextStyle(color="black"),
        color="black"

    )
    contrasena_input = ft.TextField(
        label="CONTRASEÑA",
        password=True,
        can_reveal_password=True,
        width=300,
        bgcolor="#ffffff",
        border_color="#90a4ae",
        focused_border_color="#5c6bc0",
        label_style=ft.TextStyle(color="black"),
        color="black"
    )

    mensaje = ft.Text("", color="red", size=14, text_align=ft.TextAlign.CENTER)

    def registrar(e):
        if nombre_input.value.strip() != "" and contrasena_input.value.strip() != "":
            nuevo = Usuario(
                nombre=nombre_input.value,
                contrasena=contrasena_input.value,
                rol="empleado",
                activo=True
            )
            try:
                insert_empleado(nuevo)
                mensaje.value = "Empleado registrado correctamente"
                mensaje.color = "green"
            except Exception as ex:
                mensaje.value = f"Error al registrar: {ex}"
                mensaje.color = "red"
                print("ERROR:", ex)
        else:
            mensaje.value = "Los campos no pueden estar vacíos"
            mensaje.color = "red"
        page.update()

    def cancelar(e):
        nombre_input.value = ""
        contrasena_input.value = ""
        mensaje.value = ""
        page.update()
        page.go("/")

    form_container = ft.Container(
        width=500,
        height=520,
        padding=30,
        border_radius=20,
        bgcolor="#d8d5eb",
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=25, color="#aaa", spread_radius=1, offset=ft.Offset(3, 6)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Text("ALTA DE EMPLEADOS", size=22, weight="bold", color="#333"),
                nombre_input,
                rol_input,
                estado_input,
                contrasena_input,
                mensaje,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Container(
                            content=ft.ElevatedButton(
                                "GUARDAR", on_click=registrar, style=ft.ButtonStyle(
                                    bgcolor="#5c6bc0", color="white"
                                )
                            ),
                            width=140,
                            border_radius=30,
                            shadow=ft.BoxShadow(blur_radius=10, color="#888")
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "CANCELAR", on_click=cancelar, style=ft.ButtonStyle(
                                    bgcolor="#ef5350", color="white"
                                )
                            ),
                            width=140,
                            border_radius=30,
                            shadow=ft.BoxShadow(blur_radius=10, color="#888")
                        )
                    ]
                )
            ]
        )
    )

    layout = ft.Column(
        expand=True,
        controls=[
            header,
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                bgcolor="#cdf3ff",
                content=form_container
            )
        ]
    )

    return layout

