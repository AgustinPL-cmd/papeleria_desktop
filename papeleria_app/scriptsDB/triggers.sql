USE papeleria_marlons;

DELIMITER $$

CREATE TRIGGER ValidarPrecioVentaVsCosto
BEFORE INSERT ON productos
FOR EACH ROW
BEGIN
    IF NEW.precio_unitario_venta < NEW.precio_unitario_compra THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR: El precio de venta no puede ser menor que el costo de compra';
    END IF;
END $$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER tr_reducir_stock_venta
AFTER INSERT ON Ventas
FOR EACH ROW
BEGIN
    UPDATE Productos
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id_producto = NEW.productoId;
END $$

DELIMITER ;

