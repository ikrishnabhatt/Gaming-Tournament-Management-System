import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
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
                            participant_name TEXT,
                            score INTEGER,
                            FOREIGN KEY (tournament_id) REFERENCES Tournaments(id)
                        )''')

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

    def add_participant(self, tournament_id, participant_name, score=0):
        self.cursor.execute("INSERT INTO Participants (tournament_id, participant_name, score) VALUES (?, ?, ?)", (tournament_id, participant_name, score))
        self.conn.commit()

    def get_participants_by_tournament(self, tournament_id):
        self.cursor.execute("SELECT * FROM Participants WHERE tournament_id=?", (tournament_id,))
        return self.cursor.fetchall()

    def update_participant_score(self, gamer_id, new_score):
        self.cursor.execute("UPDATE Participants SET score=? WHERE gamer_id=?", (new_score, gamer_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
