# numbWing Xwing Numeric Simulation

A tool for rapidly simulating xwing psqudo game result for the purposes of ship/upgrade/strategy analysis.

## Getting Started

<<<<<<< HEAD
Create a folder for numbWing use, e.g. *.../numbWing*
Pull this project into a subfolder, e.g. *.../numbWing/code*
Copy example_run.py from *.../numbWing/code* to *.../numbWing*
Run example_run.py, log should be output to your terminal, and result data and plots should be output to a *.../numbWing/results*

### Prerequisites

Python 2.7 with atleast numPy and pandas. 
	If you dont already have Python 2.7, you can just install the Anaconda distro and not have to worry about pacakges
		https://repo.anaconda.com/archive/Anaconda2-5.3.0-Windows-x86_64.exe
Some form of IDE is reccomended,  e.g. pyCharm, is reccommended. It will make the code much easier to edit and run and the output more convienient to view.
=======
1. Create a folder for numbWing use, henforth referred to as *.../numbwWing* (can actually be named whatever)
2. Clone this code into a subfolder called 'code'. The path to numbWing.py should be *.../numbWing/code/numbWing.py*
3. Copy example_run.py from *.../numbWing/code* to *.../numbWing*
4. Run example_run.py, log should be output to your terminal, and result data and plots should be output to a *.../numbWing/results*
5. Comment/decomment various function, and change parameters, rerun, etc. as desired in your copy of example_run.py

### Prerequisites

Python 2.7 with numpy and pandas installed
	If you dont already have Python 2.7, you can just install the Anaconda distro and not have to worry about pacakges
		https://repo.anaconda.com/archive/Anaconda2-5.3.0-Windows-x86_64.exe
Some form of IDE,  e.g. pyCharm, is reccommended. For the normal reasons, plus I a lot of long enums (constant variable name) are used so autocomplete is great.
>>>>>>> de3179ab2b88d910a55309faba731782fffc7a02


## Running the examples

<<<<<<< HEAD
By default example_run.py will the main() function which will call example_battle(). Calls to benchmark() configured for both squad and 1v1 mode are present but commented out.

### main()

The main function is the function that's alway called first, create/copy/edit function calls here to change what is performed.
```
def main():
```

### building_teams()

Team objects instantiates for Red/Onyx team. Luke and Wedge are added to Red, with 4 Tie/LN Academy Pilots added to Onyx.

```
	team_1 = Team('Red Squad')
    team_1.add(xw.t65xwing_rebel.wedgeantilles)
	...
```

### Exampel battle

Battle 50 times, log 1 of those, report battle summary

```
battle.fight(50, log_cnt=1, battle_summary_choice=True)
```

### 1v1 Benchmark

Simple implementation of a 1v1 benchmark. Cycles through all ships and conduct 1v1 battles against a 3/2 ship which always shoots first

```
battle.fight(50, log_cnt=1, battle_summary_choice=True)
```

### Squad Benchmark

Simple implementation of a squad benchmark. Cycles through all ships, assemble them in squads totalling as near 200 as possible (can go over) and conduct battles against a 4x 3/2/X ships with increasing health

```
battle.fight(50, log_cnt=1, battle_summary_choice=True)
=======
By default main() will execute first when you run example_run.py. Here you can keep your various method(function) calls. Use If statements or comments to turn call on/off.
```
def main():
	...
```

### example_match

Team objects instantiated for Red/Onyx team. Luke and Wedge are added to Red, with 4 Tie/LN Academy Pilots added to Onyx.

```
	team_1 = Team('Red Squad')
	team_1.add(xw.t65xwing_rebel.wedgeantilles)
	...
	team_2 = Team('Onyx Squad')
	team_2.add(xw.tielnfighter_galactic.academypilot)
	...
	match = Match(team_1, team_2)
	match.fight(50, brief_cnt=3, print_match_summary=True))
```

### run_benchrark - 1v1

Simple implementation of a generic ship 1v1 benchmark. Cycles through all ships and conduct 1v1 battles against a 3/2 ship which always shoots first

```
    run_benchmark(n_matches=50, log_cnt=1, brief_logs=True, mode='1v1', print_match_summary=True,
                  benchmark_attack=3, benchmark_defense=2)
```

### run_benchrark - squad

Simple implementation of a generic squad benchmark. Cycles through all ships, assemble them in squads totalling as near 200 as possible (can go over) and conduct battles against a 4x 3/2/X ships with increasing health

```
    run_benchmark(n_matches=50, log_cnt=0,  mode='squad', use_prev_results=True,
                  ships='all', benchmark_attack=3, print_match_summary=False)
>>>>>>> de3179ab2b88d910a55309faba731782fffc7a02
```

## Authors

* **prauxim** - *Initial work* - [prauxim](https://github.com/PurpleBooth)

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to guidokessels for [xwing-data2](https://github.com/guidokessels/xwing-data2) from which I source ships names and stats 

