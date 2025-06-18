import flet as ft
from papeleria_app.repositorios.producto_repo import obtener_todos_productos

class ProductosTableAdmin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.productos = obtener_todos_productos()
        self.productos_filtrados = self.productos.copy()

        # Controles de filtrado
        self.txt_busqueda = ft.TextField(
            label="Buscar producto",
            on_change=self._aplicar_filtros,
            expand=True,
            color="black",
            label_style=ft.TextStyle(color="black"),

        )

        self.dd_categoria = ft.Dropdown(
            label="Categoría",
            options=self._obtener_opciones_categorias(),
            on_change=self._aplicar_filtros,
            expand=True,
            label_style=ft.TextStyle(color="black"),
            color="black"
        )

        # DataTable
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Categoría", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Eliminar", color="white")),

            ],
            rows=self._generar_filas(),
            horizontal_margin=12,
            column_spacing=20,
            heading_row_color="#8e7db4",
            heading_row_height=40,
            data_row_max_height=40,
            expand=True
        )

    def _obtener_opciones_categorias(self):
        categorias = list({(p['id_categoria'], p['nombre_categoria']) for p in self.productos})
        return [ft.dropdown.Option("", "Todas")] + [
            ft.dropdown.Option(str(id), nombre) for id, nombre in categorias
        ]

    def _generar_filas(self, productos=None):
        productos = productos or self.productos_filtrados

        def eliminar_fila(e, fila_idx=len(tabla_productos.rows)):
            try:
                del self.data_table.rows[fila_idx]
            except:
                del self.data_table.rows[0]
            self.page.update()

        boton_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Eliminar",
            icon_color="red",
            on_click=lambda e, fila_idx=len(tabla_productos.rows): eliminar_fila(e, fila_idx)
        )
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(p['id_producto']), color="black")),
                    ft.DataCell(ft.Text(p['nombre_producto'], color="black")),
                    ft.DataCell(ft.Text(p['nombre_categoria'],color="black")),
                    ft.DataCell(ft.Text(f"${p['precio_unitario_venta']:.2f}", color="black")),
                    ft.DataCell(
                        ft.Text(
                            str(p['stock_actual']),
                            color=ft.Colors.RED if p['stock_actual'] < p['stock_minimo'] else ft.Colors.BLACK
                        )
                    ),
                    ft.DataCell(boton_eliminar)
                ]
            ) for p in productos
        ]

    def _aplicar_filtros(self, e):
        # Aplicar filtros
        filtro_nombre = self.txt_busqueda.value.lower() if self.txt_busqueda.value else None
        filtro_categoria = self.dd_categoria.value if self.dd_categoria.value else None

        self.productos_filtrados = [
            p for p in self.productos
            if (not filtro_nombre or filtro_nombre in p['nombre_producto'].lower())
               and (not filtro_categoria or str(p['id_categoria']) == filtro_categoria or filtro_categoria == "Todas")
        ]

        self.data_table.rows = self._generar_filas()
        self.page.update()

    def get_controls(self):
        return [
            ft.Row(
                controls=[
                    self.txt_busqueda,
                    self.dd_categoria,
                ],
                spacing=20
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(title=ft.Text("Inventario de Productos", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color="black")),
                        ft.Divider(),
                        ft.Container(
                            content = ft.Column(
                                controls=[self.data_table],
                                scroll=ft.ScrollMode.ALWAYS
                            ),
                            height=300,
                            border=ft.border.all(1, ft.Colors.GREY_300),
                            border_radius=8,
                            padding=10,
                            expand=True
                        )
                    ],
                    spacing=10
                ),
                padding=ft.padding.symmetric(horizontal=20),
                expand=True
            )
        ]
