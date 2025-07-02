# 📚 Gestión de Papelería  

Sistema para administrar inventario, pedidos y reportes de materiales de oficina.  

---
## 📌 **Resumen** <!-- {#resumen} -->

<!-- {#descripción-del-proyecto} -->
🔍 Sistema de gestión de papelería diseñado para **controlar ventas**,  
**gestionar emplados** y **generar reportes** en tiempo real.  

<!-- {#características-clave} -->
✨ **Funcionalidades destacadas**:  
- 📦 Monitorización de stock con alertas (`#inventario-automatizado`).  
- 📊 Dashboards interactivos (`#data-visualization`).  
- 🔄 UI/UX Dinámica (`#api-rest`).  

<!-- {#tecnologías} -->
🛠️ **Stack técnico**:  

+ Frontend: Flet(Python)(#frontend)  
+ Backend: Python (#microservicios)  
+ DB: MySql (#nosql)  

## 🖼️ Capturas del Sistema  

| **Vista**               | **Descripción**                              | **Etiqueta GitHub**               |
|-------------------------|---------------------------------------------|-----------------------------------|
| ![Pantalla de Inicio](https://i.imgur.com/PiYb3Sn.png)   | Pantalla Inicio         | `#ui` `#pantalla principal`               |
| ![Login](https://i.imgur.com/dYgOWN1.png)          | Login            | `#login`            |
| ![Pantalla principal empleado](https://i.imgur.com/svQZZNw.png)   | Sección para gestionar ventas por empleado              | `#ventas` `#empleado`            |
| ![Registrar Venta](https://i.imgur.com/hkX7vAS.png)| Registro de venta               | `#empleado` `#venta`         |
| ![Dashboard Admin](https://i.imgur.com/kPdv1f2.png)             | Dashboard Admin                | `#dashboard` `#admin`             |


---

## 📦 Módulos Principales  
+ repositorios/       # Lógica backend donde se llevana a cabo las consultas sql
+ ui/         # Sección FrontEnd en donde se ven las diferentes vistas del programa y se integra con el backend
+ models/      # Sección de las entidades de la BD convertidas en clases
