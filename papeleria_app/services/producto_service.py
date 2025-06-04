from papeleria_app.repositorios.producto_repo import insert_productos
from papeleria_app.repositorios.categoria_repo import get_categoria_by_name
import flet as ft

def registrar_producto(campos, page):
    error = validaciones_campos_insert(campos, page)
    if not error:
        valores = {}
        for i, campo in enumerate(campos):
            if isinstance(campo, ft.Row):
                etiqueta = campo.controls[0].value.replace(":", "")
                input_box = campo.controls[1]

                if isinstance(input_box, ft.TextField) or isinstance(input_box, ft.Dropdown):
                    valor = input_box.value.strip() if isinstance(input_box, ft.TextField) else input_box.value
                    valores[etiqueta] = valor

        # Validar existencia de categoría
        categoria = get_categoria_by_name(valores.get("CATEGORIA"))
        if categoria is None:
            return False, f"Categoría '{valores.get('CATEGORIA')}' no existe en la base de datos."

        # Pasar los datos al servicio
        resultado, mensaje = insert_productos(
            nombre_producto=valores.get("PRODUCTO"),
            descripcion=valores.get("DESCRIPCIÓN"),
            precio_unitario_venta=valores.get("PRECIO DE VENTA"),
            precio_unitario_compra=valores.get("PRECIO DE COMPRA"),
            stock_actual=valores.get("STOCK ACTUAL"),
            stock_minimo=valores.get("STOCK MÍNIMO"),
            id_categoria= categoria.id_categoria
        )

        # Mostrar mensaje
        return True, mensaje



def validaciones_campos_insert(campos,page):
    error = False
    campos_numericos = ["PRECIO DE VENTA", "PRECIO DE COMPRA", "STOCK ACTUAL", "STOCK MÍNIMO"]

    # Recorrer los campos en campos
    for i, campo in enumerate(campos):
        # Si el campo es de tipo Row
        if isinstance(campo, ft.Row):
            # Accede a su controls (text y textfield)
            etiqueta = campo.controls[0].value.replace(":", "")  # Elimina los ":" al final
            input_box = campo.controls[1]

            # Si input_box es textfield
            if isinstance(input_box, ft.TextField):
                valor = input_box.value.strip()

                # Validar campo vacío
                if valor == "":
                    campos[i + 1].visible = True
                    campos[i + 1].value = f"Error: el campo '{etiqueta}' no puede estar vacío.\n"
                    error = True
                # Validar que no sea menor a 0 si es numérico
                elif etiqueta in campos_numericos:
                    try:
                        numero = float(valor)
                        if numero < 0:
                            campos[i + 1].visible = True
                            campos[i + 1].value = f"Error: el campo '{etiqueta}' no puede ser menor a 0.\n"
                            error = True

                    except ValueError:
                        campos[i + 1].visible = True
                        campos[i + 1].value = f"Error: el campo '{etiqueta}' debe ser un número.\n"
                        error = True
            elif isinstance(input_box, ft.Dropdown):
                valor = input_box.value
                if valor == None:
                    campos[i + 1].visible = True
                    campos[i + 1].value = f"Error: el campo '{etiqueta}' no puede estar vacío.\n"
                    error = True

    page.update()
    return error


