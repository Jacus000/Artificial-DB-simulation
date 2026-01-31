CREATE TABLE IF NOT EXISTS accidents (
    id_accident INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_visit INT UNSIGNED NOT NULL,
    id_attraction INT UNSIGNED NOT NULL,
    id_accident_type INT UNSIGNED NOT NULL,
    accident_description TEXT DEFAULT NULL,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_accident_visit
        FOREIGN KEY (id_visit)
        REFERENCES guests_visit(id_visit)
        ON DELETE CASCADE,

    CONSTRAINT fk_accident_attraction
        FOREIGN KEY (id_attraction)
        REFERENCES attractions(id_attraction)
        ON DELETE RESTRICT,

    CONSTRAINT fk_accident_type
        FOREIGN KEY (id_accident_type)
        REFERENCES accident_type(id_accident_type)
        ON DELETE RESTRICT
);
   
