include "globals.mzn";
enum NOTES = {C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B};
array[int] of set of NOTES : CHORDS = [
                                        {C,E,G},  {C,Eb,G},  {C,Eb,Gb},
                                        {Db,F,Ab},{Db,E,Ab}, {Db,E,G},
                                        {D,Gb,A}, {D,F,A},   {D,F,Ab},
                                        {Eb,G,Bb},{Eb,Gb,Bb},{Eb,Gb,A},
                                        {E,Ab,B}, {E,G,B},   {E,G,Bb},

                                        {F,A,C}, {F,Ab,C},   {F,Ab,B},
                                        {Gb,Bb,Db},{Gb,A,Db},  {Gb,A,C},
                                        {G,B,D}, {G,Bb,D},   {G,Bb,Db},
                                        {Ab,C,Eb}, {Ab,B,Eb},   {Ab,B,D},
                                        {A,Db,E}, {A,C,E},   {A,C,Eb},
                                        {Bb,D,F}, {Bb,Db,F},   {Bb,Db,E},
                                        {B,Eb,Gb}, {B,D,Gb},   {B,D,F}
                                        ];
enum CHORD_NAMES = {CM,Cm,Cdim,
                    DbM,Dbm,Dbdim,          
                    DM,Dm,Ddim,         
                    EbM,Ebm,Ebdim,         
                    EM,Em,Edim,
                    FM,Fm,Fdim,
                    GbM,Gbm,Gbdim,
                    GM,Gm,Gdim,
                    AbM,Abm,Abdim,
                    AM,Am,Adim,
                    BbM,Bbm,Bbdim,
                    BM,Bm,Bdim};

array[1..1] of set of CHORD_NAMES : SCALE = [{CM, Dm, Em, FM, GM, Am, Bdim}] ;

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