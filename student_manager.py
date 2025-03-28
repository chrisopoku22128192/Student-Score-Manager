import mysql.connector

class StudentManager:
    def __init__(self, host="localhost", user="root", password="", database="student_management"):
        try:
            # Initialize the MySQL connection
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()  # Create a cursor object for executing queries
            print("Connected to the database successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn = None
            self.cursor = None

    def register_student(self, name):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return

        try:
            self.cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
            self.conn.commit()
            print(f"Student '{name}' registered successfully!")
        except mysql.connector.IntegrityError:
            print("Student already exists!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def register_subject(self, name):
        print(f"Registering subject: '{name}'")  # Debugging line
        name = name.strip().lower()  # Normalize subject name
        try:
            self.cursor.execute("INSERT INTO subjects (name) VALUES (%s)", (name,))
            self.conn.commit()
            print(f"Subject '{name}' registered successfully!")
        except mysql.connector.IntegrityError:
            print("Subject already exists!")

    def get_students(self):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return []

        try:
            self.cursor.execute("SELECT name FROM students")
            return [row[0] for row in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_subjects(self):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return []

        try:
            self.cursor.execute("SELECT name FROM subjects")
            return [row[0] for row in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")