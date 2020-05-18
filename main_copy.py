import sys
import os
import time
import argparse
import re
from copy import copy, deepcopy
import pulp
from functools import reduce
import pickle
import multiprocessing
import random
import datetime
import tqdm
# import matplotlib.pyplot as plt


#########################################################
# Lire 3 fois le problème
# Communiquer afin de bien être d'accord sur ce qu'il faut faire (le sujet du problème)
# Mettre sujet sur téléphone

# Voir ensemble algo:
#   - complexité
#   - structure de données à utiliser
#   - structure principale du code (étapes importantes)
#   - Performances (travailler avec des index, faire des listes et dictionnaire constant, optimiser la boucle appelée le plus de fois)
#   - les différentes input
#   - analogie avec un ancien problème ou autre
#
# Checkpoint:
#   toute les 30 minutes
#
#
#########################################################
if __name__ == '__main__':

    file = "d_tough_choices"
    DEFAULT_F = "C:\\Users\\antoi\\Documents\\GitHub\\hashcode\\2020-qualif\\in\\d_tough_choices.txt"
    OUTPUT_F = "C:\\Users\\antoi\\Documents\\GitHub\\hashcode\\2020-qualif\\out\\d_tough_choices.txt"

    parser = argparse.ArgumentParser(description='Hashcode 2020 qualif')
    parser.add_argument('-i', '--filein', help='Input file',
                        default=DEFAULT_F, type=str)
    parser.add_argument('-o', '--fileout', help='Ouput file',
                        default=OUTPUT_F, type=str)
    parser.add_argument('-v', '--verbose', default=-1,
                        help='verbose mode', type=int)
    args = parser.parse_args()

    # map(int, [int(x) for x in re.sub("\n", "", f.readline()).split(" ")])
    # [int(x) for x in re.sub("\n", "", f.readline()).split(" ")]
    # [str(x) for x in re.sub("\n", "", f.readline()).split(" ")]

    # Input process
    with open(args.filein) as f:
        booksN, librarieN, deadline = map(
            int, [int(x) for x in re.sub("\n", "", f.readline()).split(" ")])
        booksValue = [int(x)
                      for x in re.sub("\n", "", f.readline()).split(" ")]
        booksValue = [(i, booksValue[i]) for i in range(len(booksValue))]

        librairies = []
        for i in range(librarieN):
            (librairiesBooksN, signupProcess, booksPerDay) = map(
                int, [int(x) for x in re.sub("\n", "", f.readline()).split(" ")])
            books = [int(x) for x in re.sub("\n", "", f.readline()).split(" ")]
            librairies.append(
                [i, librairiesBooksN, signupProcess, booksPerDay, books])

    booksValue2 = sorted(booksValue, key=lambda c: c[1], reverse=True)
    booksIDSortedPerValue = [i[0] for i in booksValue2]

    def priority_sort(to_sort, order):
        priority = {e: p for p, e in enumerate(order)}
        r = list(sorted(to_sort, key=lambda e: priority[e]))
        return r

    # A refaire
    def compute_librairie_book_score(booksValue, lib, time):
        score = 0
        i = 0
        t = 0
        booksPerDay = lib[3]
        books = []
        while(i < len(lib[4]) and t < time):
            for i in range(i, min(i+booksPerDay, len(lib[4]))):
                score += booksValue[lib[4][i]][1]
                books.append(lib[4][i])
            t += 1
            i += 1
        return score, time-t, books

    def get_Best_librairies(librairies, booksValue, deadline, timeNow,moySignupProcess):
        librairies_scores = []
        for lib in librairies:
            libIndex = lib[0]
            signupTime = lib[2]
            time = deadline-timeNow-1-signupTime
            score, free_day, books = compute_librairie_book_score(booksValue, lib, time)
            librairies_scores.append((libIndex, score, free_day, books, signupTime))
        
        libSortedScore = sorted(librairies_scores, key=lambda c: c[1], reverse=True)
        sol = 1000000
        index = 0
        best  = libSortedScore[0]
        if((len(librairies))>10):
            coeff = int(len(librairies)/10)
        else:
            coeff = len(librairies)
        for l in libSortedScore[0:coeff]:
            if(l[2]<sol):
                sol= l[4]
                best = l
        return best[0], best[3]


        # for score,free in zip(librairies_scores,librairies_free_day):
        #     if()

    librairieBookScore = []
    timeNow = 0
    moySignupProcess = 0
    # livre dans les bibliothèques triées par valeur
    for i, lib in enumerate(librairies):
        lib[4] = priority_sort(lib[4], booksIDSortedPerValue)
        moySignupProcess+=lib[2]
    print("ok")
    moySignupProcess=moySignupProcess/len(librairies)

    print("moyenne signup process : %d"%(moySignupProcess))

    librairies_ordered_by_start = []
    timeNow = 0
    final = []
    pbar = tqdm.tqdm(total = len(librairies))
    while(timeNow < deadline-1 and len(librairies) > 0 and timeNow < deadline):
        next_lib, books = get_Best_librairies(librairies, booksValue, deadline, timeNow,moySignupProcess)
        librairies_ordered_by_start.append(next_lib)
        for i, l in enumerate(librairies):
            if l[0] == next_lib:
                next_lib = deepcopy(l)
                break
        del librairies[i]
        timeNow += next_lib[2]
        if(len(books)>0):
            final.append((next_lib[0], books))
        pbar.update(1)
        pbar.set_postfix(file=file,timeNow=timeNow)
        # mettre a jour les autres
        for x, l in enumerate(librairies):
            for i, book in enumerate(l[4]):
                if(book in books):
                    del librairies[x][4][i]


    timeNow = 0

    # output process
    with open(args.fileout, "w") as f:
        f.write(str(len(final))+"\n")
        for l in final:
            f.write(str(l[0])+" "+str(len(l[1]))+"\n")
            for b in l[1]:
                f.write(str(b)+" ")
            f.write("\n")

