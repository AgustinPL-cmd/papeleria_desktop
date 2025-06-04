import flet as ft

class Container_form:
    def __init__(self, width=500, bgcolor="#d7daf1", colorShadow="#BDBDBD", components=None):
        self.form_container = ft.Container(
            content=ft.Column(
                controls=components,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            width=width,
            border_radius=15,
            bgcolor=bgcolor,
            shadow=ft.BoxShadow(blur_radius=15, color=colorShadow),

        )

    def getForm(self):
        return self.form_container
