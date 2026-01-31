CREATE TABLE malfunction_report (
    id_malfunction_report INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_attraction INT UNSIGNED NOT NULL,
    id_employee_reported INT UNSIGNED NOT NULL,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    is_resolved BOOLEAN DEFAULT FALSE,
    is_resolved_at TIMESTAMP NULL,

    CONSTRAINT fk_malfuntion_attractions
        FOREIGN KEY (id_attraction)
        REFERENCES attractions(id_attraction)
        ON DELETE CASCADE,

    CONSTRAINT fk_malfunction_employee
        FOREIGN KEY (id_employee_reported)
        REFERENCES employees(id_employee)
);
