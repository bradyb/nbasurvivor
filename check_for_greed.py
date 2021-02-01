# Want to see how close the find_plan functions are to just taking the best
# team every week

import find_plan
import nba_schedule
import teams

if __name__ == "__main__":
    weeks = nba_schedule.load_weeks('data/nba_predictions_2021_02_01.csv', '2021-02-01')
    print(find_plan.find_best_remaining_plan(weeks).plan)

    available_teams = teams.get_available_teams('teams/teams.txt')
    greediest_teams_off_the_week = []
    for week in weeks:
        ordered_teams = [team for team, stat in sorted(week.get_all_team_stats().items(), key=lambda item: -1 * (item[1][0] / item[1][1]))]
        best_team = None
        for team in ordered_teams:
            if team in available_teams:
                best_team = team
                break
        greediest_teams_off_the_week.append(best_team)
        available_teams.remove(best_team)

    print(greediest_teams_off_the_week)

