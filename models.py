from database import Database

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db = Database("tournament.db")
        db.add_user(self.username, self.password)
        db.close()

    @staticmethod
    def get_user_by_username(username):
        db = Database("tournament.db")
        user_data = db.get_user_by_username(username)
        db.close()
        if user_data:
            return User(user_data[1], user_data[2])
        return None

class Tournament:
    def __init__(self, tournament_name, start_date, end_date):
        self.tournament_name = tournament_name
        self.start_date = start_date
        self.end_date = end_date

    def save(self):
        db = Database("tournament.db")
        db.add_tournament(self.tournament_name, self.start_date, self.end_date)
        db.close()

    @staticmethod
    def get_tournament_by_name(tournament_name):
        db = Database("tournament.db")
        tournament_data = db.get_tournament_by_name(tournament_name)
        db.close()
        if tournament_data:
            return Tournament(tournament_data[1], tournament_data[2], tournament_data[3])
        return None
        
class Participant:
    def __init__(self, tournament_id, participant_name, score=0):
        self.tournament_id = tournament_id
        self.participant_name = participant_name
        self.score = score

    def save(self):
        db = Database("tournament.db")
        db.add_participant(self.tournament_id, self.participant_name, self.score)
        db.close()

    @staticmethod
    def get_participants_by_tournament(tournament_id):
        db = Database("tournament.db")
        participants_data = db.get_participants_by_tournament(tournament_id)
        db.close()
        participants = []
        for participant_data in participants_data:
            participants.append(Participant(participant_data[1], participant_data[2], participant_data[3]))
        return participants

    def update_score(self, new_score):
        self.score = new_score
        db = Database("tournament.db")
        db.update_participant_score(self.tournament_id, self.score)
        db.close()
