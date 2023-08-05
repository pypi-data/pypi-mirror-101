import mysql.connector

# Tables 
# tables = dict()
# tables["User"] = """
#     CREATE TABLE User (
#         userId int auto_increment unique not null,
#         username varchar(100) not null,
#         name varchar(50) not null,
#         password varchar (100) not null,
#         email varchar(100) unique not null,
#         PRIMARY KEY(userId)
#     );
# """

# #Dummy Data 
# dummy_data = dict()
# dummy_data["User"] = """
#     INSERT INTO User(username, name, password, email)
#     VALUES('robin', 'Robin', 'abc', 'wafturerobin.dev@gmail.com');
# """

# db = BinMySQL("localhost", 8889, "root", "root", "SGP_User", tables, dummy_data)

# ================= EXECUTION Examples =================
# db.select_one("SELECT * FROM User")
# db.select_all("SELECT * FROM User")
# db.select_one_parameters("SELECT * FROM User WHERE userId = %s", (1,))
# db.select_all_parameters("SELECT * FROM User WHERE username = %s", ("robin",))
# db.execute("INSERT INTO User(username, name, password, email) VALUES('robin', 'Robin', 'abc', 'wafturerobin.dev@gmail.com')")
# db.execute_parameters("INSERT INTO Property(username, name, password, email) VALUES (%s, %s, %s, %s)", ('robin', 'Robin', 'abc', 'wafturerobin.dev@gmail.com'))

class BinMySQL:
    def __init__(self, db_host, db_port, db_user, db_password, db_database, tables=dict(), dummy_data=dict()):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_database = db_database
        self.tables = tables
        self.dummy_data = dummy_data

        if self.checkDBRequirements(tables) == False:
            raise ValueError(f'[{__name__}] Unable to setup Database..')

    # Get cursor
    def getDBConnection(self):
        if self.db_port != None:
            return mysql.connector.connect(host=self.db_host, port= self.db_port, user= self.db_user, password=self.db_password, database=self.db_database)
        return mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_database)
    
    def checkDBRequirements(self, tables):
        if self.db_port != None:
            self.conn = mysql.connector.connect(host=self.db_host, port= self.db_port, user= self.db_user, password=self.db_password)
        else:
            self.conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_password)
        if(self.hasDatabase(self.conn, self.db_database)):
            mycursor = self.conn.cursor()
            mycursor.execute("USE " + self.db_database)
            
            if self.hasTables(self.conn, tables) == True:
                return True

        return False

    # Database Setup
    def hasDatabase(self, conn, database):
        if self._hasDatabase(conn, database) == False:
            #Database not found, attempt to create
            print("Database not found, attempt to create...")
            mycursor = conn.cursor()
            mycursor.execute("CREATE DATABASE " + database)

        if self._hasDatabase(conn, database):
            print("DATABASE: " + database + " (ACTIVE)")
            return True
        return False
        
    def _hasDatabase(self, conn, database):
        #Try to obtain databse
        mycursor = conn.cursor()

        mycursor.execute("SHOW DATABASES")
        result = mycursor.fetchall()

        for db in result:
            if(database.lower() == db[0].lower()):
                return True
        return False

    # Tables
    def hasTables(self, conn, tables):
        for table in tables:
            createTable = self._hasTable(conn, table) == False
            if createTable:
                #Database not found, attempt to create
                print(f"Table '{table}' not found, attempt to create...")
                mycursor = conn.cursor()
                query = tables[table]
                
                mycursor.execute(query)

            if self._hasTable(conn, table):
                if createTable == True:
                    if table in self.dummy_data.keys():
                        print(f"Loading dummy data for {table}")
                        self._loadDummyData(self.conn, self.dummy_data[table])
                print(f"[{__name__}] Table '{table}' (ACTIVE)")
            else:
                print("An error has occurred, unable to create TABLE: " + table)
                return False
        return True

    def _hasTable(self, conn, table):
        #Try to obtain table
        mycursor = conn.cursor()

        mycursor.execute("SHOW TABLES")
        result = mycursor.fetchall()

        for t in result:
            if(table.lower() == t[0].lower()):
                return True
        return False

    def _loadDummyData(self, conn, dummyData):
        mycursor = conn.cursor()
        try:
            mycursor.execute(dummyData)
            conn.commit()
        except Exception as e:
            print(f"Error unable to insert dummy data for ({self.db_database}): ({str(e)})")

    #Functions
    def select_one(self, query):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query)

                result = cursor.fetchone()
                if result != None:
                    columns = cursor.description 
                    return {columns[index][0]:column for index, column in enumerate(result)}
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return None
        return None

    def select_one_params(self, query, params):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query, params)

                result = cursor.fetchone()
                if result != None:
                    columns = cursor.description 
                    return {columns[index][0]:column for index, column in enumerate(result)}
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return None
        return None

    def select_all(self, query):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query)

                columns = cursor.description 
                return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return None
        return None

    def select_all_parameters(self, query, params):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query, params)

                columns = cursor.description 
                return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return None
        return None
        
    def execute(self, query):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return False
        return False

    def execute_parameters(self, query, params):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return False
        return False

    def insert(self, query):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()

                cursor.execute('SELECT last_insert_id()')
                result = cursor.fetchone()
                if result != None:
                    return result[0]
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return None
        return None

    def insert_parameters(self, query, params):
        try:
            conn = self.getDBConnection()
            if conn != None:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()

                cursor.execute('SELECT last_insert_id()')
                result = cursor.fetchone()
                if result != None:
                    return result[0]
        except Exception as e:
            print(f"DB Error occurred ({self.db_database}): {str(e)}")
            return None
        return None
