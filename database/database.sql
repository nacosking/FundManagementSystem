CREATE TABLE funds (
    fund_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    manager_name TEXT NOT NULL,
    description TEXT,
    nav REAL NOT NULL,
    creation_date TEXT NOT NULL,
    performance REAL,
);
