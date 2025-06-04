import flet as ft

class Logo_header:
    def __init__(self, src=""):
        # Header
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(src=src, width=100, height=100),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#8285a2",
            padding=10,
            margin=0,
            height=110
        )

    def getHeader(self):
        return self.header
