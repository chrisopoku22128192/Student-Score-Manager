import mysql.connector
import matplotlib.pyplot as plt

class ScoreManager:
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

    def add_score(self, student, subject, score, ):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return False

        student = student.strip().lower()  # Normalize student name
        subject = subject.strip().lower()  # Normalize subject name

        try:
            # Get student ID
            self.cursor.execute("SELECT id FROM students WHERE LOWER(name) = %s", (student,))
            student_id = self.cursor.fetchone()
            if not student_id:
                print("Error: Student not found!")
                return False

            # Get subject ID
            self.cursor.execute("SELECT id FROM subjects WHERE LOWER(name) = %s", (subject,))
            subject_id = self.cursor.fetchone()
            if not subject_id:
                print("Error: Subject not found!")
                return False

            # Insert score
            self.cursor.execute(
                "INSERT INTO scores (student_id, subject_id, score) VALUES (%s, %s, %s)",
                (student_id[0], subject_id[0], score)
            )
            self.conn.commit()
            print(f"Score added: {student} - {subject} : {score}")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def view_scores(self):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return

        try:
            self.cursor.execute("""
                SELECT students.name, subjects.name, scores.score
                FROM scores
                JOIN students ON scores.student_id = students.id
                JOIN subjects ON scores.subject_id = subjects.id
            """)
            for row in self.cursor.fetchall():
                print(f"Student: {row[0]}, Subject: {row[1]}, Score: {row[2]}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def calculate_statistics(self, subject):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return None

        subject = subject.strip().lower()  # Normalize subject name

        try:
            # Get subject ID
            self.cursor.execute("SELECT id FROM subjects WHERE LOWER(name) = %s", (subject,))
            subject_id = self.cursor.fetchone()
            if not subject_id:
                print("Error: Subject not found!")
                return None

            # Retrieve scores
            self.cursor.execute("SELECT score FROM scores WHERE subject_id = %s", (subject_id[0],))
            scores = [row[0] for row in self.cursor.fetchall()]
            if scores:
                mean = sum(scores) / len(scores)
                median = sorted(scores)[len(scores) // 2]
                mode = max(set(scores), key=scores.count)
                std_dev = (sum((x - mean) ** 2 for x in scores) / len(scores)) ** 0.5
                return mean, median, mode, std_dev
            else:
                print("No scores available for this subject.")
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def visualize_scores(self, subject):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return

        subject = subject.strip().lower()  # Normalize subject name

        try:
            # Get subject ID
            self.cursor.execute("SELECT id FROM subjects WHERE LOWER(name) = %s", (subject,))
            subject_id = self.cursor.fetchone()
            if not subject_id:
                print("Error: Subject not found!")
                return

            # Retrieve scores
            self.cursor.execute("""
                SELECT students.name, scores.score
                FROM scores
                JOIN students ON scores.student_id = students.id
                WHERE scores.subject_id = %s
            """, (subject_id[0],))
            data = self.cursor.fetchall()
            if data:
                students, scores = zip(*data)
                plt.bar(students, scores)
                plt.xlabel('Students')
                plt.ylabel('Scores')
                plt.title(f'Scores for {subject}')
                plt.show()
            else:
                print("No scores available to visualize.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_scores(self):
        if not self.conn or not self.cursor:
            print("Database connection is not available.")
            return []

        try:
            self.cursor.execute("""
                SELECT students.name, subjects.name, scores.score
                FROM scores
                JOIN students ON scores.student_id = students.id
                JOIN subjects ON scores.subject_id = subjects.id
            """)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")