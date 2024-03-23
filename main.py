import sqlite3
import hashlib
from getpass import getpass

conn = sqlite3.connect('tournament.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Tournaments (
                tournament_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_name TEXT,
                start_date TEXT,
                end_date TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Participants (
                gamer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                participant_name TEXT,
                score INTEGER,
                FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS MatchResults (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                participant1_id INTEGER,
                participant2_id INTEGER,
                participant1_score INTEGER,
                participant2_score INTEGER,
                FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id),
                FOREIGN KEY (participant1_id) REFERENCES Participants(gamer_id),
                FOREIGN KEY (participant2_id) REFERENCES Participants(gamer_id))''')

conn.commit()

def register():
    print("===== Register =====")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists!")

def login():
    print("===== Login =====")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    if user:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False

def menu():
    print("\n===== Menu =====")
    print("1. Create Tournament")
    print("2. View Tournaments")
    print("3. Add Participant")
    print("4. View Participants")
    print("5. Remove Participant")
    print("6. Update Participant Score")
    print("7. Record Result")
    print("8. View Results")
    print("9. Logout")
    choice = input("Enter your choice: ")
    return choice

def create_tournament():
    print("\n===== Create Tournament =====")
    tournament_name = input("Enter tournament name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    c.execute("INSERT INTO Tournaments (tournament_name, start_date, end_date) VALUES (?, ?, ?)", (tournament_name, start_date, end_date))
    conn.commit()
    print("Tournament created successfully!")

def view_tournaments():
    print("\n===== View Tournaments =====")
    c.execute("SELECT * FROM Tournaments")
    tournaments = c.fetchall()
    print("\n ID, Name , Starting Date ,Ending Date \n")
    if tournaments:
        for tournament in tournaments:
            print(tournament)
    else:
        print("No tournaments found.")

def add_participant():
    print("\n===== Add Participant =====")
    tournament_id = int(input("Enter tournament ID: "))
    participant_name = input("Enter participant name: ")
    c.execute("INSERT INTO Participants (tournament_id, participant_name, score) VALUES (?, ?, 0)", (tournament_id, participant_name))
    conn.commit()
    print("Participant added successfully!")

def view_participants():  
    print("\n===== View Participants =====")
    tournament_id = int(input("Enter tournament ID: "))
    print("\PlayerID, GameID, Name , Score \n")
    c.execute("SELECT * FROM Participants WHERE tournament_id = ?", (tournament_id,))
    participants = c.fetchall()
    if participants:
        for participant in participants:
            print(participant)
    else:
        print("No participants found for this tournament.")

def remove_participant():
    print("\n===== Remove Participant =====")
    participant_id = int(input("Enter participant ID: "))
    c.execute("DELETE FROM Participants WHERE participant_id = ?", (participant_id,))
    conn.commit()
    print("Participant removed successfully!")

def update_score():
    print("\n===== Update Participant Score =====")
    participant_id = int(input("Enter participant ID: "))
    score = int(input("Enter new score: "))
    c.execute("UPDATE Participants SET score = ? WHERE participant_id = ?", (score, participant_id))
    conn.commit()
    print("Score updated successfully!")

def record_result():
    print("\n===== Record Result =====")
    tournament_id = int(input("Enter tournament ID: "))
    num_participants = int(input("Enter the number of participants in the match: "))

    match_data = []
    for i in range(num_participants):
        participant_id = int(input(f"Enter participant {i+1} ID: "))
        participant_score = int(input(f"Enter participant {i+1} score: "))
        match_data.append((tournament_id, participant_id, participant_score))
    c.executemany("INSERT INTO MatchResults (tournament_id, participant1_id, participant1_score) VALUES (?, ?, ?)", match_data)
    conn.commit()
    print("Result recorded successfully!")


def view_results():
    print("\n===== View Results =====")
    tournament_id = int(input("Enter tournament ID: "))
    
    c.execute("SELECT * FROM MatchResults WHERE tournament_id = ?", (tournament_id,))
    results = c.fetchall()
    
    if results:
        print("Match Results:")
        for result in results:
            print(f"Match ID: {result[0]}")
            print("Participants:")
            for i in range(1, len(result), 3):  
                if i + 2 < len(result): 
                    print(f"Participant ID: {result[i]}, Score: {result[i+1]}")
                else:
                    print("Incomplete participant data in the database.")
                    break
    else:
        print("No match results found for this tournament.")

while True:
    print("\n===== Game Tournament Management System =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    option = input("Enter your option: ")

    if option == '1':
        register()
    elif option == '2':
        if login():
            while True:
                choice = menu()
                if choice == '1':
                    create_tournament()
                elif choice == '2':
                    view_tournaments()
                elif choice == '3':
                    add_participant()
                elif choice == '4':
                    view_participants()
                elif choice == '5':
                    remove_participant()
                elif choice == '6':
                    update_score()
                elif choice == '7':
                    record_result()
                elif choice == '8':
                    view_results()
                elif choice == '9':
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice!")
    elif option == '3':
        print("Exiting...")
        break
    else:
        print("Invalid option!")
