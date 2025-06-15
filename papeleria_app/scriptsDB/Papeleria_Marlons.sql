CREATE DATABASE Papeleria_Marlons;
USE Papeleria_Marlons;

-- Tabla: Usuarios
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL, 
    rol ENUM('encargado', 'empleado') NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla: Categorías
CREATE TABLE Categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL
);

-- Tabla: Productos
CREATE TABLE Productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_unitario_venta DECIMAL(10, 2) NOT NULL,
    precio_unitario_compra DECIMAL(10, 2) NOT NULL,
    stock_actual INT NOT NULL,
    stock_minimo INT NOT NULL,
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria)
);

-- Tabla: Ventas
CREATE TABLE Ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT,
    total_venta DECIMAL(10, 2) NOT NULL,
    ganancia_total DECIMAL(10, 2),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- Tabla: DetalleVenta
CREATE TABLE DetalleVenta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT,
    id_producto INT,
    cantidad INT NOT NULL,
    precio_venta_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    ganancia_unitaria DECIMAL(10, 2),
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- Tabla: SugerenciasClientes
CREATE TABLE SugerenciasClientes (
    id_sugerencia INT AUTO_INCREMENT PRIMARY KEY,
    fecha_sugerencia DATETIME DEFAULT CURRENT_TIMESTAMP,
    producto_sugerido VARCHAR(100),
    comentario TEXT
);

-- Tabla: AlertasInventario
CREATE TABLE AlertasInventario (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    fecha_alerta DATETIME DEFAULT CURRENT_TIMESTAMP,
    stock_actual INT NOT NULL,
    stock_minimo INT NOT NULL,
    estado ENUM('pendiente', 'resuelto') DEFAULT 'pendiente',
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

ALTER TABLE Productos ADD estado ENUM('Activo', 'Suspendido') NOT NULL DEFAULT 'Activo';
