from getpass import getpass
from database import Database
from utils import validate_username, validate_password

def register_user():
    print("\n===== Register =====")
    while True:
        username = input("Enter username: ")
        if not validate_username(username):
            print("Invalid username! Username must be between 4 and 20 characters long and contain only alphanumeric characters and underscores.")
            continue
        break

    while True:
        password = getpass("Enter password: ")
        if not validate_password(password):
            print("Invalid password! Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
            continue
        break

    db = Database()
    user_exists = db.get_user_by_username(username)
    if user_exists:
        print("Username already exists!")
        return

    db.add_user(username, password)
    print("Registration successful!")

def login_user():
    print("\n===== Login =====")
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    db = Database()
    user = db.get_user_by_username(username)
    if user and user[2] == password:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password!")
        return False

def create_tournament():
    print("\n===== Create Tournament =====")
    tournament_name = input("Enter tournament name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    db = Database()
    tournament_exists = db.get_tournament_by_name(tournament_name)
    if tournament_exists:
        print("Tournament with that name already exists!")
        return

    db.add_tournament(tournament_name, start_date, end_date)
    print("Tournament created successfully!")

def view_tournaments():
    print("\n===== View Tournaments =====")
    db = Database()
    tournaments = db.get_all_tournaments()
    if tournaments:
        print("Tournament ID | Name | Start Date | End Date")
        for tournament in tournaments:
            print(tournament)
    else:
        print("No tournaments found.")

def add_participant():
    print("\n===== Add Participant =====")
    tournament_name = input("Enter tournament name: ")
    participant_name = input("Enter participant name: ")
    team_name = input("Enter team name: ")
    age = input("Enter participant age: ")

    db = Database()
    tournament = db.get_tournament_by_name(tournament_name)
    if not tournament:
        print("Tournament not found!")
        return

    db.add_participant(tournament[0], participant_name, team_name, age)
    print("Participant added successfully!")

def remove_participant():
    print("\n===== Remove Participant =====")
    participant_name = input("Enter participant name: ")
    db = Database()
    db.remove_participant(participant_name)
    print("Participant removed successfully!")

def remove_tournament():
    print("\n===== Remove Tournament =====")
    tournament_name = input("Enter tournament name: ")
    db = Database()
    db.remove_tournament(tournament_name)
    print("Tournament removed successfully!")

def view_participants():
    print("\n===== View Participants =====")
    tournament_name = input("Enter tournament name: ")
    db = Database()
    tournament = db.get_tournament_by_name(tournament_name)
    if not tournament:
        print("Tournament not found!")
        return

    participants = db.get_participants_by_tournament(tournament[0])
    if participants:
        print("Participant ID | Tournament ID | Team Name | Participant Name | Age | Points")
        for participant in participants:
            print(participant)
    else:
        print("No participants found for this tournament.")

def calculate_points():
    print("\n===== Assign Points =====")
    participant_name = input("Enter participant name: ")
    points = int(input("Enter points for the participant: "))

    db = Database()
    db.assign_points(participant_name, points)
    print(f"Points assigned for {participant_name}: {points}")


def announce_winners():
    print("\n===== Announce Winners =====")
    tournament_name = input("Enter tournament name: ")
    db = Database()
    tournament = db.get_tournament_by_name(tournament_name)
    if not tournament:
        print("Tournament not found!")
        return

    winners = db.announce_winners(tournament[0])
    if winners:
        print("Winners:")
        for i, winner in enumerate(winners, start=1):
            print(f"{i}. Name: {winner[3]}, Points {winner[5]}")
    else:
        print("No winners found for this tournament!")

def show_menu():
    while True:
        print("\n===== Menu =====")
        print("1. Create Tournament")
        print("2. View Tournaments")
        print("3. Remove Tournament")
        print("4. Add Participant")
        print("5. View Participants")
        print("6. Remove Participant")
        print("7. Calculate Points")
        print("8. Announce Winners")
        print("9. Logout")

        option = input("Enter your option: ")

        if option == '1':
            create_tournament()
        elif option == '2':
            view_tournaments()
        elif option == '3':
            remove_tournament()
        elif option == '4':
            add_participant()
        elif option == '5':
            view_participants()
        elif option == '6':
            remove_participant()
        elif option == '7':
            calculate_points()
        elif option == '8':
            announce_winners()
        elif option == '9':
            print("Logging out...")
            break
        else:
            print("Invalid option!")

def main():
    while True:
        print("\n===== Game Tournament Management System =====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        option = input("Enter your option: ")

        if option == '1':
            if login_user():
                show_menu()
        elif option == '2':
            register_user()
        elif option == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
