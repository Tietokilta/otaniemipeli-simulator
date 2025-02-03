import sys
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import *
    print("main imported")
else:
    raise ImportError("typing not imported")

try:
    os.remove("fig1.pdf")
    print("fig1.pdf removed")
except FileNotFoundError:
    print("fig1.pdf not found")
try:
    os.remove("fig2.pdf")
    print("fig2.pdf removed")
except FileNotFoundError:
    print("fig2.pdf not found")


THRESHOLD = 0.001

p.figure(figsize=(20, 40))

p.subplot(3, 2, 1)
p.title("Average portions per team " + sys.argv[1])
for i, nteams in enumerate(nteams_opts):
    y, x = np.histogram(nportionsavg[i], bins=50)
    x = (x[1:] + x[:-1]) / 2
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 45)
p.grid(True)
p.legend()

p.subplot(3, 2, 2)
p.title("Portions for moral winner")
for i, nteams in enumerate(nteams_opts):
    y, x = np.histogram(nportionstop[i], bins=50)
    x = (x[1:] + x[:-1]) / 2
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 55)
p.grid(True)
p.legend()

p.subplot(3, 2, 3)
p.title("Average drinks per team")
for i, nteams in enumerate(nteams_opts):
    y, x = np.histogram(ndrinksavg[i], bins=40)
    x = (x[1:] + x[:-1]) / 2
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 45)
p.grid(True)
p.legend()

p.subplot(3, 2, 4)
p.title("Drinks for moral winner")
for i, nteams in enumerate(nteams_opts):
    y = np.bincount(ndrinkstop[i])
    x = range(len(y))
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(10, 55)
p.grid(True)
p.legend()

p.subplot(3, 2, 5)
p.title("Rounds in game")
for i, nteams in enumerate(nteams_opts):
    y = np.bincount(nrounds[i])
    x = range(len(y))
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(15, 50)
p.grid(True)
p.legend()

p.subplot(3, 2, 6)
p.title("Turns in game")
for i, nteams in enumerate(nteams_opts):
    y = np.bincount(nturns[i])
    x = range(len(y))
    p.plot(x, y, label=f"{nteams} teams")
p.xlim(60, 270)
p.grid(True)
p.legend()

if "save" in sys.argv:
    p.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.2)
    p.savefig("fig1.pdf", dpi=100000, bbox_inches='tight', pad_inches=0.1)
else:
    p.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.2)
    p.show()

p.figure(figsize=(30, 100))
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

if "save" in sys.argv:
    p.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.2)
    p.savefig("fig2.pdf", dpi=100000, bbox_inches='tight', pad_inches=0.1)
else:
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
ax.set_ylim(0, 20)

p.show()
