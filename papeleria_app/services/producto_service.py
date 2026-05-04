from papeleria_app.repositorios.producto_repo import insert_productos
from papeleria_app.repositorios.categoria_repo import get_categoria_by_name
import re

def validar_nombre_producto(nombre_producto):
    pattern = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚ0-9\s\.\-]+$")
    if not nombre_producto or not nombre_producto.strip():
        return False, "El producto no puede estár vacío"

    if not re.match(pattern, nombre_producto):
        return False, "Producto Inválido"

    return True, ""

def validar_precio(precio, campo):
    try:
        valor = float(precio)
    except ValueError:
        return False, f"{campo} Inválido", 0.0

    if valor <= 0:
        return False, f"El {campo} debe ser mayor a 0.", 0.0

    return True, "", valor

def validar_stock(stock, campo):
    try:
        valor = int(stock)
    except ValueError:
        return False, "Stock Inválido", 0

    if valor < 0:
        return False, "El stock debe ser igual o mayor a 0.", 0

    return True, "", valor


def registrar_producto(nombre, descripcion, precio_venta, precio_compra, stock_actual, stock_minimo, categoria_nombre):
    bool_nombre, msg_nombre = validar_nombre_producto(nombre)
    if not bool_nombre: return bool_nombre, msg_nombre

    bool_precio_venta, msg_precio_venta, precio_venta_float = validar_precio(precio_venta, "precio de venta")
    if not bool_precio_venta: return bool_precio_venta, msg_precio_venta

    bool_precio_compra, msg_precio_compra, precio_compra_float = validar_precio(precio_compra, "precio de compra")
    if not bool_precio_compra: return bool_precio_compra, msg_precio_compra

    bool_stock_actual, msg_precio_actual, stock_actual_int = validar_stock(stock_actual, "stock actual")
    if not bool_stock_actual: return bool_stock_actual, msg_precio_actual

    bool_stock_min, msg_stock_min, stock_min_int = validar_stock(stock_minimo, "stock_minimo")
    if not bool_stock_min: return bool_stock_min, msg_stock_min

    if precio_venta_float < precio_compra_float: return False, "El precio de venta no puede ser menor al precio de compra."

    if not categoria_nombre: return False, "Categoría Obligatoria"

    categoria_id = get_categoria_by_name(categoria_nombre).id_categoria

    resultado, mensaje = insert_productos(nombre, descripcion, precio_venta_float, precio_compra_float, stock_actual_int, stock_min_int, categoria_id)


    return resultado, mensaje


