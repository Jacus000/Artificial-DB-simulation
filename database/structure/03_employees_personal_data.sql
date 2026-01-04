CREATE TABLE employee_personal_data (
    id_employee INT UNSIGNED PRIMARY KEY,
    adress VARCHAR(255),
    postal_code VARCHAR(10),
    city VARCHAR(40),
    phone_number VARCHAR(15),
    PESEL VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(255),
    
    CONSTRAINT fk_personal_employee
        FOREIGN KEY (id_employee)
        REFERENCES employees(id_employee)
        ON DELETE CASCADE
);

