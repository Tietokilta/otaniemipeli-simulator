from random import randint
import threading

from matplotlib import pyplot as p
import numpy as np

from game import game, squares

nteams_opts = [4, 5, 6, 7, 8]
ngames = 100000

n = [[] for _ in nteams_opts]
ndrinksavg = [[] for _ in nteams_opts]
nportionsavg = [[] for _ in nteams_opts]
ndrinkstop = [[] for _ in nteams_opts]
nportionstop = [[] for _ in nteams_opts]
nrounds = [[] for _ in nteams_opts]
nturns = [[] for _ in nteams_opts]
nvisits = [[0 for _ in squares] for _ in nteams_opts]
nsqdrinks = [[0 for _ in squares] for _ in nteams_opts]
nsqportions = [[0 for _ in squares] for _ in nteams_opts]

threads = []

for i in range(len(nteams_opts)):
    nteams = nteams_opts[i]
    for j in range(ngames):
        res = game(nteams)
        if j & 31 == 31:
            print(
                f"\r{nteams} teams {j} games     ",
                end="", flush=True)
        ndrinksavg[i].append(res.avg_drinks)
        ndrinkstop[i].append(res.top_drinks)
        nportionsavg[i].append(res.avg_portions)
        nportionstop[i].append(res.top_portions)
        nrounds[i].append(res.rounds)
        nturns[i].append(res.turns)
        for k, visits in enumerate(res.visits):
            nvisits[i][k] += visits
        for k, sqdrinks in enumerate(
                res.sq_drinks):
            nsqdrinks[i][k] += sqdrinks
        for k, sqportions in enumerate(
                res.sq_portions):
            nsqportions[i][k] += sqportions

print()


def analysis():
    exec(compile(open("analysis.py").read(), mode="exec", filename="analysis.py"))


analysis()
