CREATE TABLE Beneficiary(
    id CHAR(36) NOT NULL,
    beneficiary_name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Payment(
    id CHAR(36) NOT NULL,
    payer CHAR(36) REFERENCES Beneficiary(id) NOT NULL,
    recipient CHAR(36) REFERENCES Beneficiary(id) NOT NULL,
    main_cat VARCHAR(255),
    sub_cat VARCHAR(255),
    entry_date DATE NOT NULL,
    value_date DATE,
    PRIMARY KEY(id)
);

CREATE TABLE Payment_method(
    id CHAR(36) NOT NULL,
    bank VARCHAR(255),
    method VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE Linked_payment_method(
    payment_id CHAR(36) REFERENCES Payment(id) NOT NULL,
    method_id CHAR(36) REFERENCES PaymentMethod(id) NOT NULL,
    PRIMARY KEY(payment_id, method_id)
);

CREATE TABLE Product(
    id CHAR(36) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    barcode VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE Linked_product(
    payment_id REFERENCES Payment(id) NOT NULL,
    product_id REFERENCES Product(id) NOT NULL,
    price REAL NOT NULL,
    tax_percentage REAL,
    amount INT,
    mass REAL,
    volume REAL,
    PRIMARY KEY(payment_id, product_id),
);

CREATE TABLE Generic_reference(
    payment_id CHAR(36) REFERENCES Payment(id) NOT NULL,
    ref_num VARCHAR(255),
    message VARCHAR(255),
    PRIMARY KEY(payment_id)
);

CREATE TABLE OP_reference(
    payment_id CHAR(36) REFERENCES GenericReference(payment_id) NOT NULL,
    archival_id CHAR(??),
    PRIMARY KEY(payment_id)
);

CREATE TABLE Nordea_reference(
    payment_id CHAR(36) REFERENCES GenericReference(payment_id) NOT NULL,
    ref_num_payer VARCHAR(255),
    PRIMARY KEY(payment_id)
);

CREATE TABLE Tax(
    payment_id CHAR(36) REFERENCES Payment(id) NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount REAL,
    PRIMARY KEY(payment_id, description)
);