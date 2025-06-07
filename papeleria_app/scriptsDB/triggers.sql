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


