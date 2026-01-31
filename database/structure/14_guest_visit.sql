CREATE TABLE IF NOT EXISTS guests_visit (
    id_visit INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_guest INT UNSIGNED NOT NULL,
    id_ticket_type INT UNSIGNED NOT NULL,
    visit_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_visit_guest
        FOREIGN KEY (id_guest)
        REFERENCES guest(id_guest)
        ON DELETE CASCADE,

    CONSTRAINT fk_visit_ticket
        FOREIGN KEY (id_ticket_type)
        REFERENCES ticket_types(id_ticket_type)
        ON DELETE RESTRICT,
    
    CONSTRAINT uq_one_ticket
        UNIQUE (id_guest, visit_date)
);