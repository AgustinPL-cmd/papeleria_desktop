import flet as ft

class Task(ft.Row):
    def __init__(self, text):
        super().__init__()
        self.text_view = ft.Text(text)
        self.text_edit = ft.TextField(value=text, visible=False)
        self.edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=self.save)

        self.controls = [
            ft.Checkbox(),
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
        ]

    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()

    def save(self, e):
        self.edit_button.visible = True
        self.save_button.visible = False
        self.text_view.visible = True
        self.text_edit.visible = False
        self.text_view.value = self.text_edit.value
        self.update()

def main(page: ft.Page):
    def add_clicked(e):
        if new_task.value:
            page.add(Task(text=new_task.value))
            new_task.value = ''
            new_task.focus()
            new_task.update()

    new_task = ft.TextField(hint_text="What's needs to be done?", width=300)
    page.add(ft.Row([new_task, ft.ElevatedButton('Add', on_click=add_clicked)]))

if __name__ == '__main__':
    ft.app(target=main)
