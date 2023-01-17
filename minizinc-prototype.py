import time
from minizinc import Instance, Model, Solver
from play_notes import Player
import argparse
from random import shuffle


def note_to_int(note):
    if note == 'C':
        return 0
    if note in ['C#', 'Db']:
        return 1
    if note == 'D':
        return 2
    if note in ['D#', 'Eb']:
        return 3
    if note in ['E', 'Fb']:
        return 4
    if note in ['F', 'E#']:
        return 5
    if note in ['F#', 'Gb']:
        return 6
    if note == 'G':
        return 7
    if note in ['G#', 'Ab']:
        return 8
    if note == 'A':
        return 9
    if note in ['A#', 'Bb']:
        return 10
    if note in ['B', 'Cb']:
        return 11
    else:
        print('Incorrect note')
        return


def parse_chord(chord):
    return list(map(note_to_int, chord[1:-1].split(', ')))


def display_results(melody, result, a):
    player = Player()
    melody = list(map(note_to_int, melody))
    if a:
        shuffled_result = [result[i, "_output_item"].split('\n') for i in range(len(result))]
        shuffle(shuffled_result)
        for i in range(len(result)):
            chords_notes, chord_names = shuffled_result[i]
            print(f'Solution {i+1} :    {chord_names}')
            chords_notes = [parse_chord(chord)
                            for chord in chords_notes.split('|')]
            for chord_number, chord in enumerate(chords_notes):
                player.play_chord(chord)
                player.play_note(melody[chord_number]+12)
                player.stop_playing()
            time.sleep(1)
    else:
        chords_notes, chord_names = result["_output_item"].split('\n')
        print(f'Solution  :    {chord_names}')
        chords_notes = [parse_chord(chord)
                        for chord in chords_notes.split('|')]

        for chord_number, chord in enumerate(chords_notes):
            player.play_chord(chord)
            player.play_note(melody[chord_number]+12)
            player.stop_playing()

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("melody")
    parser.add_argument("--minimize_distance", action='store_true')
    parser.add_argument("--a", action='store_true')
    parser.add_argument("--max_number_dims", type=int)

    args = parser.parse_args()
    melody = args.melody.strip().split()

    model = Model("./minizinc-prototype.mzn")
    if args.minimize_distance:
        model.add_string("solve minimize sum(chord_distances);")
    else :
        model.add_string("solve::int_search(chord_nums,input_order,indomain_random) satisfy;")

    model.add_string("constraint sum(chord_distances) <= melody_length*3;")

    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)
    instance["melody"] = melody
    instance["melody_length"] = len(melody)

    if args.minimize_distance:
        result = instance.solve(
            intermediate_solutions=True if args.a else False)

    else:
        result = instance.solve(all_solutions=True if args.a else False)

    display_results(melody, result, args.a)


if __name__ == '__main__':
    main()
