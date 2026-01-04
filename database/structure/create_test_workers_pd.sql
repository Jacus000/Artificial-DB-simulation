CREATE TABLE IF NOT EXISTS test_workers_pd (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10)  NOT NULL,
    email VARCHAR(100) UNIQUE,
    PESEL VARCHAR(11) UNIQUE,
    phone_number VARCHAR(12),
    city VARCHAR(50),
    postal_code VARCHAR(10),
    street VARCHAR(50),
    house_number INT
);

