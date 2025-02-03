from random import randint
from queue import Empty
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
import sys

from matplotlib import pyplot as p
import numpy as np

from game import game, squares

nteams_opts = [4, 6, 8]
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

def simulate(i: int, pipe: Connection | None):
    ndrinksavg = []
    nportionsavg = []
    ndrinkstop = []
    nportionstop = []
    nrounds = []
    nturns = []
    nvisits = [0 for _ in squares]
    nsqdrinks = [0 for _ in squares]
    nsqportions = [0 for _ in squares]

    nteams = nteams_opts[i]
    for j in range(ngames):
        res = game(nteams)
        if j & 127 == 127:
            if pipe:
                pipe.send(128)
            else:
                print(f"\r{nteams} teams {j} games     ", end="", flush=True)
        ndrinksavg.append(res.avg_drinks)
        ndrinkstop.append(res.top_drinks)
        nportionsavg.append(res.avg_portions)
        nportionstop.append(res.top_portions)
        nrounds.append(res.rounds)
        nturns.append(res.turns)
        for k, visits in enumerate(res.visits):
            nvisits[k] += visits
        for k, sqdrinks in enumerate(
                res.sq_drinks):
            nsqdrinks[k] += sqdrinks
        for k, sqportions in enumerate(
                res.sq_portions):
            nsqportions[k] += sqportions
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
    )
    if pipe:
        pipe.send(res)
    return res

if __name__ == "__main__":
    if sys.argv[3] == "m":
        procs: list[Process] = []
        recv, send = Pipe(False)
        for i in range(len(nteams_opts)):
            proc = Process(target=simulate, args=(i, send))
            procs.append(proc)
            proc.start()
        total = 0
        while alive := sum(proc.is_alive() for proc in procs):
            print(f"\r{alive} threads {total} games", end="", flush=True)
            while recv.poll(0.1):
                item = recv.recv()
                if isinstance(item, int):
                    total += item
                else:
                    ndrinksavg[item[0]] = item[1]
                    nportionsavg[item[0]] = item[2]
                    ndrinkstop[item[0]] = item[3]
                    nportionstop[item[0]] = item[4]
                    nrounds[item[0]] = item[5]
                    nturns[item[0]] = item[6]
                    nvisits[item[0]] = item[7]
                    nsqdrinks[item[0]] = item[8]
                    nsqportions[item[0]] = item[9]
            print()
    elif sys.argv[3] == "s":
        for i in range(len(nteams_opts)):
            item = simulate(i, None)
            ndrinksavg[item[0]] = item[1]
            nportionsavg[item[0]] = item[2]
            ndrinkstop[item[0]] = item[3]
            nportionstop[item[0]] = item[4]
            nrounds[item[0]] = item[5]
            nturns[item[0]] = item[6]
            nvisits[item[0]] = item[7]
            nsqdrinks[item[0]] = item[8]
            nsqportions[item[0]] = item[9]

    print()


    def analysis():
        exec(compile(open("analysis.py").read(), mode="exec", filename="analysis.py"))


    analysis()
