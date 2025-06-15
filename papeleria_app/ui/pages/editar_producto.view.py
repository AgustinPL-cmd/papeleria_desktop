import flet as ft
from papeleria_app.repositorios.producto_repo import buscar_productos_por_nombre, actualizar_producto
from papeleria_app.models.producto import Producto

def editar_producto_view(page: ft.Page):

    busqueda_input = ft.TextField(label="Buscar producto", width=300)
    mensaje = ft.Text("", size=14)

    resultados_column = ft.Column(scroll="auto", expand=True)

    def buscar_productos(e):
        resultados_column.controls.clear()
        productos = buscar_productos_por_nombre(busqueda_input.value)

        if not productos:
            mensaje.value = "No se encontraron productos."
            page.update()
            return

        for p in productos:
            editar_btn = ft.IconButton(
                icon=ft.icons.EDIT,
                icon_color="blue",
                on_click=lambda e, prod=p: mostrar_formulario_edicion(prod)
            )

            fila = ft.Row(
                controls=[
                    ft.Text(f"{p.id_producto} - {p.nombre}"),
                    editar_btn
                ]
            )
            resultados_column.controls.append(fila)

        mensaje.value = ""
        page.update()

    def mostrar_formulario_edicion(producto: Producto):
        nombre_input = ft.TextField(label="Nombre", value=producto.nombre, width=300)
        descripcion_input = ft.TextField(label="Descripción", value=producto.descripcion, width=300)
        precio_venta_input = ft.TextField(label="Precio Venta", value=str(producto.precio_venta), width=300)
        precio_compra_input = ft.TextField(label="Precio Compra", value=str(producto.precio_compra), width=300)
        stock_input = ft.TextField(label="Stock Actual", value=str(producto.stock), width=300)
        stock_min_input = ft.TextField(label="Stock Mínimo", value=str(producto.stock_min), width=300)
        categoria_input = ft.TextField(label="ID Categoría", value=str(producto.id_categoria), width=300)

        resultado_edicion = ft.Text("", size=14)

        def guardar_cambios(e):
            try:
                nuevo_precio_venta = float(precio_venta_input.value)
                nuevo_precio_compra = float(precio_compra_input.value)

                if nuevo_precio_compra > nuevo_precio_venta:
                    resultado_edicion.value = " El precio de compra no puede ser mayor al de venta"
                    resultado_edicion.color = "red"
                    page.update()
                    return

                if nuevo_precio_venta == producto.precio_venta:
                    resultado_edicion.value = " El nuevo precio de venta debe ser diferente al actual"
                    resultado_edicion.color = "red"
                    page.update()
                    return

                producto_actualizado = Producto(
                    id_producto=producto.id_producto,
                    nombre=nombre_input.value,
                    descripcion=descripcion_input.value,
                    precio_venta=nuevo_precio_venta,
                    precio_compra=nuevo_precio_compra,
                    stock=int(stock_input.value),
                    stock_min=int(stock_min_input.value),
                    id_categoria=int(categoria_input.value)
                )

                ok, msg = actualizar_producto(producto_actualizado)
                resultado_edicion.value = msg
                resultado_edicion.color = "green" if ok else "red"
                page.update()

            except ValueError:
                resultado_edicion.value = " Verifica los campos numéricos."
                resultado_edicion.color = "red"
                page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Producto"),
            content=ft.Column(
                spacing=10,
                controls=[
                    nombre_input,
                    descripcion_input,
                    precio_venta_input,
                    precio_compra_input,
                    stock_input,
                    stock_min_input,
                    categoria_input,
                    resultado_edicion
                ]
            ),
            actions=[
                ft.TextButton("Guardar", on_click=guardar_cambios),
                ft.TextButton("Cancelar", on_click=lambda e: page.dialog.open(False))
            ]
        )
        page.dialog.open(True)
        page.update()

    layout = ft.Column(
        controls=[
            ft.Text("Editar Productos", size=22, weight="bold"),
            ft.Row(
                controls=[
                    busqueda_input,
                    ft.ElevatedButton("Buscar", on_click=buscar_productos)
                ]
            ),
            mensaje,
            resultados_column
        ]
    )

    return layout

def main(page: ft.Page):
    page.title = "Editar Productos"
    page.views.clear()
    page.views.append(
        ft.View(
            route="/editar_producto",
            controls=[editar_producto_view(page)]
        )
    )
    page.update()

ft.app(target=main)