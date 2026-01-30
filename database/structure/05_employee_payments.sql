CREATE TABLE IF NOT EXISTS employee_payments (
    id_payment INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_employee INT UNSIGNED NOT NULL,
    salary_month DATE NOT NULL,
    base_salary_id INT UNSIGNED NOT NULL,
    bonus DECIMAL(10,2) UNSIGNED DEFAULT 0,
    deduction DECIMAL(10,2) UNSIGNED DEFAULT 0,
    payment_date DATE NOT NULL,

    CONSTRAINT fk_payment_employee
        FOREIGN KEY (id_employee)
        REFERENCES employees(id_employee),

    CONSTRAINT fk_payment_history
        FOREIGN KEY (base_salary_id)
        REFERENCES salary_history(id_salary),

    CONSTRAINT uq_employee_month
        UNIQUE (id_employee, salary_month),

    CONSTRAINT chk_bonus_deduction
        CHECK (bonus >= 0 AND deduction >= 0)
);