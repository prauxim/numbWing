import random, sys, copy, json, glob, inspect, os
from random import shuffle
from collections import OrderedDict
import numpy as np
import pandas as pd
import nw_enums as nw

# try:
import nw_ship_enums as xw
# except:
#     pass


HIT = 'HIT'
CRIT = 'CRIT'
FOCUS = 'FOCUS'
BLANK = 'BLANK'
EVADE = 'EVADE'
XWING = 'XWING'
BWING = 'BWING'
TIELN = 'TIELN'
ARC = 'ARC'
Z95 = 'Z95'
FORCE = 'FORCE'
TARGET_LOCK = 'TARGET_LOCK'


#
# class Events():
#     def __init__(self):
#         self.declared_defender = 'declared_defender'



class Stats():
    def __init__(self):
        pass


# class Ship_Template():
#     def __init__(self):
#         pass

defense_stats = Stats()
defense_stats.inc_rolled = 'inc_rolled'
defense_stats.inc_landed = 'inc_landed'


def aaah():
    "Dummy function to show up first on pyCharm's alphabetized function list"
    pass

def main():

    # example_battle()
    run_benchmark(n_matches=50, log_cnt=1, brief_logs=True, mode='1v1', print_match_summary=True,
                  benchmark_attack=3, benchmark_defense=2)
    run_benchmark(n_matches=50, log_cnt=0,  mode='squad', use_prev_results=True,
                  ships='all', benchmark_attack=3, print_match_summary=False)

def example_battle():
    team_1 = Team('Red Squad')
    team_1.add(xw.t65xwing_rebel.wedgeantilles)
    team_1.add(xw.t65xwing_rebel.lukeskywalker)

    team_2 = Team('Onyx Squad')
    team_2.add(xw.tielnfighter_galactic.academypilot)
    team_2.add(xw.tielnfighter_galactic.academypilot)
    team_2.add(xw.tielnfighter_galactic.academypilot)
    team_2.add(xw.tielnfighter_galactic.academypilot)

    match = Match(team_1, team_2)
    match.fight(50, brief_cnt=3, print_match_summary=True)


def load_ships(msg=True, write_enums=False):
    # msg = True

    ships = glob.glob('./pilots/*/*json')
    # ship_data_path = './pilots/rebel-alliance/arc-170-starfighter.json'

    if write_enums: ship_def = open('xw_enums.py', 'w')
    # ship_def.write('''import enum\nclass Ship_Template(enum.Enum):\n    pass\n''')

    global SHIP_DATA
    SHIP_DATA = {}
    for ship_path in ships:

        if 'firs' in ship_path or 'resis' in ship_path:
            continue
        with open(ship_path) as f:
            data = json.load(f)

        # msg = ('tie-ln' in ship_path)
        if msg:
            print ship_path
        stats = data['stats']
        # print data['faction'] 
        faction = data['faction'].split('-')[0].split(' ')[0].lower()
        # print faction
        ship_name = '%s_%s' % (data['xws'], faction)
        if 'modifiedtieln' in ship_name:
            continue

        if write_enums:  ship_def.write('''class %s:\n''' % ship_name)
        SHIP_DATA[ship_name] = copy.copy(data)  #{'shields':0, 'attack':0, 'hull':0, 'agility': 0}
        ship_names_df = pd.read_csv('./ship_names_short.csv', index_col ='ship')
        ship_name_short = ship_names_df['short'][ship_name]
        SHIP_DATA[ship_name]['ship_name_short'] = ship_name_short
        SHIP_DATA[ship_name]['statline'] = {'shields':0, 'attack':0, 'hull':0, 'agility': 0}
        statline = SHIP_DATA[ship_name]['statline']
        if msg: print '%30s' % ship_name,
        for stat in stats:
            type = stat['type']
            value = stat['value']
            if type in statline:
                if type == 'attack':
                    if value < statline[type]:
                        continue
                statline[type] = value

        if msg: print statline
        pilot_data = {}

        SHIP_DATA[ship_name]['pilot_data_list'] = copy.copy(data['pilots'])
        SHIP_DATA[ship_name]['pilots'] = {}
        for pilot in data['pilots']:
            pilot_name = pilot['xws'].split('-')[0]
            SHIP_DATA[ship_name]['pilots'][pilot_name] = copy.copy(pilot)

            # if '4lo' in pilot_name:
            #     _=0
            if pilot_name[0] in '0123456789':
                pilot_name = '_' + pilot_name
            if '-' in pilot_name:
                pilot_name = pilot_name.split('-')[0]
            # ship_def.write('''    %s = '%s.%s'\n''' % (pilot_name,ship_name, pilot_name))
            pilot_data[pilot_name] = copy.copy(pilot)
            if msg: print '%36s %5s %5s' % (pilot_name, pilot['cost'], pilot['initiative'])

        pilot_tags = ['%s.%s' % (ship_name, x[0]) for x in sorted(pilot_data.items(), key=lambda x:x[1]['cost'])]

        cheapest = pilot_tags[0]

        if 'nashtahpup' in cheapest or 'autopilot' in cheapest:
            cheapest = pilot_tags[1]
            # print 'xx',  pilot_tags[0], '>>', pilot_tags[1]
        SHIP_DATA[ship_name]['cheapest_pilot'] = copy.copy(cheapest)
        if write_enums: ship_def.write('''    pilots = ['%s']\n''' % ("','".join(pilot_tags)))

        for pilot_tag in pilot_tags:
            ship_name, pilot_name = pilot_tag.split('.')
            if write_enums: ship_def.write('''    %s = '%s'\n''' % (pilot_name, pilot_tag))

        # if msg: print pilot_tags
        # SHIP_DATA[ship_name]['pilots'] = copy.copy(pilots)

        if write_enums: ship_def.close()


load_ships(msg=False)
def fight():
    global LOG_LVL
    LOG_LVL = 1

    team_1 = Team('Test Squad')
    team_1.add(xw.t65xwing_rebel.bluesquadronescort)
    team_1.add(xw.t65xwing_rebel.bluesquadronescort)

    team_2 = Team('Bench Squad')
    for i in range(2):
        team_2.add(xw.tielnfighter_galactic.academypilot)

    battle = Match(team_1, team_2)
    battle.fight(499, log_cnt=0)


class Table:
    def __init__(self, header=None, path=None):
        self.cols = header
        self.min_width = 8
        self.rows = []


        self.path = 'table.csv' if path is None else path

    def print_table(self):

        fOut = open(self.path, 'w')

        rows = self.cols = self.rows
        fOut.writelines([','.join(row) + '\n' for row in rows])


    def append_header(self, cols):
        self.header += cols

    def add_row(self,):

        if len(self.rows) == 0:
            self.table_init()

        map = inspect.stack()[1][0].f_locals
        print_row = self.row_format % map
        val_row = [copy.copy(map[key]) for key in self.cols]
        print print_row
        self.rows.append(copy.copy(val_row))


    def table_init(self):
        self.widths = [max(len(x), self.min_width) for x in self.cols]
        self.header = ''
        for width, col in zip(self.widths, self.cols):
            fmt = '%-' + str(width) + 's'
            self.header += fmt % col
        print self.header

        self.row_format = ''
        for width, col in zip(self.widths, self.cols):
            self.row_format += '%(' + col + ')-' + str(width) + 's'

        # print self.row_format




def run_benchmark(ships='all', hp_init=None, iterate=True,
                  n_matches=49, log_cnt=0, brief_logs=True,
                  use_prev_results=True, mode = 'squad', print_match_summary=True,
                  benchmark_attack=3, benchmark_defense=2):



    """
    Runs 1v1 or squad benchmarks for all (or some ships)

    :param ships: array if benchmark_ship indtification enums, or 'all' to run all
    :param hp_init: optional specification of stating hp, quad mode only
    :param iterate: incrementally increase health for squad test, default true
    :param n_matches: number of time to repeat battles, use low (~49) for testing, high (15k-50k) for final results
    :param log_cnt: number of battle to print detailed battle logs,  for each benchmark_ship
    :param brief_cnt: number of battle to print brief battle logs,  for each benchmark_ship
    :param use_prev_results:  use 'guide' results, ../benchmark_%s_guide.csv must exist
    :param mode: 'squad' or '1v1
    :return: Nothing
    """



    global LOG_LVL
    LOG_LVL = 1

    bm_report = True



    summary = open('../results/benchmark_%s_n%s.csv' % (mode, n_matches), 'w')
    summary.write('')

    if ships == 'all':
        ships = SHIP_DATA.keys()

    if not type(ships) == list or type(ships) == tuple:
        ships = [ships]

    Mode = mode[0].upper() + mode[1:].lower()
    print '\nRunning %s Benchmark...\n  n=%s, %s test ships, Benchmark Atk/Agi: %s/%s' % (Mode, n_matches, len(ships), benchmark_attack, benchmark_defense)
    if mode == '1v1':

        metrics = ['hits_rolled', 'hits_landed', 'inc_hits', 'hits_taken', 'off_focus', 'def_focus']
        header = ['benchmark_ship', 'pilot', 'cost', '1v1dmg'] + metrics
        summary.write(','.join(header) + '\n')

    elif mode == 'squad':

        metrics = ['hits_rolled', 'hits_landed', 'inc_hits', 'hits_taken', 'off_focus', 'def_focus']
        header = ['benchmark_ship', 'pilot', 'faction', 'cost', 'squad_size', 'squad_cost', 'win_rate_1', 'win_rate_2', 'enemy_health_1',
                  'enemy_health_2']  # + metrics
        summary.write(','.join(header) + '\n')

        if use_prev_results:
            prev_res_path = '../results/benchmark_squad_guide.csv'
            if os.path.exists(prev_res_path):
                print '  Using %s to set inital benchmark hitpoints' % prev_res_path
                prev_res = pd.read_csv(prev_res_path, index_col='ship')
            else:
                print 'Cannot use predictive guess for initial hitpoints, please create a copy squad benchamr mark resuls names at the path ../results/benchmark_squad_guide.csv'
                use_prev_results = False


    for ship_type in ships:
        tst_ship = Ship(ship_type)

        p_battle = None
        p_bm_health = 0


        team_1 = Team('Test Squad')
        team_1.add(tst_ship)

        if mode =='1v1':

            tst_ship = Ship(ship_type)
            team_1 = Team('Test Squad')
            team_1.add(tst_ship)

            team_2 = Team('Bench Squad')
            bench_ship = Ship(xw.tielnfighter_galactic.academypilot)
            bench_ship.pilot_name = 'benchmark_ship'
            bench_ship.base_hull = 999
            bench_ship.initiative = 9
            bench_ship.base_attack = benchmark_attack
            bench_ship.base_agility = benchmark_defense
            team_2.add(bench_ship)
            enemy_health = 'n/a'

            if bm_report: print '\n---- 1v1 Benchmark: %s n=%s\n' % (tst_ship.tag, n_matches)

            # battle = Battle(team_1, team_2)
            # battle.fight(n, log_cnt=0, battle_summary=False)

            battle = Match(team_1, team_2)
            battle.fight(n_matches, brief_logs=brief_logs, log_cnt=log_cnt, print_match_summary=print_match_summary)

            dmg = round(1000 - battle.victor_health_remaining, 2)
            row = [tst_ship.ship_name_short, tst_ship.pilot_name, tst_ship.cost, dmg]
            if mode == 'squad':
                row += [win_rate_1, win_rate_2, enemy_health_1, enemy_health_2]

            for metric in metrics:
                metric = tst_ship.records[metric] if metric in tst_ship.records else 0
                row.append(round(np.mean(metric), 2))

            row = [str(x) for x in row]
            #
            # print '---- 1v1 summary ----\n%s matches\n' % n_matches
            #
            #
            # print ''.join(['%-16s' %x[:15] for x in header[:2]]), ''.join(['%-12s' %x for x in header[2:]])
            # print ''.join(['%-16s' %x[:15] for x in row[:2]]), ''.join(['%-12s' %x for x in row[2:]])
            #
            # print '\n-------\n\n'

            # sys.exit()
            summary.write(','.join(row) + '\n')

        elif mode == 'squad':


            team_1 = Team('Test Squad')
            team_1.add(tst_ship)
            squad_size = 1
            cost = team_1.ships[0].cost
            squad_cost = copy.copy(cost)
            while squad_cost < (200-0.5*cost):
                squad_size += 1
                squad_cost += cost
                tst_ship = Ship(ship_type)
                team_1.add(tst_ship)


            enemy_health_1, enemy_health_2, win_rate_1, win_rate_2 = 0, 0, 0, 0

            if hp_init == None:
                hp_init = 4
            if use_prev_results:
                # prev_res = pd.DataFrame.from_csv('../results/benchmark_squad_guide.csv')
                hp_init = prev_res.loc[tst_ship.ship_name_short]['enemy_health_1'] - 1
            bm_health_offset = 0
            run_cnt=0

            if bm_report: print '\n---- Squad Benchmark: %sx %s @ %spts n=%s' % (squad_size, tst_ship.tag, squad_cost, n_matches)
            for bm_health_base in range(hp_init, 99):
                run_cnt+=1
                bm_health = bm_health_base + bm_health_offset
                team_2 = Team('Bench Squad')
                health = [bm_health/4,bm_health/4,bm_health/4,bm_health/4]
                for i in range(3):
                    if bm_health%4 > i:
                        health[i] += 1

                # if bm_report: print '   Benchmark Squad Health: %s   Total: %s' % (str(health), bm_health)
                for i in range(4):
                    benchmark_ship = Ship(xw.kihraxzfighter_scum)
                    benchmark_ship.pilot_name = 'benchmark_pilot'
                    benchmark_ship.initiative = 9
                    team_2.add(benchmark_ship)
                bm_ships = team_2.ships
                for i in range(4):
                    bm_ships[i].statline['hull'] = copy.copy(health[i])
                    bm_ships[i].statline['shields'] = 0
                    bm_ships[i].set_base_stats()
                    benchmark_ship.base_attack = benchmark_attack
                    benchmark_ship.base_agility = benchmark_defense

                battle = Match(team_1, team_2)
                battle.fight(n_matches, log_cnt=log_cnt, brief_logs=brief_logs, print_match_summary=print_match_summary)

                if bm_report: print '   Benchmark Squad Health: %s   Total: %s   Test squad winrate: %s' % (str(health), bm_health, battle.team_1_winrate)

                # print '!', battle.team_1_winrate

                if (battle.team_1_winrate < 50) or (not iterate):
                    if run_cnt == 1 and iterate:
                        # if bm_health_offset < 0:
                        #     raise Exception('Double bm_health offset!')
                        bm_health_offset = -4
                        run_cnt = 0
                        continue

                    # enemy_health_1 = 4*(bm_health) -1
                    # enemy_health_2 = 4*bm_health

                    win_rate_1 = 0 if p_battle == None else p_battle.team_1_winrate
                    win_rate_2 = battle.team_1_winrate

                    # print '>>', [win_rate_1, win_rate_2, enemy_health_1, enemy_health_2]
                    # break

                    row = [tst_ship.ship_name_short, tst_ship.pilot_name, tst_ship.ship_data['faction'], tst_ship.cost, squad_size, tst_ship.cost*squad_size]
                    row += [win_rate_1, win_rate_2, p_bm_health, bm_health]

                    # for metric in metrics:
                    #     metric = tst_ship.records[metric] if metric in tst_ship.records else 0
                    #     row.append(round(np.mean(metric), 2))

                    row = [str(x) for x in row]
                    # print '!!', row
                    summary.write(','.join(row) + '\n')
                    break
                p_battle = copy.deepcopy(battle)
                p_bm_health = copy.deepcopy(bm_health)

    summary.close()


def test_mod_dice():
    ship = Ship('tstDum', ship_type=XWING)
    ship.performs_setup()
    ship.perform_activation()
    ship.attack_results = [HIT, FOCUS, FOCUS]

    print ship.attack_results
    ship.modify_dice(die_type=HIT)

    print ship.attack_results


def test_off_roll(ships, n=2):

    # ships = []

    if not type(ships) == list:
        ships = [ships]

    ships_new = []
    for ship in ships:
        class_name = ship.__class__.__name__
        if class_name == 'Team':
            ships_new += ship.ships



    ships = ships_new
    # all_ships = team_red.ships + team_blue.ships

    for i in range(n):
        for ship in ships:
            defender = Ship(xw.asf01bwing_rebel.bluesquadronpilot)
            defender.name = 'target_dummy'
            defender.performs_setup()
            defender.perform_end_phase()
            defender.perform_activation()
            ship.performs_setup()
            ship.perform_end_phase()
            ship.perform_activation()
            ship.perform_attack(defender)

    # sys.exit()


def test_def_roll(team_blue, team_red):
    all_ships = team_red.ships + team_blue.ships

    for ship in all_ships:
        ship.performs_setup()
        ship.perform_end_phase()
        ship.perform_activation()
        ship.roll_defense(2)
        ship.modify_dice(die_type=EVADE)

    sys.exit()


class Match():

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.match_set_cnt = 0
        self.match_logs = OrderedDict()

        self.round = 0

        self.print_match_log = True

    def match_log(self, msg):
        if self.print_match_log:
            print msg

    def fight(self, n=1, log_cnt=0, brief_logs=True, print_match_summary='use_log'):

        """
        Core game simulation method

        :param n: Number of time to repeat
        :param log_cnt: Number of matches to print details log for
        :param log_mode: Brief or Detailed logs,  nw.Flags.brief
        :param print_match_summary: True, False, or 'use_log' to do match summary for detailed log only
        :return:
        """

        global LOG_LVL
        self.match_set_cnt += 1

        # def fight1(team_blue, team_red):

        team_blue = self.team1
        team_red = self.team2
        all_ships = team_red.ships + team_blue.ships

        all_ships_act_order = sorted(all_ships, key=lambda x: x.initiative)
        all_ships_atk_order = copy.copy(all_ships_act_order)
        all_ships_atk_order.reverse()

        wins = []
        blue_mov = []
        red_mov = []

        n_battle = n

        battle_data = {}

        for i in range(n_battle):

            match_cnt = i + 1

            self.print_match_log = False
            self.brief = False
            self.print_match_log = log_cnt >= match_cnt

            if self.print_match_log and brief_logs:
                self.print_match_log = False
                self.brief = True

            if print_match_summary == 'use_log':
                match_summary = log_cnt >= match_cnt
            else:
                match_summary = print_match_summary

            for ship in all_ships:
                ship.print_brief = self.brief
                ship.print_match_log = self.print_match_log

            self.match_log('\n--- Battle %s ---' % (i + 1))
            self.match_tag = '%s.%s' % (self.match_set_cnt, i + 1)

            self.match_log('\n-- Setup --')
            for ship in all_ships_act_order:
                ship.performs_setup()

            rnd_cnt = 0
            while 1:
                rnd_cnt += 1



                self.match_log('\n-- Round %s --' % rnd_cnt)


                done = False
                # shuffle(all_ships_act_order)

                self.match_log('\n- Activation -')
                for ship in all_ships_act_order:
                    ship.match_cnt = match_cnt
                    ship.rnd_cnt = rnd_cnt
                    ship.perform_activation()
                    tag = ship.name
                    battle_data[tag] = {}

                self.match_log('\n- Engagement -')
                for ship in all_ships_atk_order:

                    if ship.dead:
                        continue

                    attacking_team = team_red if ship in team_red.ships else team_blue
                    other_team = team_blue if ship in team_red.ships else team_red

                    tag = ship.name

                    defender = ship.choose_target(other_team)

                    # ship.perform_action()
                    battle_data[tag] = ship.perform_attack(defender)

                    if other_team.dead():
                        # print '%s dies\n' % other_team.name
                        break

                    # for ship in all_ships_act_order:
                    #     ship.report_status()

                self.match_log('\n- End Phase-')
                for ship in all_ships_act_order:
                    ship.perform_end_phase()
                for ship in all_ships_act_order:
                    ship.report_status()

                blue_dead = team_blue.dead()
                read_dead = team_red.dead()
                if blue_dead and read_dead:
                    wins.append('T')
                    done = True
                elif blue_dead:
                    wins.append('red')
                    red_mov.append(team_red.remaining_health())
                    # print
                    done = True
                    # team_red.ships[0].report_status(lvl=3)
                elif read_dead:
                    wins.append('blue')
                    health = team_blue.remaining_health()
                    blue_mov.append(health)
                    done = True



                if done:
                    self.match_log('- Battle %s over -\n' % match_cnt)
                    if self.brief:
                        print '------\n'
                    # print '-gg-'
                    break



        def get_per(res, reses):
            return round(100 * reses.count(res) / float(len(reses)), 2)

        team_1_wins = get_per('blue', wins)
        team_2_wins = get_per('red', wins)
        ties = get_per('T', wins)

        self.team_1_winrate = copy.copy(team_1_wins)

        net_mov = round(((sum(blue_mov) - sum(red_mov)) / float(len(wins))), 2)
        self.victor_health_remaining, self.victor = (str(net_mov), team_blue.name) if net_mov > 0 else (str(net_mov * -1), team_red.name)
        self.victor_health_remaining = float(self.victor_health_remaining)

        def battle_summary_ph():
            pass
        if match_summary:
            battle_summary_path = '../results/battle_summary.txt'
            f_write(battle_summary_path,'')
            print '--- Battle Set Summary ---\n'


            print n, 'battles'
            print team_blue.name, ':', ', '.join([x.name for x in team_blue.ships])
            print team_red.name, ':', ', '.join([x.name for x in team_red.ships])

            # for ship in team_red.ships:
            #     print ship.name, ship.base_hull, ship.base_shields
            # blue_mov = round(sum(blue_mov)/float(len(blue_mov)),2)
            # red_mov = round(sum(red_mov)/float(len(red_mov)),2)
            print '%s Winrate: %s%%    %s Winrate: %s%%    Ties: %s%%' % (team_blue.name, team_1_wins, team_red.name, team_2_wins, ties)
            print 'Mean Health Remaining: %s %s' % (self.victor_health_remaining, self.victor)
            # ('inc_hits', self.total_hits(attacker_roll))
            # self.record('hits_taken'
            stats = ['hits_rolled', 'hits_landed', 'inc_hits', 'hits_taken', 'off_focus', 'def_focus'] #np.mean(res)
            print '\n - Die Result Averages -'
            col_width = 10
            header = ' ' * 32
            for stat in stats:
                header += '%-15s' % stat

            print header

            for ship in all_ships_atk_order:
                row = '%-32s' % ship.name
                for stat in stats:
                    # if stat in ship.records:
                    res = ship.records[stat] if stat in ship.records else 0
                    mean = np.mean(res)
                    val = '%-15s' % round(mean, 2)
                    # else:
                    #     val = 'n/r'
                    # print res
                    # print mean
                    # print val
                    row += val
                print row

                f_addline(battle_summary_path, '')



    # print wins


class Team():
    def __init__(self, name, ships=[]):
        self.name = name
        self.ships = []

    def add(self, identifier):


        try:
            name = '%s %s (%s)' % (self.name, (len(self.ships) + 1), identifier.pilot_name)
            ship = identifier
        except:
            ship = Ship(identifier)
            name = '%s %s (%s)' % (self.name, (len(self.ships)+1), ship.pilot_name)
        ship.name = name
        self.ships.append(ship)
        ship.team = self

    def remaining_ships(self):
        return [x for x in self.ships if not x.dead]

    def dead(self):

        deads = [ship.dead for ship in self.ships]
        return min(deads)

    def remaining_health(self):
        return sum([x.report_status(lvl=-99) for x in self.ships])


#
# def get_ship_data(identifier):
#     try:
#         identifier = identifier.pilots[0]
#     except:
#         pass
#     ship, pilot = identifier.split('.')
#     return ship, pilot




class Ship():
    def __init__(self, identifier):

        # ship class input
        try:
            identifier = identifier.pilots[0] #effective just a bounce to next check
        except:
            pass

        #  ship string identifier
        if identifier in SHIP_DATA:
            identifier = SHIP_DATA[identifier]['cheapest_pilot']
            # print '>', identifier
        # u'sabinewren-tielnfighter'
        self.tag = identifier
        self.ship_name, self.pilot_name = identifier.split('.')
        self.ship_data = SHIP_DATA[self.ship_name]
        self.pilot_data = SHIP_DATA[self.ship_name]['pilots'][self.pilot_name]
        self.statline = self.ship_data['statline']
        self.initiative = self.pilot_data['initiative']
        self.cost = self.pilot_data['cost']
        self.ship_name_short = self.ship_data['ship_name_short']
        self.effects = []
        self.match_cnt = 0
        self.rnd_cnt = 0
        self.print_brief = False
        self.name = self.pilot_name

        self.set_base_stats()

        self.default_token = FOCUS
        self.tokens = {TARGET_LOCK: 0, FOCUS: 0, EVADE: 0, FORCE: 0}

        #
        self.print_match_log = True
        # print self.ship_data
        # print self.pilot_data

        # try:
        #     name = int(name)
        #     self.name = 'Ship %i' % name
        # except:
        #     self.name = name
        #
        # self.ship_type = ship_type
        #
        self.force_base = 0
        self.force_regen = 0
        self.report_lvl = 1

        self.force = self.tokens[FORCE]
        self.focus = self.tokens[FOCUS]
        self.evade = self.tokens[EVADE]
        self.target_lock = self.tokens[TARGET_LOCK]

        self.temp_agility_modifer = 0
        self.temp_attack_modifer = 0
        #
        # ship_stats = SHIP_STATS  # {XWING: [3, 2, 2, 4], TIELN: [2, 3, 3, 0], BWING: [3, 1, 4, 4]}
        #
        # if ship_type is not None:
        #     stats = ship_stats[self.ship_type]
        #     self.set_base_stats(stats)
        #
        # self.triggers = {}
        #

        self.stats = []
        self.records = {}
        self.log_level = 1

        self.triggers = {nw.Events.declared_defender: []}
        self.setup_ship_abilities()


    def null(self):
        pass

    def set_base_stats(self):

        self.base_attack = self.statline['attack']
        self.base_agility = self.statline['agility']
        self.base_shields = self.statline['shields']
        self.base_hull = self.statline['hull']
        # self.base_attack, self.base_agility, self.base_hull, self.base_shields = stats

    def choose_target(self, opposing_team):
        enemy_ships = opposing_team.remaining_ships()

        ship_healths = [(ship, (ship.shields + ship.hull)) for ship in enemy_ships]
        ship_healths = sorted(ship_healths, key=lambda x:x[1])

        shuffle(enemy_ships)
        defender = ship_healths[0][0]


        self.report('engages', defender.name, lvl=2)
        return defender

    def performs_setup(self):

        self.attack = self.base_attack
        self.focus = 0
        self.evade = 0
        self.dead = False

        self.agility = self.base_agility
        self.shields = self.base_shields
        self.hull = self.base_hull

        self.attack_results = []

        self.force = copy.copy(self.force_base)
        self.report_status(verb='performs setup ')

    def perform_activation(self):

        self.tokens[self.default_token] += 1
        self.report('gains', self.default_token)

    def perform_attack(self, defender):


        self.current_attack_target = defender
        res = {'hits_rolled': 0, 'hits_landed': 0}

        self.trigger_effects(nw.Events.performing_attack)

        # print ''

        self.roll_attack(self.attack)
        self.modify_dice()

        res['hits_rolled'] += self.attack_results.count(HIT) + self.attack_results.count(CRIT)

        dmg = defender.perform_defense(self.attack_results)
        if dmg == None: dmg = []
        res['hits_landed'] += dmg.count(HIT) + dmg.count(CRIT)

        self.record('hits_rolled', self.total_hits(self.attack_results))
        self.record('hits_landed', self.total_hits(dmg))

        # self.report('')
        attacker_hp = '[H:%s/%s]' % (self.shields, self.hull)
        defender_hp = '[H:%s/%s]' % (defender.shields, defender.hull)
        brief = 'Battle:%-5sRnd:%-3s %-32s %-11s %-2s dmg -> %-32s %-10s' % (self.match_cnt, self.rnd_cnt, self.name[:30], attacker_hp, res['hits_landed'], defender.name[:30], defender_hp)
        if defender.dead:
            brief += ' DESTROYED'
        if self.print_brief:
            print brief
        # self.report_brief(brief)

        self.temp_attack_modifer = 0
        return res

    def report_brief(self, msg):
        print msg

    def trigger_effects(self, trigger):

        trash = []
        for effect in self.effects:
            if effect.trigger == trigger:
                self.report('triggers', effect.name)

                # effect.trigger(self)

                for sub_effect in effect.sub_effects:
                    def df():
                        pass
                    if type(sub_effect) == type(df):
                        sub_effect(self)

            if effect.use_once == True:
                trash.append(effect)

        for effect in trash:
            self.effects.remove(effect)



    def perform_defense(self, attacker_roll):

        if 'Luke' in self.name:
            _=0

        self.trigger_effects(nw.Events.declared_defender)

        self.attacker_roll = attacker_roll

        agi_mod = self.temp_agility_modifer
        if not agi_mod == 0:
            mod = '%s green dice reduction' % agi_mod if agi_mod < 0 else '%s green dice bonus' % agi_mod
            self.report('has', 'temportary %s' % mod)
        self.roll_defense(self.agility + agi_mod)

        dmg_init = self.compare_results()
        if dmg_init > 0:
            self.modify_dice(die_type=EVADE)


        dmg = self.compare_results(apply=True)

        inc_hits = self.total_hits(attacker_roll)
        self.record('inc_hits', inc_hits)
        evades = inc_hits-dmg
        # if evades > 0:
        #     self.report('evades', evades)

        # if self.print_battle_log and evades > 0 and 'patrol' in self.pilot_name:
        #     _=0


        self.record('hits_taken', dmg)

        # print ''
        dmg = [HIT for x in range(dmg)]


        self.temp_agility_modifer = 0
        return dmg  # needs to return actual results, currently returns all HITS

    def total_hits(self, roll):
        return roll.count(HIT) + roll.count(CRIT)

    def record(self,k,v):

        if not k in self.records:
            self.records[k] = []
        else:
            _=0


        self.records[k].append(v)


    def perform_end_phase(self):
        self.regen_force()
        self.tokens[FOCUS] = 0
        self.tokens[EVADE] = 0

    def regen_force(self):

        if self.force_base > 1:
            if self.force < self.force_base:
                self.force += 1

                self.report('gains 1 force for %s total' % (self.force))

            else:
                self.report('does not regen force becasue it is at a max of %s' % self.force_base)

    def modify_dice(self, die_type=HIT):
        # self.report('uses', FOCUS)

        focus_use_metric = {HIT: 'off_focus', EVADE: 'def_focus'}[die_type]
        focus_used = 0
        token = None

        defensive = False
        if die_type == EVADE:
            defensive = True
            if self.name == TIELN:
                _ = 0

        results = self.attack_results if die_type == HIT else self.defensive_results

        if 'Luke' in self.name:
            _=0
        name = self.name
        if self.tokens[TARGET_LOCK] > 0 and die_type == HIT:
            blanks = results.count(BLANK)
            if blanks > 0:
                non_blanks = [x for x in results if not x == BLANK ]
                reroll = self.roll_attack(blanks, reroll=True)
                results = non_blanks + reroll
            self.target_lock -= 1
            self.report('used Target Lock')
            # self.report('rerolls to ', str(results))

        if results.count(FOCUS) < 1:
            pass
        elif self.force > 0:
            token = FORCE
        elif self.tokens[FOCUS] > 0:
            token = FOCUS
        else:
            self.record(focus_use_metric, 0)
            # self.report('No tokens!! : %s' % str(self.tokens))

        if token == FOCUS:
            foci = results.count(FOCUS)

            focus_used = 1
            results = [die_type if x == FOCUS else x for x in results]

            self.report('uses %s token to change %s <o>s to %s' % (token, foci, die_type))

        elif token == FORCE:
            while self.force > 0 and results.count(FOCUS) > 0:
                self.force -= 1
                results.remove(FOCUS)
                results.append(die_type)
                self.report('uses %s token to change <o> to %s, %s force remaining' % (token, die_type, self.force))
                # self.report('has %s force tokens remaining' % (self.force))

        if defensive:
            self.defensive_results = results
        else:
            self.attack_results = results

        self.record(focus_use_metric, focus_used)

        attack_defense = 'defensive' if defensive else 'attack'
        self.report('%s results are' % attack_defense, results)

        self.report('#')
    def report(self, verb, noun='', lvl=1):
        # self.report_lvl = 0

        # print '..'
        global LOG_LEVEL

        indent = (4 - lvl) * '  '
        li = len(indent)
        name = self.name
        if '#' in verb:
            verb = verb.replace('#', '')
            name = ''

        if self.print_match_log:
        # if LOG_LVL == 1:
            print '%s %s %s %s' % (indent, name, verb, noun)

    def roll_attack(self, n, reroll=False):
        results = []
        for i in range(n):
            results.append([HIT, HIT, HIT, CRIT, FOCUS, FOCUS, BLANK, BLANK][random.randint(0, 7)])

        verb = 'rerolls' if reroll else 'rolls'
        self.report('%s attack' % verb, results)

        if reroll:
            return results
        self.attack_results = results

    def roll_defense(self, n):
        results = []
        for i in range(n):
            results.append([EVADE, EVADE, EVADE, FOCUS, FOCUS, BLANK, BLANK, BLANK][random.randint(0, 7)])
        self.report('rolls defense', results)
        self.defensive_results = results

    def compare_results(self, apply=False):
        self.hits = self.attacker_roll.count(HIT) + self.attacker_roll.count(CRIT)
        self.evades = self.defensive_results.count(EVADE)

        if 'patrol' in self.pilot_name:
            _=0

        # print '>Apply:', apply
        # print '>', self.attacker_roll
        # print '>', self.defensive_results

        if self.hits > self.evades:
            damage = self.hits - self.evades
        else:
            damage = 0

        # print '> h/ev/dmg:',self.hits, self.evades, damage

        if apply:
            # self.report('takes %s damage' % damage)

            if damage == 0:
                self.report('take no damage')

            elif damage < self.shields:
                self.shields -= damage
                self.report('takes %s shield damage' % damage)

            elif damage >= self.shields:
                hull_damage = damage - self.shields

                self.report('takes %s shield damage' % self.shields)
                self.shields = 0
                self.report('takes %s hull damage' % hull_damage)
                self.hull -= hull_damage
                # self.report_status()
            self.report('has', '%s shields / %s hull' % (self.shields, self.hull))
            if self.hull < 1:
                self.report('is', 'destroyed')

                self.dead = True

            # print ''
        # print '>>', damage
            self.report('#')
        return damage


    def report_status(self, lvl=1, verb='has'):

        if self.dead:
            verb = 'DESTROYED, ' + verb
        msg = 'Attack:%(base_attack)s | Agility:%(base_agility)s | Hull:%(hull)s/%(base_hull)s hull | Shields: %(shields)s/%(base_shields)s' % self.__dict__
        if self.force_base > 0:
            msg += ' | Force: %(force)s' % self.__dict__
        self.report(verb, msg, lvl=lvl)

        return self.shields + self.hull


    def add_effect(self, effect):
        self.effects.append(effect)
    def setup_ship_abilities(self):

        pilot_ability = None
        ship_ability = None

        if self.tag == xw.t65xwing_rebel.wedgeantilles:

            pilot_ability = Ability(trigger=nw.Events.performing_attack)

            def wedge_pilot_effect(self):
                self.current_attack_target.temp_agility_modifer -= 1

            pilot_ability.add_effect(wedge_pilot_effect)

        if self.tag == xw.t65xwing_rebel.lukeskywalker:
            self.force_base = 2
            self.force_regen = 1
            self.default_token = TARGET_LOCK

            pilot_ability = Ability(trigger=nw.Events.declared_defender)

            def luke_pilot_effect(self):
                self.regen_force()

            pilot_ability.add_effect(luke_pilot_effect)




        # if self.tag == xw.starviperclassattackplatform_scum.guri:
        #     pilot_ability = Ability(trigger=nw.Events.engagement_phase_start)
        #     pilot_ability.proc_rate = 0.75
        #
        #     def guri_ability_effect():
        #         self.tokens[FOCUS] += 1
        #     pilot_ability.add_effect(guri_ability_effect)

        if pilot_ability is not None:
            self.add_effect(pilot_ability)

        if ship_ability is not None:
            self.add_effect(ship_ability)


class Ability():
    def __init__(self, name='pilot ability', action=None, trigger=None):
        self.name = name
        self.limited_used = False
        self.use_once = False
        self.used_remaining = 1
        self.trigger = trigger
        self.action=action
        self.sub_effects = []
        self.proc_rate = 1.0

    def add_effect(self, effect):
        self.sub_effects.append(effect)


# A set of function to make file read/write easier because I'm a lazy bum
def f_core(path, text, mode, lvl=2):
    fl = open(path, mode)
    if 'r' in mode:
        txt = fl.read()
        fl.close()
        return txt
    else:
        fl.write(text)
        fl.close()
        return path

f_clear = lambda path: f_core(path, '', 'w')
f_add = lambda path, text: f_core(path, text, 'a')
f_addline = lambda path, text: f_core(path, str(text) + '\n', 'a')
f_addlines = lambda path, text: f_core(path, '\n'.join(text), 'a')
f_write = lambda path, text: f_core(path, text, 'w')
f_writeline = lambda path, text: f_core(path, str(text) + '\n', 'w')
f_writelines = lambda path, text: f_core(path, '\n'.join(text), 'w')


if __name__ == '__main__':
    main()
