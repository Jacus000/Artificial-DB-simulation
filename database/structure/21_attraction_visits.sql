CREATE TABLE IF NOT EXISTS attraction_visits (
    id_attraction_visit INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_visit INT UNSIGNED NOT NULL,
    id_attraction INT UNSIGNED NOT NULL,
    visit_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_att_visit_visit
        FOREIGN KEY (id_visit)
        REFERENCES guests_visit(id_visit)
        ON DELETE CASCADE,

    CONSTRAINT fk_att_visit_attraction
        FOREIGN KEY (id_attraction)
        REFERENCES attractions(id_attraction)
        ON DELETE CASCADE
);
