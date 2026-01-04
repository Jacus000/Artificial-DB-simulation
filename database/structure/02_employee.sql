CREATE TABLE IF NOT EXISTS employees(
    id_employee INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    second_name VARCHAR(40) NOT NULL,
    gender ENUM('woman', 'man') NOT NULL,
    id_position INT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employees_position
        FOREIGN KEY (id_position)
        REFERENCES positions(id_position)
);