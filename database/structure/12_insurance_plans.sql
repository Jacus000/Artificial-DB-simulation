CREATE TABLE IF NOT EXISTS insurance_plans (
    id_plan INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(255) NOT NULL,
    plan_description TEXT DEFAULT NULL
);
