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

def create_plan_hash(plan):
    return ','.join(sorted(plan))

plan_memo = {}

def find_best_remaining_plan_helper(weeks, week_index, team, available_teams):
    if len(available_teams) == 1:
        wins_this_week, games_this_week = weeks[week_index].get_team_stats(team)
        return Plan([team], Record(wins_this_week, games_this_week))
    week = weeks[week_index]
    teams_playing_this_week = week.get_teams_playing_this_week()
    options_for_remaining_weeks = []
    print(team, available_teams)
    remaining_teams = available_teams.copy()
    remaining_teams.remove(team)        
    team_wins, team_games_played = week.get_team_stats(team)

    plan_hash = create_plan_hash(remaining_teams)
    if plan_hash in plan_memo:
        best_plan = plan_memo[plan_hash]
    else:
        for next_team in remaining_teams:
            if next_team not in teams_playing_this_week:
                continue
            options_for_remaining_weeks.append(
                find_best_remaining_plan_helper(weeks, week_index + 1, next_team, remaining_teams))

        best_plan = options_for_remaining_weeks[0]
        best_record = (best_plan.record.wins + team_wins) / (best_plan.record.games + team_games_played)
        for option in options_for_remaining_weeks:
            record = option.record
            temp_record = (record.wins + team_wins) / (record.games + team_games_played)
            if temp_record > best_record:
                best_plan = option
                best_record = temp_record
        plan_memo[plan_hash] =  best_plan

    return Plan([team] + best_plan.plan, Record(team_wins + best_plan.record.wins, team_games_played + best_plan.record.games))

def find_best_remaining_plan(weeks, start_week_index):
    options = []
    for team in AVAILABLE_TEAMS:
        options.append(find_best_remaining_plan_helper(weeks, 0, team, AVAILABLE_TEAMS))
    
    best_plan = options[0]
    best_record = (best_plan.record.wins) / (best_plan.record.games)
    for option in options:
        record = option.record
        temp_record = (record.wins) / (record.games)
        if temp_record > best_record:
            best_plan = option
            best_record = temp_record
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

best_plan = find_best_remaining_plan(weeks, 0)
print(best_plan.plan)
print(best_plan.record.wins, best_plan.record.games)