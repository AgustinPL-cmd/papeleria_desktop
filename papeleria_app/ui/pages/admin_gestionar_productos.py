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
from papeleria_app.services.producto_service import registrar_producto


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
    tabla_productos = ProductosTable(page, on_editar_callback=lambda pid: abrir_dialogo_editar(pid))

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

    # Función que registra el producto
    def guardar_click(e):
        "Limpiar mensajes de errores previos"
        for msg in [mensaje_nombre, mensaje_descripcion, mensaje_precio_venta, mensaje_precio_compra, mensaje_stock_actual, mensaje_stock_minimo, mensaje_categoria]:
            msg.value = ""
            msg.visible = False

        #Recolectar Valores
        nombre = campo_nombre.controls[1].value
        desc = campo_desc.controls[1].value
        precio_venta = campo_precio_venta.controls[1].value
        precio_compra = campo_precio_compra.controls[1].value
        stock_actual = campo_stock_actual.controls[1].value
        stock_min = campo_stock_min.controls[1].value
        categoria = campo_categoria.controls[1].value

        #Llamar al servicio
        exito, mensaje = registrar_producto(nombre,desc,precio_venta,precio_compra,stock_actual,stock_min,categoria)

        # Mostrar mensaje en la etiqueta de confirmación
        mensaje_confirmacion.value = mensaje
        mensaje_confirmacion.color = "green" if exito else "red"

        if exito:
            limpiar_formulario()
        else:
            page.update()

        print(f"DEBUG: exito={exito}, mensaje='{mensaje}'")



    def limpiar_formulario():
        campo_nombre.controls[1].value = ""
        campo_desc.controls[1].value = ""
        campo_precio_venta.controls[1].value = ""
        campo_precio_compra.controls[1].value = ""
        campo_stock_actual.controls[1].value = ""
        campo_stock_min.controls[1].value = ""
        campo_categoria.controls[1].value = None

        for msg in [mensaje_nombre, mensaje_descripcion, mensaje_precio_venta,
                mensaje_precio_compra, mensaje_stock_actual, mensaje_stock_minimo,
                mensaje_categoria]:
            msg.value = ""
            msg.visible = False

        page.update()

    def limpiar_click(e):
        limpiar_formulario()

    # Diálogo de edición de producto
    def abrir_dialogo_editar(id_producto):
        from papeleria_app.services.producto_service import obtener_producto_por_id, editar_producto

        # Obtener datos del producto
        producto = obtener_producto_por_id(id_producto)
        if not producto:
            mensaje_confirmacion.value = "Error: Producto no encontrado"
            mensaje_confirmacion.color = "red"
            page.update()
            return

        # Obtener lista de categorías para el dropdown
        from papeleria_app.repositorios.categoria_repo import get_categorias
        categorias_lista = get_categorias()
        opciones_categorias = [ft.dropdown.Option(cat) for cat in categorias_lista]

        # Campos del formulario de edición
        campo_nombre_edit = ft.TextField(label="Nombre del producto", value=producto['nombre_producto'], expand=True)
        campo_desc_edit = ft.TextField(label="Descripción", value=producto['descripcion'] or "", expand=True,
                                       multiline=True)
        campo_precio_venta_edit = ft.TextField(label="Precio de venta", value=str(producto['precio_unitario_venta']),
                                               expand=True)
        campo_precio_compra_edit = ft.TextField(label="Precio de compra", value=str(producto['precio_unitario_compra']),
                                                expand=True)
        campo_stock_actual_edit = ft.TextField(label="Stock actual", value=str(producto['stock_actual']), expand=True)
        campo_stock_minimo_edit = ft.TextField(label="Stock mínimo", value=str(producto['stock_minimo']), expand=True)
        campo_categoria_edit = ft.Dropdown(
            label="Categoría",
            options=opciones_categorias,
            value=producto['nombre_categoria'],
            expand=True
        )

        # Mensaje de error/éxito dentro del diálogo
        mensaje_dialogo = ft.Text("", color="red", size=12)

        def guardar_edicion(e):
            # Recolectar valores
            nombre = campo_nombre_edit.value
            descripcion = campo_desc_edit.value
            precio_venta = campo_precio_venta_edit.value
            precio_compra = campo_precio_compra_edit.value
            stock_actual = campo_stock_actual_edit.value
            stock_minimo = campo_stock_minimo_edit.value
            categoria = campo_categoria_edit.value

            # Validar campos obligatorios
            if not nombre:
                mensaje_dialogo.value = "El nombre del producto es obligatorio"
                mensaje_dialogo.color = "red"
                page.update()
                return

            # Llamar al servicio
            exito, mensaje = editar_producto(
                id_producto, nombre, descripcion, precio_venta, precio_compra,
                stock_actual, stock_minimo, categoria
            )

            if exito:
                # Cerrar diálogo
                page.close(dialogo_edicion)
                # Mostrar mensaje global
                mensaje_confirmacion.value = mensaje
                mensaje_confirmacion.color = "green"
                # Recargar tabla
                tabla_productos.recargar_datos()
                page.update()
            else:
                mensaje_dialogo.value = mensaje
                mensaje_dialogo.color = "red"
                page.update()

        # Crear el diálogo
        dialogo_edicion = ft.AlertDialog(
            title=ft.Text(f"Editar Producto: {producto['nombre_producto']}"),
            content=ft.Container(
                content=ft.Column([
                    campo_nombre_edit,
                    campo_desc_edit,
                    ft.Row([campo_precio_venta_edit, campo_precio_compra_edit], spacing=10),
                    ft.Row([campo_stock_actual_edit, campo_stock_minimo_edit], spacing=10),
                    campo_categoria_edit,
                    mensaje_dialogo,
                ], spacing=15, height=400),
                width=500,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_edicion)),
                ft.ElevatedButton("Guardar cambios", on_click=guardar_edicion, bgcolor="#090040", color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialogo_edicion)

    campo_nombre =bti("PRODUCTO", on_change=limpiar_errores).getComponent()
    campo_desc = bti("DESCRIPCIÓN", on_change=limpiar_errores).getComponent()
    campo_precio_venta = bti("PRECIO DE VENTA", on_change=limpiar_errores).getComponent()
    campo_precio_compra = bti("PRECIO DE COMPRA", on_change=limpiar_errores).getComponent()
    campo_stock_actual = bti("STOCK ACTUAL", on_change=limpiar_errores).getComponent()
    campo_stock_min = bti("STOCK MÍNIMO", on_change=limpiar_errores).getComponent()
    campo_categoria = bti("CATEGORIA", categorias_nombre, on_change=limpiar_errores).getComponent()

    campos_registro = [
        campo_nombre,
        mensaje_nombre,
        campo_desc,
        mensaje_descripcion,
        campo_precio_venta,
        mensaje_precio_venta,
        campo_precio_compra,
        mensaje_precio_compra,
        campo_stock_actual,
        mensaje_stock_actual,
        campo_stock_min,
        mensaje_stock_minimo,
        campo_categoria,
        mensaje_categoria,
        mensaje_confirmacion
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