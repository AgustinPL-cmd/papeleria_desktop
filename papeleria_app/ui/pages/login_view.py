import flet as ft
from papeleria_app.ui.components.error_text import Error_text
from papeleria_app.ui.components.logo_header import Logo_header
from papeleria_app.ui.components.basic_text_input import Basic_Text_input as bti
from papeleria_app.ui.components.container_form import Container_form
from papeleria_app.repositorios.usuario_repo import verificar_usuario

user = None


def login_view():

    def limpiar_mensaje(e):
        output.value = ""
        output.update()

    header = Logo_header("images/logo_blanco.jpg").getHeader()

    # Entradas de usuario y contraseña
    user_row = bti("USUARIO", on_change=limpiar_mensaje).getComponent()
    password_row = bti("CONTRASEÑA", password=True, on_change=limpiar_mensaje).getComponent()

    output = ft.Text("", color="red", text_align=ft.TextAlign.CENTER)

    inputs = [
        user_row,
        Error_text().get_error_text(),
        password_row,
        Error_text().get_error_text()
    ]

    column_inputs = ft.Column(
        controls=inputs,
        horizontal_alignment=ft.CrossAxisAlignment.END,
    )


    def redireccionamiento(e, rol):
        if rol == "encargado":
            e.page.go("/admin_dashboard_view")
        else:
            e.page.go("/empleado_dashboard_view")


    # Verificación al presionar el botón
    def verificacion(e):
        user_input = user_row.controls[1].value
        password_input = password_row.controls[1].value
        usuario, mensaje = verificar_usuario(user_input, password_input)
        if usuario is None:
            output.value = mensaje
            output.update()
            print(mensaje)
        else:
            e.page.client_storage.set("usuario", {
                "user": usuario
            })

            redireccionamiento(e, usuario.rol)




    button_ingresar = ft.ElevatedButton("INGRESAR", width=200, on_click=verificacion)


    # Formulario que incluye botón y mensaje
    form = Container_form(
        components=[
            column_inputs,
            button_ingresar,
            output
        ],
        width=400,
        height=300
    ).getForm()

    layout = ft.Column(
        controls=[
            header,
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=form
            )
        ],
        expand=True,
    )

    return ft.View(
        route="/login",
        controls=[layout],
        bgcolor="#cdf3ff",
        padding=0,
        appbar=None
    )

