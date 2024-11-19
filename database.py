import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('ecommerce.db')
        self.cursor = self.conn.cursor()

    def CreateTableBuyer(self):
        self.cursor.execute('''
        CREATE TABLE Buyer(
        buyer_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        b_id        INTEGER,
        b_name       varchar (25),
        b_email      VARCHAR (30),
        b_password     VARCHAR (30)
        )
        ''')
        self.conn.commit()

    def insertIntoBuyer(self,  b_id, b_name, b_email, b_password):
        self.cursor.execute(
            f"INSERT INTO Buyer(buyer_id, b_id, b_name, b_email, b_password) VALUES (NULL, '{b_id}', '{b_name}', '{b_email}', '{b_password}')")
        self.conn.commit()

    def returnBuyer(self):
        self.cursor.execute("SELECT * FROM Buyer")
        items = self.cursor.fetchall()
        return items

    def deleteBuyer(self, b_id):
        self.cursor.execute(f"DELETE FROM Buyer WHERE b_id = '{b_id}'")
        self.conn.commit()

    def deleteBuyertable(self):
        self.cursor.execute("DROP TABLE Buyer")

    def CreateTableSeller(self):
        self.cursor.execute('''
        CREATE TABLE Seller(
        seller_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        s_id    INTEGER,
        s_name       varchar (25),
        s_email      VARCHAR (30),
        s_password     VARCHAR (30)
        )
        ''')
        self.conn.commit()

    def insertIntoSeller(self,s_id,s_name,s_email,s_password):
        #self.cursor.execute(f"INSERT INTO Seller(seller_id,s_id,s_name,s_email,s_password) VALUES (NULL,'{s_id}','{s_name}','{s_email}','{s_password}')")
        self.cursor.execute(f"INSERT INTO Seller(seller_id,s_id,s_name,s_email,s_password) VALUES (NULL,'{s_id}',\"{s_name}\",'{s_email}','{s_password}')")


        self.conn.commit()



    def returnSeller(self):
        self.cursor.execute("SELECT * FROM Seller")
        items = self.cursor.fetchall()
        return items

    def deleteSeller(self, s_id):
        self.cursor.execute(f"DELETE FROM Seller WHERE s_id = '{s_id}'")
        self.conn.commit()

    def deleteSellertable(self):
        self.cursor.execute("DROP TABLE Seller")

    def CreateTableItem(self):
        self.cursor.execute('''
            CREATE TABLE Item (
                item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                item_index INTEGER,
                product_name TEXT,
                retail_price REAL,
                discounted_price REAL,
                image TEXT,
                description TEXT,
                product_rating REAL,
                brand TEXT,
                buyer_id INTEGER,
                i_id INTEGER,
                seller_id INTEGER,
                FOREIGN KEY(buyer_id) REFERENCES Buyer(buyer_id),
                FOREIGN KEY(seller_id) REFERENCES Seller(seller_id)
            )
        ''')
        self.conn.commit()

    def insertIntoItem(self, item_index, product_name, retail_price, discounted_price, image, description,
                       product_rating, brand, buyer_id, i_id, seller_id):
        query = """
            INSERT INTO Item(item_id,item_index,product_name, retail_price, discounted_price, image, description, product_rating, brand, buyer_id,i_id,seller_id) 
            VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)
        """
        self.cursor.execute(query, (
            item_index,
            product_name,
            retail_price,
            discounted_price,
            image,
            description,
            product_rating,
            brand,
            buyer_id,
            i_id,
            seller_id
        ))
        self.conn.commit()

    # def CreateTableItem(self):
    #     self.cursor.execute('''
    #         CREATE TABLE Item (
    #             item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    #             item_index INTEGER,
    #             product_name TEXT,
    #             retail_price REAL,
    #             discounted_price REAL,
    #             image TEXT,
    #             description TEXT,
    #             product_rating REAL,
    #             brand TEXT,
    #             buyer_id INTEGER,
    #             i_id INTEGER,
    #             seller_id INTEGER,
    #             FOREIGN KEY(buyer_id) REFERENCES Buyer(buyer_id),
    #             FOREIGN KEY(seller_id) REFERENCES Seller(seller_id)
    #         )
    #     ''')
    #
    #     self.conn.commit()
    #
    #
    # def insertIntoItem(self,item_index,product_name,retail_price,discounted_price,image,description,product_rating,brand,buyer_id,i_id,seller_id):
    #
    #     self.cursor.execute(f"INSERT INTO Item(item_id,item_index,product_name, retail_price, discounted_price, image, description, product_rating, brand, buyer_id,i_id,seller_id) VALUES (NULL,'{item_index}','{product_name}', {retail_price}, {discounted_price}, '{image}', '{description}', {product_rating}, '{brand}', '{buyer_id}', '{i_id}', '{seller_id}')")
    #
    #     self.conn.commit()

    def returnItem(self):
        self.cursor.execute("SELECT * FROM Item")
        items = self.cursor.fetchall()
        return items

    def deleteItem(self, index):
        self.cursor.execute(f"DELETE FROM Item WHERE s_id = '{index}'")
        self.conn.commit()

    def deleteItemtable(self):
        self.cursor.execute("DROP TABLE Item")

    #COALESCE('{buyer_id}', NULL)