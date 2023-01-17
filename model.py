from ortools.sat.python import cp_model
import json

def create_basic_model() :
    model = None
    return model

def write_valid_chords_to_file() :
    chords = {}
    chords['major_chords'] = {}
    chords['minor_chords'] = {}
    chords['dim_chords'] = {}
    chords['aug_chords'] = {}
    with open('data/notes.json') as f :
        notes = json.load(f)
    for n, i in notes.items() :
        chords['major_chords'][n] = [i, i+4 % 12, i+7 % 12]
        chords['minor_chords'][n] = [i, i+3 % 12, i+7 % 12]
        chords['dim_chords'][n] = [i, i+3 % 12, i+6 % 12]
        chords['aug_chords'][n] = [i, i+4 % 12, i+8 % 12]

    with open('data/chords.json', 'w') as f :
        json.dump(chords,f, indent=2) 

if __name__ == '__main__' :
    write_valid_chords_to_file()
