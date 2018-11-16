from numbWing import *

def main():

    example_battle()
    # run_benchmark(n_battles=1, brief_cnt=1, use_prev_results=True, mode='squad')
    # run_benchmark(n_battles=1, brief_cnt=1, use_prev_results=True, mode='1v1')

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

if __name__ == '__main__':
    main()
