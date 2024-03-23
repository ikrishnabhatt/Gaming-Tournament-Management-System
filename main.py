import sqlite3
import hashlib
from getpass import getpass

# Database connection
conn = sqlite3.connect('tournament.db')
c = conn.cursor()

# Create tables if they don't exist
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
                participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                participant_name TEXT,
                score INTEGER,
                FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id))''')

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
    print("8. View Participants")
    print("5. Remove Participant")
    print("4. Update Participant Score")
    print("7. View Results")
    print("6. Record Result")
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
    participant1_id = int(input("Enter participant 1 ID: "))
    participant2_id = int(input("Enter participant 2 ID: "))
    participant1_score = int(input("Enter participant 1 score: "))
    participant2_score = int(input("Enter participant 2 score: "))
    
    # Update scores for participant 1
    c.execute("UPDATE Participants SET score = score + ? WHERE participant_id = ?", (participant1_score, participant1_id))
    
    # Update scores for participant 2
    c.execute("UPDATE Participants SET score = score + ? WHERE participant_id = ?", (participant2_score, participant2_id))
    
    # Add match details to a new table or log file, if required
    
    conn.commit()
    print("Result recorded successfully!")


def view_results():
    print("\n===== View Results =====")
    tournament_id = int(input("Enter tournament ID: "))
    
    # Fetch match results for the specified tournament
    c.execute("SELECT * FROM MatchResults WHERE tournament_id = ?", (tournament_id,))
    results = c.fetchall()
    
    if results:
        print("Match Results:")
        for result in results:
            print(f"Participant 1 ID: {result[1]}, Participant 2 ID: {result[2]}, Participant 1 Score: {result[3]}, Participant 2 Score: {result[4]}")
    else:
        print("No match results found for this tournament.")

# Main program
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
                    record_result()
                elif choice == '7':
                    view_results()
                elif choice == '8':
                    update_score()
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
