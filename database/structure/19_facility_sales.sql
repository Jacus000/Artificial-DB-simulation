CREATE TABLE IF NOT EXISTS facility_sales (
    id_sale INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sale_date TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    id_facility INT UNSIGNED,
    payment_method ENUM('Cash', 'Card', 'BLIK', 'Gift_card'),

    CONSTRAINT fk_facility
        FOREIGN KEY (id_facility)
        REFERENCES facilities(id_facility)
);