import flet as ft
from papeleria_app.ui.components.basic_text_input import Basic_Text_input as bti
from papeleria_app.ui.components.logo_header import Logo_header
from papeleria_app.ui.components.container_form import Container_form
from papeleria_app.repositorios.categoria_repo import get_categorias
from papeleria_app.ui.components.error_text import Error_text
import papeleria_app.services.producto_service as producto_service


def registro_producto_view(page: ft.Page):

    categorias_nombre = get_categorias()
    page.scroll = True


    def guardar_click(e):
        exito, confirmacion = producto_service.registrar_producto(campos, page)
        mensaje.value = confirmacion

    def limpiar_errores(e):
        for i in range(0, len(campos), 2):  # Solo iteramos en las filas con Row
            fila = campos[i]
            mensaje = campos[i + 1]

            if isinstance(fila, ft.Row) and len(fila.controls) > 1:
                input_control = fila.controls[1]

                if input_control == e.control:
                    mensaje.value = ""
                    mensaje.visible = False
                    break

        page.update()

    def limpiar_click(e):
        for campo in campos:
            campo.value = ""
        mensaje.value = ""
        page.update()

    #Página base
    page.bgcolor = "#fdf9d8"
    page.title = "Registro de Productos"
    page.padding=0


    #Header
    header = Logo_header(src="../../images/logo_blanco.jpg").getHeader()

    #Mensajes de error
    mensaje_nombre = Error_text().get_error_text()
    mensaje_descripcion = Error_text().get_error_text()
    mensaje_precio_venta = Error_text().get_error_text()
    mensaje_precio_compra = Error_text().get_error_text()
    mensaje_stock_actual = Error_text().get_error_text()
    mensaje_stock_minimo = Error_text().get_error_text()
    mensaje_categoria = Error_text().get_error_text()

    #Inputs
    campos = [
        bti("PRODUCTO", on_change=limpiar_errores).getComponent(),
        mensaje_nombre,
        bti("DESCRIPCIÓN", on_change=limpiar_errores).getComponent(),
        mensaje_descripcion,
        bti("PRECIO DE VENTA", on_change=limpiar_errores).getComponent(),
        mensaje_precio_venta,
        bti("PRECIO DE COMPRA", on_change=limpiar_errores).getComponent(),
        mensaje_precio_compra,
        bti("STOCK ACTUAL", on_change=limpiar_errores).getComponent(),
        mensaje_stock_actual,
        bti("STOCK MÍNIMO", on_change=limpiar_errores).getComponent(),
        mensaje_stock_minimo,
        bti("CATEGORIA", categorias_nombre, on_change=limpiar_errores).getComponent(),
        mensaje_categoria,
    ]

    inputs = ft.Column(
        controls= campos,
        horizontal_alignment= ft.CrossAxisAlignment.END,
    )

    #Botones
    botones = ft.Row(
        controls = [
            ft.ElevatedButton("Guardar", on_click=guardar_click),
            ft.OutlinedButton("Limpiar", on_click=limpiar_click, style= ft.ButtonStyle(color="#002639"))
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Mensaje de Confirmación
    mensaje = ft.Text("", color="red", text_align=ft.TextAlign.CENTER)

    #Formulario
    form_container = Container_form(components=[inputs,botones, mensaje], width=600).getForm()

    #Estructura General
    page.add(
        header,
        ft.Row(
            controls = [form_container],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=registro_producto_view)




