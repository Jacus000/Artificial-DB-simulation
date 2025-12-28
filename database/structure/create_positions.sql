CREATE TABLE positions(
    id_position INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    position_name VARCHAR(100) NOT NULL UNIQUE,
    id_sector INT UNSIGNED NOT NULL,

    CONSTRAINT fk_workers_sector
        FOREIGN KEY id_sector
        REFERENCES sectors(id_sector)
);