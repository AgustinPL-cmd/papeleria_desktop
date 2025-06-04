class Usuario:
    def __init__(self, id_usuario=None, nombre="", contrasena="", rol="empleado", activo=True):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contrasena = contrasena
        self.rol = rol
        self.activo = activo

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
