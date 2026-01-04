CREATE TABLE IF NOT EXISTS accident_type (
    id_accident_type INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    accident_type_name VARCHAR(255) NOT NULL UNIQUE,
    suggest_compensation DECIMAL(10,2) NOT NULL
);
