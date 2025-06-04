class AlertaInventario:
    def __init__(self, id_alerta=None, fecha_alerta=None, estado="pendiente", productoId=None):
        self.id_alerta = id_alerta
        self.fecha_alerta = fecha_alerta
        self.estado = estado
        self.productoId = productoId

    def __str__(self):
        return f"Alerta [{self.estado}] - Producto ID: {self.productoId}"
