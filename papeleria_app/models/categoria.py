class Categoria:
    def __init__(self, id_categoria=None, nombre_categoria=""):
        self.id_categoria = id_categoria
        self.nombre_categoria = nombre_categoria

    def __str__(self):
        return self.nombre_categoria

