class Producto:
    def __init__(self, id_producto=None, nombre_producto="", descripcion="", precio_unitario_venta=0.0,
                 precio_unitario_compra=0.0, stock_actual=0, stock_minimo=0, id_categoria=None):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.descripcion = descripcion
        self.precio_unitario_venta = precio_unitario_venta
        self.precio_unitario_compra = precio_unitario_compra
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.id_categoria = id_categoria

    def __str__(self):
        return f"{self.nombre_producto} - Stock: {self.stock_actual}"
