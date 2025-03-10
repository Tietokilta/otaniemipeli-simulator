from random import randint
from queue import Empty
from concurrent.futures import ProcessPoolExecutor, Future
import sys
import time

from matplotlib import pyplot as p
import numpy as np

from game import game, squares, drinks

nteams_opts = [4,5,6,7,8]
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
ndrinksbytype = [{d: 0 for d in drinks} for _ in nteams_opts]

bsize = 512
bmask = bsize - 1

def simulate(i: int, ngames: int):
    ndrinksavg = []
    nportionsavg = []
    ndrinkstop = []
    nportionstop = []
    nrounds = []
    nturns = []
    nvisits = [0 for _ in squares]
    nsqdrinks = [0 for _ in squares]
    nsqportions = [0 for _ in squares]
    ndrinksbytype = {d: 0 for d in drinks}

    nteams = nteams_opts[i]
    for j in range(ngames):
        try:
            res = game(nteams)
        except KeyboardInterrupt:
            break
        if ngames > bsize and j & bmask == bmask:
            print(f"\r{nteams} teams {j} games     ", end="", flush=True)
        ndrinksavg.append(res.avg_drinks)
        ndrinkstop.append(res.top_drinks)
        nportionsavg.append(res.avg_portions)
        nportionstop.append(res.top_portions)
        nrounds.append(res.rounds)
        nturns.append(res.turns)
        for k, visits in enumerate(res.visits):
            nvisits[k] += visits
        for k, sqdrinks in enumerate(res.sq_drinks):
            nsqdrinks[k] += sqdrinks
        for k, sqportions in enumerate(res.sq_portions):
            nsqportions[k] += sqportions
        for d in drinks:
            ndrinksbytype[d] += res.drinks_by_type[d]
    res = (
        i,
        ndrinksavg,
        nportionsavg,
        ndrinkstop,
        nportionstop,
        nrounds,
        nturns,
        nvisits,
        nsqdrinks,
        nsqportions,
        ndrinksbytype,
    )
    return res

if __name__ == "__main__":
    if sys.argv[3] == "m":
        pool = ProcessPoolExecutor()
        start = time.time()
        try:
            futs: list[Future] = []
            for i in range(len(nteams_opts)):
                for j in range(round(ngames / bsize)):
                    futs.append(pool.submit(simulate, i, bsize))
            total = 0
            for fut in futs:
                total += bsize
                res = fut.result()
                print(f"\rpool: {nteams_opts[res[0]]} teams {total} games", end="", flush=True)
                ndrinksavg[res[0]] += res[1]
                nportionsavg[res[0]] += res[2]
                ndrinkstop[res[0]] += res[3]
                nportionstop[res[0]] += res[4]
                nrounds[res[0]] += res[5]
                nturns[res[0]] += res[6]
                for s in range(len(squares)):
                    nvisits[res[0]][s] += res[7][s]
                    nsqdrinks[res[0]][s] += res[8][s]
                    nsqportions[res[0]][s] += res[9][s]
                for d in drinks:
                    ndrinksbytype[res[0]][d] += res[10][d]
        finally:
            pool.shutdown(True, cancel_futures=True)
            end = time.time()
            print(f"\n{end - start:.2f} seconds")
    elif sys.argv[3] == "s":
        for i in range(len(nteams_opts)):
            res = simulate(i, None)
            ndrinksavg[res[0]] = res[1]
            nportionsavg[res[0]] = res[2]
            ndrinkstop[res[0]] = res[3]
            nportionstop[res[0]] = res[4]
            nrounds[res[0]] = res[5]
            nturns[res[0]] = res[6]
            nvisits[res[0]] = res[7]
            nsqdrinks[res[0]] = res[8]
            nsqportions[res[0]] = res[9]
            ndrinksbytype[res[0]] = res[10]

    print()


    def analysis():
        exec(compile(open("analysis.py").read(), mode="exec", filename="analysis.py"))


    analysis()
