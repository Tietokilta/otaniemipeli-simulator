from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import List
from datetime import datetime

class PlaceType(str, Enum):
    normal = "normal"
    food = "food"
    sauna = "sauna"
    special = "special"
    guild = "guild"


class UserType(str, Enum):
    admin = "admin"
    ie = "ie"
    referee = "referee"
    secretary = "secretary"
    team = "team"

    def as_str(self) -> str:
        return self.value

    def display(self) -> str:
        # same behavior as Rust: lowercased string
        return self.value.lower()


@dataclass
class SocketAuth:
    token: str


@dataclass
class MessageBack:
    ok: bool
    echo: str


@dataclass
class LoginInfo:
    username: str
    password: str


@dataclass
class UserTypes:
    user_types: List[UserType] = field(default_factory=list)

    @classmethod
    def new(cls) -> "UserTypes":
        return cls()

    def push(self, user_type: UserType) -> None:
        self.user_types.append(user_type)


@dataclass
class UserInfo:
    uid: int
    username: str
    email: str
    user_types: UserTypes


@dataclass
class SessionInfo:
    uid: int
    session_hash: str
    user_types: UserTypes


@dataclass
class UserSessionInfo:
    user: UserInfo
    session: SessionInfo


@dataclass
class GameInfo:
    id: int
    name: str
    board: str
    finished: bool
    start_time: datetime  # equivalent of chrono::DateTime<Utc>


@dataclass
class PostGame:
    name: str
    board: int


@dataclass
class Games:
    games: List[GameInfo]


@dataclass
class Board:
    id: int
    name: str


@dataclass
class Boards:
    boards: List[Board]


@dataclass
class Place:
    place_id: int
    place_name: str
    rule: str
    place_type: PlaceType


@dataclass
class Places:
    places: List[Place]


@dataclass
class Connection:
    board_id: int
    origin: int
    target: int
    on_land: bool
    backwards: bool
    dashed: bool


# forward refs handled by __future__ import
@dataclass
class Drink:
    id: int
    name: str


@dataclass
class PlaceDrink:
    place_number: int
    board_id: int
    drink: Drink
    refill: bool
    optional: bool
    n: int
    n_update: str



@dataclass
class PlaceDrinks:
    drinks: List[PlaceDrink]


@dataclass
class BoardPlace:
    board_id: int
    place: Place
    place_number: int
    start: bool
    end: bool
    x: float
    y: float
    connections: List[Connection]
    drinks: PlaceDrinks


@dataclass
class BoardPlaces:
    board: Board
    places: List[BoardPlace]


@dataclass
class Ingredient:
    id: int
    name: str
    abv: float
    carbonated: bool


@dataclass
class Ingredients:
    ingredients: List[Ingredient]


@dataclass
class IngredientQty:
    ingredient: Ingredient
    quantity: float


@dataclass
class DrinkIngredients:
    drink: Drink
    quantity: float
    abv: float
    ingredients: List[IngredientQty]

    @cached_property
    def ethanol(self) -> float:
        return self.quantity * self.abv


@dataclass
class DrinkIngredientsPost:
    drink: Drink
    ingredients: List[IngredientQty]


@dataclass
class DrinksIngredients:
    drink_ingredients: List[DrinkIngredients]


@dataclass
class ResultIntJson:
    int: int


@dataclass
class Drinks:
    drinks: List[Drink]


@dataclass
class IngredientIdQuery:
    ingredient_id: int
