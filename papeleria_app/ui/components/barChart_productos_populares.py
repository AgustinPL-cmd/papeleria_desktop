import flet as ft


class BarChartProductosPopulares:
    def __init__(self, titulo: str, datos: list):
        """
        :param titulo: Título de la gráfica
        :param datos: Lista de tuplas (cantidad, nombre_producto)
        """
        self.titulo = titulo
        self.datos = datos

    def construir_grafica(self):
        # Preparar datos para barras
        barras = []
        etiquetas_x = []
        max_valor = 0

        for i, (cantidad, nombre) in enumerate(self.datos):
            barras.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=cantidad,
                            width=30,
                            color="#1da3c2",
                            border_radius=ft.border_radius.all(8)
                        )
                    ]
                )
            )
            etiquetas_x.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Container(
                        ft.Text(nombre, size=12, max_lines=1, overflow="ellipsis", color="black"),
                        width=80,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=10),

                    )
                )
            )
            max_valor = max(max_valor, cantidad)

        max_y = ((max_valor + 10) // 10) * 10  # Redondear hacia arriba en múltiplos de 10

        labels_y = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Text(str(i), size=12, weight=ft.FontWeight.BOLD, color="black")
            ) for i in range(0,int( max_y + 1), int(max(1, max_y // 5)))
        ]

        chart = ft.BarChart(
            bar_groups=barras,
            left_axis=ft.ChartAxis(labels=labels_y, labels_size=40),
            bottom_axis=ft.ChartAxis(labels=etiquetas_x, labels_size=50),
            horizontal_grid_lines=ft.ChartGridLines(color="#e0e0e0", width=1, dash_pattern=[4, 4]),
            border=ft.border.all(2, "#e0e0e0"),
            tooltip_bgcolor="#e0e0e0",
            tooltip_padding=10,
            max_y=max_y,
            interactive=True,
            expand=True,
            bgcolor="#ffffff",
            width= 600
        )

        return chart
