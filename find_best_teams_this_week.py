import argparse
import nba_schedule
import teams

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="start of the current week, like YYYY-MM-DD.")
    args = parser.parse_args()
    weeks = nba_schedule.load_weeks('data/nba_predictions_' + args.date.replace('-', '_') + '.csv', args.date)
    print(weeks[0].get_best_teams_this_week())