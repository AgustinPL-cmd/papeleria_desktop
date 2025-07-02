# papeleria_app/repositorios/empleado_repo.py

from typing import List
from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    rol: str
    activo: bool

empleados_simulados = [
    Usuario(nombre="Ana Escobedo", rol="empleado", activo=True),
    Usuario(nombre="Agustín Lopez", rol="empleado", activo=True),
    Usuario(nombre="Citlalli Lira", rol="empleado", activo=True),
    Usuario(nombre="Juan Pérez", rol="empleado", activo=True),
]

def obtener_empleados_simulados() -> List[Usuario]:
    return empleados_simulados

def eliminar_o_suspender_empleado(nombre: str) -> bool:
    global empleados_simulados
    if nombre == "Juan Pérez":
        # Eliminación física porque no tiene ventas
        empleados_simulados = [e for e in empleados_simulados if e.nombre != nombre]
        return True
    else:
        # Cambiar estado a inactivo porque tiene ventas
        for e in empleados_simulados:
            if e.nombre == nombre:
                if e.activo:
                    e.activo = False
                    return True
                else:
                    # Ya está inactivo
                    return False
    return False