CREATE TABLE IF NOT EXISTS facility_expenses (
    id_expense INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    expense_date TIMESTAMP,
    expense_cost DECIMAL(10,2) NOT NULL,
    id_facility INT UNSIGNED,
    expense_category ENUM(
        'FoodAndBeverages', 
        'AlcoholSupplies',  
        'Merchandise',      
        'PhotoMaterials',     
        'Utilities',      
        'Maintenance',       
        'Cleaning',      
        'Security',    
        'LicensingAndPermits'                                
    ) NOT NULL,

    CONSTRAINT fk_facility_expenses
        FOREIGN KEY (id_facility)
        REFERENCES facilities(id_facility)
);