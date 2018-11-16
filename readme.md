# numbWing Xwing Numeric Simulation

A tool for rapidly simulating xwing pseudo-game results for the purposes of ship/upgrade/strategy analysis.

See [this document](https://docs.google.com/spreadsheets/d/1VnyW3T58IwbWJut5lsA-ENhPpKDiGgfEvwx1bO5U_E0/edit?usp=sharing) for more info and example results

The below information is only for those wishing to run the code, which is in a pre-alpha state. While the examples should run, setup may be non-trivial, and the code may not be very stable if parameters are changed. You've been warned!

## Getting Started

1. Create a folder for numbWing use, henforth referred to as *.../numbwWing* (can actually be named whatever)
2. Clone this code into a subfolder called 'code'. The path to numbWing.py should be *.../numbWing/code/numbWing.py*
3. Copy example_run.py from *.../numbWing/code* to *.../numbWing*
4. Run example_run.py, log should be output to your terminal, and result data and plots should be output to a *.../numbWing/results*
5. Comment/decomment various function, and change parameters, rerun, etc. as desired in your copy of example_run.py

### Prerequisites
1
Python 2.7 with numpy and pandas installed
	If you dont already have Python 2.7, you can just install the Anaconda distro and not have to worry about pacakges
		https://repo.anaconda.com/archive/Anaconda2-5.3.0-Windows-x86_64.exe
Some form of IDE,  e.g. pyCharm, is reccommended. For the normal reasons, plus I a lot of long enums (constant variable name) are used so autocomplete is great.


## Running the examples

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
```

## Authors

* **prauxim** - *Initial work* - [prauxim](https://github.com/PurpleBooth)

## License

This project is licensed under the GPLv2 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to guidokessels for [xwing-data2](https://github.com/guidokessels/xwing-data2) from which I source ships names and stats 

