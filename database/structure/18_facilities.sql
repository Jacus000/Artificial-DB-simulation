CREATE TABLE IF NOT EXISTS facilities (
    id_facility INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    facility_name VARCHAR(255) NOT NULL,
    facility_type ENUM('restaurant', 'bar', 'souvenir_shop', 'casino', 'photo_booth'),
    id_sector INT UNSIGNED,

    CONSTRAINT fk_facility_sector
        FOREIGN KEY (id_sector)
        REFERENCES sectors(id_sector)
);