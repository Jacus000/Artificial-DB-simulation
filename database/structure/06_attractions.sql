CREATE TABLE attractions (
    id_attraction INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    att_name VARCHAR(255) NOT NULL,
    att_type VARCHAR(60) NOT NULL,
    is_vr_capable BOOLEAN DEFAULT FALSE,
    att_description TEXT,
    height_limit_cm INT UNSIGNED,
    capacity_per_attraction INT UNSIGNED
);

