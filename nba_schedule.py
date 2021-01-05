from datetime import datetime
from datetime import timedelta
import operator

class Record():
    def __init__(self, wins, games):
        self.wins = wins
        self.games = games
    
    def add_wins(self, wins):
        self.wins += wins

    def add_games(self, games):
        self.games += games

class Plan():
    def __init__(self, plan, record):
        self.plan = plan
        self.record = record

class Game():
    def __init__(self, date, team_1, team_2, team_1_prob, team_2_prob):
        self.date =  datetime.strptime(date, '%Y-%m-%d').date()
        self.team_1 = team_1
        self.team_2 = team_2
        self.team_1_prob = float(team_1_prob)
        self.team_2_prob = float(team_2_prob)


class Week():
    def __init__(self, week_start):
        self.games = [] # Sequence[Game]
        self.week_start = week_start
    
    def add_game(self, game: Game):
        self.games.append(game)

    def get_team_stats(self, team):
        week_score = 0.0
        games_played = 0
        for game in self.games:
            if team == game.team_1:
                week_score += game.team_1_prob
                games_played+=1
            elif team == game.team_2:
                week_score += game.team_2_prob
                games_played+=1
        return week_score, games_played

    def get_teams_playing_this_week(self):
        teams_playing_this_week = []
        for game in self.games:
            if game.team_1 not in teams_playing_this_week:
                teams_playing_this_week.append(game.team_1)
            elif game.team_2 not in teams_playing_this_week:
                teams_playing_this_week.append(game.team_2)
        return teams_playing_this_week

    def get_end_of_week(self):
        end_of_week = self.week_start + timedelta(days=6)
        return end_of_week.date()

    def get_start_of_next_week(self):
        start_of_next_week = self.week_start + timedelta(days=7)
        return start_of_next_week

    def get_all_team_stats(self):
        scores_by_team = {}
        teams_playing_this_week = self.get_teams_playing_this_week()

        for team in teams_playing_this_week:
            scores_by_team[team] = self.get_team_stats(team)

        return scores_by_team

    def get_best_team_of_week(self):        
        return max(self.get_all_team_stats().items(), key=operator.itemgetter(1))
