import flet as ft
from papeleria_app.repositorios.producto_repo import obtener_todos_productos


class ProductosTable:
    def __init__(self, page: ft.Page, on_editar_callback=None):
        self.page = page
        self.on_editar_callback = on_editar_callback
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
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
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
        rows = []
        for p in productos:
            # Botón de editar
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color="#090040",
                tooltip="Editar producto",
                on_click=lambda e, pid=p['id_producto']: self._on_editar_click(pid)
            )

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p['id_producto']), color="black")),
                        ft.DataCell(ft.Text(p['nombre_producto'], color="black")),
                        ft.DataCell(ft.Text(p['nombre_categoria'], color="black")),
                        ft.DataCell(ft.Text(f"${p['precio_unitario_venta']:.2f}", color="black")),
                        ft.DataCell(
                            ft.Text(
                                str(p['stock_actual']),
                                color=ft.Colors.RED if p['stock_actual'] < p['stock_minimo'] else ft.Colors.BLACK
                            )
                        ),
                        ft.DataCell(btn_editar),
                    ]
                )
            )
        return rows

    def _on_editar_click(self, id_producto):
        if self.on_editar_callback:
            self.on_editar_callback(id_producto)

    def _aplicar_filtros(self, e):
        filtro_nombre = self.txt_busqueda.value.lower() if self.txt_busqueda.value else None
        filtro_categoria = self.dd_categoria.value if self.dd_categoria.value else None

        self.productos_filtrados = [
            p for p in self.productos
            if (not filtro_nombre or filtro_nombre in p['nombre_producto'].lower())
               and (not filtro_categoria or str(p['id_categoria']) == filtro_categoria or filtro_categoria == "Todas")
        ]

        self.data_table.rows = self._generar_filas()
        self.page.update()

    def recargar_datos(self):
        """Recarga los productos desde la base de datos y refresca la tabla"""
        self.productos = obtener_todos_productos()
        self.productos_filtrados = self.productos.copy()
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
                        ft.ListTile(title=ft.Text("Inventario de Productos", style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                                  color="black")),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
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