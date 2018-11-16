import os, sys
running_from_source = os.path.isfile('./numbWing.py')
if os.path.isfile('./code/numbWing.py'):
    os.chdir('./code')
elif not running_from_source:
    print 'Could not find numbWing.py, place in same folder as the numbWing code directory (but not in the code folder)\nExiting...'
    sys.exit()

from numbWing import *


#
# Make edits below
#

def main():


    if not os.path.isdir('../results'):
        os.mkdir('../results')

    example_battle()

    run_benchmark(n_matches=50, log_cnt=1, brief_logs=True, mode='1v1', print_match_summary=True,
                  benchmark_attack=3, benchmark_defense=2)

    run_benchmark(n_matches=50, log_cnt=0,  mode='squad', use_prev_results=True,
                  ships='all', benchmark_attack=3, benchmark_defense=2, print_match_summary=False)

def example_battle():
    team_1 = Team('Red Squad')
    team_1.add(xw.t65xwing_rebel.wedgeantilles)
    team_1.add(xw.t65xwing_rebel.lukeskywalker)

    team_2 = Team('Onyx Squad')
    team_2.add(xw.tielnfighter_galactic.academypilot)
    team_2.add(xw.tielnfighter_galactic.academypilot)
    team_2.add(xw.tielnfighter_galactic.academypilot)
    team_2.add(xw.tielnfighter_galactic.academypilot)

    battle = Match(team_1, team_2)
    battle.fight(50, log_cnt=1, print_match_summary=True)


#
# Make edits above
#

if __name__ == '__main__':
    main()
    if running_from_source:
        print '\nWarning!\nThis is a user script, make a copy to top folder if you wish to save and changes when updating\nExiting...'
