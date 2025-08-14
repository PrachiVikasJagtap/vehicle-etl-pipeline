CREATE TABLE vehicle_specs (
    id SERIAL PRIMARY KEY,
    year INT,
    make_id INT,
    make_name VARCHAR(100),
    model_id INT,
    model_name VARCHAR(100),
    trim_id INT,
    trim_name VARCHAR(100),
    body_type VARCHAR(100),
    engine_type VARCHAR(100),
    exterior_color VARCHAR(100),
    interior_color VARCHAR(100),
    mileage VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select*from vehicle_specs