CREATE TABLE inspections (
    id_inspection INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_attraction INT UNSIGNED NOT NULL,
    id_employee INT UNSIGNED NOT NULL,
    inspection_date DATE NOT NULL,
    next_inspection_date DATE DEFAULT NULL,
    result ENUM('passed', 'failed') NOT NULL,

    CONSTRAINT fk_inspections_attraction
        FOREIGN KEY (id_attraction)
        REFERENCES attractions(id_attraction)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_inspection_worker
        FOREIGN KEY (id_employee)
        REFERENCES employees(id_employee)
        ON DELETE RESTRICT
);

