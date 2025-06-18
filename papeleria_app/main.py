import flet as ft

from papeleria_app.ui.pages.admin_compra import admin_registrar_compra
from papeleria_app.ui.pages.admin_gestionar_empleado import admin_gestionar_empleado
from papeleria_app.ui.pages.admin_gestionar_productos import admin_gestionar_productos
from papeleria_app.ui.pages.admin_gestionar_ventas import admin_gestionar_venta
from papeleria_app.ui.pages.empleado_registrar_sugerencia import  registro_sugerencia_view
from papeleria_app.ui.pages.admin_dashboard_view import admin_dashboard_view
from papeleria_app.ui.pages.empleado_dashboard_view import empleado_dashboard_view
from papeleria_app.ui.pages.empleado_registrar_venta_view import empleado_registrar_venta_view
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
        elif page.route == "/empladoRegistrarVenta":
            page.views.clear()
            page.views.append(empleado_registrar_venta_view(page))
        elif page.route == "/empleadoRegistrarSugerencia":
            page.views.clear()
            page.views.append(registro_sugerencia_view(page))
        elif page.route == "/adminGestionarProductos":
            page.views.clear()
            page.views.append(admin_gestionar_productos(page))
        elif page.route == "/adminGestionarEmpleados":
            page.views.clear()
            page.views.append(admin_gestionar_empleado(page))
        elif page.route == "/admin_gestionar_venta":
            page.views.clear()
            page.views.append(admin_gestionar_venta(page))
        elif page.route == "/admin_registrar_compra":
            page.views.clear()
            page.views.append(admin_registrar_compra(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)

