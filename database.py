import sqlite3

class Database:
    def __init__(self, db_name="game.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password TEXT
                        )''')

        # Tournaments table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Tournaments (
                            id INTEGER PRIMARY KEY,
                            tournament_name TEXT UNIQUE,
                            start_date TEXT,
                            end_date TEXT
                        )''')

        # Participants table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Participants (
                            id INTEGER PRIMARY KEY,
                            tournament_id INTEGER,
                            team_name TEXT,
                            participant_name TEXT,
                            age INTEGER,
                            points INTEGER,
                            FOREIGN KEY (tournament_id) REFERENCES Tournaments(id)
                        )''')

        # Check and create missing columns
        self.add_missing_columns()

    def add_missing_columns(self):
        # Check and create missing columns in the Users table
        self.cursor.execute('''PRAGMA table_info(Users)''')
        columns = self.cursor.fetchall()
        existing_columns = [column[1] for column in columns]  # Extract existing column names
        if 'username' not in existing_columns:
            self.cursor.execute('''ALTER TABLE Users ADD COLUMN username TEXT UNIQUE''')
        if 'password' not in existing_columns:
            self.cursor.execute('''ALTER TABLE Users ADD COLUMN password TEXT''')

        # Check and create missing columns in the Participants table
        self.cursor.execute('''PRAGMA table_info(Participants)''')
        columns = self.cursor.fetchall()
        existing_columns = [column[1] for column in columns]  # Extract existing column names
        if 'age' not in existing_columns:
            self.cursor.execute('''ALTER TABLE Participants ADD COLUMN age INTEGER''')
        if 'points' not in existing_columns:
            self.cursor.execute('''ALTER TABLE Participants ADD COLUMN points INTEGER DEFAULT 0''')

        self.conn.commit()

    def add_user(self, username, password):
        self.cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def add_tournament(self, tournament_name, start_date, end_date):
        self.cursor.execute("INSERT INTO Tournaments (tournament_name, start_date, end_date) VALUES (?, ?, ?)", (tournament_name, start_date, end_date))
        self.conn.commit()

    def get_tournament_by_name(self, tournament_name):
        self.cursor.execute("SELECT * FROM Tournaments WHERE tournament_name=?", (tournament_name,))
        return self.cursor.fetchone()

    def remove_tournament(self, tournament_name):
        self.cursor.execute("DELETE FROM Tournaments WHERE tournament_name=?", (tournament_name,))
        self.conn.commit()

    def add_participant(self, tournament_id, participant_name, team_name, age):
        self.cursor.execute("INSERT INTO Participants (tournament_id, participant_name, team_name, age) VALUES (?, ?, ?, ?)", (tournament_id, participant_name, team_name, age))
        self.conn.commit()

    def remove_participant(self, participant_name):
        self.cursor.execute("DELETE FROM Participants WHERE participant_name=?", (participant_name,))
        self.conn.commit()

    def get_participants_by_tournament(self, tournament_id):
        self.cursor.execute("SELECT * FROM Participants WHERE tournament_id=?", (tournament_id,))
        return self.cursor.fetchall()

    def calculate_points(self, participant_name):
        self.cursor.execute("SELECT points FROM Participants WHERE participant_name=?", (participant_name,))
        return self.cursor.fetchone()

    def announce_winners(self, tournament_id):
        self.cursor.execute("SELECT * FROM Participants WHERE tournament_id=? ORDER BY points DESC LIMIT 3", (tournament_id,))
        return self.cursor.fetchall()

    def get_all_tournaments(self):
        self.cursor.execute("SELECT * FROM Tournaments")
        return self.cursor.fetchall()

    def assign_points(self, participant_name, points):
        self.cursor.execute("UPDATE participants SET points=? WHERE participant_name=?", (points, participant_name))
        self.conn.commit()
