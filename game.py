from dataclasses import dataclass, field, replace
from random import randint
from collections.abc import Callable
from functools import cached_property
from statistics import mean
import sys


def d6():
    return randint(1, 6)


def drinkroll_min():
    return min(d6(), d6())

def newroll_min() -> (int, bool):
    roll1 = d6()
    roll2 = d6()

    roll = min(roll1, roll2)
    is_double = roll1 == roll2

    return roll, is_double


@dataclass
class Drink:
    abv: float
    vol: float

    @cached_property
    def ethanol(self):
        return self.abv * 0.01 * self.vol


drinks: dict[str, Drink] = {}


for l in open("drinks.txt"):
    l = l.strip()
    if not l or l.startswith("//"):
        continue
    name, content = l.split(" ")
    bits = content.split(",")
    alc_total = 0
    vol_total = 0
    while bits:
        abv, vol, carb = bits[:3]
        bits = bits[3:]
        abv = float(abv.removesuffix("%"))
        vol = float(vol)
        vol_total += vol
        alc_total += abv * 0.01 * vol
    vol = vol_total
    abv = alc_total / vol_total if vol_total else 0.0
    drinks[name] = Drink(abv, vol)


PORTION = drinks["beer"].ethanol


@dataclass
class Square:
    name: str
    drinks: Callable[[int], list[Drink]] = field(default_factory=list)
    refill: bool = False
    teleport: str | None = None


sqtypes: dict[str, Square] = {}
place_file = sys.argv[1]
for l in open(place_file):
    l = l.strip()
    if not l or l.startswith("//"):
        continue
    name, *bits = l.split(" ")
    assert name not in sqtypes
    drinkfuncs = []
    refill = False
    while bits:
        bit = bits.pop(0)
        match bit:
            case "refill":
                refill = True
            case _:
                drinkfuncs.append(
                    eval(f"lambda drink: lambda nvisits: [drink] * {bits.pop(0)}")(
                        drinks[bit]
                    )
                )
    sqtypes[name] = Square(
        name,
        (
            lambda drinkfuncs: lambda nvisits: sum(
                (f(nvisits=nvisits) for f in drinkfuncs),
                [],
            )
        )(drinkfuncs),
        refill,
    )


squares: list[Square] = []
sqnames: dict[str, int] = {}
board_file = sys.argv[2]
for l in open(board_file):
    l = l.strip()
    if not l or l.startswith("//"):
        continue
    bits = l.split(" ")
    if bits[0].isdigit():
        mult = int(bits.pop(0))
    else:
        mult = 1
    tname = bits.pop(0)
    sq = replace(sqtypes[tname])
    for bit in bits:
        match bit[0]:
            case "#":
                sqnames[bit[1:]] = len(squares)
            case ">":
                sq.teleport = bit[1:]
            case _:
                raise ValueError(bit)
    for _ in range(mult):
        squares.append(sq)

endpos = next(i for i, sq in enumerate(squares) if sq.name == "end")


@dataclass
class Result:
    rounds: int
    turns: int
    top_portions: float
    avg_portions: float
    top_drinks: int
    avg_drinks: float
    visits: list[int]
    sq_drinks: list[int]
    sq_portions: list[float]


def game(nplayers: int):
    drunk = [False] * len(squares)
    visits = [0] * len(squares)
    sq_drinks = [0] * len(squares)
    sq_portions = [0] * len(squares)
    players = [0] * nplayers
    drinks = [0] * nplayers
    portions = [0.0] * nplayers
    rounds = 0
    turns = 0
    done = False
    while not done:
        rounds += 1
        for p in range(nplayers):
            turns += 1
            move, is_double = newroll_min()
            pos = players[p]
            if pos < endpos and pos + move > endpos: # going past end square
                extra = pos + move - endpos
                pos = endpos - extra
            elif pos + move >= len(squares): # leaving tampere
                pos = len(squares) - 1
            else: # other moves
                pos += move
            final_destination = False
            while not final_destination:
                players[p] = pos
                visits[pos] += 1
                sq = squares[pos]
                if not drunk[pos]:
                    to_drink: list[Drink] = sq.drinks(nvisits=visits[pos])
                    if is_double and sq.name != "varasto":
                        to_drink += to_drink[:]
                    now_drinks = len(to_drink)
                    now_portions = sum(d.ethanol for d in to_drink) / PORTION
                    if sq.name == "varasto":
                        ykkos_count = 2 if is_double else 1
                        drinker = p
                        for _ in range(ykkos_count):
                            while True:
                                if d6() == 1:
                                    drinks[p] += now_drinks
                                    portions[p] += now_portions
                                    break
                                else:
                                    drinker = (drinker + 1) % nplayers
                    else:
                        drinks[p] += now_drinks
                        portions[p] += now_portions
                        sq_drinks[pos] += now_drinks
                        sq_portions[pos] += now_portions
                    if not sq.refill:
                        drunk[pos] = True
                # teleporting
                if sq.name == "keto":
                    pos -= d6()
                elif sq.teleport:
                    pos = sqnames[sq.teleport]
                else:
                    final_destination = True
            if sq.name == "end":
                done = True
                break
    return Result(
        rounds,
        turns,
        max(portions),
        mean(portions),
        max(drinks),
        mean(drinks),
        visits,
        sq_drinks,
        sq_portions,
    )
