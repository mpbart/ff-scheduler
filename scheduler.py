from ring_buffer import RingBuffer
from itertools import chain, combinations
import random

# Conference 1
XENU = ['Harsha', 'Pepoy', 'Johan']
SHIVA = ['Jack', 'Duhaime', 'Peter']

# Conference 2
YAHWEH = ['Pomeroy', 'Holbrook', 'Ali']
ALLAH = ['Varano', 'Nezich', 'Barton']
TEAMS = list(chain.from_iterable([YAHWEH, XENU, SHIVA, ALLAH]))

class Scheduler:
    def __init__(self):
        self.num_teams = len(TEAMS)
        self.num_matchup_weeks = 14
        self.teams_per_division = 3
        self.conference_matchups = 1
        # set the conference matchup week randomly sometime between the second and
        # second to last week
        self.conference_matchup_week = random.randint(1, self.num_matchup_weeks - 2)
        self.teams = {team: self.blank_schedule() for team in TEAMS}
        self.division_map = self.create_division_map()
        self.conference_map = {'YAHWEH': 'ALLAH', 'ALLAH': 'YAHWEH', 'XENU': 'SHIVA', 'SHIVA': 'XENU'}
        # Shuffle the order of players defined in divisions to ensure randomness for who conference
        # matchups happen against
        random.shuffle(XENU)
        random.shuffle(SHIVA)
        random.shuffle(YAHWEH)
        random.shuffle(ALLAH)

    def blank_schedule(self):
        return {week: None for week in xrange(self.num_matchup_weeks)}

    def create_division_map(self):
        d = {team: 'XENU' for team in XENU}
        d.update({team: 'SHIVA' for team in SHIVA})
        d.update({team: 'YAHWEH' for team in YAHWEH})
        d.update({team: 'ALLAH' for team in ALLAH})
        return d

    # Play all teams once - 11 weeks
    # Play division teams again - 2 weeks
    # Play conference team again - 1 week
    def generate_schedule(self):
        self.generate_all_matchups(0)
        self.generate_division_matchups(11)
        self.generate_conference_matchups(11)
        self.shuffle_weeks()
        return self.teams

    def generate_all_matchups(self, start_week):
        c = RingBuffer(self.teams.keys())
        week = start_week
        for _ in xrange(self.num_teams - 1):
            for home_team, away_team in c.get_opposites():
                self.teams[home_team][week] = away_team
                self.teams[away_team][week] = home_team
            c.shift()
            week += 1

    def generate_division_matchups(self, start_week):
        for teams in [YAHWEH, ALLAH, SHIVA, XENU]:
            for matchup in combinations(teams, 2):
                for i in xrange(start_week, start_week + 3):
                    if self.teams[matchup[0]][i] == None and self.teams[matchup[1]][i] == None:
                        self.teams[matchup[0]][i] = matchup[1]
                        self.teams[matchup[1]][i] = matchup[0]
                        break

    def generate_conference_matchups(self, start_week):
        matchups = []
        for week in xrange(start_week, start_week + 3):
            candidates = {self.division_map[team]: team for team in self.teams.iterkeys() if self.teams[team][week] == None}
            matchups.extend([(candidates.get('YAHWEH'), candidates.get('ALLAH'), week), (candidates.get('XENU'), candidates.get('SHIVA'), week)])

        for matchup in matchups:
            self.teams[matchup[0]][matchup[2]] = matchup[1]
            self.teams[matchup[1]][matchup[2]] = matchup[0]

    def shuffle_weeks(self):
        weeks = [i for i in xrange(self.num_matchup_weeks)]
        random.shuffle(weeks)
        for idx, week in enumerate(weeks):
            for team in self.teams.iterkeys():
                self.teams[team][idx], self.teams[team][week] =  self.teams[team][week], self.teams[team][idx]


    def display(self, num_weeks):
        print "Team",
        for week in range(num_weeks):
            print "   %8d" % (week + 1),
            if week == num_weeks - 1: print ""
        for team in sorted(self.teams.keys()):
            print "  %8s" % team,
            for week in range(num_weeks):
                matchup = self.teams[team][week]
                print "   %08s" % matchup,
                if week == num_weeks - 1: print ""
