include "globals.mzn";
enum NOTES = {C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B};
array[int] of set of NOTES : CHORDS = [
                                        {C,E,G},  {C,Eb,G},
                                        {Db,F,Ab},{Db,E,Ab},
                                        {D,Gb,A}, {D,F,A},
                                        {Eb,G,Bb},{Eb,Gb,Bb},
                                        {E,Ab,B}, {E,G,B},

                                        {F,A,C}, {F,Ab,C},
                                        {Gb,Bb,Db},{Gb,A,Db},
                                        {G,B,D}, {G,Bb,D},
                                        {Ab,C,Eb}, {Ab,B,Eb},
                                        {A,Db,E}, {A,C,E},
                                        {Bb,D,F}, {Bb,Db,F},
                                        {B,Eb,Gb}, {B,D,Gb}
                                        ];
enum CHORD_NAMES = {CM,Cm,
                    DbM,Dbm,         
                    DM,Dm,         
                    EbM,Ebm,        
                    EM,Em,
                    FM,Fm,
                    GbM,Gbm,
                    GM,Gm,
                    AbM,Abm,
                    AM,Am,
                    BbM,Bbm,
                    BM,Bm};

array[1..1] of set of CHORD_NAMES : SCALE = [{CM, Dm, Em, FM, GM, Am}] ;

% INPUT
int : melody_length ;
array[1..melody_length] of NOTES : melody ;

array[1..melody_length] of var int : chord_nums ;
array[1..melody_length-1] of var int : chord_distances ;

function int : distance(NOTES : n1, NOTES: n2) =
            min([abs(n1-n2),abs(n2-n1),12-abs(n1-n2),12-abs(n2-n1)]);

function var int : chord_distance(var set of NOTES : c1,var set of NOTES: c2) =
            sum(n1 in c1)
                (min(n2 in c2)(distance(n1,n2))) ;

constraint forall(i in 1..melody_length-1)
        (chord_distances[i] = chord_distance(CHORDS[chord_nums[i]], CHORDS[chord_nums[i+1]])) ;

% Chords should all be different
constraint alldifferent(chord_nums);

% Chords should include the melody notes
constraint forall(i in 1..melody_length)(melody[i] in CHORDS[chord_nums[i]]);

% C Major diatonic chords
% constraint forall(i in 1..4)(CHORD_NAMES[chord_nums[i]] in SCALE[1]);

output["\(CHORDS[chord_nums[i]])" ++ if i=melody_length then "" else "|" endif | i in 1..melody_length] ++ ["\n"] ++
        ["\(CHORD_NAMES[chord_nums[i]]) " | i in 1..melody_length];