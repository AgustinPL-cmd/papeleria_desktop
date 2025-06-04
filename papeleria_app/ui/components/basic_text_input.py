import flet as ft

class Basic_Text_input:
    def __init__(self, label, dropdown_content=None, on_change = None):
        self.text = label
        self.dropdown_content = dropdown_content
        self.label = ft.Text(
            value=label + ":",
            color="black",
            size=16,
            weight=ft.FontWeight.BOLD,
            width=140,
        )

        # Solo crear campo de texto si NO hay dropdown
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
                on_change= on_change
            )

            self.rowText = ft.Row(
                controls=[self.label, self.textfield],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

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
                on_change= on_change
            )

            self.rowDrop = ft.Row(
                controls=[self.label, self.dropdown],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

    def get_options(self):
        return [ft.dropdown.Option(item) for item in self.dropdown_content]

    def getRowText(self):
        return self.rowText

    def getRowDrop(self):
        return self.rowDrop

    def getText(self):
        return  self.text