USE papeleria_marlons;

-- Insertar usuarios
INSERT INTO Usuarios (nombre, contrasena, rol) VALUES
('admin', 'admin123', 'encargado'), -- contraseña: password
('Juan Pérez', 'emp123', 'empleado');

-- Insertar categorías
INSERT INTO Categorias (nombre_categoria) VALUES
('Papelería'),
('Material de Oficina'),
('Arte y Dibujo'),
('Escolar'),
('Electrónica');

-- Insertar productos
INSERT INTO Productos (nombre_producto, descripcion, precio_unitario_venta, precio_unitario_compra, stock_actual, stock_minimo, id_categoria) VALUES
('Lápiz HB', 'Lápiz grafito número 2', 5.00, 2.50, 100, 20, 1),
('Cuaderno Profesional', 'Cuaderno de 100 hojas rayadas', 45.00, 25.00, 50, 10, 4),
('Bolígrafo Azul', 'Paquete con 10 bolígrafos azules', 35.00, 18.00, 80, 15, 1),
('Tijeras Escolares', 'Tijeras de punta redonda', 25.00, 12.00, 30, 5, 4),
('Goma de Borrar', 'Goma blanca estándar', 8.00, 3.50, 120, 30, 1),
('Marcadores Permanentes', 'Set de 6 colores', 65.00, 35.00, 40, 8, 3),
('Calculadora Científica', 'Calculadora con 240 funciones', 150.00, 90.00, 15, 3, 5),
('Carpeta de Argollas', 'Carpeta tamaño carta con argollas', 55.00, 30.00, 25, 5, 2),
('Resaltadores', 'Paquete con 5 colores', 40.00, 22.00, 60, 12, 1),
('USB 32GB', 'Memoria USB marca Kingston', 120.00, 70.00, 20, 4, 5);

-- Insertar ventas (con números de venta repetidos para agrupar)
-- 5 ventas de hoy
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(NOW(), 2, 10.00, 1001, 1, 2),
(NOW(), 1, 45.00, 1001, 2, 2),
(NOW(), 3, 75.00, 1002, 3, 2),
(NOW(), 1, 25.00, 1002, 4, 2),
(NOW(), 2, 16.00, 1003, 5, 2),
(NOW(), 1, 65.00, 1003, 6, 2),
(NOW(), 1, 150.00, 1004, 7, 2),
(NOW(), 2, 110.00, 1004, 8, 2),
(NOW(), 3, 120.00, 1005, 9, 2),
(NOW(), 1, 120.00, 1005, 10, 2);

-- 5 ventas de ayer
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(DATE_SUB(NOW(), INTERVAL 1 DAY), 5, 25.00, 1006, 1, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 2, 90.00, 1006, 2, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 1, 35.00, 1007, 3, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 3, 75.00, 1007, 4, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 4, 32.00, 1008, 5, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 1, 65.00, 1008, 6, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 2, 300.00, 1009, 7, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 1, 55.00, 1009, 8, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 2, 80.00, 1010, 9, 2),
(DATE_SUB(NOW(), INTERVAL 1 DAY), 1, 120.00, 1010, 10, 2);

-- 10 ventas del resto del mes
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(DATE_SUB(NOW(), INTERVAL 2 DAY), 3, 15.00, 1011, 1, 2),
(DATE_SUB(NOW(), INTERVAL 2 DAY), 1, 45.00, 1011, 2, 2),
(DATE_SUB(NOW(), INTERVAL 3 DAY), 2, 70.00, 1012, 3, 2),
(DATE_SUB(NOW(), INTERVAL 3 DAY), 1, 25.00, 1012, 4, 2),
(DATE_SUB(NOW(), INTERVAL 4 DAY), 5, 40.00, 1013, 5, 2),
(DATE_SUB(NOW(), INTERVAL 4 DAY), 1, 65.00, 1013, 6, 2),
(DATE_SUB(NOW(), INTERVAL 5 DAY), 1, 150.00, 1014, 7, 2),
(DATE_SUB(NOW(), INTERVAL 5 DAY), 2, 110.00, 1014, 8, 2),
(DATE_SUB(NOW(), INTERVAL 6 DAY), 3, 120.00, 1015, 9, 2),
(DATE_SUB(NOW(), INTERVAL 6 DAY), 1, 120.00, 1015, 10, 2);


USE Papeleria_Marlons;

-- Insertar un nuevo empleado
INSERT INTO Usuarios (nombre, contrasena, rol) 
VALUES ('Ana López', 'emp456', 'empleado');

-- Insertar 5 nuevas ventas para el nuevo empleado
-- Venta 1 (2 productos)
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(NOW(), 3, 15.00, 1016, 1, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López')),
(NOW(), 1, 45.00, 1016, 2, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López'));

-- Venta 2 (2 productos)
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(NOW(), 2, 70.00, 1017, 3, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López')),
(NOW(), 1, 25.00, 1017, 4, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López'));

-- Venta 3 (2 productos)
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(NOW(), 4, 32.00, 1018, 5, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López')),
(NOW(), 1, 65.00, 1018, 6, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López'));

-- Venta 4 (2 productos)
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(NOW(), 1, 150.00, 1019, 7, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López')),
(NOW(), 2, 110.00, 1019, 8, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López'));

-- Venta 5 (2 productos)
INSERT INTO Ventas (fecha_venta, cantidad, subtotal, numVenta, productoId, usuarioId) VALUES
(NOW(), 3, 120.00, 1020, 9, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López')),
(NOW(), 1, 120.00, 1020, 10, (SELECT id_usuario FROM Usuarios WHERE nombre = 'Ana López'));
