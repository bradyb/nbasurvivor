def get_available_teams(file_name):
    with open(file_name, 'r') as available_teams_file:
        available_teams_file_lines = available_teams_file.readlines()
        return [team.strip() for team in available_teams_file_lines]