import sqlite3
from uuid import uuid4

class PaymentDatabase:
    def __init__(self, filepath):
        self.db = sqlite3.connect(filepath)
        self.cursor = self.db.cursor()

    def create_db(self):
        self.cursor.execute("""
            CREATE TABLE Beneficiary(
                id CHAR(36) NOT NULL,
                beneficiary_name VARCHAR(255) NOT NULL,
                PRIMARY KEY(id)
            );
            """)

        self.cursor.execute("""
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
            """)

        self.cursor.execute("""
            CREATE TABLE Payment_method(
                id CHAR(36) NOT NULL,
                bank VARCHAR(255),
                method VARCHAR(255),
                PRIMARY KEY(id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE Linked_payment_method(
                payment_id CHAR(36) REFERENCES Payment(id) NOT NULL,
                method_id CHAR(36) REFERENCES PaymentMethod(id) NOT NULL,
                PRIMARY KEY(payment_id, method_id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE Product(
                id CHAR(36) NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                barcode VARCHAR(255),
                PRIMARY KEY(id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE Linked_product(
                payment_id REFERENCES Payment(id) NOT NULL,
                product_id REFERENCES Product(id) NOT NULL,
                price REAL NOT NULL,
                tax_percentage REAL,
                amount INTEGER,
                mass REAL,
                volume REAL,
                PRIMARY KEY(payment_id, product_id),
            );
            """)

        self.cursor.execute("""
            CREATE TABLE Generic_reference(
                payment_id CHAR(36) REFERENCES Payment(id) NOT NULL,
                ref_num VARCHAR(255),
                message VARCHAR(255),
                PRIMARY KEY(payment_id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE OP_reference(
                payment_id CHAR(36) REFERENCES GenericReference(payment_id) NOT NULL,
                archival_id CHAR(??),
                PRIMARY KEY(payment_id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE Nordea_reference(
                payment_id CHAR(36) REFERENCES GenericReference(payment_id) NOT NULL,
                ref_num_payer VARCHAR(255),
                PRIMARY KEY(payment_id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE Tax(
                payment_id CHAR(36) REFERENCES Payment(id) NOT NULL,
                description VARCHAR(255) NOT NULL,
                amount REAL,
                PRIMARY KEY(payment_id, description)
            );
            """)
        # Convert PKs to autoincrement
        self.db.commit()

    def check_if_exists(self, table, attribute, value):
        return False

    def new_row(self, table, attribute, value, *args):
        existing_id = self.check_if_exists(table, attribute, value)

        if not existing_id:
            # Generate UUID -> check that not in table
            # Write new row based on args
            pass


    def close_db(self):
        self.db.close()
