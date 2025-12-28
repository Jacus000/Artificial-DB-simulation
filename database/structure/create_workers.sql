CREATE TABLE workers(
    id_worker INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    second_name VARCHAR(40) NOT NULL,
    gender ENUM('woman', 'men') NOT NULL,
    salary DECIMAL(10,2) UNSIGNED NOT NULL,
    position VARCHAR(30) NOT NULL,
    phone_number VARCHAR(14) UNIQUE,
    email VARCHAR(255) UNIQUE,
    id_sector INT UNSIGNED NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_workers_sector
        FOREIGN KEY id_sector
        REFERENCES sectors(id_sector)
);