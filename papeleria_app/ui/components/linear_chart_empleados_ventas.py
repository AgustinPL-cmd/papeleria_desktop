import flet as ft
from datetime import datetime
from collections import defaultdict


class GraficaLinealPorEmpleado:
    def __init__(self, titulo: str, datos: list, tipo_x: str, tipo_valor: str = "total_ventas"):
        """
        :param titulo: Título de la gráfica
        :param datos: Lista de tuplas (empleado, etiqueta_x, total_ventas, total_ingresos, ganancia_neta)
        :param tipo_x: Tipo de eje X: 'dia', 'semana', 'mes'
        :param tipo_valor: Qué valor mostrar en la gráfica: 'total_ventas', 'total_ingresos', 'ganancia_neta'
        """
        self.titulo = titulo
        self.datos = datos
        self.tipo_x = tipo_x
        self.tipo_valor = tipo_valor
        self.ejes_x_ordenados = self._obtener_eje_x()

    def _obtener_eje_x(self):
        if self.tipo_x == 'dia':
            return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        elif self.tipo_x == 'semana':
            return [str(i) for i in range(1, 5)]
        elif self.tipo_x == 'mes':
            mes_actual = datetime.now().month
            return [
                str((mes_actual - 2) % 12 or 12),
                str((mes_actual - 1) % 12 or 12),
                str(mes_actual)
            ]
        return []

    def construir_grafica(self):
        # Agrupar datos por empleado
        datos_por_empleado = defaultdict(dict)
        max_valor = 0
        print(self.datos)
        for empleado, x_label, total_v, total_i, ganancia in self.datos:
            valor = {
                "total_ventas": total_v,
                "total_ingresos": total_i,
                "ganancia_neta": ganancia
            }.get(self.tipo_valor, total_v)
            datos_por_empleado[empleado][x_label] = valor
            max_valor = max(max_valor, valor)

        # Asignar colores por empleado
        colores = [
            "#1da3c2", "#17b39e", "#9561e2", "#f39c12", "#c0392b", "#2ecc71", "#34495e"
        ]
        colores_iter = iter(colores)

        # Crear líneas para cada empleado
        data_series = []
        for empleado, valores in datos_por_empleado.items():
            puntos = []
            for i, etiqueta in enumerate(self.ejes_x_ordenados):
                valor = valores.get(etiqueta, 0)
                puntos.append(ft.LineChartDataPoint(i, float(valor), tooltip=f"{empleado}: {valor:.2f}"))
            color = next(colores_iter, "#000000")
            data_series.append(
                ft.LineChartData(
                    data_points=puntos,
                    stroke_width=4,
                    curved=True,
                    stroke_cap_round=True,
                    color=color,
                )
            )

        max_y = ((max_valor + 100) // 100) * 100

        # Etiquetas del eje X
        etiquetas_dict = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }

        if self.tipo_x == 'dia':
            etiquetas_x = [etiquetas_dict.get(et, et) for et in self.ejes_x_ordenados]
        elif self.tipo_x == 'semana':
            etiquetas_x = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]
        elif self.tipo_x == 'mes':
            meses_es = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            }
            etiquetas_x = [meses_es[int(m)] for m in self.ejes_x_ordenados]
        else:
            etiquetas_x = []

        labels_x = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Container(
                    ft.Text(
                        etiquetas_x[i] if i < len(etiquetas_x) else "",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
                    ),
                    margin=ft.margin.only(top=10),
                ),
            ) for i in range(len(self.ejes_x_ordenados))
        ]

        labels_y = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Text(str(i), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
            ) for i in range(0, int(max_y + 1), 100)
        ]

        return ft.LineChart(
            data_series=data_series,
            left_axis=ft.ChartAxis(labels=labels_y, labels_size=50),
            bottom_axis=ft.ChartAxis(labels=labels_x, labels_size=32),
            min_y=0,
            max_y=max_y,
            min_x=-0.2,
            max_x=10,
            tooltip_bgcolor="#e0e0e0",
            tooltip_padding=10,
            horizontal_grid_lines=ft.ChartGridLines(color="#e0e0e0", width=1, dash_pattern=[5, 5]),
            vertical_grid_lines=ft.ChartGridLines(color="#f0f0f0", width=1),
            border=ft.border.all(2, "#e0e0e0"),
            bgcolor="#ffffff",
            width=1100,
            height=280
        )
