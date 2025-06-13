import flet as ft

from papeleria_app.ui.pages.admin_dashboard_view import admin_dashboard_view
from papeleria_app.ui.pages.empleado_dashboard_view import empleado_dashboard_view
from papeleria_app.ui.pages.inicio_view import inicio_view
from papeleria_app.ui.pages.login_view import login_view

def main(page: ft.Page):
    def route_change(e):
        if page.route == "/":
            page.views.clear()
            page.views.append(inicio_view())
        elif page.route == "/login":
            page.views.clear()
            page.views.append(login_view())
        elif page.route == "/admin_dashboard_view":
            page.views.clear()
            page.views.append(admin_dashboard_view(page))
        elif page.route == "/empleado_dashboard_view":
            page.views.clear()
            page.views.append(empleado_dashboard_view(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)

