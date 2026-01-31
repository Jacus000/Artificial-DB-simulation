CREATE TABLE IF NOT EXISTS guest (
    id_guest INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender ENUM('woman', 'man') NOT NULL
);

