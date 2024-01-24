import sqlite3

class DbOperation:
    def connect_to_db(self):
        conn = sqlite3.connect('password_records.db')
        return conn

    def create_table(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            website TEXT NOT NULL,
            username VARCHAR(200),
            password VARCHAR(50)
        );
        '''

        with conn:
            cursor = conn.cursor()
            cursor.execute(query)

    def create_record(self, data, table_name="password_info"):
        website = data['website']
        username = data['username']
        password = data['password']
        conn = self.connect_to_db()
        query = f'''
        INSERT INTO {table_name}('website','username','password')
        VALUES (?,?,?);
        '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username, password))

    def show_records(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name};
        '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(query)
            list_records = cursor.fetchall()
            return list_records

    def update_record(self, data, table_name="password_info"):
        ID = data['ID']
        website = data['website']
        username = data['username']
        password = data['password']
        conn = self.connect_to_db()
        query = f'''
        UPDATE {table_name} SET website=?,username=?,password=?
        WHERE ID=?;
        '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username, password, ID))

    def delete_record(self, ID, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        DELETE FROM {table_name} WHERE ID=?;
        '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (ID,))

    def search_records(self, keyword, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name}
        WHERE website LIKE ? OR username LIKE ? OR password LIKE ?;
        '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            list_records = cursor.fetchall()
            return list_records
        
    def get_record_by_website_username(self, website, username, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name}
        WHERE website = ? AND username = ?;
        '''
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, (website, username))
            record = cursor.fetchone()
            return record


# Usage example:
if __name__ == "__main__":
    db_class = DbOperation()
    db_class.create_table()
