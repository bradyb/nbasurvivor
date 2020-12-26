import csv
from datetime import datetime
from datetime import timedelta

DATE_INDEX = 0
TEAM_1_INDEX = 4
TEAM_2_INDEX = 5
TEAM_1_PROB = 20
TEAM_2_PROB = 21

AVAILABLE_TEAMS = []
with open('teams.txt', 'r') as available_teams_file:
    available_teams_file_lines = available_teams_file.readlines()
    AVAILABLE_TEAMS = [team.strip() for team in available_teams_file_lines]

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

def find_best_remaining_plan(weeks, week_index, available_teams, current_plan, current_record):
    if len(available_teams) == 0:
        return Plan(current_plan, current_record)
    if week_index == len(weeks):
        return Plan(current_plan, current_record)
    week = weeks[week_index]
    teams_playing_this_week = week.get_teams_playing_this_week()
    options_for_remaining_weeks = []
    for team in available_teams:
        if team not in teams_playing_this_week:
            continue
        remaining_teams = available_teams.copy()
        remaining_teams.remove(team)
        wins, games = week.get_team_stats(team)
        new_record = Record(current_record.wins + wins, current_record.games + games)
        options_for_remaining_weeks.append(
            find_best_remaining_plan(weeks, week_index + 1, remaining_teams, current_plan + [team], new_record))
    best_plan = options_for_remaining_weeks[0]
    best_record = best_plan.record.wins / best_plan.record.games
    for option in options_for_remaining_weeks:
        record = option.record
        if record.wins / record.games > best_record:
            best_plan = option
            best_record = record.wins / record.games
    return best_plan

games = open('nba_predictions_2020_12_21.csv', newline='')
game_reader = csv.reader(games)
current_week = Week(datetime.strptime('2020-12-21', '%Y-%m-%d'))
weeks = []
last_week = None
for game_line in game_reader:
    game = Game(game_line[DATE_INDEX], game_line[TEAM_1_INDEX], game_line[TEAM_2_INDEX], game_line[TEAM_1_PROB], game_line[TEAM_2_PROB])
    if game.date <= current_week.get_end_of_week():
        current_week.add_game(game)
    else:
        weeks.append(current_week)
        current_week = Week(current_week.get_start_of_next_week())
        last_week = current_week
weeks.append(last_week)

best_plan = find_best_remaining_plan(weeks, 0, AVAILABLE_TEAMS, [], Record(0.0, 0))
print(best_plan.plan)
print(best_plan.record.wins, best_plan.record.games)