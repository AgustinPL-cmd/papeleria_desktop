class SugerenciaCliente:
    def __init__(self, id_sugerencia=None, fecha_sugerencia=None, producto_sugerido="", comentario=""):
        self.id_sugerencia = id_sugerencia
        self.fecha_sugerencia = fecha_sugerencia
        self.producto_sugerido = producto_sugerido
        self.comentario = comentario

    def __str__(self):
        return f"Sugerencia: {self.producto_sugerido}"
