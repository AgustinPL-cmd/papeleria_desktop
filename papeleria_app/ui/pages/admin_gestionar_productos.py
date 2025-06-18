import flet as ft
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.linear_chart_ventas_semana_actual import GraficaLinealVentas
from papeleria_app.ui.components.menu_lateral_encargado import menu_lateral_encargado
from papeleria_app.repositorios.ventas_repo import (
    ventas_semana_actual,
    ventas_semana_pasada,
    ventas_mes_actual,
    ventas_trimestre_actual
)
from papeleria_app.ui.components.productosTable import ProductosTable
from papeleria_app.ui.components.basic_text_input import Basic_Text_input as bti
from papeleria_app.ui.components.container_form import Container_form
from papeleria_app.repositorios.categoria_repo import get_categorias
from papeleria_app.ui.components.error_text import Error_text
import papeleria_app.services.producto_service as producto_service


def admin_gestionar_productos(page: ft.Page):
    dlg_usuario = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargando..."),
        content=ft.Text("Espere un momento"),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )

    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]

    header = header_empleado(user, page, dlg_usuario)
    menu_lateral = menu_lateral_encargado()
    tabla_productos = ProductosTable(page)

    titulo_grafica_ventas = ft.Text("Ventas de esta semana", size=20, weight=ft.FontWeight.BOLD, color="#090040")

    # Gráfica ventas
    datos = ventas_semana_actual()
    grafica_ventas = GraficaLinealVentas(titulo="Ventas Semana Actual", datos=datos, tipo_x="dia")
    container_grafica_venta = ft.Container(
        content=grafica_ventas.construir_grafica(),
        padding=20,
        bgcolor="#ffffff",
        border_radius=20,
        clip_behavior=ft.ClipBehavior.NONE,
        expand=True
    )

    # Función para actualizar la gráfica y el título
    def actualizar_grafica_ventas(nombre, consulta_funcion, tipo_x):
        def handler(e):
            titulo_grafica_ventas.value = nombre
            nuevos_datos = consulta_funcion()
            nueva_grafica = GraficaLinealVentas(titulo=nombre, datos=nuevos_datos, tipo_x=tipo_x)
            container_grafica_venta.content = nueva_grafica.construir_grafica()
            page.update()

        return handler

    # Botones de selección
    botones_grafica_ventas = ft.Row(
        controls=[
            titulo_grafica_ventas,
            ft.ElevatedButton("Esta semana",
                              on_click=actualizar_grafica_ventas("Ventas de esta semana", ventas_semana_actual, "dia")),
            ft.ElevatedButton("Semana pasada",
                              on_click=actualizar_grafica_ventas("Ventas de la semana pasada", ventas_semana_pasada,
                                                                 "dia")),
            ft.ElevatedButton("Este mes",
                              on_click=actualizar_grafica_ventas("Ventas de este mes", ventas_mes_actual, "semana")),
            ft.ElevatedButton("Trimestre",
                              on_click=actualizar_grafica_ventas("Ventas del trimestre", ventas_trimestre_actual,
                                                                 "mes")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10,
        wrap=True
    )

    # Componentes para la pestaña de registro de producto
    categorias_nombre = get_categorias()
    mensaje_confirmacion = ft.Text("", color="red", text_align=ft.TextAlign.CENTER)

    # Mensajes de error
    mensaje_nombre = Error_text().get_error_text()
    mensaje_descripcion = Error_text().get_error_text()
    mensaje_precio_venta = Error_text().get_error_text()
    mensaje_precio_compra = Error_text().get_error_text()
    mensaje_stock_actual = Error_text().get_error_text()
    mensaje_stock_minimo = Error_text().get_error_text()
    mensaje_categoria = Error_text().get_error_text()

    def limpiar_errores(e):
        for i in range(0, len(campos_registro), 2):
            fila = campos_registro[i]
            mensaje = campos_registro[i + 1]

            if isinstance(fila, ft.Row) and len(fila.controls) > 1:
                input_control = fila.controls[1]

                if input_control == e.control:
                    mensaje.value = ""
                    mensaje.visible = False
                    break

        page.update()

    def guardar_click(e):
        exito, confirmacion = producto_service.registrar_producto(campos_registro, page)
        mensaje_confirmacion.value = confirmacion
        mensaje_confirmacion.color = "green" if exito else "red"
        page.update()


    def limpiar_click(e):
        for campo in campos_registro:
            if hasattr(campo, 'value'):
                campo.value = ""
        mensaje_confirmacion.value = ""
        page.update()

    campos_registro = [
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

    inputs_registro = ft.Column(
        controls=campos_registro,
        horizontal_alignment=ft.CrossAxisAlignment.END,
    )

    botones_registro = ft.Row(
        controls=[
            ft.ElevatedButton("Guardar", on_click=guardar_click),
            ft.OutlinedButton("Limpiar", on_click=limpiar_click, style=ft.ButtonStyle(color="#002639"))
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    form_registro = Container_form(
        components=[inputs_registro, botones_registro, mensaje_confirmacion],
        width=800
    ).getForm()

    # Contenido principal organizado en pestañas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Dashboard",
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            botones_grafica_ventas,
                            container_grafica_venta,
                        ],
                        spacing=20,
                        expand=True
                    ),
                    padding=20
                )
            ),
            ft.Tab(
                text="Inventario",
                content=ft.Column(
                    controls=tabla_productos.get_controls(),
                    spacing=20,
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),
            ),
            ft.Tab(
                text="Registrar Producto",
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[form_registro],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                )
            )
        ],
        expand=True,
        label_color="#090040",
        unselected_label_color="#03A6A1",
        scrollable=True
    )

    contenido_principal = ft.Container(
        content=tabs,
        padding=ft.padding.only(top=20),
        expand=True
    )

    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.Container(
                ft.Column(
                    controls=[
                        header,
                        contenido_principal
                    ]
                ),
                expand=True
            ),
        ],
        spacing=5,
        expand=True
    )

    return ft.View(
        route="/adminGestionarProductos",
        controls=[layout, dlg_usuario],
        bgcolor="#f2f7fb",
        padding=0,
        appbar=None
    )