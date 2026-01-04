CREATE TABLE IF NOT EXISTS salary_history (
    id_salary INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_employee INT UNSIGNED NOT NULL,
    base_amount DECIMAL(10,2) UNSIGNED NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE DEFAULT NULL,

    CONSTRAINT fk_employees
        FOREIGN KEY (id_employee)
        REFERENCES employees(id_employee)
)

