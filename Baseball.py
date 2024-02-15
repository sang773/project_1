import os
import sys

def read_teams_data(given_folder):
    teams_file_path = os.path.join(given_folder, 'teams.dat')
    with open(teams_file_path, 'r') as teams_file:
        teams_data = {line.split(':')[1].strip(): line.split(':')[0].strip() for line in teams_file}
    return teams_data


def read_games_data(given_folder):
    games_file_path = os.path.join(given_folder, 'games.dat')
    games_data = []
    with open(games_file_path, 'r') as games_file:
        for line in games_file:
            date, team1, team2, score1, score2 = line.strip().split(':')
            games_data.append((date, team1, team2, int(score1), int(score2)))
    return games_data

def calculate_standings(teams_data, games_data):
    team_stats = {}
    for _, team1, team2, score1, score2 in games_data:
        if team1 not in team_stats:
            team_stats[team1] = {'WINS': 0, 'LOSSES': 0, 'TIES': 0}
        if team2 not in team_stats:
            team_stats[team2] = {'WINS': 0, 'LOSSES': 0, 'TIES': 0}
        
        if score1 > score2:
            team_stats[team1]['WINS'] = team_stats[team1]['WINS'] + 1
            team_stats[team2]['LOSSES'] = team_stats[team2]['LOSSES'] + 1
        elif score1 < score2:
            team_stats[team2]['WINS'] = team_stats[team2]['WINS'] + 1
            team_stats[team1]['LOSSES'] = team_stats[team1]['LOSSES'] + 1
        else:
            team_stats[team1]['TIES'] = team_stats[team1]['TIES'] + 1
            team_stats[team2]['TIES'] = team_stats[team2]['TIES'] + 1
    
    standings = []
    for team_code in teams_data:
        stats = team_stats.get(team_code, {'WINS': 0, 'LOSSES': 0, 'TIES': 0})
        total_games = stats['WINS'] + stats['LOSSES'] + stats['TIES']
        win_percent = (stats['WINS'] + (stats['TIES'] / 2)) / total_games if total_games > 0 else 0
        standings.append((team_code, stats['WINS'], stats['LOSSES'], stats['TIES'], win_percent))
    
    return sorted(standings, key=lambda x: x[4], reverse=True)

def display_standings(standings):
    print("{:<20} {:>6} {:>6} {:>6} {:>7}".format("TEAM", "WINS", "LOSSES", "TIES", "PERCENT"))
    print('-' * 20 + ' ' + '-' * 6 + ' ' + '-' * 6 + ' ' + '-' * 6 + ' ' + '-' * 7)
    for team_code, wins, losses, ties, win_percent in standings:
        print("{:<20} {:>6} {:>6} {:>6} {:>6.3f}".format(team_code, wins, losses, ties, win_percent))

def display_team_results(games_data, teams_data, team_code):
    team_name = teams_data.get(team_code)
    if team_name is None:
        print("Invalid team code")
        return
    
    print(f"Team: {team_name}\n")
    print("{:>10} {:>11} {:>4} {:>5} {:>7}".format("DATE", "OPPONENT", "US", "THEM", "RESULT"))
    
    wins = losses = ties = 0
    
    for date, team1, team2, score1, score2 in games_data:
        if team1 == team_code:
            result = "WIN" if score1 > score2 else "LOSS" if score1 < score2 else "TIE"
            wins += 1 if result == "WIN" else 0
            losses += 1 if result == "LOSS" else 0
            ties += 1 if result == "TIE" else 0
            opponent = team2
            print(f"{date} {opponent:>11} {score1:>4} {score2:>5} {result:>7}")
        elif team2 == team_code:
            result = "WIN" if score2 > score1 else "LOSS" if score2 < score1 else "TIE"
            wins += 1 if result == "WIN" else 0
            losses += 1 if result == "LOSS" else 0
            ties += 1 if result == "TIE" else 0
            opponent = "at" + " " + team1
            print(f"{date} {opponent:>11} {score2:>4} {score1:>5} {result:>7}")
    
    print(f"\nOverall Record: {wins}-{losses}-{ties}")

def main():
    given_folder = sys.argv[1]
    teams_data = read_teams_data(given_folder)
    games_data = read_games_data(given_folder)
    
    while True:
        print("\n(s) Standings\n(t) Team results\n(q) Quit")
        value = input("What do you want to see: ").strip().lower()
        
        if value == 's':
            standings = calculate_standings(teams_data, games_data)
            display_standings(standings)
        elif value == 't':
            team_code = input("Enter team code (e.g. ARI, ATL, CHC, CLE, STL): ").strip().upper()
            display_team_results(games_data, teams_data, team_code)
        elif value == 'q':
            break
        else:
            print("Invalid value. Please select 's', 't', or 'q'.")

if __name__ == "__main__":
    main()