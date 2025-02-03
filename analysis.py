import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import *


THRESHOLD = 0.001

p.subplot(3, 2, 1)
p.title("Average portions per team " + sys.argv[1])
xmax = 0
for i, nteams in enumerate(nteams_opts):
    y, x = np.histogram(nportionsavg[i], bins=50)
    imax = np.nonzero(y > ngames * THRESHOLD)[0][-1]
    xmax = max(xmax, x[imax + 1])
    x = (x[1:] + x[:-1]) / 2
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 45)
p.grid(True)
p.legend()

p.subplot(3, 2, 2)
p.title("Portions for moral winner")
xmax = 0
for i, nteams in enumerate(nteams_opts):
    y, x = np.histogram(nportionstop[i], bins=50)
    imax = np.nonzero(y > ngames * THRESHOLD)[0][-1]
    xmax = max(xmax, x[imax + 1])
    x = (x[1:] + x[:-1]) / 2
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 55)
p.grid(True)
p.legend()

p.subplot(3, 2, 3)
p.title("Average drinks per team")
xmax = 0
for i, nteams in enumerate(nteams_opts):
    y, x = np.histogram(ndrinksavg[i], bins=40)
    imax = np.nonzero(y > ngames * THRESHOLD)[0][-1]
    xmax = max(xmax, x[imax + 1])
    x = (x[1:] + x[:-1]) / 2
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 45)
p.grid(True)
p.legend()

p.subplot(3, 2, 4)
p.title("Drinks for moral winner")
xmax = 0
for i, nteams in enumerate(nteams_opts):
    y = np.bincount(ndrinkstop[i])
    x = range(len(y))
    imax = np.nonzero(y > ngames * THRESHOLD)[0][-1]
    xmax = max(xmax, x[imax + 1])
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 55)
p.grid(True)
p.legend()

p.subplot(3, 2, 5)
p.title("Rounds in game")
xmax = 0
for i, nteams in enumerate(nteams_opts):
    y = np.bincount(nrounds[i])
    x = range(len(y))
    imax = np.nonzero(y > ngames * THRESHOLD)[0][-1]
    xmax = max(xmax, x[imax + 1])
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(15, 50)
p.grid(True)
p.legend()

p.subplot(3, 2, 6)
p.title("Turns in game")
xmax = 0
for i, nteams in enumerate(nteams_opts):
    y = np.bincount(nturns[i])
    x = range(len(y))
    imax = np.nonzero(y > ngames * THRESHOLD)[0][-1]
    xmax = max(xmax, x[imax + 1])
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(60, 270)
p.grid(True)
p.legend()

p.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.2)

p.show()

p.subplot(3, 1, 1)
p.title("Most visited squares " + sys.argv[1])

p.xticks(
    range(len(squares)), [sq.name for sq in squares], size="small", rotation="vertical"
)
p.grid(True)

for i, nteams in enumerate(nteams_opts):
    x = range(len(squares))
    y = nvisits[i]
    p.plot(x, y, label=f"{nteams} teams")
p.legend()

p.subplot(3, 1, 2)
p.title("Drinks/square")

p.xticks(
    range(len(squares)), [sq.name for sq in squares], size="small", rotation="vertical"
)
p.grid(True)

for i, nteams in enumerate(nteams_opts):
    x = range(len(squares))
    y = [v / ngames / nteams for v in nsqdrinks[i]]
    p.plot(x, y, label=f"{nteams} teams")
p.legend()

p.subplot(3, 1, 3)
p.title("Portions/square")

p.xticks(
    range(len(squares)), [sq.name for sq in squares], size="small", rotation="vertical"
)
p.grid(True)

for i, nteams in enumerate(nteams_opts):
    x = range(len(squares))
    y = [v / ngames / nteams for v in nsqportions[i]]
    p.plot(x, y, label=f"{nteams} teams")
p.legend()

p.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.3)
p.show()

fig, ax = p.subplots(layout="constrained")
ax.set_title("Drinks by type " + sys.argv[1])

bw = 1 / (1 + len(nteams_opts))
for i, nteams in enumerate(nteams_opts):
    x = np.arange(len(drinks)) + i * bw
    y = [ndrinksbytype[i][d] / ngames / nteams for d in drinks]
    ax.bar(x, y, bw, label=f"{nteams} teams")

ax.set_xticks(np.arange(len(drinks)) + bw, list(drinks))
p.show()
