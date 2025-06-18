import flet as ft


class GraficaPieVentas:
    def __init__(self, datos: list[tuple[int, str]], titulo: str = ""):
        """
        Inicializa la gráfica de pie con datos.

        Args:
            datos: Lista de tuplas (cantidad, nombre)
            titulo: Título opcional para la gráfica
        """
        self.datos = datos
        self.titulo = titulo
        self._configurar_estilos()

    def _configurar_estilos(self):
        """Configura los estilos visuales de la gráfica"""
        self.normal_radius = 50
        self.hover_radius = 60
        self.center_space = 70
        self.normal_title_style = ft.TextStyle(
            size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
        )
        self.hover_title_style = ft.TextStyle(
            size=18,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
        )

        # Paleta de colores moderna
        self.colors = [
            "#4285F4",  # Azul
            "#34A853",  # Verde
            "#FBBC05",  # Amarillo
            "#EA4335",  # Rojo
            "#673AB7",  # Morado
            "#FF9800",  # Naranja
            "#009688",  # Verde azulado
            "#E91E63",  # Rosa
        ]

    def _crear_secciones(self):
        """Crea las secciones del gráfico de pie"""
        total = sum(cantidad for cantidad, _ in self.datos) if self.datos else 1
        secciones = []

        for idx, (cantidad, nombre) in enumerate(self.datos):
            porcentaje = (cantidad / total) * 100
            color = self.colors[idx % len(self.colors)]

            secciones.append(
                ft.PieChartSection(
                    porcentaje,
                    title=f"{cantidad}",  # Mostrar cantidad absoluta
                    title_style=self.normal_title_style,
                    color=color,
                    radius=self.normal_radius,
                    badge=ft.Text(nombre[:15], size=11, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),  # Mostrar nombre (limitado a 15 chars)
                    badge_position=0.95,
                )
            )

        return secciones

    def _manejar_evento(self, chart: ft.PieChart, e: ft.PieChartEvent):
        """Maneja el evento hover sobre las secciones"""
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        chart.update()

    def crear(self) -> ft.PieChart:
        """
        Crea y devuelve el componente de gráfica de pie

        Returns:
            ft.PieChart: Gráfica configurada lista para usar
        """
        secciones = self._crear_secciones()

        chart = ft.PieChart(
            sections=secciones,
            sections_space=0,
            center_space_radius=self.center_space,
            on_chart_event=lambda e: self._manejar_evento(chart, e),
            expand=True,
        )

        return chart