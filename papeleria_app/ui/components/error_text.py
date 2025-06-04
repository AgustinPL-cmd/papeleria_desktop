import flet as ft

class Error_text:
    def __init__(self, color = "red", visible=False, size=14, value=""):
        self.text = ft.Text(
            color=color,
            visible=visible,
            size=size,
            value = value
        )

    def get_error_text(self):
        return self.text