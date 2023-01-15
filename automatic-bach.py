import argparse
from musicpy import *
import re
from minizinc import Instance, Model, Solver

def play_guitar() :

    guitar = (C('CM7', 3, 1/4, 1/8)^2 |
            C('G7sus', 2, 1/4, 1/8)^2 |
            C('A7sus', 2, 1/4, 1/8)^2 |
            C('Em7', 2, 1/4, 1/8)^2 | 
            C('FM7', 2, 1/4, 1/8)^2 |
            C('CM7', 3, 1/4, 1/8)@1 |
            C('AbM7', 2, 1/4, 1/8)^2 |
            C('G7sus', 2, 1/4, 1/8)^2) * 2

    play(guitar, bpm=100, instrument=25)

def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument("melody")
    parser.add_argument("--minimize_distance", action='store_true')
    parser.add_argument("--a", action='store_true')

    args = parser.parse_args()
    melody = args.melody.strip().split() 

    model = Model("./automatic-bach.mzn")
    if args.minimize_distance :
        model.add_string("solve minimize sum(chord_distances)")
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)
    instance["melody"] = melody

    def print_results(result, a) :
        if a :
            for i in range(len(result)) :
                print(result[i,"_output_item"])
        else : 
            print(result)

    if args.minimize_distance :
        result = instance.solve(intermediate_solutions=True if args.a else False)
        print_results(result,args.a)

    else : 
        result = instance.solve(all_solutions=True if args.a else False)
        print_results(result,args.a)

    play_guitar()

if __name__=='__main__' :
    main()