-- Insertar datos en la tabla plans
INSERT INTO `plans` (
    id, title, subtitle, price, max_branch_offices, max_warehouses, max_purchases, max_users, max_products, max_services, max_documents
) VALUES
(1, 'Básico', 'Ideal para pequeñas empresas con una sola sucursal', 99.00, 1, 1, 100, 2, 50, 50, 1000),
(2, 'Empresarial', 'Para empresas en crecimiento con múltiples sucursales', 299.00, 5, 10, 1000, 50, 500, 500, 10000),
(3, 'Corporativo', 'Para grandes empresas con operaciones extensas', 699.00, 20, 50, 5000, 200, 2000, 2000, 50000);

-- Insertar datos en la tabla currencies
INSERT INTO `currencies` (id, name, description, code, symbol) VALUES
(1, 'US Dollar', 'United States Dollar', 'USD', '$'),
(2, 'Euro', 'European Union Currency', 'EUR', '€'),
(3, 'British Pound', 'United Kingdom Currency', 'GBP', '£'),
(4, 'Japanese Yen', 'Japanese Currency', 'JPY', '¥'),
(5, 'Mexican Peso', 'Mexican Currency', 'MXN', '$'),
(6, 'Peruvian Sol', 'Currency of Peru', 'PEN', 'S/');

-- Insertar datos en la tabla roles
INSERT INTO `roles` (id, name, description, created_at) VALUES
(1, 'Administrador', 'Administrador del sistema con todos los permisos', NOW()),
(2, 'Gerente', 'Encargado de la supervisión general de la empresa', NOW()),
(3, 'Jefe de Ventas', 'Responsable del área de ventas', NOW()),
(4, 'Jefe de Almacén', 'Encargado de la gestión de almacenes', NOW()),
(5, 'Contador', 'Encargado de la contabilidad y finanzas', NOW()),
(6, 'Recursos Humanos', 'Encargado de la gestión del personal', NOW()),
(7, 'Soporte Técnico', 'Responsable de la asistencia técnica', NOW()),
(8, 'Analista de Datos', 'Analiza y genera reportes para la empresa', NOW());

-- Insertar datos en la tabla permissions
INSERT INTO `permissions` (id, name, description) VALUES
(1, 'manage_users', 'Crear, editar y eliminar usuarios'),
(2, 'view_reports', 'Ver informes y reportes'),
(3, 'edit_financials', 'Editar información financiera'),
(4, 'manage_inventory', 'Administrar el inventario'),
(5, 'process_sales', 'Procesar ventas'),
(6, 'approve_purchases', 'Aprobar compras'),
(7, 'manage_roles', 'Administrar roles y permisos'),
(8, 'access_sensitive_data', 'Acceder a datos sensibles');

-- Insertar asignaciones de permisos al rol Admin (tendrá todos los permisos)
INSERT INTO `role_permissions` (role_id, permission_id)
SELECT r.id, p.id
FROM roles r, permissions p
WHERE r.name = 'Administrador';

-- Asignar permisos específicos a otros roles
INSERT INTO `role_permissions` (role_id, permission_id)
SELECT r.id, p.id FROM roles r
JOIN permissions p ON 
(r.name = 'Gerente' AND p.name IN ('view_reports', 'approve_purchases', 'process_sales')) OR
(r.name = 'Jefe de Ventas' AND p.name IN ('process_sales', 'view_reports')) OR
(r.name = 'Jefe de Almacén' AND p.name IN ('manage_inventory', 'approve_purchases')) OR
(r.name = 'Contador' AND p.name IN ('edit_financials', 'view_reports')) OR
(r.name = 'Recursos Humanos' AND p.name IN ('manage_users')) OR
(r.name = 'Soporte Técnico' AND p.name IN ('access_sensitive_data')) OR
(r.name = 'Analista de Datos' AND p.name IN ('view_reports', 'access_sensitive_data'));

-- Insertar datos en la tabla users
INSERT INTO `users` (password, role_id, username, avatar, email, settings, shortcuts)
VALUES (
    '$2a$12$Bs0zCFp19Y7CBjrUuyTlNecseEPNx0pVVjW72jmBMP6P/JbsXyE0e', -- password
    1,
    'Jlenin',
    '/assets/images/avatars/brian-hughes.jpg',
    'admin@facil.com',
    '{"layout": {}, "theme": {}}',
    '["apps.calendar", "apps.mailbox", "apps.contacts"]'
);

UPDATE `users` SET
    employee_id = 1, company_id = 1, role_id = 1,
    avatar = '/assets/images/avatars/brian-hughes.jpg',
    settings = '{"layout": {}, "theme": {}}',
    shortcuts = '["apps.calendar", "apps.mailbox", "apps.contacts"]'
WHERE id = 1;

-- Insertar datos en la tabla companies
INSERT INTO `companies` (id, name, ruc, email, phone, address, status, created_by, created_at) VALUES
(1, 'Ferretería San Juan S.A.', '20123456789', 'contacto@ferresanjuan.com', '015678901', 'Av. Universitaria 1234, Lima, Perú', 1, 1, NOW()),
(2, 'Materiales del Norte SAC', '20456789012', 'ventas@matnorte.com', '016543210', 'Calle Comercio 456, Trujillo, Perú', 1, 1, NOW());

-- Insertar datos en la tabla sucursales
INSERT INTO `branch_offices` (id, company_id, name, address, phone, status, created_by, created_at) VALUES
(1, 1, 'Sucursal Lima', 'Av. Aviación 2345, Lima, Perú', '014567890', 1, 1, NOW()),
(2, 1, 'Sucursal Arequipa', 'Calle Mercaderes 789, Arequipa, Perú', '054678901', 1, 1, NOW()),
(3, 1, 'Sucursal Cusco', 'Av. El Sol 555, Cusco, Perú', '084567123', 1, 1, NOW()),
(4, 1, 'Sucursal Chiclayo', 'Calle Balta 789, Chiclayo, Perú', '074678345', 1, 1, NOW()),
(5, 2, 'Sucursal Trujillo', 'Av. América Norte 123, Trujillo, Perú', '044345678', 1, 1, NOW()),
(6, 2, 'Sucursal Piura', 'Av. Grau 432, Piura, Perú', '073567890', 1, 1, NOW()),
(7, 2, 'Sucursal Tacna', 'Jr. Bolognesi 210, Tacna, Perú', '052678234', 1, 1, NOW()),
(8, 2, 'Sucursal Huancayo', 'Calle Real 678, Huancayo, Perú', '064345789', 1, 1, NOW());

-- Insertar datos en la tabla almacenes
INSERT INTO `warehouses` (id, branch_office_id, name, description, address, status, created_by, created_at) VALUES
(1, 1, 'Almacén Central Lima', 'Almacén principal en Lima', 'Av. Aviación 2345, Lima, Perú', 1, 1, NOW()),
(2, 1, 'Depósito Lima', 'Depósito de materiales', 'Calle Industrial 567, Lima, Perú', 1, 1, NOW()),
(3, 2, 'Almacén Arequipa', 'Centro de distribución en el sur', 'Calle Mercaderes 789, Arequipa, Perú', 1, 1, NOW()),
(4, 3, 'Almacén Cusco', 'Depósito de herramientas en Cusco', 'Av. El Sol 555, Cusco, Perú', 1, 1, NOW()),
(5, 4, 'Almacén Chiclayo', 'Depósito de ferretería en Chiclayo', 'Calle Balta 789, Chiclayo, Perú', 1, 1, NOW()),
(6, 5, 'Almacén Trujillo', 'Almacén central en Trujillo', 'Av. América Norte 123, Trujillo, Perú', 1, 1, NOW()),
(7, 6, 'Almacén Piura', 'Depósito de materiales en Piura', 'Av. Grau 432, Piura, Perú', 1, 1, NOW()),
(8, 7, 'Almacén Tacna', 'Centro de distribución en Tacna', 'Jr. Bolognesi 210, Tacna, Perú', 1, 1, NOW()),
(9, 8, 'Almacén Huancayo', 'Depósito de herramientas en Huancayo', 'Calle Real 678, Huancayo, Perú', 1, 1, NOW());

-- Insertar datos en la tabla suscripciones
INSERT INTO `subscriptions` (id, company_id, plan_id, end_date, status) VALUES
(1, 1, 1, '2026-03-01 15:04:41.474091', 'active');

-- Insertar datos en la tabla work_areas
INSERT INTO `work_areas` (id, name, description, status, created_by, created_at) VALUES
(1, 'Desarrollo de Software', 'Área encargada del desarrollo de aplicaciones', 1, 1, NOW()),
(2, 'Recursos Humanos', 'Gestión de personal y administración', 1, 1, NOW()),
(3, 'Finanzas', 'Gestión financiera y contabilidad', 1, 1, NOW()),
(4, 'Logística', 'Manejo de inventarios y distribución', 1, 1, NOW()),
(5, 'Marketing', 'Publicidad y estrategias de mercado', 1, 1, NOW());

-- Insertar datos en la tabla job_positions
INSERT INTO `job_positions` (id, work_area_id, name, description, status, created_by, created_at) VALUES
(1, 1, 'Ingeniero de Software', 'Desarrollo de aplicaciones y sistemas', 1, 1, NOW()),
(2, 1, 'Arquitecto de Software', 'Diseño y planificación de sistemas complejos', 1, 1, NOW()),
(3, 2, 'Gerente de Recursos Humanos', 'Supervisión del área de RRHH', 1, 1, NOW()),
(4, 2, 'Especialista en Reclutamiento', 'Búsqueda y selección de personal', 1, 1, NOW()),
(5, 3, 'Analista Financiero', 'Gestión de análisis financiero y reportes', 1, 1, NOW()),
(6, 4, 'Coordinador de Logística', 'Gestión de almacenes y transporte', 1, 1, NOW()),
(7, 5, 'Especialista en Marketing Digital', 'Estrategias de marketing online', 1, 1, NOW());

-- Insertar datos en la tabla employees
INSERT INTO `employees` (
    id, names, surname, second_surname, photo, warehouse_id, 
    document_type, document_number, birth_date, gender, email, phone, address, 
    hire_date, job_position_id, salary, status, created_at
) VALUES
(1, 'Lenin Josue', 'Monrroy', 'Vasquez', 'https://example.com/photos/gloria.jpg', 1,
 'dni', '72329210', '2002-01-25', 'M', 'lenin.monrroy@facil.com', '992754901', 
 'Jr. Ayacucho 369, Chorrillos, Lima', '2025-01-01', 1, 4500.00, 1, NOW()),
(2, 'Juan Carlos', 'González', 'Pérez', 'https://example.com/photos/juan.jpg', 1,
 'dni', '12345678', '1985-06-12', 'M', 'juan.gonzalez@example.com', '987654321', 
 'Av. Larco 123, Miraflores, Lima', '2015-08-10', 3, 7500.00, 1, NOW()),
(3, 'María Elena', 'Rodríguez', 'Lopez', 'https://example.com/photos/maria.jpg', 2,
 'dni', '87654321', '1990-03-25', 'F', 'maria.rodriguez@example.com', '987123456', 
 'Calle Los Cedros 456, San Isidro, Lima', '2018-05-20', 5, 4800.00, 1, NOW()),
(4, 'Pedro Luis', 'Fernández', 'Castro', 'https://example.com/photos/pedro.jpg', 3,
 'dni', '56781234', '1982-12-01', 'M', 'pedro.fernandez@example.com', '975312468', 
 'Jr. Amazonas 789, Ate, Lima', '2010-09-15', 6, 5500.00, 1, NOW()),
(5, 'Ana Gabriela', 'Salazar', 'Torres', 'https://example.com/photos/ana.jpg', 4,
 'dni', '34567890', '1995-07-19', 'F', 'ana.salazar@example.com', '965478123', 
 'Urb. Santa Anita, Lima', '2020-02-01', 4, 3200.00, 1, NOW()),
(6, 'Luis Eduardo', 'Cárdenas', 'Reyes', 'https://example.com/photos/luis.jpg', 5,
 'dni', '23456789', '1988-11-30', 'M', 'luis.cardenas@example.com', '951236547', 
 'Av. Grau 456, Barranco, Lima', '2016-07-18', 1, 4600.00, 1, NOW()),
(7, 'Carmen Rosa', 'Mendoza', 'Flores', 'https://example.com/photos/carmen.jpg', 6,
 'dni', '65432178', '1992-05-15', 'F', 'carmen.mendoza@example.com', '941235478', 
 'Calle Primavera 123, Surco, Lima', '2019-11-23', 5, 5200.00, 1, NOW()),
(8, 'Jorge Andrés', 'Vargas', 'Ramos', 'https://example.com/photos/jorge.jpg', 7,
 'dni', '32178945', '1979-09-10', 'M', 'jorge.vargas@example.com', '932145678', 
 'Calle Los Olivos 789, San Juan de Lurigancho, Lima', '2005-03-10', 2, 12000.00, 1, NOW()),
(9, 'Patricia Verónica', 'Ortiz', 'Fernández', 'https://example.com/photos/patricia.jpg', 8,
 'dni', '78965412', '1998-08-20', 'F', 'patricia.ortiz@example.com', '965412378', 
 'Av. Canadá 789, La Victoria, Lima', '2022-06-12', 7, 1800.00, 1, NOW()),
(10, 'Ricardo Antonio', 'Sánchez', 'Gómez', 'https://example.com/photos/ricardo.jpg', 9,
 'dni', '15935746', '1987-04-14', 'M', 'ricardo.sanchez@example.com', '911234567', 
 'Jr. Tupac Amaru 456, Rimac, Lima', '2014-12-05', 1, 6800.00, 1, NOW()),
(11, 'Silvia Beatriz', 'Chávez', 'Rivas', 'https://example.com/photos/silvia.jpg', 1,
 'dni', '25874136', '1993-06-22', 'F', 'silvia.chavez@example.com', '923654789', 
 'Calle San Felipe 321, Magdalena, Lima', '2017-09-30', 6, 5400.00, 1, NOW()),
(12, 'José Fernando', 'Navarro', 'Soto', 'https://example.com/photos/jose.jpg', 2,
 'dni', '75395148', '1980-10-05', 'M', 'jose.navarro@example.com', '987456321', 
 'Av. Universitaria 852, Los Olivos, Lima', '2007-04-28', 3, 8200.00, 1, NOW()),
(13, 'Gloria Elisabeth', 'Rojas', 'Espinoza', 'https://example.com/photos/gloria.jpg', 3,
 'dni', '36985214', '1991-02-08', 'F', 'gloria.rojas@example.com', '975214563', 
 'Jr. Ayacucho 369, Chorrillos, Lima', '2021-01-14', 6, 4500.00, 1, NOW());

-- Insertar datos en la tabla taxes
INSERT INTO `taxes` (id, name, description, rate, tax_type, created_by) VALUES
(1, 'IGV', 'Impuesto General a las Ventas (18%)', 18.00, 0, 1),
(2, 'ISC', 'Impuesto Selectivo al Consumo', 10.00, 0, 1),
(3, 'Percepción', 'Percepción de IGV', 2.00, 0, 1),
(4, 'Retención', 'Retención del IGV', 3.00, 0, 1),
(5, 'Impuesto Fijo', 'Ejemplo de impuesto con monto fijo', 5.00, 1, 1);

-- Insertar datos en la tabla exchange_rates
INSERT INTO `exchange_rates` (id, base_currency_id, target_currency_id, exchange_rate, created_by) VALUES
(1, 6, 1, 3.80, 1), -- PEN a USD
(2, 6, 2, 4.10, 1), -- PEN a EUR
(3, 6, 3, 4.80, 1), -- PEN a GBP
(4, 6, 4, 0.028, 1); -- PEN a JPY

-- Insertar datos en la tabla categories
INSERT INTO `categories` (id, name, description, status, created_by, created_at) VALUES
(1, 'Herramientas Manuales', 'Categoría para herramientas como martillos, destornilladores, llaves, etc.', 1, 1, NOW()),
(2, 'Herramientas Eléctricas', 'Categoría para taladros, sierras eléctricas, lijadoras y otras herramientas eléctricas.', 1, 1, NOW()),
(3, 'Materiales de Construcción', 'Materiales como cemento, ladrillos, arena y piedra.', 1, 1, NOW()),
(4, 'Pinturas y Acabados', 'Pinturas, barnices, brochas, rodillos y accesorios para acabados.', 1, 1, NOW()),
(5, 'Plomería', 'Tubos, conexiones, válvulas, llaves de paso y artículos de plomería.', 1, 1, NOW()),
(6, 'Electricidad', 'Cables, enchufes, interruptores, luminarias y artículos eléctricos.', 1, 1, NOW()),
(7, 'Jardinería', 'Herramientas de jardinería, fertilizantes, semillas y macetas.', 1, 1, NOW()),
(8, 'Seguridad Industrial', 'Cascos, guantes, gafas de seguridad y ropa reflectante.', 1, 1, NOW()),
(9, 'Adhesivos y Selladores', 'Siliconas, pegamentos, masillas y selladores de todo tipo.', 1, 1, NOW()),
(10, 'Tornillería y Fijaciones', 'Tornillos, clavos, pernos, tuercas y arandelas.', 1, 1, NOW()),
(11, 'Cerraduras', 'Cerraduras para puertas de todo tipo, incluyendo residenciales y comerciales.', 1, 1, NOW()),
(12, 'Ferretería General', 'Bisagras, rieles, soportes y artículos generales.', 1, 1, NOW()),
(13, 'Automatización y Domótica', 'Motores, sistemas de automatización y dispositivos de domótica.', 1, 1, NOW()),
(14, 'Maquinaria Pesada', 'Pequeña maquinaria como mezcladoras, compactadoras y otros equipos.', 1, 1, NOW()),
(15, 'Accesorios para Baño y Cocina', 'Grifería, accesorios para baño y artículos para cocina.', 1, 1, NOW()),
(16, 'Vidrio y Acrílicos', 'Cristales, acrílicos y materiales relacionados.', 1, 1, NOW()),
(17, 'Equipos de Medición', 'Cintas métricas, niveles, calibradores y otros instrumentos de medición.', 1, 1, NOW()),
(18, 'Maderas y Derivados', 'Tablas, triplay, MDF y otros derivados de madera.', 1, 1, NOW()),
(19, 'Sistemas de Riego', 'Tuberías, aspersores y equipos para riego.', 1, 1, NOW()),
(20, 'Calentadores y Climatización', 'Calentadores, ventiladores y aire acondicionado.', 1, 1, NOW()),
(21, 'Candados', 'Candados de seguridad de diferentes niveles de protección.', 1, 1, NOW()),
(22, 'Cilindros', 'Cilindros para cerraduras y sistemas de seguridad.', 1, 1, NOW()),
(23, 'Cerrojos', 'Sistemas de cerrojos manuales y automáticos.', 1, 1, NOW()),
(24, 'Accesorios de Cerrajería', 'Componentes y accesorios para sistemas de cerrajería.', 1, 1, NOW());

-- Insertar datos en la tabla brands
INSERT INTO `brands` (id, name, description, logo_url, website_url, status, created_by, created_at) VALUES
(1, 'DeWalt', 'Fabricante de herramientas eléctricas y accesorios para profesionales y aficionados.', 'https://example.com/logos/dewalt.png', 'https://www.dewalt.com', 1, 1, NOW()),
(2, 'Bosch', 'Marca reconocida por herramientas eléctricas, electrodomésticos y tecnología industrial.', 'https://example.com/logos/bosch.png', 'https://www.bosch.com', 1, 1, NOW()),
(3, 'Stanley', 'Líder en herramientas manuales, medidores y productos de almacenamiento.', 'https://example.com/logos/stanley.png', 'https://www.stanleytools.com', 1, 1, NOW()),
(4, 'Makita', 'Proveedor global de herramientas eléctricas y equipos industriales.', 'https://example.com/logos/makita.png', 'https://www.makitatools.com', 1, 1, NOW()),
(5, 'Black+Decker', 'Fabricante de herramientas eléctricas, jardinería y electrodomésticos.', 'https://example.com/logos/blackdecker.png', 'https://www.blackanddecker.com', 1, 1, NOW()),
(6, 'Truper', 'Empresa líder en herramientas manuales, eléctricas y accesorios de ferretería.', 'https://example.com/logos/truper.png', 'https://www.truper.com', 1, 1, NOW()),
(7, 'Klein Tools', 'Fabricante de herramientas manuales y equipos eléctricos de alta calidad.', 'https://example.com/logos/klein.png', 'https://www.kleintools.com', 1, 1, NOW()),
(8, 'Hilti', 'Proveedor especializado en herramientas y sistemas de fijación para construcción.', 'https://example.com/logos/hilti.png', 'https://www.hilti.com', 1, 1, NOW()),
(9, 'Fischer', 'Expertos en soluciones de fijación y anclajes para construcción.', 'https://example.com/logos/fischer.png', 'https://www.fischer.com', 1, 1, NOW()),
(10, 'RIDGID', 'Marca especializada en herramientas para plomería y construcción.', 'https://example.com/logos/ridgid.png', 'https://www.ridgid.com', 1, 1, NOW()),
(11, 'Irwin', 'Fabricante de herramientas de corte, sujeción y perforación.', 'https://example.com/logos/irwin.png', 'https://www.irwin.com', 1, 1, NOW()),
(12, '3M', 'Líder en productos industriales como adhesivos, cintas, abrasivos y más.', 'https://example.com/logos/3m.png', 'https://www.3m.com', 1, 1, NOW()),
(13, 'Troy-Bilt', 'Especialista en herramientas y equipos de jardinería.', 'https://example.com/logos/troybilt.png', 'https://www.troybilt.com', 1, 1, NOW()),
(14, 'Husqvarna', 'Fabricante de herramientas para jardinería, agricultura y construcción.', 'https://example.com/logos/husqvarna.png', 'https://www.husqvarna.com', 1, 1, NOW()),
(15, 'Craftsman', 'Marca confiable en herramientas manuales, eléctricas y almacenamiento.', 'https://example.com/logos/craftsman.png', 'https://www.craftsman.com', 1, 1, NOW()),
(16, 'Milwaukee', 'Proveedor de herramientas eléctricas y accesorios de alta calidad.', 'https://example.com/logos/milwaukee.png', 'https://www.milwaukeetool.com', 1, 1, NOW()),
(17, 'Metabo', 'Especialista en herramientas eléctricas y accesorios industriales.', 'https://example.com/logos/metabo.png', 'https://www.metabo.com', 1, 1, NOW()),
(18, 'Bostitch', 'Fabricante de herramientas de fijación como engrampadoras y clavos.', 'https://example.com/logos/bostitch.png', 'https://www.bostitch.com', 1, 1, NOW()),
(19, 'Simpson Strong-Tie', 'Líder en soluciones de anclaje y conectores estructurales.', 'https://example.com/logos/simpson.png', 'https://www.strongtie.com', 1, 1, NOW()),
(20, 'Paslode', 'Fabricante de herramientas de fijación neumáticas y a gas.', 'https://example.com/logos/paslode.png', 'https://www.paslode.com', 1, 1, NOW()),
(21, 'Assa Abloy', 'Líder mundial en soluciones de apertura de puertas, incluyendo cerraduras y sistemas de seguridad.', 'https://example.com/logos/assaabloy.png', 'https://www.assaabloy.com', 1, 1, NOW()),
(22, 'Mul-T-Lock', 'Fabricante de sistemas de cerraduras de alta seguridad.', 'https://example.com/logos/multlock.png', 'https://www.mul-t-lock.com', 1, 1, NOW()),
(23, 'Medeco', 'Especialistas en cerraduras de alta seguridad y sistemas de llaves controladas.', 'https://example.com/logos/medeco.png', 'https://www.medeco.com', 1, 1, NOW()),
(24, 'Kwikset', 'Fabricante de cerraduras residenciales y sistemas de llaves inteligentes.', 'https://example.com/logos/kwikset.png', 'https://www.kwikset.com', 1, 1, NOW()),
(25, 'Schlage', 'Marca reconocida en cerraduras residenciales y comerciales.', 'https://example.com/logos/schlage.png', 'https://www.schlage.com', 1, 1, NOW()),
(26, 'Yale', 'Pioneros en cerrajería con más de 180 años de experiencia.', 'https://example.com/logos/yale.png', 'https://www.yale.com', 1, 1, NOW()),
(27, 'Master Lock', 'Fabricante líder de candados y soluciones de seguridad.', 'https://example.com/logos/masterlock.png', 'https://www.masterlock.com', 1, 1, NOW()),
(28, 'ABUS', 'Especialistas en candados y sistemas de seguridad de alta calidad.', 'https://example.com/logos/abus.png', 'https://www.abus.com', 1, 1, NOW()),
(29, 'EVVA', 'Fabricante austriaco de sistemas de cerraduras de alta seguridad.', 'https://example.com/logos/evva.png', 'https://www.evva.com', 1, 1, NOW()),
(30, 'Sargent', 'Proveedor de soluciones de seguridad mecánicas y electrónicas.', 'https://example.com/logos/sargent.png', 'https://www.sargentlock.com', 1, 1, NOW());

-- Insertar datos en la tabla units_of_measurement
INSERT INTO `units_of_measurement` (id, name, shortcut, description, status, created_by, created_at) VALUES
(1, 'Unidad', 'und', 'Producto vendido por unidades individuales', 1, 1, NOW()),
(2, 'Juego', 'kit', 'Conjunto de piezas que se venden como un paquete completo', 1, 1, NOW()),
(3, 'Paquete', 'pqte', 'Varios artículos empaquetados juntos como una unidad de venta', 1, 1, NOW()),
(4, 'Caja', 'caja', 'Contenedor con múltiples unidades, paquetes o juegos', 1, 1, NOW()),
(5, 'Docena', 'doc', 'Conjunto de doce unidades del mismo producto', 1, 1, NOW()),
(6, 'Metro lineal', 'ml', 'Medida de longitud en metros', 1, 1, NOW()),
(7, 'Metro cuadrado', 'm²', 'Medida de área o superficie', 1, 1, NOW()),
(8, 'Kilogramo', 'kg', 'Medida de peso/masa equivalente a 1000 gramos', 1, 1, NOW()),
(9, 'Gramo', 'g', 'Medida de peso/masa', 1, 1, NOW()),
(10, 'Litro', 'lt', 'Medida de volumen para líquidos', 1, 1, NOW());

-- Insertar datos en la tabla products
INSERT INTO `products` (
    id, name, brand_id, unit_of_measurement_id, handle, description, tags, featured_image, images, 
    prices_cf, cost, tax_rate, quantity, sku, width, height, depth, weight, 
    barcode, extra_shipping_fee, status, created_by, created_at
) VALUES 
(1, 
    'Cerradura de Embutir Yale Superior', 6, 1, 'cerradura-embutir-yale-superior', 
    'Cerradura de embutir de alta seguridad con 5 puntos de anclaje. Ideal para puertas de entrada.', 
    '["seguridad", "puerta principal", "5 puntos"]', 'img-01',
    '[{"url":"uploads/images/products/01-320x200.jpg","featured":"img-01"}]',
    '[
        {
            "id": 1,
            "name": "price_1",
            "price": 33.7239
        },
        {
            "id": 2,
            "name": "price_2",
            "price": 34.0578
        },
        {
            "id": 3,
            "name": "price_3",
            "price": 34.3917
        },
        {
            "id": 4,
            "name": "price_4",
            "price": 34.7256
        },
        {
            "id": 5,
            "name": "price_5",
            "price": 35.0595
        },
        {
            "id": 6,
            "name": "price_6",
            "price": 35.3934
        },
        {
            "id": 7,
            "name": "price_7",
            "price": 35.7273
        },
        {
            "id": 8,
            "name": "price_8",
            "price": 36.0612
        },
        {
            "id": 9,
            "name": "price_9",
            "price": 36.3951
        },
        {
            "id": 10,
            "name": "price_10",
            "price": 36.729
        },
        {
            "id": 11,
            "name": "price_11",
            "price": 37.0629
        },
        {
            "id": 12,
            "name": "price_12",
            "price": 37.3968
        },
        {
            "id": 13,
            "name": "price_13",
            "price": 37.7307
        },
        {
            "id": 14,
            "name": "price_14",
            "price": 38.0646
        },
        {
            "id": 15,
            "name": "price_15",
            "price": 38.3985
        },
        {
            "id": 16,
            "name": "price_16",
            "price": 38.7324
        },
        {
            "id": 17,
            "name": "price_17",
            "price": 39.0663
        },
        {
            "id": 18,
            "name": "price_18",
            "price": 39.4002
        },
        {
            "id": 19,
            "name": "price_19",
            "price": 39.7341
        },
        {
            "id": 20,
            "name": "price_20",
            "price": 40.068
        }
    ]',
    80, 18.00, 15, 'YALE-EMB-001', 8.5, 24.0, 7.2, 1.8, 
    '123456789012', 5.00, 1, 1
, NOW()),
(2, 
    'Candado ABUS Granit Plus', 8, 2, 'candado-abus-granit-plus',
    'Candado de seguridad Granit Plus con protección contra cortes y palancas. Nivel de seguridad 10.',
    '["alta seguridad", "antirobo", "exterior"]', 'img-02',
    '[{"url":"uploads/images/products/02-320x200.jpg","featured":"img-02"}]',
    '[
        {
            "id": 1,
            "name": "price_1",
            "price": 32.8957
        },
        {
            "id": 2,
            "name": "price_2",
            "price": 33.2214
        },
        {
            "id": 3,
            "name": "price_3",
            "price": 33.5471
        },
        {
            "id": 4,
            "name": "price_4",
            "price": 33.8728
        },
        {
            "id": 5,
            "name": "price_5",
            "price": 34.1985
        },
        {
            "id": 6,
            "name": "price_6",
            "price": 34.5242
        },
        {
            "id": 7,
            "name": "price_7",
            "price": 34.8499
        },
        {
            "id": 8,
            "name": "price_8",
            "price": 35.1756
        },
        {
            "id": 9,
            "name": "price_9",
            "price": 35.5013
        },
        {
            "id": 10,
            "name": "price_10",
            "price": 35.827
        },
        {
            "id": 11,
            "name": "price_11",
            "price": 36.1527
        },
        {
            "id": 12,
            "name": "price_12",
            "price": 36.4784
        },
        {
            "id": 13,
            "name": "price_13",
            "price": 36.8041
        },
        {
            "id": 14,
            "name": "price_14",
            "price": 37.1298
        },
        {
            "id": 15,
            "name": "price_15",
            "price": 37.4555
        },
        {
            "id": 16,
            "name": "price_16",
            "price": 37.7812
        },
        {
            "id": 17,
            "name": "price_17",
            "price": 38.1069
        },
        {
            "id": 18,
            "name": "price_18",
            "price": 38.4326
        },
        {
            "id": 19,
            "name": "price_19",
            "price": 38.7583
        },
        {
            "id": 20,
            "name": "price_20",
            "price": 39.084
        }
    ]',
    60, 18.00, 22, 'ABUS-GRP-002', 6.0, 9.0, 4.5, 0.8,
    '987654321098', 3.50, 1, 1
, NOW()),
(3, 
    'Cilindro Mul-T-Lock Interactive', 2, 3, 'cilindro-multlock-interactive',
    'Cilindro de alta seguridad con tecnología Interactive. Protección contra bumping y picking.',
    '["alta seguridad", "antimanipulación", "cilindro europeo"]', 'img-03',
    '[{"url":"uploads/images/products/03-320x200.jpg","featured":"img-03"}]',
    '[
        {
            "id": 1,
            "name": "price_1",
            "price": 36.8751
        },
        {
            "id": 2,
            "name": "price_2",
            "price": 37.2402
        },
        {
            "id": 3,
            "name": "price_3",
            "price": 37.6053
        },
        {
            "id": 4,
            "name": "price_4",
            "price": 37.9704
        },
        {
            "id": 5,
            "name": "price_5",
            "price": 38.3355
        },
        {
            "id": 6,
            "name": "price_6",
            "price": 38.7006
        },
        {
            "id": 7,
            "name": "price_7",
            "price": 39.0657
        },
        {
            "id": 8,
            "name": "price_8",
            "price": 39.4308
        },
        {
            "id": 9,
            "name": "price_9",
            "price": 39.7959
        },
        {
            "id": 10,
            "name": "price_10",
            "price": 40.161
        },
        {
            "id": 11,
            "name": "price_11",
            "price": 40.5261
        },
        {
            "id": 12,
            "name": "price_12",
            "price": 40.8912
        },
        {
            "id": 13,
            "name": "price_13",
            "price": 41.2563
        },
        {
            "id": 14,
            "name": "price_14",
            "price": 41.6214
        },
        {
            "id": 15,
            "name": "price_15",
            "price": 41.9865
        },
        {
            "id": 16,
            "name": "price_16",
            "price": 42.3516
        },
        {
            "id": 17,
            "name": "price_17",
            "price": 42.7167
        },
        {
            "id": 18,
            "name": "price_18",
            "price": 43.0818
        },
        {
            "id": 19,
            "name": "price_19",
            "price": 43.4469
        },
        {
            "id": 20,
            "name": "price_20",
            "price": 43.812
        }
    ]',
    95, 18.00, 8, 'MTL-INT-003', 3.5, 6.0, 3.5, 0.3,
    '456789012345', 2.00, 1, 1
, NOW()),
(4, 
    'Cerrojo Electrónico Schlage Encode', 5, 4, 'cerrojo-electronico-schlage-encode',
    'Cerrojo electrónico con WiFi integrado y apertura mediante smartphone. Compatible con asistentes de voz.',
    '["inteligente", "wifi", "huella digital", "teclado"]', 'img-04',
    '[{"url":"uploads/images/products/04-320x200.jpg","featured":"img-04"}]',
    '[
        {
            "id": 1,
            "name": "price_1",
            "price": 38.7537
        },
        {
            "id": 2,
            "name": "price_2",
            "price": 39.1374
        },
        {
            "id": 3,
            "name": "price_3",
            "price": 39.5211
        },
        {
            "id": 4,
            "name": "price_4",
            "price": 39.9048
        },
        {
            "id": 5,
            "name": "price_5",
            "price": 40.2885
        },
        {
            "id": 6,
            "name": "price_6",
            "price": 40.6722
        },
        {
            "id": 7,
            "name": "price_7",
            "price": 41.0559
        },
        {
            "id": 8,
            "name": "price_8",
            "price": 41.4396
        },
        {
            "id": 9,
            "name": "price_9",
            "price": 41.8233
        },
        {
            "id": 10,
            "name": "price_10",
            "price": 42.207
        },
        {
            "id": 11,
            "name": "price_11",
            "price": 42.5907
        },
        {
            "id": 12,
            "name": "price_12",
            "price": 42.9744
        },
        {
            "id": 13,
            "name": "price_13",
            "price": 43.3581
        },
        {
            "id": 14,
            "name": "price_14",
            "price": 43.7418
        },
        {
            "id": 15,
            "name": "price_15",
            "price": 44.1255
        },
        {
            "id": 16,
            "name": "price_16",
            "price": 44.5092
        },
        {
            "id": 17,
            "name": "price_17",
            "price": 44.8929
        },
        {
            "id": 18,
            "name": "price_18",
            "price": 45.2766
        },
        {
            "id": 19,
            "name": "price_19",
            "price": 45.6603
        },
        {
            "id": 20,
            "name": "price_20",
            "price": 46.044
        }
    ]',
    210, 18.00, 5, 'SCH-ENC-004', 12.0, 4.5, 2.8, 2.5,
    '789012345678', 8.00, 1, 1
, NOW()),
(5, 
    'Juego de Llaves Controladas Medeco', 3, 5, 'juego-llaves-controladas-medeco',
    'Juego de 5 llaves controladas con sistema de seguridad patentado. Incluye tarjeta de registro.',
    '["llaves controladas", "alta seguridad", "kit"]', 'img-05',
    '[{"url":"uploads/images/products/10-320x200.jpg","featured":"img-05"}]',
    '[
        {
            "id": 1,
            "name": "price_1",
            "price": 43.3896
        },
        {
            "id": 2,
            "name": "price_2",
            "price": 43.8192
        },
        {
            "id": 3,
            "name": "price_3",
            "price": 44.2488
        },
        {
            "id": 4,
            "name": "price_4",
            "price": 44.6784
        },
        {
            "id": 5,
            "name": "price_5",
            "price": 45.108
        },
        {
            "id": 6,
            "name": "price_6",
            "price": 45.5376
        },
        {
            "id": 7,
            "name": "price_7",
            "price": 45.9672
        },
        {
            "id": 8,
            "name": "price_8",
            "price": 46.3968
        },
        {
            "id": 9,
            "name": "price_9",
            "price": 46.8264
        },
        {
            "id": 10,
            "name": "price_10",
            "price": 47.256
        },
        {
            "id": 11,
            "name": "price_11",
            "price": 47.6856
        },
        {
            "id": 12,
            "name": "price_12",
            "price": 48.1152
        },
        {
            "id": 13,
            "name": "price_13",
            "price": 48.5448
        },
        {
            "id": 14,
            "name": "price_14",
            "price": 48.9744
        },
        {
            "id": 15,
            "name": "price_15",
            "price": 49.404
        },
        {
            "id": 16,
            "name": "price_16",
            "price": 49.8336
        },
        {
            "id": 17,
            "name": "price_17",
            "price": 50.2632
        },
        {
            "id": 18,
            "name": "price_18",
            "price": 50.6928
        },
        {
            "id": 19,
            "name": "price_19",
            "price": 51.1224
        },
        {
            "id": 20,
            "name": "price_20",
            "price": 51.552
        }
    ]',
    50, 18.00, 12, 'MED-KEY-005', 15.0, 10.0, 1.5, 0.5,
    '234567890123', 2.50, 1, 1
, NOW()),
(6, 
    'Producto 1 de Alta Seguridad', 1, 6, 'producto-1-alta-seguridad',
    'Descripción del Producto 1 con características avanzadas.',
    '["seguridad", "producto 1", "avanzado"]', 'img-01',
    '[{"url":"uploads/images/products/01-320x200.jpg","featured":"img-01"}]',
    '[
        {
            "id": 1,
            "name": "price_1",
            "price": 44.44
        },
        {
            "id": 2,
            "name": "price_2",
            "price": 44.88
        },
        {
            "id": 3,
            "name": "price_3",
            "price": 45.32
        },
        {
            "id": 4,
            "name": "price_4",
            "price": 45.76
        },
        {
            "id": 5,
            "name": "price_5",
            "price": 46.2
        },
        {
            "id": 6,
            "name": "price_6",
            "price": 46.64
        },
        {
            "id": 7,
            "name": "price_7",
            "price": 47.08
        },
        {
            "id": 8,
            "name": "price_8",
            "price": 47.52
        },
        {
            "id": 9,
            "name": "price_9",
            "price": 47.96
        },
        {
            "id": 10,
            "name": "price_10",
            "price": 48.4
        },
        {
            "id": 11,
            "name": "price_11",
            "price": 48.84
        },
        {
            "id": 12,
            "name": "price_12",
            "price": 49.28
        },
        {
            "id": 13,
            "name": "price_13",
            "price": 49.72
        },
        {
            "id": 14,
            "name": "price_14",
            "price": 50.16
        },
        {
            "id": 15,
            "name": "price_15",
            "price": 50.6
        },
        {
            "id": 16,
            "name": "price_16",
            "price": 51.04
        },
        {
            "id": 17,
            "name": "price_17",
            "price": 51.48
        },
        {
            "id": 18,
            "name": "price_18",
            "price": 51.92
        },
        {
            "id": 19,
            "name": "price_19",
            "price": 52.36
        },
        {
            "id": 20,
            "name": "price_20",
            "price": 52.8
        }
    ]',
    20, 18.00, 10, 'PROD-001', 5.0, 5.0, 5.0, 1.0,
    '000000000001', 2.00, 1, 1
, NOW()),
(7, 'Producto 2 de Alta Seguridad', 2, 7, 'producto-2-alta-seguridad',
'Descripción del Producto 2 con características avanzadas.',
'["seguridad", "producto 2", "avanzado"]',
'img-02',
'[{"url":"uploads/images/products/02-320x200.jpg","featured":"img-02"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 44.44
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 44.88
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 45.32
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 45.76
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 46.2
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 46.64
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 47.08
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 47.52
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 47.96
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 48.4
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 48.84
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 49.28
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 49.72
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 50.16
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 50.6
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 51.04
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 51.48
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 51.92
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 52.36
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 52.8
    }
]',
22, .00, 20, 'PROD-002', 6.0, 6.0, 6.0, 1.2,
'000000000002', 2.50, 1, 1, NOW()),
(8, 'Producto 3 de Alta Seguridad', 3, 8, 'producto-3-alta-seguridad',
'Descripción del Producto 3 con características avanzadas.',
'["seguridad", "producto 3", "avanzado"]',
'img-03',
'[{"url":"uploads/images/products/03-320x200.jpg","featured":"img-03"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 38.38
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 38.76
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 39.14
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 39.52
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 39.9
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 40.28
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 40.66
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 41.04
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 41.42
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 41.8
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 42.18
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 42.56
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 42.94
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 43.32
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 43.7
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 44.08
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 44.46
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 44.84
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 45.22
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 45.6
    }
]',
24, .00, 30, 'PROD-003', 7.0, 7.0, 7.0, 1.5,
'000000000003', 3.00, 1, 1, NOW()),
(9, 'Producto 4 de Alta Seguridad', 4, 9, 'producto-4-alta-seguridad',
'Descripción del Producto 4 con características avanzadas.',
'["seguridad", "producto 4", "avanzado"]',
'img-04',
'[{"url":"uploads/images/products/04-320x200.jpg","featured":"img-04"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 39.9152
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 40.3104
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 40.7056
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 41.1008
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 41.496
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 41.8912
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 42.2864
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 42.6816
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 43.0768
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 43.472
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 43.8672
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 44.2624
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 44.6576
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 45.0528
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 45.448
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 45.8432
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 46.2384
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 46.6336
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 47.0288
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 47.424
    }
]',
26, .00, 40, 'PROD-004', 8.0, 8.0, 8.0, 2.0,
'000000000004', 3.50, 1, 1, NOW()),
(10, 'Producto 5 de Alta Seguridad', 5, 10, 'producto-5-alta-seguridad',
'Descripción del Producto 5 con características avanzadas.',
'["seguridad", "producto 5", "avanzado"]',
'img-05',
'[{"url":"uploads/images/products/10-320x200.jpg","featured":"img-05"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 42.521
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 42.942
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 43.363
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 43.784
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 44.205
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 44.626
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 45.047
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 45.468
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 45.889
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 46.31
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 46.731
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 47.152
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 47.573
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 47.994
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 48.415
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 48.836
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 49.257
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 49.678
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 50.099
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 50.52
    }
]',
28, .00, 50, 'PROD-005', 9.0, 9.0, 9.0, 2.5,
'000000000005', 4.00, 1, 1, NOW()),
(11, 'Producto 6 de Alta Seguridad', 6, 1, 'producto-6-alta-seguridad',
'Descripción del Producto 6 con características avanzadas.',
'["seguridad", "producto 6", "avanzado"]',
'img-06',
'[{"url":"uploads/images/products/11-512x512.jpg","featured":"img-06"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 42.5008
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 42.9216
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 43.3424
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 43.7632
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 44.184
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 44.6048
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 45.0256
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 45.4464
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 45.8672
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 46.288
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 46.7088
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 47.1296
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 47.5504
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 47.9712
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 48.392
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 48.8128
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 49.2336
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 49.6544
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 50.0752
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 50.496
    }
]',
30, .00, 60, 'PROD-006', 10.0, 10.0, 10.0, 3.0,
'000000000006', 4.50, 1, 1, NOW()),
(12, 'Producto 7 de Alta Seguridad', 7, 2, 'producto-7-alta-seguridad',
'Descripción del Producto 7 con características avanzadas.',
'["seguridad", "producto 7", "avanzado"]',
'img-07',
'[{"url":"uploads/images/products/12-512x512.jpg","featured":"img-07"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 43.3896
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 43.8192
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 44.2488
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 44.6784
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 45.108
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 45.5376
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 45.9672
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 46.3968
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 46.8264
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 47.256
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 47.6856
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 48.1152
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 48.5448
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 48.9744
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 49.404
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 49.8336
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 50.2632
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 50.6928
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 51.1224
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 51.552
    }
]',
32, .00, 70, 'PROD-007', 11.0, 11.0, 11.0, 3.5,
'000000000007', 5.00, 1, 1, NOW()),
(13, 'Producto 8 de Alta Seguridad', 8, 3, 'producto-8-alta-seguridad',
'Descripción del Producto 8 con características avanzadas.',
'["seguridad", "producto 8", "avanzado"]',
'img-08',
'[{"url":"uploads/images/products/13-160x160.jpg","featured":"img-08"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 53.0048
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 53.5296
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 54.0544
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 54.5792
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 55.104
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 55.6288
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 56.1536
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 56.6784
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 57.2032
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 57.728
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 58.2528
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 58.7776
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 59.3024
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 59.8272
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 60.352
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 60.8768
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 61.4016
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 61.9264
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 62.4512
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 62.976
    }
]',
34, .00, 80, 'PROD-008', 12.0, 12.0, 12.0, 4.0,
'000000000008', 5.50, 1, 1, NOW()),
(14, 'Producto 9 de Alta Seguridad', 9, 4, 'producto-9-alta-seguridad',
'Descripción del Producto 9 con características avanzadas.',
'["seguridad", "producto 9", "avanzado"]',
'img-09',
'[{"url":"uploads/images/products/14-640x480.jpg","featured":"img-09"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 45.5611
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 46.0122
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 46.4633
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 46.9144
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 47.3655
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 47.8166
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 48.2677
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 48.7188
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 49.1699
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 49.621
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 50.0721
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 50.5232
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 50.9743
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 51.4254
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 51.8765
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 52.3276
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 52.7787
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 53.2298
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 53.6809
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 54.132
    }
]',
36, .00, 90, 'PROD-009', 13.0, 13.0, 13.0, 4.5,
'000000000009', 6.00, 1, 1, NOW()),
(15, 'Producto 10 de Alta Seguridad', 10, 5, 'producto-10-alta-seguridad',
'Descripción del Producto 10 con características avanzadas.',
'["seguridad", "producto 10", "avanzado"]',
'img-10',
'[{"url":"uploads/images/products/15-640x480.jpg","featured":"img-10"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 72.9624
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 73.6848
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 74.4072
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 75.1296
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 75.852
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 76.5744
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 77.2968
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 78.0192
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 78.7416
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 79.464
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 80.1864
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 80.9088
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 81.6312
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 82.3536
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 83.076
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 83.7984
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 84.5208
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 85.2432
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 85.9656
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 86.688
    }
]',
38, .00, 100, 'PROD-010', 14.0, 14.0, 14.0, 5.0,
'000000000010', 6.50, 1, 1, NOW()),
(16, 'Producto 11 de Alta Seguridad', 11, 6, 'producto-11-alta-seguridad',
'Descripción del Producto 11 con características avanzadas.',
'["seguridad", "producto 11", "avanzado"]',
'img-11',
'[{"url":"uploads/images/products/16-640x480.jpg","featured":"img-11"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 49.5708
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 50.0616
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 50.5524
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 51.0432
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 51.534
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 52.0248
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 52.5156
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 53.0064
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 53.4972
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 53.988
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 54.4788
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 54.9696
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 55.4604
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 55.9512
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 56.442
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 56.9328
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 57.4236
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 57.9144
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 58.4052
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 58.896
    }
]',
40, .00, 110, 'PROD-011', 15.0, 15.0, 15.0, 5.5,
'000000000011', 7.00, 1, 1, NOW()),
(17, 'Producto 12 de Alta Seguridad', 12, 7, 'producto-12-alta-seguridad',
'Descripción del Producto 12 con características avanzadas.',
'["seguridad", "producto 12", "avanzado"]',
'img-12',
'[{"url":"uploads/images/products/17-640x480.jpg","featured":"img-12"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 26.1994
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 26.4588
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 26.7182
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 26.9776
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 27.237
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 27.4964
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 27.7558
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 28.0152
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 28.2746
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 28.534
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 28.7934
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 29.0528
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 29.3122
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 29.5716
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 29.831
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 30.0904
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 30.3498
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 30.6092
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 30.8686
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 31.128
    }
]',
42, .00, 120, 'PROD-012', 16.0, 16.0, 16.0, 6.0,
'000000000012', 7.50, 1, 1, NOW()),
(18, 'Producto 13 de Alta Seguridad', 13, 8, 'producto-13-alta-seguridad',
'Descripción del Producto 13 con características avanzadas.',
'["seguridad", "producto 13", "avanzado"]',
'img-13',
'[{"url":"uploads/images/products/18-640x480.jpg","featured":"img-13"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 28.8254
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 29.1108
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 29.3962
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 29.6816
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 29.967
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 30.2524
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 30.5378
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 30.8232
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 31.1086
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 31.394
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 31.6794
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 31.9648
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 32.2502
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 32.5356
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 32.821
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 33.1064
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 33.3918
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 33.6772
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 33.9626
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 34.248
    }
]',
44, .00, 130, 'PROD-013', 17.0, 17.0, 17.0, 6.5,
'000000000013', 8.00, 1, 1, NOW()),
(19, 'Producto 14 de Alta Seguridad', 14, 9, 'producto-14-alta-seguridad',
'Descripción del Producto 14 con características avanzadas.',
'["seguridad", "producto 14", "avanzado"]',
'img-14',
'[{"url":"uploads/images/products/19-640x480.jpg","featured":"img-14"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 28.8254
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 29.1108
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 29.3962
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 29.6816
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 29.967
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 30.2524
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 30.5378
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 30.8232
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 31.1086
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 31.394
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 31.6794
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 31.9648
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 32.2502
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 32.5356
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 32.821
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 33.1064
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 33.3918
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 33.6772
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 33.9626
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 34.248
    }
]',
46, .00, 140, 'PROD-014', 18.0, 18.0, 18.0, 7.0,
'000000000014', 8.50, 1, 1, NOW()),
(20, 'Producto 15 de Alta Seguridad', 15, 10, 'producto-15-alta-seguridad',
'Descripción del Producto 15 con características avanzadas.',
'["seguridad", "producto 15", "avanzado"]',
'img-15',
'[{"url":"uploads/images/products/20-640x480.jpg","featured":"img-15"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 28.8254
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 29.1108
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 29.3962
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 29.6816
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 29.967
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 30.2524
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 30.5378
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 30.8232
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 31.1086
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 31.394
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 31.6794
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 31.9648
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 32.2502
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 32.5356
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 32.821
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 33.1064
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 33.3918
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 33.6772
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 33.9626
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 34.248
    }
]',
48, .00, 150, 'PROD-015', 19.0, 19.0, 19.0, 7.5,
'000000000015', 9.00, 1, 1, NOW()),
(21, 'Producto 16 de Alta Seguridad', 16, 1, 'producto-16-alta-seguridad',
'Descripción del Producto 16 con características avanzadas.',
'["seguridad", "producto 16", "avanzado"]',
'img-16',
'[{"url":"uploads/images/products/21-640x480.jpg","featured":"img-16"}]',
'[
    {
        "id": 1,
        "name": "price_1",
        "price": 42.4301
    },
    {
        "id": 2,
        "name": "price_2",
        "price": 42.8502
    },
    {
        "id": 3,
        "name": "price_3",
        "price": 43.2703
    },
    {
        "id": 4,
        "name": "price_4",
        "price": 43.6904
    },
    {
        "id": 5,
        "name": "price_5",
        "price": 44.1105
    },
    {
        "id": 6,
        "name": "price_6",
        "price": 44.5306
    },
    {
        "id": 7,
        "name": "price_7",
        "price": 44.9507
    },
    {
        "id": 8,
        "name": "price_8",
        "price": 45.3708
    },
    {
        "id": 9,
        "name": "price_9",
        "price": 45.7909
    },
    {
        "id": 10,
        "name": "price_10",
        "price": 46.211
    },
    {
        "id": 11,
        "name": "price_11",
        "price": 46.6311
    },
    {
        "id": 12,
        "name": "price_12",
        "price": 47.0512
    },
    {
        "id": 13,
        "name": "price_13",
        "price": 47.4713
    },
    {
        "id": 14,
        "name": "price_14",
        "price": 47.8914
    },
    {
        "id": 15,
        "name": "price_15",
        "price": 48.3115
    },
    {
        "id": 16,
        "name": "price_16",
        "price": 48.7316
    },
    {
        "id": 17,
        "name": "price_17",
        "price": 49.1517
    },
    {
        "id": 18,
        "name": "price_18",
        "price": 49.5718
    },
    {
        "id": 19,
        "name": "price_19",
        "price": 49.9919
    },
    {
        "id": 20,
        "name": "price_20",
        "price": 50.412
    }
]',
50, .00, 160, 'PROD-016', 20.0, 20.0, 20.0, 8.0,
'000000000016', 9.50, 1, 1, NOW());

-- Insertar datos en la tabla product_categories
INSERT INTO `product_categories` (id, product_id, category_id) VALUES
(1, 1, 1),
(2, 1, 5),
(3, 2, 2),
(4, 2, 5),
(5, 3, 3),
(6, 3, 1),
(7, 4, 4),
(8, 4, 1),
(9, 5, 5),
(10, 5, 1);

-- Insertar datos en la tabla customers
INSERT INTO `customers` (
    id, names, surname, second_surname, 
    company_name, document_type, document_number, email, address, phone, created_by
) VALUES
(1, 'Juan Carlos', 'Pérez', 'Gómez', NULL, 'dni', '12345678', 'juan.perez@gmail.com', 'Av. Los Olivos 123, Lima', '987654321', 1),
(2, 'María Luisa', 'Torres', 'Ramírez', NULL, 'dni', '87654321', 'maria.torres@gmail.com', 'Calle La Marina 456, Arequipa', '912345678', 1),
(3, NULL, NULL, NULL, 'Inversiones El Buen Precio SAC', 'ruc', '20481234567', 'contacto@buenprecio.com', 'Jr. Las Flores 789, Trujillo', '923456789', 1),
(4, 'Luis Alberto Manuel', 'García', 'López', NULL, 'dni', '23456789', 'luis.garcia@gmail.com', 'Av. Brasil 321, Lima', '934567890', 1),
(5, 'Ana Sofía', 'Martínez', 'Díaz', NULL, 'dni', '34567890', 'ana.martinez@gmail.com', 'Calle Los Pinos 654, Cusco', '945678901', 1),
(6, NULL, NULL, NULL, 'Tech Solutions SAC', 'ruc', '20551234567', 'info@techsolutions.com', 'Av. La Paz 987, Arequipa', '956789012', 1),
(7, 'Carlos Andrés', 'Fernández', 'Vargas', NULL, 'dni', '45678901', 'carlos.fernandez@gmail.com', 'Jr. San Martín 123, Trujillo', '967890123', 1),
(8, 'Lucía Isabel', 'Hernández', 'Morales', NULL, 'dni', '56789012', 'lucia.hernandez@gmail.com', 'Av. Los Alamos 456, Lima', '978901234', 1),
(9, NULL, NULL, NULL, 'Construcciones Modernas SAC', 'ruc', '20661234567', 'contacto@construccionesmodernas.com', 'Calle Los Olivos 789, Cusco', '989012345', 1),
(10, 'Pedro José', 'Sánchez', 'Ruiz', NULL, 'dni', '67890123', 'pedro.sanchez@gmail.com', 'Av. Los Jardines 321, Arequipa', '990123456', 1),
(11, 'Elena María', 'Díaz', 'Gómez', NULL, 'dni', '78901234', 'elena.diaz@gmail.com', 'Jr. Las Rosas 654, Trujillo', '901234567', 1),
(12, NULL, NULL, NULL, 'Importaciones Globales SAC', 'ruc', '20771234567', 'info@importacionesglobales.com', 'Av. Los Pinos 987, Lima', '912345678', 1),
(13, 'Miguel Ángel', 'López', 'García', NULL, 'dni', '89012345', 'miguel.lopez@gmail.com', 'Calle Los Laureles 123, Cusco', '923456789', 1),
(14, 'Carmen Rosa', 'Gómez', 'Fernández', NULL, 'dni', '90123456', 'carmen.gomez@gmail.com', 'Av. Los Claveles 456, Arequipa', '934567890', 1),
(15, NULL, NULL, NULL, 'Logística Rápida SAC', 'ruc', '20881234567', 'contacto@logisticarapida.com', 'Jr. Las Palmeras 789, Trujillo', '945678901', 1);

-- Insertar datos en la tabla suppliers
INSERT INTO `suppliers` (id, ruc, name, email, phone, address, created_by) VALUES 
(1, '12345678901', 'Ferro Perú S.A.', 'contacto@ferroperu.com', '+51 1 234 5678', 'Av. Argentina 1543, Callao, Lima, Perú', 1),
(2, '12345678902', 'Sodimac Perú S.A.', 'ventas@sodimac.com.pe', '+51 1 411 6000', 'Av. Javier Prado Este 4200, Surco, Lima, Perú', 1),
(3, '12345678903', 'Maestro Perú S.A.', 'info@maestro.com.pe', '+51 1 614 6000', 'Av. La Marina 2350, San Miguel, Lima, Perú', 1),
(4, '12345678904', 'Disensa Perú', 'atencion@disensa.com.pe', '+51 1 719 2000', 'Av. Alfredo Mendiola 5545, Los Olivos, Lima, Perú', 1),
(5, '12345678905', 'Promart Homecenter', 'soporte@promart.com.pe', '+51 1 619 1616', 'Av. Tomás Marsano 3675, Surquillo, Lima, Perú', 1),
(6, '12345678906', 'Ferretería EPA', 'contacto@epa.com.pe', '+51 1 705 0000', 'Av. Nicolás Ayllón 5777, Ate, Lima, Perú', 1),
(7, '12345678907', 'Cementos Pacasmayo', 'ventas@pacasmayo.com.pe', '+51 44 608 400', 'Av. Pacasmayo 230, Trujillo, La Libertad, Perú', 1),
(8, '12345678908', 'Fierros & Aceros S.A.', 'ventas@fierrosyacerossa.com', '+51 1 336 7890', 'Av. Industrial 4230, San Martín de Porres, Lima, Perú', 1),
(9, '12345678909', 'Siderperu', 'clientes@siderperu.com.pe', '+51 44 481 110', 'Av. Néstor Gambetta 1234, Chimbote, Áncash, Perú', 1),
(10, '12345678910', 'Construrama Perú', 'info@construrama.com.pe', '+51 1 345 6789', 'Jr. Puno 1350, Cercado de Lima, Lima, Perú', 1),
(11, '12345678911', 'Indeco Perú', 'ventas@indeco.com.pe', '+51 1 213 7000', 'Av. Canadá 3350, San Luis, Lima, Perú', 1),
(12, '12345678912', 'Ferrotodo S.A.C.', 'ventas@ferrotodo.com.pe', '+51 1 555 7777', 'Av. Colonial 1498, Cercado de Lima, Lima, Perú', 1),
(13, '12345678913', 'Metales Peruanos S.A.', 'info@metalesperuanos.com', '+51 1 619 8000', 'Jr. Parinacochas 565, La Victoria, Lima, Perú', 1),
(14, '12345678914', 'Grupo Fierro', 'contacto@grupofierro.com.pe', '+51 1 567 8900', 'Av. Faucett 3000, Callao, Lima, Perú', 1),
(15, '12345678915', 'Grupo Ferretero S.A.C.', 'ventas@grupoferretero.com.pe', '+51 1 700 1234', 'Av. Los Héroes 350, San Juan de Miraflores, Lima, Perú', 1),
(16, '12345678916', 'Ferretería del Norte', 'norte@ferreterianorte.com.pe', '+51 44 345 6789', 'Av. España 1245, Trujillo, La Libertad, Perú', 1),
(17, '12345678917', 'Aceros Arequipa', 'info@acerosarequipa.com', '+51 54 284 400', 'Av. Aviación 1000, Cerro Colorado, Arequipa, Perú', 1),
(18, '12345678918', 'Tornillos y Herramientas S.A.C.', 'ventas@tyh.com.pe', '+51 1 765 4321', 'Av. Nicolás de Piérola 250, Cercado de Lima, Lima, Perú', 1);

-- Insertar datos en la tabla payment_methods
INSERT INTO `payment_methods` (id, name, description, status, created_by)
VALUES 
(1, 'Efectivo', 'Pago en efectivo', 1, 1),
(2, 'Tarjeta de Crédito', 'Pago con tarjeta de crédito', 1, 1),
(3, 'Transferencia Bancaria', 'Pago por transferencia bancaria', 1, 1),
(4, 'Yape', 'Pago mediante Yape', 1, 1),
(5, 'Plin', 'Pago mediante Plin', 1, 1);

-- Insertar datos en la tabla registros de caja
INSERT INTO `cash_registers` (id, warehouse_id, user_open_id, initial_amount)
VALUES (1, 1, 1, 100.00);

-- Insertar datos en la tabla movimientos de caja
INSERT INTO `cash_movements` (id, cash_register_id, movement_type, payment_method_id, amount, description, user_id)
VALUES (1, 1, 'income', 2, 150.00, 'Venta de productos', 1);

-- Insertar datos en la tabla quotes
INSERT INTO `quotes` (
    id, reference, customer_id, user_id, warehouse_id, currency_id, exchange_rate, issue_date, expiration_date, quote_status,
    approved_by, approved_at, canceled_by, canceled_at, subtotal, discount, total
) VALUES
(1, 'CT-00001', 1, 1, 1, 6, 1.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'pending', NULL, NULL, NULL, NULL, 200.00, 10.00, 209.00),
(2, 'CT-00002', 3, 1, 2, 6, 1.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'approved', 1, CURRENT_TIMESTAMP, NULL, NULL, 450.00, 20.00, 472.00),
(3, 'CT-00003', 5, 1, 3, 2, 4.1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'pending', NULL, NULL, NULL, NULL, 600.00, 30.00, 627.00),
(4, 'CT-00004', 7, 1, 4, 1, 1.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'rejected', NULL, NULL, 1, CURRENT_TIMESTAMP, 300.00, 15.00, 313.50),
(5, 'CT-00005', 9, 1, 5, 5, 3.7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'pending', NULL, NULL, NULL, NULL, 520.00, 25.00, 544.50),
(6, 'CT-00006', 11, 1, 6, 3, 0.85, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'approved', 1, CURRENT_TIMESTAMP, NULL, NULL, 750.00, 35.00, 786.25),
(7, 'CT-00007', 13, 1, 7, 4, 155.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'canceled', NULL, NULL, 1, CURRENT_TIMESTAMP, 180.00, 9.00, 189.10),
(8, 'CT-00008', 15, 1, 8, 6, 1.0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'pending', NULL, NULL, NULL, NULL, 310.00, 16.00, 323.40);

-- Insertar datos en la tabla quote_details
INSERT INTO `quote_details` (
    id, quote_id, product_id, quantity, price, discount, subtotal, total
) VALUES
(1, 1, 1, 2, 20.00, 2.00, 40.00, 38.00),
(2, 1, 2, 3, 25.00, 3.00, 75.00, 72.00),
(3, 2, 3, 1, 30.00, 0.00, 30.00, 30.00),
(4, 2, 4, 2, 28.00, 2.00, 56.00, 54.00),
(5, 3, 5, 4, 22.00, 4.00, 88.00, 84.00),
(6, 3, 6, 2, 26.00, 2.00, 52.00, 50.00),
(7, 4, 7, 3, 23.00, 3.00, 69.00, 66.00),
(8, 5, 8, 1, 32.00, 0.00, 32.00, 32.00),
(9, 6, 9, 5, 9.31, 1.00, 46.55, 45.55),
(10, 7, 1, 2, 20.00, 2.00, 40.00, 38.00),
(11, 8, 2, 3, 25.00, 3.00, 75.00, 72.00);

-- Insertar datos en la tabla sale_orders
INSERT INTO `sale_orders` (
    id, reference, warehouse_id, customer_id, user_id, quote_id, issue_date, currency_id, exchange_rate, discount, subtotal, total, order_status, date_approved
) VALUES
(1, 'OV-00001', 1, 1, 1, NULL, CURRENT_TIMESTAMP, 6, 3.74, 2.00, 50.00, 66.00, 'approved', CURRENT_DATE),
(2, 'OV-00002', 1, 2, 1, 1, CURRENT_TIMESTAMP, 6, 3.74, 0.00, 100.00, 118.00, 'canceled', NULL),
(3, 'OV-00003', 1, 3, 1, NULL, CURRENT_TIMESTAMP, 6, 3.74, 5.00, 200.00, 241.00, 'issued', NULL),
(4, 'OV-00004', 1, 1, 1, 2, CURRENT_TIMESTAMP, 6, 3.74, 10.00, 300.00, 342.00, 'approved', CURRENT_DATE);

-- Insertar datos en la tabla sale_order_details
INSERT INTO `sale_order_details` (
    id, product_name, sale_order_id, product_id, quantity, discount_method, discount, price, subtotal, total
) VALUES
(1, 'A Walk Amongst Friends - Canvas Print', 1, 1, 1, 0, NULL, 10.24, 10.24, 10.24),
(2, 'A Walk Amongst Friends - Canvas Print', 2, 1, 2, 0, NULL, 10.24, 20.48, 20.48),
(3, 'A Walk Amongst Friends - Canvas Print', 3, 1, 5, 0, NULL, 10.24, 51.20, 51.20);

-- Insertar datos en la tabla purchase_orders
INSERT INTO `purchase_orders` (id, reference, warehouse_id, supplier_id, currency_id, exchange_rate, discount, issue_date, tax, subtotal, total, order_status, created_by, migrate_purchase)
VALUES
(1, 'OC-00001', 1, 1, 6, 3.75, 5.00, '2024-07-01 10:00:00', 10.00, 180.00, 198.00, 'canceled', 1, 0),
(2, 'OC-00002', 2, 2, 6, 3.70, 0.00, '2024-07-03 15:30:00', 8.00, 240.00, 259.20, 'approved', 1, 0),
(3, 'OC-00003', 3, 3, 6, 3.80, 10.00, '2024-07-05 12:45:00', 9.50, 500.00, 547.50, 'partial', 1, 1),
(4, 'OC-00004', 4, 4, 6, 3.85, 3.00, '2024-07-07 09:20:00', 7.00, 300.00, 321.00, 'rejected', 1, 0),
(5, 'OC-00005', 5, 5, 6, 3.78, 5.00, '2024-07-09 14:10:00', 6.50, 420.00, 447.30, 'approved', 1, 0),
(6, 'OC-00006', 6, 6, 6, 3.79, 8.00, '2024-07-11 17:50:00', 8.20, 350.00, 378.70, 'partial', 1, 1),
(7, 'OC-00007', 7, 7, 6, 3.76, 2.00, '2024-07-13 11:05:00', 7.80, 275.00, 296.45, 'received', 1, 0),
(8, 'OC-00008', 8, 8, 6, 3.77, 0.00, '2024-07-15 13:25:00', 8.50, 600.00, 648.00, 'rejected', 1, 0),
(9, 'OC-00009', 9, 9, 6, 3.74, 4.00, '2024-07-17 16:40:00', 9.00, 480.00, 523.20, 'approved', 1, 1),
(10, 'OC-00010', 2, 10, 6, 3.80, 6.00, '2024-07-19 10:10:00', 7.50, 550.00, 591.25, 'received', 1, 0);

-- Insertar datos en la tabla purchase_order_details
INSERT INTO `purchase_order_details` (id, purchase_order_id, product_id, quantity, price, subtotal, total)
VALUES
(1, 1, 1, 5, 20.00, 100.00, 100.00),
(2, 1, 2, 3, 25.00, 75.00, 75.00),
(3, 2, 3, 4, 30.00, 120.00, 120.00),
(4, 2, 4, 2, 28.00, 56.00, 56.00),
(5, 3, 5, 5, 22.00, 110.00, 110.00),
(6, 3, 6, 3, 26.00, 78.00, 78.00),
(7, 4, 7, 4, 23.00, 92.00, 92.00),
(8, 4, 8, 2, 32.00, 64.00, 64.00),
(9, 5, 9, 3, 9.31, 27.93, 27.93),
(10, 6, 1, 6, 20.00, 120.00, 120.00),
(11, 7, 2, 5, 25.00, 125.00, 125.00),
(12, 8, 3, 7, 30.00, 210.00, 210.00),
(13, 9, 4, 4, 28.00, 112.00, 112.00),
(14, 10, 5, 6, 22.00, 132.00, 132.00);

-- Insertar datos en la tabla purchases
INSERT INTO `purchases` (
    id, reference, invoice_number, supplier_id, warehouse_id, currency_id, exchange_rate, 
    purchase_status, purchase_order_id, issue_date, received_date, payment_date, 
    discount, subtotal, tax, total, total_paid, change_amount, payment_method_id, 
    created_by, document_attachment, notes
)
VALUES
(1, 'CP-00001', 'INV-001', 3, 3, 6, 3.80, 'partial', 3, '2024-07-05', '2024-07-06', NULL, 10.00, 500.00, 9.50, 547.50, 0.00, 0.00, 1, 1, NULL, NULL),
(2, 'CP-00002', 'INV-002', 6, 6, 6, 3.79, 'partial', 6, '2024-07-11', '2024-07-12', NULL, 8.00, 350.00, 8.20, 378.70, 0.00, 0.00, 1, 1, NULL, NULL),
(3, 'CP-00003', 'INV-003', 7, 7, 6, 3.76, 'received', 7, '2024-07-13', '2024-07-14', '2024-07-15', 2.00, 275.00, 7.80, 296.45, 296.45, 0.00, 2, 1, NULL, NULL),
(4, 'CP-00004', 'INV-004', 9, 9, 6, 3.74, 'received', 9, '2024-07-17', '2024-07-18', '2024-07-19', 4.00, 480.00, 9.00, 523.20, 523.20, 0.00, 2, 1, NULL, NULL),
(5, 'CP-00005', 'INV-005', 10, 2, 6, 3.80, 'received', 10, '2024-07-19', '2024-07-20', '2024-07-21', 6.00, 550.00, 7.50, 591.25, 591.25, 0.00, 1, 1, NULL, NULL),
(6, 'CP-00006', 'INV-006', 2, 2, 6, 3.70, 'received', 2, '2024-07-03', '2024-07-04', '2024-07-05', 0.00, 240.00, 8.00, 259.20, 259.20, 0.00, 2, 1, NULL, NULL),
(7, 'CP-00007', 'INV-007', 1, 1, 6, 3.75, 'received', 1, '2024-07-01', '2024-07-02', '2024-07-03', 5.00, 180.00, 10.00, 198.00, 198.00, 0.00, 2, 1, NULL, NULL),
(8, 'CP-00008', 'INV-008', 4, 4, 6, 3.85, 'canceled', 4, '2024-07-07', NULL, NULL, 3.00, 300.00, 7.00, 321.00, 0.00, 0.00, NULL, 1, NULL, NULL),
(9, 'CP-00009', 'INV-009', 8, 8, 6, 3.77, 'canceled', 8, '2024-07-15', NULL, NULL, 0.00, 600.00, 8.50, 648.00, 0.00, 0.00, NULL, 1, NULL, NULL),
(10, 'CP-00010', 'INV-010', 5, 5, 6, 3.78, 'draft', 5, '2024-07-09', NULL, NULL, 5.00, 420.00, 6.50, 447.30, 0.00, 0.00, NULL, 1, NULL, NULL),
(11, 'CP-00011', 'INV-011', 2, 2, 6, 3.70, 'paid', 2, '2024-07-03', '2024-07-04', '2024-07-05', 0.00, 240.00, 8.00, 259.20, 259.20, 0.00, 2, 1, NULL, 'Pago adelantado'),
(12, 'CP-00012', 'INV-012', 6, 6, 6, 3.79, 'unpaid', 6, '2024-07-11', NULL, NULL, 8.00, 350.00, 8.20, 378.70, 0.00, 0.00, 1, 1, NULL, 'Pendiente de abono');

-- Insertar datos en la tabla purchase_details
INSERT INTO `purchase_details` (id, purchase_id, product_id, quantity, price, discount, subtotal, total)
VALUES
(1, 1, 5, 5, 22.00, 0.00, 110.00, 110.00),
(2, 1, 6, 3, 26.00, 0.00, 78.00, 78.00),
(3, 2, 1, 6, 20.00, 0.00, 120.00, 120.00),
(4, 3, 2, 5, 25.00, 0.00, 125.00, 125.00),
(5, 4, 4, 4, 28.00, 0.00, 112.00, 112.00),
(6, 5, 5, 6, 22.00, 0.00, 132.00, 132.00),
(7, 6, 3, 4, 30.00, 0.00, 120.00, 120.00),
(8, 6, 4, 2, 28.00, 0.00, 56.00, 56.00),
(9, 7, 1, 5, 20.00, 0.00, 100.00, 100.00),
(10, 7, 2, 3, 25.00, 0.00, 75.00, 75.00),
(11, 8, 7, 4, 23.00, 0.00, 92.00, 92.00),
(12, 8, 8, 2, 32.00, 0.00, 64.00, 64.00),
(13, 9, 3, 7, 30.00, 0.00, 210.00, 210.00),
(14, 10, 9, 3, 9.31, 0.00, 27.93, 27.93),
(15, 11, 3, 4, 30.00, 0.00, 120.00, 120.00),
(16, 11, 4, 2, 28.00, 0.00, 56.00, 56.00),
(17, 12, 1, 6, 20.00, 0.00, 120.00, 120.00),
(18, 12, 6, 2, 24.00, 0.00, 48.00, 48.00); 

-- Insertar datos en la tabla purchase_order_payments
INSERT INTO `purchase_order_payments` (id, payment_method_id, purchase_order_id, payment_date, amount, currency_id, exchange_rate, reference_number, status, notes) VALUES
(1, 1, 1, '2023-10-01 10:00:00', 1500.00, 6, 1.0, NULL, 'completed', 'Pago en efectivo en tienda'),
(2, 2, 2, '2023-10-02 15:30:00', 2500.00, 6, 1.0, '123456789', 'completed', 'Pago con tarjeta Visa terminada en 1234'),
(3, 3, 3, '2023-10-03 09:45:00', 3000.00, 6, 1.0, '987654321', 'completed', 'Transferencia desde BCP'),
(4, 4, 4, '2023-10-04 12:15:00', 500.00, 6, 1.0, 'YP123456', 'completed', 'Pago con Yape desde el número 999888777'),
(5, 5, 5, '2023-10-05 14:20:00', 750.00, 6, 1.0, 'PL987654', 'completed', 'Pago con Plin desde el número 999111222');

-- Insertar datos en la tabla sales
INSERT INTO `sales` (id, document_type, series, number, bill, issue_date, warehouse_id, customer_id, currency_id, user_id, exchange_rate, discount, subtotal, total, total_paid, change_amount, sale_status, payment_method_id, sale_order_id)
VALUES
(1, 'ticket', 'B001', 1000001, 'B001-1000001', NOW(), 1, 1, 6, 1, 3.80, 5.00, 100.00, 113.00, 113.00, 0, 'issued', 1, NULL),
(2, 'invoice', 'F001', 1000001, 'F001-1000001', NOW(), 1, 2, 1, 1, 1.00, 0.00, 200.00, 236.00, 240.00, 4, 'paid', 2, NULL),
(3, 'ticket', 'B001', 1000002, 'B001-1000002', NOW(), 2, 3, 2, 1, 1.10, 10.00, 150.00, 166.00, 170.00, 4, 'unpaid', 3, 1),
(4, 'invoice', 'F001', 1000002, 'F001-1000002', NOW(), 1, 4, 5, 1, 17.50, 0.00, 180.00, 212.40, 212.40, 0, 'issued', 1, 2),
(5, 'ticket', 'B001', 1000003, 'B001-1000003', NOW(), 3, 5, 6, 1, 3.80, 5.00, 120.00, 135.60, 135.60, 0, 'pending', 2, NULL),
(6, 'invoice', 'F001', 1000003, 'F001-1000003', NOW(), 2, 6, 3, 1, 1.20, 0.00, 90.00, 106.20, 106.20, 0, 'canceled', 3, NULL),
(7, 'invoice', 'F001', 1000004, 'F001-1000004', NOW(), 3, 7, 4, 1, 0.85, 2.00, 300.00, 354.00, 360.00, 6, 'issued', 1, 3),
(8, 'invoice', 'F001', 1000005, 'F001-1000005', NOW(), 1, 8, 6, 1, 3.80, 0.00, 110.00, 124.30, 124.30, 0, 'paid', 2, NULL);

-- Insertar datos en la tabla sale_details
INSERT INTO `sale_details` (id, product_name, sale_id, product_id, quantity, discount_method, discount, price, subtotal, total)
VALUES
(1, 'Laptop HP', 1, 1, 2, 1, 5.00, 50.00, 100.00, 113.00),
(2, 'Mouse Logitech', 1, 2, 1, 1, 0.00, 20.00, 20.00, 22.60),
(3, 'Monitor LG', 2, 3, 1, 1, 0.00, 200.00, 200.00, 236.00),
(4, 'Teclado Mecánico', 3, 4, 3, 0, 10.00, 50.00, 150.00, 166.00),
(5, 'Silla Gamer', 4, 5, 1, 1, 0.00, 180.00, 180.00, 212.40),
(6, 'Impresora Epson', 5, 6, 2, 1, 5.00, 60.00, 120.00, 135.60),
(7, 'Tablet Samsung', 6, 7, 1, 1, 0.00, 90.00, 90.00, 106.20),
(8, 'Disco Duro SSD', 7, 8, 3, 0, 2.00, 100.00, 300.00, 354.00),
(9, 'Auriculares Sony', 8, 9, 2, 1, 0.00, 55.00, 110.00, 124.30);

-- Insertar datos en la tabla opportunity_tracking
INSERT INTO `opportunity_tracking` (id, customer_id, user_id, title, status) VALUES
(1, 1, 1, 'Compra de herramientas eléctricas', 'open'),
(2, 2, 1, 'Adquisición de materiales de construcción', 'lost'),
(3, 3, 1, 'Pedido de maquinaria pesada', 'won'),
(4, 4, 1, 'Solicitud de cotización para ferretería', 'lost'),
(5, 5, 1, 'Proyecto de remodelación de oficinas', 'in_progress'),
(6, 6, 1, 'Compra de equipos de protección personal', 'won'),
(7, 7, 1, 'Solicitud de compra de cemento y fierros', 'open'),
(8, 8, 1, 'Pedido de herramientas manuales', 'lost'),
(9, 9, 1, 'Cotización de pintura y acabados', 'won'),
(10, 10, 1, 'Requerimiento de tuberías y conexiones', 'in_progress');

-- Insertar datos en la tabla purchase_requests
INSERT INTO `purchase_requests` (id, reference, supplier_id, user_id, request_date, expected_delivery_date, status, priority, total_cost, approved_by, approval_date, notes)
VALUES
(1, 'PR000001', 1, 1, '2024-02-01', '2024-02-10', 'pending', 'high', 1500.00, NULL, NULL, 'Solicitud urgente para proyecto A'),
(2, 'PR000002', 2, 1, '2024-02-02', '2024-02-15', 'approved', 'medium', 2450.50, 1, '2024-02-03 10:30:00', 'Pedido aprobado para almacén'),
(3, 'PR000003', 3, 1, '2024-02-03', '2024-02-18', 'pending', 'low', 780.00, NULL, NULL, 'Compra de materiales básicos'),
(4, 'PR000004', 1, 1, '2024-02-05', '2024-02-12', 'approved', 'high', 3120.75, 1, '2024-02-06 15:00:00', 'Solicitud para nueva obra'),
(5, 'PR000005', 4, 1, '2024-02-06', '2024-02-20', 'rejected', 'medium', 930.50, 1, '2024-02-07 12:45:00', 'Rechazado por presupuesto insuficiente'),
(6, 'PR000006', 5, 1, '2024-02-07', '2024-02-25', 'pending', 'low', 1200.00, NULL, NULL, 'Pedido de herramientas'),
(7, 'PR000007', 2, 1, '2024-02-08', '2024-02-14', 'approved', 'medium', 5670.90, 1, '2024-02-09 09:20:00', 'Material aprobado para producción'),
(8, 'PR000008', 3, 1, '2024-02-09', '2024-02-22', 'pending', 'high', 850.75, NULL, NULL, 'Solicitud para mantenimiento'),
(9, 'PR000009', 4, 1, '2024-02-10', '2024-02-28', 'rejected', 'medium', 2100.30, 1, '2024-02-11 14:00:00', 'Rechazado por duplicidad'),
(10, 'PR000010', 1, 1, '2024-02-11', '2024-03-01', 'approved', 'high', 4730.00, 1, '2024-02-12 11:10:00', 'Pedido importante para obra nueva');

INSERT INTO `purchase_request_details` (id, purchase_request_id, product_id, quantity, unit_price, estimated_cost, received_quantity, status, comments)
VALUES
(1, 1, 2, 10, 150.00, 1500.00, 0, 'pending', 'Pendiente de aprobación'),
(2, 2, 3, 5, 490.10, 2450.50, 5, 'received', 'Recibido sin problemas'),
(3, 3, 1, 15, 52.00, 780.00, 0, 'pending', 'Esperando confirmación de proveedor'),
(4, 4, 4, 8, 390.00, 3120.75, 8, 'received', 'Entrega completada correctamente'),
(5, 5, 5, 7, 133.50, 930.50, 0, 'canceled', 'Pedido cancelado por error en solicitud'),
(6, 6, 2, 12, 100.00, 1200.00, 0, 'pending', 'Pendiente de stock'),
(7, 7, 3, 6, 945.15, 5670.90, 6, 'received', 'Material recibido con una unidad defectuosa'),
(8, 8, 1, 5, 170.15, 850.75, 0, 'pending', 'Esperando autorización'),
(9, 9, 4, 10, 210.03, 2100.30, 0, 'canceled', 'Orden duplicada, cancelada'),
(10, 10, 5, 20, 236.50, 4730.00, 20, 'received', 'Pedido recibido correctamente y en buen estado');

-- Insertar datos en la tabla stock_control
INSERT INTO `stock_control` (id, warehouse_id, product_id, current_stock, current_booking, created_by) VALUES
(1, 1, 3, 50, 20, 1),
(2, 2, 5, 30, 10, 1),
(3, 3, 7, 20, 19, 1),
(4, 4, 1, 10, 42, 1),
(5, 5, 9, 40, 8, 1),
(6, 6, 2, 20, 45, 1),
(7, 7, 4, 30, 18, 1),
(8, 8, 6, 20, 39, 1),
(9, 9, 8, 30, 31, 1),
(10, 1, 3, 20, 32, 1);

-- Insertar datos en la tabla inventory_movements
INSERT INTO `inventory_movements` (id, warehouse_id, product_id, movement_type, quantity, user_id) VALUES
(1, 1, 2, 'entry', 100, 1),
(2, 2, 4, 'exit', 50, 1),
(3, 3, 6, 'entry', 200, 1),
(4, 4, 8, 'exit', 150, 1),
(5, 5, 1, 'entry', 300, 1),
(6, 6, 3, 'exit', 120, 1),
(7, 7, 5, 'entry', 80, 1),
(8, 8, 7, 'exit', 90, 1),
(9, 9, 9, 'entry', 250, 1),
(10, 1, 2, 'exit', 70, 1);

-- Insertar datos en la tabla systems
INSERT INTO `systems` (id, name, description) VALUES
(1, 'Nubefact', 'Integración con el sistema de facturación electrónica Nubefact.'),
(2, 'Odoo', 'Integración con el ERP Odoo para sincronización de datos.'),
(3, 'SUNAT', 'Conexión directa con SUNAT para validación de comprobantes.'),
(4, 'SMTP', 'Configuración del servidor de correo para envíos automáticos.'),
(5, 'Pasarela de Pagos', 'Pasarelas de pago como Culqi, MercadoPago y PayU.'),
(6, 'Sistema Propio', 'Configuraciones internas del sistema ERP.'),
(7, 'Certificados Digitales', 'Llaves y certificados digitales del sistema.');

-- Insertar datos en la tabla keys
INSERT INTO `keys` (id, system_id, name, description, config_key, config_value, status, created_by) VALUES
(1, 1, 'Nubefact API URL', 'URL base para conexión a la API de Nubefact', 'nubefact_api_url', 'https://api.nubefact.com/api/v1/e421b983-cc37-45ca-8bbf-b4b5e4af3136', 1, 1),
(2, 1, 'Nubefact API Token', 'Token de autenticación para emisión de comprobantes en Nubefact', 'nubefact_api_token', '9a048f724546488eb4e3da7a46e27b110732865e97de49c5a07f930c57a45ffc', 1, 1),
(3, 2, 'Odoo Base URL', 'URL base para conexión al servidor Odoo XML-RPC', 'odoo_base_url', 'https://erp.miempresa.com/xmlrpc/2/object', 1, 1),
(4, 2, 'Odoo Database Name', 'Nombre de la base de datos de Odoo', 'odoo_db_name', 'erp_miempresa', 1, 1),
(5, 2, 'Odoo Username', 'Usuario administrador de Odoo', 'odoo_username', 'admin', 1, 1),
(6, 2, 'Odoo Password', 'Contraseña del usuario de Odoo', 'odoo_password', 'odooPass123', 1, 1),
(7, 3, 'SUNAT SOL Username', 'Usuario SOL para conexión a SUNAT', 'sunat_sol_username', '20555555555MODDATOS', 1, 1),
(8, 3, 'SUNAT SOL Password', 'Contraseña SOL del usuario para SUNAT', 'sunat_sol_password', 'miClaveSegura123', 1, 1),
(9, 3, 'SUNAT URL Beta', 'URL del servicio web de SUNAT en ambiente de prueba', 'sunat_beta_url', 'https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService', 1, 1),
(10, 3, 'SUNAT URL Producción', 'URL del servicio web de SUNAT en producción', 'sunat_prod_url', 'https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService', 1, 1),
(11, 3, 'SUNAT Certificate Path', 'Ruta del certificado digital para SUNAT', 'sunat_cert_path', '/certs/sunat_cert.pfx', 1, 1),
(12, 3, 'SUNAT Certificate Password', 'Contraseña del certificado digital SUNAT', 'sunat_cert_password', 'certPassword123', 1, 1),
(13, 4, 'SMTP Host', 'Servidor de correo SMTP', 'smtp_host', 'smtp.miempresa.com', 1, 1),
(14, 4, 'SMTP Port', 'Puerto del servidor SMTP', 'smtp_port', '587', 1, 1),
(15, 4, 'SMTP User', 'Correo electrónico utilizado para enviar los correos', 'smtp_user', 'noreply@miempresa.com', 1, 1),
(16, 4, 'SMTP Password', 'Contraseña del correo SMTP', 'smtp_password', 'correoSuperSeguro123', 1, 1),
(17, 4, 'SMTP Encryption', 'Método de cifrado utilizado (TLS o SSL, 1)', 'smtp_encryption', 'TLS', 1, 1),
(18, 5, 'Culqi Public Key', 'Llave pública para el cliente en Culqi', 'culqi_public_key', 'pk_test_CULQIPUBLICKEY', 1, 1),
(19, 5, 'Culqi Private Key', 'Llave secreta para operaciones en Culqi', 'culqi_private_key', 'sk_test_CULQIPRIVATEKEY', 1, 1),
(20, 5, 'Culqi API URL', 'URL base para el servicio de Culqi', 'culqi_api_url', 'https://api.culqi.com/v2', 1, 1),
(21, 5, 'MercadoPago Public Key', 'Llave pública para el cliente en MercadoPago', 'mercadopago_public_key', 'PUBLIC_MP_KEY', 1, 1),
(22, 5, 'MercadoPago Access Token', 'Token de acceso privado de MercadoPago', 'mercadopago_access_token', 'ACCESS_TOKEN_MP', 1, 1),
(23, 6, 'Sistema Nombre', 'Nombre de la empresa o sistema', 'system_name', 'ERP Mi Empresa', 1, 1),
(24, 6, 'Sistema Modo', 'Modo del sistema (produccion/desarrollo, 1)', 'system_mode', 'produccion', 1, 1),
(25, 6, 'JWT Secret', 'Llave secreta utilizada para firmar los JWT tokens', 'jwt_secret', 'jwtSuperSecret123456', 1, 1),
(26, 6, 'Token Expiración', 'Tiempo de expiración del token JWT en minutos', 'jwt_expiration_minutes', '120', 1, 1),
(27, 6, 'URL Frontend', 'URL del frontend del sistema', 'frontend_url', 'https://miempresa.app', 1, 1),
(28, 6, 'URL Backend', 'URL del backend del sistema', 'backend_url', 'https://api.miempresa.com', 1, 1),
(29, 7, 'Certificado SSL Path', 'Ruta donde se almacena el certificado SSL', 'ssl_cert_path', '/certs/ssl_cert.pem', 1, 1),
(30, 7, 'Llave Privada SSL Path', 'Ruta donde se almacena la llave privada del SSL', 'ssl_private_key_path', '/certs/ssl_key.pem', 1, 1),
(31, 7, 'Certificado SSL Password', 'Contraseña para el acceso al certificado SSL si aplica', 'ssl_cert_password', 'sslPassword123', 1, 1),
(32, 7, 'Certificado SUNAT PFX', 'Ruta del archivo PFX del certificado digital SUNAT', 'sunat_cert_pfx_path', '/certs/sunat_cert.pfx', 1, 1),
(33, 7, 'Password SUNAT PFX', 'Password del archivo PFX de SUNAT', 'sunat_cert_pfx_password', 'pfxPassword321', 1, 1);

-- Insertar tipos de asistencia básicos
INSERT INTO `attendance_types` (id, name, code, description) VALUES
(1, 'Teletrabajo', 'TELE', 'Día laboral en modalidad de teletrabajo'),
(2, 'Viaje de Negocios', 'VIAJ', 'Asistencia registrada durante viaje de negocios'),
(3, 'Capacitación Externa', 'CAPE', 'Asistencia a capacitación fuera de la oficina'),
(4, 'Licencia por Maternidad', 'MAT', 'Licencia por maternidad/paternidad'),
(5, 'Licencia por Duelo', 'DUEL', 'Licencia por fallecimiento de familiar'),
(6, 'Normal', 'NORM', 'Asistencia normal en horario laboral'),
(7, 'Tardanza', 'TARD', 'El empleado llegó tarde'),
(8, 'Salida Temprana', 'SALT', 'El empleado salió antes de tiempo'),
(9, 'Falta Justificada', 'FJUS', 'Falta con justificación aprobada'),
(10, 'Falta Injustificada', 'FINJ', 'Falta sin justificación');

-- Insertar asistencias
INSERT INTO `attendances` (id, employee_id, attendance_type_id, date, check_in, check_out, worked_hours, late_minutes, status) VALUES
(1, 1, 1, '2023-01-02', '2023-01-02 08:58:00', '2023-01-02 17:05:00', 8.12, 0, 'approved'),
(2, 1, 1, '2023-01-03', '2023-01-03 09:15:00', '2023-01-03 17:10:00', 7.92, 15, 'approved'),
(3, 2, 1, '2023-01-02', '2023-01-02 08:50:00', '2023-01-02 17:00:00', 8.17, 0, 'approved'),
(4, 3, 3, '2023-01-02', '2023-01-02 09:30:00', '2023-01-02 17:45:00', 8.25, 30, 'approved'),
(5, 4, 1, '2023-01-02', '2023-01-02 08:45:00', '2023-01-02 16:50:00', 8.08, 0, 'approved'),
(6, 5, 6, '2023-01-02', NULL, NULL, 8.00, 0, 'approved'), -- Teletrabajo
(7, 6, 1, '2023-01-03', '2023-01-03 09:05:00', '2023-01-03 17:10:00', 8.08, 5, 'approved'),
(8, 7, 4, '2023-01-03', NULL, NULL, 0.00, 0, 'approved'), -- Falta justificada
(9, 8, 7, '2023-01-03', NULL, NULL, 8.00, 0, 'approved'), -- Viaje de negocios
(10, 9, 1, '2023-01-04', '2023-01-04 08:55:00', '2023-01-04 17:30:00', 8.58, 0, 'approved');

-- Insertar tipos de ausencia básicos
INSERT INTO `absence_types` (id, name, code, description, requires_approval, is_paid) VALUES
(1, 'Licencia por Paternidad', 'LPAT', 'Licencia por nacimiento de hijo', 1, 1),
(2, 'Licencia Sindical', 'LSIN', 'Licencia para actividades sindicales', 1, 0),
(3, 'Licencia por Examen', 'LEXA', 'Licencia para rendir exámenes académicos', 1, 0),
(4, 'Licencia sin Goce', 'LSGO', 'Licencia sin goce de haber', 1, 0),
(5, 'Licencia por Donación', 'LDON', 'Licencia por donación de sangre/órganos', 1, 1),
(6, 'Enfermedad', 'ENF', 'Ausencia por enfermedad', 1, 1),
(7, 'Vacaciones', 'VAC', 'Días de vacaciones', 1, 1),
(8, 'Permiso Personal', 'PER', 'Permiso personal remunerado', 1, 1),
(9, 'Permiso No Remunerado', 'PNR', 'Permiso personal no remunerado', 1, 0),
(10, 'Licencia Médica', 'LIC', 'Licencia médica prolongada', 1, 1);

-- Insertar solicitudes de asistencia
INSERT INTO `absence_requests` (id, employee_id, absence_type_id, start_date, end_date, reason, status, approved_by) VALUES
(1, 1, 2, '2023-02-10', '2023-02-10', 'Vacaciones programadas', 'approved', 1),
(2, 2, 1, '2023-02-15', '2023-02-17', 'Cuadro gripal con fiebre', 'approved', 1),
(3, 3, 3, '2023-03-01', '2023-03-01', 'Permiso personal para trámites', 'approved', 1),
(4, 4, 6, '2023-03-05', '2023-03-05', 'Licencia por paternidad - nacimiento de hijo', 'approved', 1),
(5, 5, 2, '2023-03-10', '2023-03-20', 'Vacaciones familiares', 'approved', 1),
(6, 6, 1, '2023-04-01', '2023-04-03', 'Infección estomacal', 'approved', 1),
(7, 7, 7, '2023-04-15', '2023-04-15', 'Reunión sindical', 'approved', 1),
(8, 8, 4, '2023-05-02', '2023-05-02', 'Permiso no remunerado para mudanza', 'approved', 1),
(9, 9, 8, '2023-05-10', '2023-05-10', 'Examen final de maestría', 'approved', 1),
(10, 10, 5, '2023-05-15', '2023-05-15', 'Donación de sangre', 'approved', 1);

-- Insertar vacaciones
INSERT INTO `vacations` (id, employee_id, start_date, end_date, days_taken, status, approved_by) VALUES
(1, 1, '2023-06-01', '2023-06-10', 8, 'approved', 1),
(2, 2, '2023-06-15', '2023-06-30', 12, 'approved', 1),
(3, 3, '2023-07-01', '2023-07-07', 5, 'approved', 1),
(4, 4, '2023-07-10', '2023-07-21', 10, 'approved', 1),
(5, 5, '2023-08-01', '2023-08-14', 10, 'approved', 1),
(6, 6, '2023-08-15', '2023-08-25', 7, 'approved', 1),
(7, 7, '2023-09-01', '2023-09-08', 6, 'approved', 1),
(8, 8, '2023-09-10', '2023-09-22', 9, 'approved', 1),
(9, 9, '2023-10-01', '2023-10-06', 4, 'approved', 1),
(10, 10, '2023-10-15', '2023-10-27', 9, 'approved', 1);

-- Insertar saldos de vacaciones
INSERT INTO `vacation_balances` (id, employee_id, year, total_days, days_taken) VALUES
(1, 1, 2023, 30, 8),
(2, 2, 2023, 30, 12),
(3, 3, 2023, 30, 5),
(4, 4, 2023, 30, 10),
(5, 5, 2023, 30, 10),
(6, 6, 2023, 30, 7),
(7, 7, 2023, 30, 6),
(8, 8, 2023, 30, 9),
(9, 9, 2023, 30, 4),
(10, 10, 2023, 30, 9);

-- Insertar horario laboral estándar
INSERT INTO `work_schedules` (id, name, description, is_default) VALUES
(1, 'Horario Turnos Rotativos', 'Turnos rotativos mañana/tarde de 6 horas', 0),
(2, 'Horario Medio Tiempo', 'Horario de medio tiempo (4 horas diarias)', 0),
(3, 'Horario Oficina Estándar', 'Lunes a Viernes de 9:00 a 18:00 con 1 hora de almuerzo', 1);

-- Insertar detalles del horario estándar
INSERT INTO `schedule_details` (id, schedule_id, day_of_week, start_time, end_time, is_working_day) VALUES
(1, 2, 1, '08:00:00', '14:00:00', 1), -- Lunes mañana
(2, 2, 1, '14:00:00', '20:00:00', 1), -- Lunes tarde
(3, 2, 2, '08:00:00', '14:00:00', 1), -- Martes mañana
(4, 2, 2, '14:00:00', '20:00:00', 1), -- Martes tarde
(5, 2, 3, '08:00:00', '14:00:00', 1), -- Miércoles mañana
(6, 2, 3, '14:00:00', '20:00:00', 1), -- Miércoles tarde
(7, 2, 4, '08:00:00', '14:00:00', 1), -- Jueves mañana
(8, 2, 4, '14:00:00', '20:00:00', 1), -- Jueves tarde
(9, 2, 5, '08:00:00', '14:00:00', 1), -- Viernes mañana
(10, 2, 5, '14:00:00', '20:00:00', 1), -- Viernes tarde
(11, 2, 6, '00:00:00', '00:00:00', 0), -- Sábado
(12, 2, 0, '00:00:00', '00:00:00', 0), -- Domingo
-- Horario Medio Tiempo
(13, 3, 1, '09:00:00', '13:00:00', 1), -- Lunes
(14, 3, 2, '09:00:00', '13:00:00', 1), -- Martes
(15, 3, 3, '09:00:00', '13:00:00', 1), -- Miércoles
(16, 3, 4, '09:00:00', '13:00:00', 1), -- Jueves
(17, 3, 5, '09:00:00', '13:00:00', 1), -- Viernes
(18, 3, 6, '00:00:00', '00:00:00', 0), -- Sábado
(19, 3, 0, '00:00:00', '00:00:00', 0); -- Domingo

-- Insertar horarios de empleados
INSERT INTO `employee_schedules` (id, employee_id, schedule_id, effective_date) VALUES
(1, 1, 1, '2023-01-01'),
(2, 2, 1, '2023-01-01'),
(3, 3, 1, '2023-01-01'),
(4, 4, 1, '2023-01-01'),
(5, 5, 1, '2023-01-01'),
(6, 6, 2, '2023-01-01'),
(7, 7, 2, '2023-01-01'),
(8, 8, 1, '2023-01-01'),
(9, 9, 3, '2023-01-01'),
(10, 10, 1, '2023-01-01');

-- Insertar vacaciones
INSERT INTO `holidays` (id, name, date, recurring, status) VALUES
(1, 'Año Nuevo', '2023-01-01', 1, 1),
(2, 'Jueves Santo', '2023-04-06', 0, 1),
(3, 'Viernes Santo', '2023-04-07', 0, 1),
(4, 'Día del Trabajo', '2023-05-01', 1, 1),
(5, 'San Pedro y San Pablo', '2023-06-29', 1, 1),
(6, 'Fiestas Patrias', '2023-07-28', 1, 1),
(7, 'Fiestas Patrias', '2023-07-29', 1, 1),
(8, 'Santa Rosa de Lima', '2023-08-30', 1, 1),
(9, 'Combate de Angamos', '2023-10-08', 1, 1),
(10, 'Navidad', '2023-12-25', 1, 1);

-- Insertar solicitudes de tiempo extra
INSERT INTO `overtime_requests` (id, employee_id, date, start_time, end_time, reason, status, approved_by) VALUES
(1, 1, '2023-01-05', '18:00:00', '20:30:00', 'Terminar reporte mensual', 'approved', 1),
(2, 2, '2023-01-10', '18:00:00', '21:00:00', 'Revisión de inventario', 'approved', 1),
(3, 3, '2023-02-15', '18:00:00', '19:30:00', 'Preparación de auditoría', 'approved', 1),
(4, 4, '2023-02-20', '18:00:00', '20:00:00', 'Implementación nuevo sistema', 'approved', 1),
(5, 5, '2023-03-01', '18:00:00', '22:00:00', 'Cierre fiscal', 'approved', 1),
(6, 6, '2023-03-10', '14:00:00', '18:00:00', 'Capacitación personal nuevo', 'approved', 1),
(7, 7, '2023-04-05', '18:00:00', '21:00:00', 'Mantenimiento servidores', 'approved', 1),
(8, 8, '2023-04-12', '18:00:00', '20:00:00', 'Migración de datos', 'approved', 1),
(9, 9, '2023-05-03', '13:00:00', '17:00:00', 'Evento corporativo', 'approved', 1),
(10, 10, '2023-05-15', '18:00:00', '23:00:00', 'Lanzamiento de producto', 'approved', 1);

-- Insertar nóminas
INSERT INTO `payrolls` (id, reference, period_start, period_end, payment_date, status, created_by) VALUES
(1, 'NOM-202301', '2023-01-01', '2023-01-31', '2023-02-05', 'paid', 1),
(2, 'NOM-202302', '2023-02-01', '2023-02-28', '2023-03-05', 'paid', 1),
(3, 'NOM-202303', '2023-03-01', '2023-03-31', '2023-04-05', 'paid', 1),
(4, 'NOM-202304', '2023-04-01', '2023-04-30', '2023-05-05', 'paid', 1),
(5, 'NOM-202305', '2023-05-01', '2023-05-31', '2023-06-05', 'paid', 1),
(6, 'NOM-202306', '2023-06-01', '2023-06-30', '2023-07-05', 'paid', 1),
(7, 'NOM-202307', '2023-07-01', '2023-07-31', '2023-08-05', 'paid', 1),
(8, 'NOM-202308', '2023-08-01', '2023-08-31', '2023-09-05', 'paid', 1),
(9, 'NOM-202309', '2023-09-01', '2023-09-30', '2023-10-05', 'paid', 1),
(10, 'NOM-202310', '2023-10-01', '2023-10-31', '2023-11-05', 'paid', 1);

-- Insertar detalles de nóminas
INSERT INTO `payroll_details` (id, payroll_id, employee_id, base_salary, days_worked, hours_worked, overtime_hours, overtime_pay, net_pay, status) VALUES
(1, 1, 1, 4500.00, 22, 176.0, 2.5, 168.75, 4668.75, 'paid'),
(2, 1, 2, 7500.00, 22, 176.0, 3.0, 506.25, 8006.25, 'paid'),
(3, 1, 3, 4800.00, 21, 168.0, 1.5, 108.00, 4908.00, 'paid'),
(4, 1, 4, 5500.00, 22, 176.0, 2.0, 185.00, 5685.00, 'paid'),
(5, 1, 5, 3200.00, 20, 160.0, 4.0, 192.00, 3392.00, 'paid'),
(6, 1, 6, 4600.00, 22, 132.0, 4.0, 276.00, 4876.00, 'paid'),
(7, 1, 7, 5200.00, 21, 126.0, 3.0, 312.00, 5512.00, 'paid'),
(8, 1, 8, 12000.00, 22, 176.0, 2.0, 900.00, 12900.00, 'paid'),
(9, 1, 9, 1800.00, 22, 88.0, 4.0, 108.00, 1908.00, 'paid'),
(10, 1, 10, 6800.00, 22, 176.0, 5.0, 637.50, 7437.50, 'paid');

-- Insertar beneficios de empleados
INSERT INTO `employee_benefits` (id, employee_id, benefit_type, description, amount, start_date) VALUES
(1, 1, 'Seguro Médico', 'Cobertura médica familiar', 250.00, '2023-01-01'),
(2, 2, 'Seguro Médico', 'Cobertura médica premium', 350.00, '2023-01-01'),
(3, 3, 'Vale de Almuerzo', 'Subsidio alimentario mensual', 150.00, '2023-01-01'),
(4, 4, 'Vale de Almuerzo', 'Subsidio alimentario mensual', 150.00, '2023-01-01'),
(5, 5, 'Seguro de Vida', 'Seguro de vida grupo', 100.00, '2023-01-01'),
(6, 6, 'Celular Corporativo', 'Plan de datos y llamadas', 120.00, '2023-01-01'),
(7, 7, 'Gimnasio', 'Membresía corporativa', 80.00, '2023-01-01'),
(8, 8, 'Auto Empresa', 'Vehículo corporativo', 800.00, '2023-01-01'),
(9, 9, 'Vale de Almuerzo', 'Subsidio alimentario mensual', 150.00, '2023-01-01'),
(10, 10, 'Seguro Médico', 'Cobertura médica familiar', 250.00, '2023-01-01');

-- Insertar revisiones de rendimiento
INSERT INTO `performance_reviews` (id, employee_id, reviewer_id, review_date, next_review_date, performance_score, strengths, areas_for_improvement, status) VALUES
(1, 1, 1, '2023-06-15', '2023-12-15', 4, 'Excelente trabajo en equipo, proactivo', 'Mejorar presentaciones ejecutivas', 'completed'),
(2, 2, 1, '2023-06-16', '2023-12-16', 5, 'Liderazgo excepcional, resultados consistentes', 'Manejo de estrés en picos de trabajo', 'completed'),
(3, 3, 1, '2023-06-17', '2023-12-17', 3, 'Creatividad en soluciones, puntualidad', 'Necesita más iniciativa en proyectos', 'completed'),
(4, 4, 1, '2023-06-18', '2023-12-18', 4, 'Gran capacidad analítica, detallista', 'Comunicación más asertiva con pares', 'completed'),
(5, 5, 1, '2023-06-19', '2023-12-19', 3, 'Buen manejo de clientes, empático', 'Profundizar conocimiento técnico', 'completed'),
(6, 6, 1, '2023-06-20', '2023-12-20', 4, 'Alto rendimiento bajo presión', 'Mejorar documentación de procesos', 'completed'),
(7, 7, 1, '2023-06-21', '2023-12-21', 5, 'Innovación constante, mentoría', 'Equilibrar perfeccionismo con productividad', 'completed'),
(8, 8, 1, '2023-06-22', '2023-12-22', 5, 'Visión estratégica, toma de decisiones', 'Delegar más responsabilidades', 'completed'),
(9, 9, 1, '2023-06-23', '2023-12-23', 3, 'Actitud positiva, aprendizaje rápido', 'Mayor autonomía en tareas', 'completed'),
(10, 10, 1, '2023-06-24', '2023-12-24', 4, 'Excelente manejo de proyectos complejos', 'Mejorar estimación de tiempos', 'completed');

-- Insertar incidencias de empleados
INSERT INTO `employee_incidents` (id, employee_id, incident_type, incident_date, observation, discount, total_to_pay, reported_by, status) VALUES
(1, 3, 'Retraso frecuente', '2023-02-10', '5 retrasos en 2 semanas', 100, 1400, 1, 'resolved'),
(2, 5, 'Conflicto interpersonal', '2023-03-15', 'Discusión acalorada con compañero', 100, 1400, 1, 'resolved'),
(3, 7, 'Error en proceso', '2023-04-05', 'Error en reporte financiero', 100, 1400, 1, 'resolved'),
(4, 1, 'Uso indebido de recursos', '2023-04-20', 'Uso excesivo de impresora para personal', 100, 1400, 1, 'closed'),
(5, 9, 'Ausencia no comunicada', '2023-05-02', 'No asistió sin aviso previo', 100, 1400, 1, 'resolved'),
(6, 2, 'Violación política', '2023-05-10', 'Compartió credenciales de acceso', 100, 1400, 1, 'investigating'),
(7, 4, 'Accidente laboral', '2023-06-01', 'Caída en escaleras', 100, 1400, 1, 'resolved'),
(8, 6, 'Maltrato a subordinado', '2023-06-15', 'Comentarios inapropiados a practicante', 100, 1400, 1, 'investigating'),
(9, 10, 'Fuga información', '2023-07-03', 'Envió datos confidenciales a personal externo', 100, 1400, 1, 'open'),
(10, 8, 'Conflicto de interés', '2023-07-10', 'Trabajo paralelo con competidor', 100, 1400, 1, 'investigating');