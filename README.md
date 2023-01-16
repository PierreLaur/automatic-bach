## automatic-bach  

### Setup
Requirements :
- `pip install requirements.txt`
- Install [Minizinc](https://www.minizinc.org/) >= 3.5 (the version on apt is 3.4 as of jan 2023)

example usage :
- Generate a valid harmonization `python automatic-bach.py 'C C C C'`
- Generate all possible harmonizations in random order `python automatic-bach.py 'C C C C' --a`
- Find a solution that minimizes distance between chords `python automatic-bach.py 'C C C C' --minimize_distance`