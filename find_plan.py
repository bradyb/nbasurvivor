import csv
from datetime import datetime
import nba_schedule
from nba_schedule import Week
from nba_schedule import Game
from nba_schedule import Record
from nba_schedule import Plan
import teams

AVAILABLE_TEAMS = teams.get_available_teams('teams/teams.txt')

def create_plan_hash(plan):
    return ','.join(sorted(plan))

plan_memo = {}

def find_best_remaining_plan_helper(weeks, week_index, team, available_teams):
    if len(available_teams) == 1:
        wins_this_week, games_this_week = weeks[week_index].get_team_stats(team)
        return Plan([team], Record(wins_this_week, games_this_week))
    if week_index == len(weeks):
        return Plan([], Record(0.0, 0))
    week = weeks[week_index]
    teams_playing_this_week = week.get_teams_playing_this_week()
    options_for_remaining_weeks = []
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

def find_best_remaining_plan(weeks):
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


if __name__ == "__main__":
    weeks = nba_schedule.load_weeks('data/nba_predictions_2021_01_04.csv', '2021-01-04')
    best_plan = find_best_remaining_plan(weeks)
    print(best_plan.plan)
    print(best_plan.record.wins, best_plan.record.games)