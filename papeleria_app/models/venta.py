class Venta:
    def __init__(self, id_venta=None, fecha_venta=None, cantidad=0, subtotal=0.0,
                 numVenta=0, productoId=None, usuarioId=None):
        self.id_venta = id_venta
        self.fecha_venta = fecha_venta
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.numVenta = numVenta
        self.productoId = productoId
        self.usuarioId = usuarioId

    def __str__(self):
        return f"Venta #{self.numVenta} - {self.cantidad} productos"
