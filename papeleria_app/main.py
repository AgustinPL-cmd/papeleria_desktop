import flet as ft
from papeleria_app.ui.pages.registro_producto import registro_producto_view

def main(page: ft.Page):
    registro_producto_view(page)

ft.app(target=main)
