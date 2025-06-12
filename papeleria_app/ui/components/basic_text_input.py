import flet as ft

class Basic_Text_input:
    def __init__(self, label, dropdown_content=None, on_change=None, password=False):
        self.text = label
        self.dropdown_content = dropdown_content

        self.label = ft.Text(
            value=label + ":",
            color="black",
            size=16,
            weight=ft.FontWeight.BOLD,
            width=140
        )

        # Campo de texto
        if dropdown_content is None:
            self.textfield = ft.TextField(
                bgcolor="#8285a2",
                filled=True,
                border_color="transparent",
                color="black",
                focused_border_color="#002639",
                text_style=ft.TextStyle(
                    color="black",
                    size=16,
                ),
                expand=True,
                on_change=on_change,
                password=password,
                can_reveal_password=password
            )

            self.component = ft.Row(
                controls=[self.label, self.textfield],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        # Dropdown
        else:
            self.dropdown = ft.Dropdown(
                bgcolor="#131D4F",
                filled=True,
                border_color="transparent",
                color="white",
                focused_border_color="#8285a2",
                text_style=ft.TextStyle(
                    color="white",
                    size=16,
                ),
                expand=True,
                options=self.get_options(),
                on_change=on_change
            )

            self.component = ft.Row(
                controls=[self.label, self.dropdown],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

    def get_options(self):
        return [ft.dropdown.Option(item) for item in self.dropdown_content]

    def getComponent(self):
        return self.component

    def getValue(self):
        if hasattr(self, 'textfield'):
            return self.textfield.value
        elif hasattr(self, 'dropdown'):
            return self.dropdown.value
        return None
