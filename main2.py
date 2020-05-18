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

    DEFAULT_F = "C:\\Users\\berto\\Documents\\hashcode\\hashcode\\2020-qualif\\in\\d_tough_choices.txt"
    OUTPUT_F = "C:\\Users\\berto\\Documents\\hashcode\\hashcode\\2020-qualif\\out\\d_out.txt"

    parser = argparse.ArgumentParser(description='Hashcode 2020 qualif')
    parser.add_argument('-i', '--filein', help='Input file',default=DEFAULT_F, type=str)
    parser.add_argument('-o', '--fileout', help='Ouput file',default=OUTPUT_F, type=str)
    parser.add_argument('-v', '--verbose', default=-1,help='verbose mode', type=int)
    args = parser.parse_args()

    # map(int, [int(x) for x in re.sub("\n", "", f.readline()).split(" ")])
    # [int(x) for x in re.sub("\n", "", f.readline()).split(" ")]
    # [str(x) for x in re.sub("\n", "", f.readline()).split(" ")]

    # Input process
    with open(args.filein) as f:
        booksN,librarieN,deadline = map(int, f.readline().split(" "))
        line  = [int(x) for x in re.sub("\n", "", f.readline()).split(" ")]
        booksValue = {}
        for i in range(len(line)):
            booksValue[i]=line[i]
        librairies = []
        for i in range(librarieN):
            (j,librairiesBooksN,signupProcess) = map(int, f.readline().split(" "))
            books = [int(x) for x in re.sub("\n", "", f.readline()).split(" ")]
            books.sort(key = lambda x : booksValue[x],reverse=True)
            librairies.append([i,j,librairiesBooksN,signupProcess,books])
        booksDone = {}
    librairies.sort(key = lambda x : x[1]-20*x[2],reverse=True)
    # librairies.sort(key = lambda x : (x[2]+65*(x[3]/x[1])/(20*sum([booksValue[i] for i in x[4]]))))
    librairiesOutput = []
    for library in librairies:
        if not librairiesOutput:
            time=0
        else:
            lib = librairiesOutput[len(librairiesOutput)-1]
            time= lib[len(lib)-1]
        time+=library[2]
        currentTime = time
        libraryAndBooks = []
        libraryAndBooks.append(library[0])
        i=0
        while currentTime < deadline and i<len(library[4]):
            if library[4][i] not in booksDone:
                libraryAndBooks.append(library[4][i])
                booksDone[library[4][i]]=1
            if i%library[3]==0:
                currentTime+=1 
            i+=1   
        libraryAndBooks.append(time)
        if(len(libraryAndBooks)>2):
            librairiesOutput.append(libraryAndBooks)



    # output process
    with open(args.fileout,"w") as f:
        size = len(librairiesOutput)
        f.write(str(size)+"\n")
        for library in librairiesOutput:
            borne = len(library)-2
            f.write(str(library[0])+" "+str(borne)+"\n")
            ch = ""
            if borne!=0:
                for i in range(1,len(library)-2):
                    ch+=str(library[i])+" "
                ch+=str(library[len(library)-2])+"\n"
                f.write(ch)

