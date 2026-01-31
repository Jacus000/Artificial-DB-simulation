CREATE TABLE IF NOT EXISTS guests_personal_data (
    id_guest INT UNSIGNED PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE DEFAULT NULL,
    height INT UNSIGNED,
    email VARCHAR(255) UNIQUE DEFAULT NULL,
    pesel CHAR(11) UNIQUE DEFAULT NULL,
    city VARCHAR(255) NOT NULL,

    CONSTRAINT fk_guest_personal_data
        FOREIGN KEY (id_guest)
        REFERENCES guest(id_guest)
        ON DELETE CASCADE
);