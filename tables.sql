-- Створення таблиці типів ліків
CREATE TABLE DrugTypes (
    type_id SERIAL PRIMARY KEY, type_name VARCHAR(100)
);

-- Створення таблиці заявників
CREATE TABLE Applicants (
    applicant_id SERIAL PRIMARY KEY, name VARCHAR(255), country VARCHAR(100), address TEXT
);

-- Створення таблиці виробників
CREATE TABLE Manufacturers (
    manufacturer_id SERIAL PRIMARY KEY, name VARCHAR(255), country VARCHAR(100), address TEXT
);

-- Створення основної таблиці ліків
CREATE TABLE Drugs (
    id VARCHAR(50) PRIMARY KEY, trade_name VARCHAR(255),
    international_name VARCHAR(255), form TEXT, conditions VARCHAR(100),
    composition TEXT, pharmacotherapeutic_group TEXT,
    atc_code VARCHAR(50), applicant_id INT REFERENCES Applicants(applicant_id),
    registration_number VARCHAR(50),
    start_date DATE, end_date DATE,
    drug_type_id INT REFERENCES DrugTypes(type_id)
);

-- Створення таблиці термінів придатності
CREATE TABLE ShelfLife (
    drug_id VARCHAR(50) PRIMARY KEY REFERENCES Drugs(id),
    bio_origin BOOLEAN, plant_origin BOOLEAN,
    orphan_drug BOOLEAN, homeopathic BOOLEAN,
    mnn_type BOOLEAN, manual_url TEXT,
    shelf_life TEXT, shelf_life_value NUMERIC, shelf_life_unit VARCHAR(50)
);

-- Створення зв'язкової таблиці між ліками та виробниками
CREATE TABLE DrugManufacturers (
    drug_id VARCHAR(50) REFERENCES Drugs(id),
    manufacturer_id INT REFERENCES Manufacturers(manufacturer_id),
    PRIMARY KEY (drug_id, manufacturer_id)
);