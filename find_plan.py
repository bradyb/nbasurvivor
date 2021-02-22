import argparse
import csv
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

def find_best_remaining_plan_helper(weeks, week_index, team, available_teams, record_so_far):
    if len(available_teams) == 1:
        wins_this_week, games_this_week = weeks[week_index].get_team_stats(team)
        return Plan([team], Record(wins_this_week, games_this_week) + record_so_far)
    if week_index == len(weeks):
        return Plan([], record_so_far)
    week = weeks[week_index]
    teams_playing_this_week = week.get_teams_playing_this_week()
    options_for_remaining_weeks = []
    remaining_teams = available_teams.copy()
    remaining_teams.remove(team)        
    curr_team_record = week.get_team_record(team)

    plan_hash = create_plan_hash(remaining_teams)
    if plan_hash in plan_memo:
        best_plan = plan_memo[plan_hash]
    else:
        for next_team in remaining_teams:
            if next_team not in teams_playing_this_week:
                continue
            options_for_remaining_weeks.append(
                find_best_remaining_plan_helper(weeks, week_index + 1, next_team, remaining_teams, record_so_far))

        best_plan = options_for_remaining_weeks[0]
        best_record = (best_plan.record + curr_team_record).get_percentage()
        for option in options_for_remaining_weeks:
            record = option.record
            temp_record = (record + curr_team_record).get_percentage()
            if temp_record > best_record:
                best_plan = option
                best_record = temp_record
        plan_memo[plan_hash] =  best_plan

    return Plan([team] + best_plan.plan, best_plan.record + curr_team_record)

def find_best_remaining_plan(weeks, record_so_far):
    options = []
    for team in AVAILABLE_TEAMS:
        options.append(find_best_remaining_plan_helper(weeks, 0, team, AVAILABLE_TEAMS, record_so_far))
    
    best_plan = options[0]
    best_record = best_plan.record.get_percentage()
    for option in options:
        record = option.record
        temp_record = record.get_percentage()
        if temp_record > best_record:
            best_plan = option
            best_record = temp_record
    return best_plan


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="start of the current week, like YYYY-MM-DD.")
    args = parser.parse_args()
    weeks = nba_schedule.load_weeks('data/nba_predictions_' + args.date.replace('-', '_') + '.csv', args.date)
    record_so_far = Record(16, 29)
    best_plan = find_best_remaining_plan(weeks, record_so_far)
    print(best_plan.plan)
    print(best_plan.record.wins, best_plan.record.games)