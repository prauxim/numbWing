import random, sys, copy, json, glob, inspect, os
from random import shuffle
from collections import OrderedDict
import numpy as np
import pandas as pd
import enum
from jutil import *

# try:
import xw_enums as xw
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

class Events(enum.Enum):
    declared_defender = 2001

class Stats():
    def __init__(self):
        pass


# class Ship_Template():
#     def __init__(self):
#         pass

defense_stats = Stats()
defense_stats.inc_rolled = 'inc_rolled'
defense_stats.inc_landed = 'inc_landed'


def aaaaah():
    pass

def main():
    # load_ships(msg=False)

    #
    # a,b,c = 0, 0, 0
    # table = Table(['a', 'b', 'c'])
    # table.add_row()
    # a,b,c = 1, 1, 1
    # table.add_row()
    #
    # _=0



    # import xwing_data as xw
    # norra = Ship(xw.arc170starfighter.norrawexley)
    # arc = Ship(xw.arc170starfighter)
    # try:
    #     norra = Ship(xw.arc170starfighter.norrawexley)
    # except:
    #     print 'Norra Wex init failed'
    #
    #
    # try:
    #     arc = Ship(xw.arc170starfighter)
    # except:
    #     print 'Arc default failed'

    # print arc
    # run_benchmark()
    run_benchmark(n_battles=1, brief_cnt=0, use_predictive=True, mode='squad')
    # run_benchmark(n_battles=1, brief_cnt=0, use_predictive=True)


    _=0


def load_ships(msg=True):
    # msg = True

    ships = glob.glob('C:/wd/pr/misc/xwing/numbWing/xwing-data2-master/data/pilots/*/*json')
    # ship_data_path = 'C:/wd/pr/misc/xwing/numbWing/xwing-data2-master/data/pilots/rebel-alliance/arc-170-starfighter.json'

    ship_def = open('xw_enums.py', 'w')
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

        ship_def.write('''class %s:\n''' % ship_name)
        SHIP_DATA[ship_name] = copy.copy(data)  #{'shields':0, 'attack':0, 'hull':0, 'agility': 0}
        ship_name_short = pd.DataFrame.from_csv('ship_names_short.csv')['short'][ship_name]
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
            print 'xx',  pilot_tags[0], '>>', pilot_tags[1]
        SHIP_DATA[ship_name]['cheapest_pilot'] = copy.copy(cheapest)
        ship_def.write('''    pilots = ['%s']\n''' % ("','".join(pilot_tags)))

        for pilot_tag in pilot_tags:
            ship_name, pilot_name = pilot_tag.split('.')
            ship_def.write('''    %s = '%s'\n''' % (pilot_name, pilot_tag))

        # if msg: print pilot_tags
        # SHIP_DATA[ship_name]['pilots'] = copy.copy(pilots)

    ship_def.close()


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

    battle = Battle(team_1, team_2)
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




def run_benchmark(test_ship='t65xwing_rebel.bluesquadronescort',
                  ships='all', hp_init=None, iterate=True,
                  n_battles=49, log_cnt=0, brief_cnt=1,
                  use_predictive=False, mode = 'squad'):

    global LOG_LVL
    LOG_LVL = 1

    bm_report = True
    n_use_prev_results = 250

    summary = open('../results/benchmark_%s_n%s.csv' % (mode, n_battles), 'w')
    summary.write('')

    if mode == '1v1':

        metrics = ['hits_rolled', 'hits_landed', 'inc_hits', 'hits_taken', 'off_focus', 'def_focus']
        header = ['ship', 'pilot', 'cost', '1v1dmg'] + metrics
        summary.write(','.join(header) + '\n')

    elif mode == 'squad':

        metrics = ['hits_rolled', 'hits_landed', 'inc_hits', 'hits_taken', 'off_focus', 'def_focus']
        header = ['ship', 'pilot', 'faction', 'cost', 'squad_size', 'squad_cost', 'win_rate_1', 'win_rate_2', 'enemy_health_1',
                  'enemy_health_2']  # + metrics
        summary.write(','.join(header) + '\n')

    if ships == 'all':
        ships = SHIP_DATA.keys()
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


            bench_ship = Ship(xw.tielnfighter_galactic.academypilot)
            bench_ship.pilot_name = 'benchmark_ship'
            bench_ship.base_hull = 999
            bench_ship.initiative = 9
            team_2.add(bench_ship)
            enemy_health = 'n/a'

            # battle = Battle(team_1, team_2)
            # battle.fight(n, log_cnt=0, battle_summary=False)

            battle = Battle(team_1, team_2)
            battle.fight(n_battles, log_cnt=1, battle_summary=True)

            dmg = round(1000 - battle.victor_health_remaining, 2)
            row = [tst_ship.ship_name_short, tst_ship.pilot_name, tst_ship.cost, dmg]
            if mode == 'squad':
                row += [win_rate_1, win_rate_2, enemy_health_1, enemy_health_2]

            for metric in metrics:
                metric = tst_ship.records[metric] if metric in tst_ship.records else 0
                row.append(round(np.mean(metric), 2))

            row = [str(x) for x in row]
            print row
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
            if (n_battles > n_use_prev_results) or use_predictive:
                df = pd.DataFrame.from_csv('../results/benchmark_squad_guide.csv')
                hp_init = df.loc[tst_ship.ship_name_short]['enemy_health_1'] - 1
            bm_health_offset = 0
            run_cnt=0

            if bm_report: print '\n---- Squad Benchmark: %sx %s @ %spts n=%s' % ( squad_size, tst_ship.tag, squad_cost, n_battles)
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
                    ship = Ship(xw.kihraxzfighter_scum)
                    ship.pilot_name = 'benchmark_pilot'
                    ship.initiative = 9
                    team_2.add(ship)
                bm_ships = team_2.ships
                for i in range(4):
                    bm_ships[i].statline['hull'] = copy.copy(health[i])
                    bm_ships[i].statline['shields'] = 0
                    bm_ships[i].set_base_stats()

                battle = Battle(team_1, team_2)
                # log_cnt = 1 if bm_health_base == hp_init else 0
                battle.fight(n_battles, log_cnt=log_cnt, brief_cnt=brief_cnt)

                if bm_report: print '   Benchmark Squad Health: %s   Total: %s   Winrate: %s' % (str(health), bm_health, battle.team_1_winrate)

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
    ship.respawn()
    ship.perform_activation()
    ship.attack_results = [HIT, FOCUS, FOCUS]

    print ship.attack_results
    ship.modify_dice(die_type=HIT)

    print ship.attack_results


def test_off_roll(team_blue, team_red):
    all_ships = team_red.ships + team_blue.ships

    for ship in all_ships:
        defender = Ship('target_dummy BWING', ship_type=BWING)
        defender.respawn()
        defender.shields = 1
        defender.reset()
        defender.perform_activation()
        ship.respawn()
        ship.reset()
        ship.perform_activation()
        ship.perform_attack(defender)

    sys.exit()


def test_def_roll(team_blue, team_red):
    all_ships = team_red.ships + team_blue.ships

    for ship in all_ships:
        ship.respawn()
        ship.reset()
        ship.perform_activation()
        ship.roll_defense(2)
        ship.modify_dice(die_type=EVADE)

    sys.exit()


class Battle():

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.battle_set_cnt = 0
        self.battle_logs = OrderedDict()

        self.round = 0

        self.print_battle_log = True

    def battle_log(self, msg):
        if self.print_battle_log:
            print msg

    def fight(self, n=1, log_cnt=1, brief_cnt=1, battle_summary_choice='use_log'):
        global LOG_LVL
        self.battle_set_cnt += 1

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

            battle_cnt = i + 1

            self.brief = brief_cnt >= battle_cnt

            if battle_summary_choice == 'use_log':
                battle_summary = log_cnt >= battle_cnt
            else:
                battle_summary = battle_summary_choice

            self.print_battle_log = log_cnt >= battle_cnt
            for ship in all_ships:
                ship.print_brief = self.brief
                ship.print_battle_log = self.print_battle_log

            self.battle_log('\n--- Battle %s ---' % (i+1))
            self.battle_tag = '%s.%s' % (self.battle_set_cnt, i + 1)

            self.battle_log('\n-- Setup --')
            for ship in all_ships_act_order:
                ship.respawn()

            rnd_cnt = 0
            while 1:
                rnd_cnt += 1



                self.battle_log('\n-- Round %s --' % rnd_cnt)


                done = False
                # shuffle(all_ships_act_order)

                self.battle_log('\n- Activation -')
                for ship in all_ships_act_order:
                    ship.battle_cnt = battle_cnt
                    ship.rnd_cnt = rnd_cnt
                    ship.perform_activation()
                    tag = ship.name
                    battle_data[tag] = {}

                self.battle_log('\n- Engagement -')
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

                self.battle_log('\n- End Phase-')
                for ship in all_ships_act_order:
                    ship.report_status()
                    ship.reset()

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
        if battle_summary:
            battle_summary_path = '../results/battle_summart.txt'
            f_write(battle_summary_path,'')
            print '--- Battle Set Summary ---\n'


            print team_blue.name, ':', ', '.join([x.name for x in team_blue.ships])
            print team_red.name, ':', ', '.join([x.name for x in team_red.ships])

            for ship in team_red.ships:
                print ship.name, ship.base_hull, ship.base_shields
            print n, 'battles'
            # blue_mov = round(sum(blue_mov)/float(len(blue_mov)),2)
            # red_mov = round(sum(red_mov)/float(len(red_mov)),2)
            print '%s: %s%%    %s: %s%%    Ties: %s%%' % (team_blue.name, team_1_wins, team_red.name, team_2_wins, ties)
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

        self.set_base_stats()
        #
        self.print_battle_log = True
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

        self.default_token = FOCUS

        self.tokens = {TARGET_LOCK: 0, FOCUS: 0, EVADE: 0, FORCE: 0}

        self.force = self.tokens[FORCE]
        self.focus = self.tokens[FOCUS]
        self.evade = self.tokens[EVADE]
        self.target_lock = self.tokens[TARGET_LOCK]
        #
        # ship_stats = SHIP_STATS  # {XWING: [3, 2, 2, 4], TIELN: [2, 3, 3, 0], BWING: [3, 1, 4, 4]}
        #
        # if ship_type is not None:
        #     stats = ship_stats[self.ship_type]
        #     self.set_base_stats(stats)
        #
        self.triggers = {Events.declared_defender: self.null}
        #

        self.stats = []
        self.records = {}
        self.log_level = 1

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

    def respawn(self):

        self.attack = self.base_attack
        self.focus = 0
        self.evade = 0
        self.dead = False

        self.agility = self.base_agility
        self.shields = self.base_shields
        self.hull = self.base_hull

        self.attack_results = []

        self.force = copy.copy(self.force_base)
        self.report_status(verb='respawns at')

    def perform_activation(self):

        self.tokens[self.default_token] += 1
        self.report('gains', self.default_token)

    def perform_attack(self, defender):

        res = {'hits_rolled': 0, 'hits_landed': 0}
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
        health = '[H:%s/%s]' % (self.shields, self.hull)
        brief = 'Battle:%-5sRnd:%-3s %-32s %-8s %2s dmg -> %32s' % (self.battle_cnt, self.rnd_cnt, self.name[:30], health, res['hits_landed'], defender.name[:30])
        if defender.dead:
            brief += '  DESTROYED'
        else:
            brief += '   S: %-2s H: %-2s' % (defender.shields, defender.hull)
        if self.print_brief:
            print brief
        # self.report_brief(brief)

        return res

    def report_brief(self, msg):
        print msg

    def perform_defense(self, attacker_roll):

        if 'Luke' in self.name:
            _=0

        self.triggers[Events.declared_defender]()

        self.attacker_roll = attacker_roll
        self.roll_defense(self.agility)

        dmg_init = self.compare_die()
        if dmg_init > 0:
            self.modify_dice(die_type=EVADE)


        dmg = self.compare_die(apply=True)

        inc_hits = self.total_hits(attacker_roll)
        self.record('inc_hits', inc_hits)
        evades = inc_hits-dmg
        if evades > 0:
            self.report('evades', evades)

        # if self.print_battle_log and evades > 0 and 'patrol' in self.pilot_name:
        #     _=0


        self.record('hits_taken', dmg)

        # print ''
        dmg = [HIT for x in range(dmg)]
        return dmg  # needs to return actual results, currently returns all HITS

    def total_hits(self, roll):
        return roll.count(HIT) + roll.count(CRIT)

    def record(self,k,v):

        if not k in self.records:
            self.records[k] = []
        else:
            _=0


        self.records[k].append(v)


    def reset(self):
        self.tokens[FOCUS] = 0
        self.tokens[EVADE] = 0
        self.regen_force()

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
            self.report('rerolls to ', str(results))

        if results.count(FOCUS) < 1:
            pass
        elif self.force > 0:
            token = FORCE
        elif self.tokens[FOCUS] > 0:
            token = FOCUS
        else:
            self.record(focus_use_metric, 0)
            self.report('No tokens!! : %s' % str(self.tokens))

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
                self.report('uses %s token to change <o> to %s' % (token, die_type))
                self.report('has %s force tokens remaining' % (self.force))

        if defensive:
            self.defensive_results = results
        else:
            self.attack_results = results

        self.record(focus_use_metric, focus_used)

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

        if self.print_battle_log:
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

    def compare_die(self, apply=False):
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
        self.report('#')
        # print '>>', damage
        return damage

    def report_status(self, lvl=0, verb='has'):

        if self.dead:
            verb = 'DESTROYED, ' + verb
        msg = 'Attack:%(base_attack)s | Agility:%(base_agility)s | Hull:%(hull)s/%(base_hull)s hull | Shields: %(shields)s/%(base_shields)s' % self.__dict__
        self.report(verb, msg, lvl=lvl)

        return self.shields + self.hull

class Named_Pilots():
    def __init__(self):
        pass

    def Luke_Skywalker(self):
        ship = Ship('Luke', XWING)

        ship.force_base = 2
        ship.force_regen = 1
        ship.default_token = TARGET_LOCK
        ship.triggers[Events.declared_defender] = ship.regen_force

        return ship

# #
#
# class X_Wing():
#     def __init__(self):
#         pass
#
#     def Luke_Skywalker(self):
#         ship = Ship('Luke', XWING)
#         ship.initiative = 5
#         ship.force_base = 2
#         ship.force_regen = 1
#         ship.default_token = TARGET_LOCK
#         ship.triggers[Events.declared_defender] = ship.regen_force
#         return ship
#
# #
# # x_wing = X_Wing()
#
# class Tie_LN():
#     def __init__(self):
#         pass
#     def Academy_Pilot(self):
#         ship = Ship('Academy Pilot', TIELN)
#         ship.initiative = 1
#         return ship
#
# tie_ln = Tie_LN()
#






#
# class Luke(Ship):
#     def __init__(self):
#         Ship.__init__(self, 'Luke', XWING)
#         # self.force = 2
#         self.force_base = 2
#         self.force_regen = 1
#         self.default_token = TARGET_LOCK
#         self.triggers[events.declared_defender] = self.regen_force
    #
    # def perform_defense(self, attacker_roll):
    #     Ship.regen_force(self)
    #     Ship.perform_defense(self, attacker_roll)


#
# class Shara(Ship):
#     def __init__(self):
#         Ship.__init__(self, 'Shara', ARC)



if __name__ == '__main__':
    main()
