INSERT INTO `roles` (id, name, description, created_at) VALUES
(1, 'Administrador', 'Administrador del sistema con todos los permisos', NOW()),
(2, 'Vendedor', 'Encargado de la gestión y atención de ventas a clientes', NOW()),
(3, 'Almacenero', 'Responsable de la administración y control del inventario', NOW());

UPDATE `users` SET
    role_id = 1,
    avatar = '/assets/images/avatars/brian-hughes.jpg',
    settings = '{"layout": {}, "theme": {}}',
    shortcuts = '["apps.calendar", "apps.mailbox", "apps.contacts"]'
WHERE id = 1;

INSERT INTO `units_of_measurement` (id, name, shortcut, description, status, created_by, created_at) VALUES
(1, 'Unidad', 'und', 'Producto vendido por unidades individuales', 1, 1, NOW()),
(2, 'Juego', 'kit', 'Conjunto de piezas que se venden como un paquete completo', 1, 1, NOW()),
(3, 'Caja', 'caja', 'Contenedor con múltiples unidades, paquetes o juegos', 1, 1, NOW()),
(4, 'Docena', 'doc', 'Conjunto de doce unidades del mismo producto', 1, 1, NOW()),
(5, 'Par', 'par', NULL, 1, 1, NOW());