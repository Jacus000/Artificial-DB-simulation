CREATE TABLE IF NOT EXISTS attraction_costs (
    id_attraction_cost INT AUTO_INCREMENT PRIMARY KEY,
    id_attraction INT UNSIGNED NOT NULL,
    cost_type ENUM('power', 'maintenance', 'repair', 'other') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    cost_date DATE NOT NULL,
    id_malfunction INT UNSIGNED DEFAULT NULL,

    CONSTRAINT fk_attraction_cost
        FOREIGN KEY (id_attraction)
        REFERENCES attractions(id_attraction),

    CONSTRAINT fk_malfunctions
        FOREIGN KEY (id_malfunction)
        REFERENCES malfunction_report(id_malfunction_report)
);

