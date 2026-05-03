from papeleria_app.repositorios.usuario_repo import update_usuario
from papeleria_app.repositorios.usuario_repo import get_empleado_by_id as get_empleado_by_id_repo
from papeleria_app.models.usuario import Usuario


def get_empleado_by_id(id_usuario):
    return get_empleado_by_id_repo(id_usuario)

def edit_empleado(empleado_id, nombre, activo):
    if not nombre or len(nombre.strip()) < 3:
        return False, "El nombre debe de tener al menos 3 caracteres"

    activo_bool = bool(activo)

    usuario = Usuario(
        id_usuario=empleado_id,
        nombre=nombre,
        contrasena="",
        rol="empleado",
        activo=activo_bool
    )

    return update_usuario(usuario)