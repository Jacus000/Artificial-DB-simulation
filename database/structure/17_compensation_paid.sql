CREATE TABLE IF NOT EXISTS compensation_paid (
    id_payout INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_accident INT UNSIGNED NOT NULL UNIQUE,
    amount_paid DECIMAL(10,2) UNSIGNED NOT NULL CHECK (amount_paid >= 0),
    payout_date DATE NOT NULL,
    is_covered_by_insurance BOOLEAN NOT NULL DEFAULT 1,

    CONSTRAINT fk_compensation_accident
        FOREIGN KEY (id_accident)
        REFERENCES accidents(id_accident)
        ON DELETE CASCADE
);

