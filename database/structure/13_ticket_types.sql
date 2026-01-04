CREATE TABLE IF NOT EXISTS ticket_types (
    id_ticket_type INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ticket_type_name VARCHAR(255) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    id_plan INT UNSIGNED NOT NULL,

    CONSTRAINT fk_insurance_plan
        FOREIGN KEY (id_plan)
        REFERENCES insurance_plans(id_plan)
);

