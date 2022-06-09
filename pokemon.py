"""
=== Assignment 1 ===
CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Marina Tawfik, Saima Ali.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Marina Tawfik, Saima Ali.
"""

from __future__ import annotations
from typing import Optional, List, Dict, Tuple, TextIO


def load_trainers(f_trainers: TextIO, world: World) -> None:
    """Populate world with the trainers available in the open text file
    f_trainers.

    See the a1 handout for a description of the file structure.

    You will need to create all of the pokemon for each trainer, then
    make use of World.add_trainer() and world.add_pokemon().

    HINT: use world.get_pokemon_type and world.get_pokemon_weakness

    Preconditions:
        - Pokemon type to name and type to weakness mapping has been
        populated.
        - f is open and is set to the beginning of the file.
        - The file has >= 1 lines
    """
    t = None
    for line in f_trainers:
        if line != '':
            if line.startswith('TRAINER:'):
                s = line.split(':')[-1].strip().lower()
                # print(s)
                n = f_trainers.readline()
                n = n.split(':')[-1].strip()
                t = Trainer(s, int(n))
                world.add_trainer(t)
            elif line.startswith('POKEMON:'):
                p = line.split(':')[-1].strip().lower()
                # print(p)
                lvl = f_trainers.readline().split(':')[-1].strip()
                # print(lvl)
                max_hp = f_trainers.readline().split(':')[-1].strip()
                # print(max_hp)
                attk = f_trainers.readline().split(':')[-1].strip()
                # print(attk)
                defense = f_trainers.readline().split(':')[-1].strip()
                # print(defense)
                pk_type = world.get_pokemon_type(p)
                weakness = world.get_pokemon_weakness(pk_type)
                # pk_type = world.get_pokemon_type(p)
                pkmn = Pokemon(p, pk_type, weakness, int(lvl), int(max_hp),
                               int(attk), int(defense))
                world.add_pokemon(pkmn)
                if t is not None:
                    t.add_pokemon(pkmn)


def load_pokemon_types(f_pokemon: TextIO) -> Dict[str, List[str]]:
    """ Given the the open text file f_pokemon, return a dictionary where
    each key is a pokemon elemental type and the corresponding value is the
    list of pokemon names with that elemental type.
    """
    # This function is implemented for you, do NOT change it!
    curr_type = None

    mapping = {}
    for line in f_pokemon:
        line = line.strip()

        if line != "":
            if line.startswith("TYPE"):
                curr_type = line.split(":")[-1].strip().lower()
                mapping[curr_type] = []
            else:
                mapping[curr_type].append(line.strip().title())

    return mapping


def load_pokemon_weakness(
        f_pokemon_weakness: TextIO
) -> Dict[str, Dict[str, float]]:
    """ Given the the open text file f_pokemon_weakness, return a dictionary
    where each key is a pokemon elemental type and the corresponding value
    is a dictionary that provides the mapping between a pokemon type and its
    corresponding added battle advantage.
    """
    # This function is implemented for you, do NOT change it!
    mapping = {}
    for line in f_pokemon_weakness:
        line = line.strip()
        ws_index = line.index("\t")
        curr_type = line[0:ws_index].strip().lower()

        weaknesses = line[ws_index + 1:].strip()
        weakness_mapping = {}
        for weakness in weaknesses.split(","):
            if weakness.strip() != "":
                contents = weakness.strip().split(":")
                opponent_type = contents[0].strip().lower()
                weakness_mapping[opponent_type] = float(contents[1])

        if curr_type != "":
            mapping[curr_type] = weakness_mapping

    return mapping


class Pokemon:
    """A pokemon.

    === Instance Attributes ===
    name: The name of this Pokemon.
    type: The elemental type of this Pokemon.
    weakness: The Pokemon elemental types to which this pokemon is susceptible
        to extra damage. The keys is the elemental type to which this pokemon
        is susceptible, and the corresponding value is representative of the
        amount of extra damage inflicted by the elemental type on the current
        Pokemon.
    attack_points: The amount of damage this Pokemon inflicts on other Pokemon.
    defense_points: The amount of damage this Pokemon can avoid.
    level: The current level of this Pokemon.
    max_hp: The maximum value of health points this Pokemon can have.
    curr_hp: The current health points of this Pokemon. The pokemon starts with
        full health points.
    fainted: Whether this pokemon is fainted. The Pokemon is initially not
        fainted.
    in_hospital: Whether this pokemon is currently hospitalized. The Pokemon
        is initially not hospitalized.
    owner: The owner of this Pokemon; None if it is a wild Pokemon.

    === Representation Invariants ===
    - For each value, v, of weakness, 0.0 <= v <= 1.0
    - attack_points >= 1
    - defense_points >= 1
    - level >= 1
    - max_hp >= 1
    - curr_hp >= 1
    - name == name.title()
    - curr_hp == 0 if the pokemon is fainted, and if the pokemon is
        fainted curr_hp == 0

    === Sample Usage ===
    >>> pokemon = Pokemon(
    ...     "pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
    ... )
    >>> pokemon.name == 'Pikachu'
    True
    >>> pokemon.type == 'electric'
    True
    >>> pokemon.attack_points
    10
    >>> pokemon.defense_points
    5
    >>> "ground" in pokemon.weakness
    True
    >>> pokemon.weakness["ground"]
    1.0
    >>> print(pokemon.owner)
    None
    >>> pokemon.max_hp
    100
    >>> pokemon.curr_hp
    100
    >>> pokemon.fainted
    False
    >>> pokemon.in_hospital
    False
    """
    name: str
    type: str
    weakness: Dict[str, float]
    attack_points: int
    defense_points: int
    level: int
    max_hp: int
    curr_hp: int
    fainted: bool
    in_hospital: bool
    owner: Optional[Trainer]

    def __init__(
            self, name: str, pokemon_type: str, weakness: Dict[str, float],
            level: int, max_hp: int, attack_points: int, defense_points: int
    ) -> None:
        """Initialize this Pokemon.

        Pokemon starts as a wild Pokemon (with no owner), healthy
        and with the maximum value possible of health points.

        See class-level docstring for example usage.
        """
        self.name = name.title()
        self.type = pokemon_type
        self.weakness = weakness
        self.level = level
        self.max_hp = max_hp
        self.attack_points = attack_points
        self.defense_points = defense_points
        self.fainted = False
        self.in_hospital = False
        self.owner = None
        self.curr_hp = max_hp

    def __str__(self) -> str:
        """Return a str representing this Pokemon.
        """
        # This method is implemented for you, do NOT change it!
        weakness_str = "None" \
            if len(self.weakness) == 0 \
            else "\n\t\t" + "\n\t\t".join(self.weakness.keys())

        return f"{self.name} [LVL {self.level}]\n" + \
               f"\tTYPE:\t{self.type}\n" + \
               f"\tWEAKNESS TO:\t{weakness_str}" + \
               f"\tHP:\t{self.curr_hp}/{self.max_hp}\n" + \
               f"\tATK:\t{self.attack_points}\n" + \
               f"\tDEF:\t{self.defense_points}"


class Trainer:
    """A Pokemon trainer.

    === Instance Attributes ===
    name: The name of this Pokemon trainer, title-cased.
    level: The level of this Pokemon trainer.
    num_pokeballs: The number of pokeballs owned by this Pokemon trainer.
    coins: The number of coins owned by this Pokemon trainer.

    === Private Attributes ===
    _all_pokemon: A list of all Pokemon owned by this trainer.
    _battles: A record of all the battles this trainer has participated in.
        Each key is an opponent that this trainer has battled against. The
        corresponding value is a tuple, where the first element is the number of
        battles won by this trainer and the second element is the number of
        battles won by the opponent.

    === Representation Invariants ===
    - name == name.title()
    - level >= 1
    - num_pokeballs >= 0
    - coins >= 0
    - For each key, k, of _battles, k._battles[0] == _battles[k][1] and
        k._battles[1] == _battles[k][0]
    - For each value, v, of _battles, v[0] >= 0 and v[1] >= 0

    === Sample Usage ===
    >>> ash = Trainer("Ash")
    >>> ash.name == "Ash"
    True
    >>> ash.level
    1
    >>> ash.num_pokeballs
    10
    >>> ash.coins
    10
    >>> pikachu = Pokemon("Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    >>> ash.add_pokemon(pikachu)
    >>> pikachu.owner == ash
    True
    """
    name: str
    level: int
    num_pokeballs: int
    coins: int
    _all_pokemon: List[Pokemon]
    _battles: Dict[Trainer, Tuple[int, int]]

    def __init__(
            self, name: str, level: int = 1, num_pokeballs: int = 10,
            coins: int = 10
    ) -> None:
        """Initialize this Pokemon trainer with the provided name (title-cased),
        level, number of pokeballs num_pokeballs, the amount of coins coins,
        no owned Pokemon, and no battles.

        See class-level docstring for usage examples.
        """
        self.name = name.title()
        self.level = level  # or self.level = level
        self.num_pokeballs = num_pokeballs
        self.coins = coins
        self._all_pokemon = []
        self._battles = {}

    def add_pokemon(self, pokemon: Pokemon) -> None:
        """Add a pokemon to this trainer's pokemon collection by modifying the
        _all_pokemon attribute. Appends the pokemon to _all_pokemon
        if the pokemon is not in _all_pokemon.

        Do nothing if pokemon is already included in the trainer's collection.

        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> ash = Trainer("Ash")
        >>> ash.add_pokemon(pikachu)
        >>> len(ash.get_all_pokemon())
        1
        >>> ash.add_pokemon(pikachu)
        >>> len(ash.get_all_pokemon())
        1
        >>> pikachu.owner == ash
        True
        """
        # This method is implemented for you. Do NOT change it!
        if pokemon not in self._all_pokemon:
            self._all_pokemon.append(pokemon)
            pokemon.owner = self

    def get_all_pokemon(self) -> List[Pokemon]:
        """Return a shallow copy of the trainer's pokemon collection,
        _all_pokemon

        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> ash = Trainer("Ash")
        >>> ash.add_pokemon(pikachu)
        >>> trainer_pokemon = ash.get_all_pokemon()
        >>> pikachu in trainer_pokemon
        True
        >>> trainer_pokemon.remove(pikachu)
        >>> len(trainer_pokemon)
        0
        >>> len(ash.get_all_pokemon())
        1
        """
        # shallow_copy = []
        # for pokemon in self._all_pokemon:
        #     shallow_copy = shallow_copy + [pokemon]
        #
        # return shallow_copy
        shallow_copy = []
        for pokemon in self._all_pokemon:
            shallow_copy.append(pokemon)
        return shallow_copy

    def choose_pokemon(
            self, opposing_pokemon: Optional[Pokemon]
    ) -> Optional[Pokemon]:
        """Choose a Pokemon to send to battle.

        In this context, "available Pokemon" refers to Pokemon
        that are neither fainted nor hospitalized.

        If opposing_pokemon is None, return the trainer's pokemon
        with the highest level.

        If opposing_pokemon is not None, return the highest-level available
        Pokemon that provides the highest advantage based on the
        opposing_pokemon's weakness.

        In the case of ties, return any of tied Pokemon.

        Return None if this trainer has no Pokemon.

        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> squirtle = Pokemon(
        ...     "Squirtle", "water", {"grass" : 0.5, "electric": 0.7},
        ...     1, 100, 10, 5
        ... )
        >>> bulbasaur = Pokemon(
        ...     "Bulbasaur", "grass",
        ...     {"fire" : 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        ...     1, 100, 10, 5
        ... )
        >>> sandshrew = Pokemon(
        ...     "Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1},
        ...     1, 100, 5, 15
        ... ) # sandshrew has a higher weakness to grass than water
        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> ash.add_pokemon(pikachu)
        >>> ash.add_pokemon(squirtle)
        >>> ash.add_pokemon(bulbasaur)
        >>> ash.choose_pokemon(sandshrew).name == 'Bulbasaur'
        True
        """
        available_pokemon = self._get_available_pokemon()
        # highest_level = self._get_highest_level()
        # max_level = highest_level.level

        if available_pokemon is not None:

            highest_level = self._get_highest_level()
            max_level = highest_level.level

            if opposing_pokemon is None:
                return highest_level

            elif opposing_pokemon is not None:
                highest_level_pokemon = []
                for pkm in available_pokemon:
                    if pkm.level == max_level:
                        highest_level_pokemon.append(pkm)
                all_types = []
                for pkm in highest_level_pokemon:
                    all_types.append(pkm.type)

                new_dict = {}
                for w in all_types:
                    if w in opposing_pokemon.weakness:
                        new_dict[w] = opposing_pokemon.weakness[w]
                if new_dict == {}:
                    return highest_level
                max_weakness = max(new_dict, key=new_dict.get)
                for pkm in highest_level_pokemon:
                    if pkm.type == max_weakness:
                        return pkm
        else:
            return None
        return None
        # We need to get the highest level Pokemons
        # Break the tie between the highest level Pokemon by choosing one
        # that has the advantage over the opposing.

    def _get_available_pokemon(self) -> Optional[List[Pokemon]]:
        """Return List of Pokemon who are not in hospital or fainted.

        """
        all_pokemon = self.get_all_pokemon()
        available_pokemon = []
        if all_pokemon:
            for pokemon in all_pokemon:
                if pokemon.fainted is False and pokemon.in_hospital is False:
                    available_pokemon = available_pokemon + [pokemon]
        if available_pokemon:
            return available_pokemon
        else:
            return None

    def _get_highest_level(self) -> Optional[Pokemon]:
        """Return the Pokemon with the highest level from a list of Pokemon who
        are not in hospital or are not fainted.

        """
        available_pokemon = self._get_available_pokemon()
        if available_pokemon:
            level_list = []

            for pokemon in available_pokemon:
                level_list.append(pokemon.level)
            max_level = max(level_list)
            which_index = level_list.index(max_level)
            highest_level = available_pokemon[which_index]

            return highest_level
        else:
            return None

    def get_win_rate(self) -> Optional[float]:
        """Return the rate of battles won by this trainer, rounded to the
        tenth decimal place.

        The win rate of a trainer is defined as

            win rate = (# of wins) / (total # of battles)

        Return None If the trainer has not participated in any battles.

        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> misty = Trainer("Misty", 1, 5, 15)
        >>> ash.get_win_rate() is None
        True
        >>> ash.record_battle_outcome(misty, False)
        >>> misty.record_battle_outcome(ash, True)
        >>> ash.get_win_rate()
        0.0
        >>> ash.record_battle_outcome(misty, True)
        >>> misty.record_battle_outcome(ash, False)
        >>> print(ash.get_win_rate())
        0.5
        """
        if self._battles == {}:
            return None
        else:
            total_wins = 0
            total_battles = 0
            for opponent in self._battles:
                total_wins = total_wins + self._battles[opponent][0]
                total_battles = (total_battles + self._battles[opponent][0]
                                 + self._battles[opponent][1])
            win_rate = total_wins / total_battles
            # return total_battles
            return round(win_rate, 1)

    def record_battle_outcome(
            self, opponent: Trainer, won_battle: bool
    ) -> None:
        """Update this Pokemon trainer's battle statistics in _battles
         based on the value of won_battle.

        won_battle is True if the Pokemon trainer has won
        the battle, and False otherwise.

        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> misty = Trainer("Misty", 1, 5, 15)
        >>> ash.get_win_rate() is None
        True
        >>> misty.get_win_rate() is None
        True
        >>> ash.record_battle_outcome(misty, False)
        >>> misty.record_battle_outcome(ash, True)
        >>> ash.get_win_rate()
        0.0
        >>> misty.get_win_rate()
        1.0
        >>> ash.record_battle_outcome(misty, True)
        >>> misty.record_battle_outcome(ash, False)
        >>> ash.get_win_rate()
        0.5
        >>> misty.get_win_rate()
        0.5
        """
        while opponent not in self._battles:
            self._battles[opponent] = (0, 0)

        if won_battle is False:
            numbers = list(self._battles[opponent])
            numbers[1] = numbers[1] + 1
            self._battles[opponent] = tuple(numbers)

        elif won_battle is True:
            numbers = list(self._battles[opponent])
            numbers[0] = numbers[0] + 1
            # numbers[1] = numbers[1] + 1
            self._battles[opponent] = tuple(numbers)

    def request_pokecenter_admission(
            self, pokemon: Pokemon, pokecenter: PokeCenter
    ) -> bool:
        """Request the pokecenter admit the pokemon for treatment.
        Admission of the pokemon is dependent on the capacity of the
        pokecenter.

        Return False if the pokemon is not owned by the trainer.

        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> squirtle = Pokemon(
        ...     "Squirtle", "water", {"grass" : 0.5, "electric": 0.7},
        ...     1, 100, 10, 5
        ... )
        >>> ash.add_pokemon(pikachu)
        >>> ash.add_pokemon(squirtle)
        >>> pikachu.fainted = True
        >>> squirtle.fainted = True
        >>> pokecenter = PokeCenter("PC1", 1)
        >>> pokecenter.get_availability()
        1
        >>> ash.request_pokecenter_admission(pikachu, pokecenter)
        True
        >>> pikachu.in_hospital
        True
        >>> pokecenter.get_availability()
        0
        >>> ash.request_pokecenter_admission(squirtle, pokecenter)
        False
        >>> squirtle.in_hospital
        False
        """
        # This method is implemented for you. Do NOT change it!
        return (pokemon in self._all_pokemon
                and pokecenter.admit_pokemon(pokemon))

    def request_pokecenter_discharge(
            self, pokemon: Pokemon, pokecenter: PokeCenter
    ) -> bool:
        """Request the pokecenter discharge the pokemon.

        Return False if the pokemon is not owned by the trainer.
        """
        # This method is implemented for you. Do NOT change it!
        return (pokemon in self._all_pokemon
                and pokemon.in_hospital
                and pokecenter.discharge_pokemon(pokemon))


class PokeCenter:
    """A PokeCenter.

    === Instance Attributes ===
    id: The id of this pokecenter.
    max_capacity: The maximum number of Pokemon that can be admitted to this
        pokecenter.

    === Private Attributes ===
    _admitted_pokemon: A list of all admitted Pokemon.

    === Representation Invariants ===
    - max_capacity >= 0
    - len(_admitted_pokemon) <= max_capacity
    - id == id.upper()

    === Sample Usage ===
    >>> pokecenter = PokeCenter("PC1", 10)
    >>> pikachu = Pokemon(
    ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
    ... )
    >>> pikachu.fainted = True
    >>> pokecenter.admit_pokemon(pikachu)
    True
    >>> pokecenter.get_availability()
    9
    """
    id: str
    max_capacity: int
    _admitted_pokemon: List[Pokemon]

    def __init__(self, pokecenter_id: str, max_capacity: int) -> None:
        """Initialize this pokecenter with this pokecenter_id (upper-cased),
        max_capacity, and no admitted Pokemon.

        See class-level docstring for sample usage.
        """
        self.id = pokecenter_id.upper()
        self.max_capacity = max_capacity
        self._admitted_pokemon = []

    def __str__(self) -> str:
        """Return a str representing this PokeCenter
        """
        # This method is implemented for you. Do NOT change it!
        return f"PokeCenter {self.id}\n\t" \
               f"Availability: {self.get_availability()}/{self.max_capacity}"

    def heal_admitted_pokemon(self) -> None:
        """Heal all admitted pokemon to this Pokecenter.

        >>> pokecenter = PokeCenter("PC1", 2)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 0.5}, 1, 100, 10, 5
        ... )
        >>> pikachu.curr_hp = int(0.5 * pikachu.max_hp)
        >>> pokecenter.admit_pokemon(pikachu)
        True
        >>> pokecenter.heal_admitted_pokemon()
        >>> pikachu.curr_hp == pikachu.max_hp
        True
        """
        # This method is implemented for you. Do NOT change it!
        for pokemon in self._admitted_pokemon:
            pokemon.fainted = False
            pokemon.curr_hp = pokemon.max_hp

    def get_availability(self) -> int:
        """Return the number of available spots in this pokecenter.

        >>> pokecenter = PokeCenter("PC1", 10)
        >>> pokecenter.get_availability()
        10
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> pikachu.fainted = True
        >>> pokecenter.admit_pokemon(pikachu)
        True
        >>> pokecenter.get_availability()
        9
        """
        return self.max_capacity - len(self._admitted_pokemon)

    def is_admitted(self, pokemon: Pokemon) -> bool:
        """Return True if pokemon has been admitted to this Pokecenter,
        and False otherwise.

        >>> pokecenter = PokeCenter("PC1", 2)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> pokecenter.is_admitted(pikachu)
        False
        >>> pokecenter.admit_pokemon(pikachu)
        True
        >>> pokecenter.is_admitted(pikachu)
        True
        """
        # This method is implemented for you. Do NOT change it!
        return pokemon in self._admitted_pokemon

    def admit_pokemon(self, pokemon: Pokemon) -> bool:
        """Admit the Pokemon to this pokecenter if the pokecenter has available
        spaces and the Pokemon is not already hospitalized.
        Change the Pokemon to indicate that it is currently hospitalized.

        Return True if the Pokemon has been admitted successfully to the
        Pokecenter, and False otherwise

        >>> pokecenter = PokeCenter("PC1", 2)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> pokecenter.admit_pokemon(pikachu)
        True
        >>> pikachu.in_hospital
        True
        """
        if self.get_availability() >= 1 and pokemon.in_hospital is False:
            self._admitted_pokemon.append(pokemon)
            pokemon.in_hospital = True
            return True
        else:
            return False

    def discharge_pokemon(self, pokemon: Pokemon) -> bool:
        """If the pokemon is ready to be discharged, discharge pokemon from
        this Pokecenter.

        Check that the pokemon is ready to be discharged. If it is,
        remove the pokemon from the _admitted_pokemon attribute and
        update the pokemon.in_hospital status to False.

        Return True if the pokemon has been discharged successfully and
        False otherwise.

        A pokemon is ready to be discharged if it is currently admitted to this
        pokecenter and is no longer fainted and its health points have been
        restored.

        >>> pokecenter = PokeCenter("PC1", 2)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> pikachu.fainted = True
        >>> pokecenter.admit_pokemon(pikachu)
        True
        >>> pokecenter.heal_admitted_pokemon()
        >>> pokecenter.discharge_pokemon(pikachu)
        True
        >>> pikachu.fainted
        False
        """
        if self.is_admitted(pokemon) and not pokemon.fainted \
                and pokemon.curr_hp == pokemon.max_hp:
            self._admitted_pokemon.remove(pokemon)
            pokemon.in_hospital = False
            return True
        else:
            return False


class World:
    """A collection of all trainers, pokemon and pokecenters.

    === Private Attributes ===
    _player: The main trainer.
    _trainers: A list of trainers that exist in this world, including the main
        trainer.
    _pokemon: A list of pokemon that exist in this world.
    _pokecenters: A list of pokecenters that exist in this world.
    _type_to_name_mapping: A mapping between Pokemon elemental types and names.
        Each key is a pokemon elemental type and each value is a list of names
        of all the pokemon that have that type.
    _type_to_weakness_mapping: A mapping between the Pokemon type and weakness.
        Each key is a Pokemon type and each value is a dictionary that provides
        the mapping between a pokemon type and its corresponding added
        battle advantage.

    === Representation Invariants ===
    - _player in _trainers
    - For each trainer, t, in _trainers, t.all_pokemon are a subset of _pokemon
    - For each pokemon, p, in _pokemon,
        * p.owner in _trainers
        * p.name in _type_to_name_mapping[p.type]
        * p.weakness = _type_to_weakness_mapping[p.type]
    - no duplicate values in _pokecenters
    - no duplicate values in _trainers
    - no duplicate values in _pokemon

    === Sample Usage ===
    >>> player = Trainer("CSC148-trainer", 1, 5, 15)
    >>> world = World(player)
    >>> ash = Trainer("Ash", 1, 5, 15)
    >>> pikachu = Pokemon(
    ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
    >>> squirtle = Pokemon(
    ...     "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, 1, 100, 10, 5
    ... )
    >>> sandshrew = Pokemon(
    ...     "Sandshrew", "ground", {"water": 0.1, "grass": 0.5, "ice": 0.1},
    ...     1, 100, 5, 15
    ... )
    >>> world.add_trainer(ash)
    >>> world.add_pokemon(pikachu)
    >>> world.add_pokemon(squirtle)
    >>> world.add_pokemon(sandshrew)
    >>> len(world.get_wild_pokemon())
    3
    """
    _player: Trainer
    _trainers: List[Trainer]
    _pokemon: List[Pokemon]
    _pokecenters: List[PokeCenter]
    _type_to_name_mapping: Dict[str, List[str]]
    _type_to_weakness_mapping: Dict[str, Dict[str, float]]

    def __init__(self, player: Trainer) -> None:
        """Initialize this World, with _player set to player, no pokemon (i.e.
        _pokemon is empty), no pokecenters (i.e. _pokecenter is empty),
        and a single trainer (player).

        See the class-level docstring for description of usage.
        """
        self._player = player
        self._trainers = [self._player]
        self._pokemon = []
        self._pokecenters = []
        # Do NOT change the following two lines!!
        self._type_to_weakness_mapping = {}
        self._type_to_name_mapping = {}

    def get_pokemon_weakness(self, pokemon_type: str) -> Dict[str, float]:
        """Return the weakness for the given Pokemon type pokemon_type.
        Each key in the returned value is a type to which pokemon_type is
        susceptible and the corresponding value is the additional advantage
        that type has over pokemon_type.
        """
        # This method is implemented for you. Do NOT change it!
        return self._type_to_weakness_mapping.get(pokemon_type.lower(), {})

    def get_pokemon_type(self, pokemon_name: str) -> Optional[str]:
        """Return the Pokemon type of the given Pokemon name pokemon_name.
        Return None if the type is not known.
        """
        # This method is implemented for you. Do NOT change it!
        for k, v in self._type_to_name_mapping.items():
            if pokemon_name.title() in v:
                return k
        return None

    def add_trainer(self, trainer: Trainer) -> None:
        """Add trainer to this world. If the trainer is already added, do
        nothing.

        >>> player = Trainer("CSC148-trainer", 1, 5, 15)
        >>> world = World(player)
        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> world.add_trainer(ash)
        """
        # This method is implemented for you. Do NOT change it!
        if trainer not in self._trainers:
            self._trainers.append(trainer)

    def add_pokemon(self, pokemon: Pokemon) -> None:
        """Add pokemon to this world.

        Appends the pokemon to _pokemon if pokemon is not in _pokemon.
        If the pokemon is already in _pokemon, do nothing.

        >>> player = Trainer("CSC148-trainer", 1, 5, 15)
        >>> world = World(player)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> world.add_pokemon(pikachu)
        """
        # This method is implemented for you. Do NOT change it!
        if pokemon not in self._pokemon:
            self._pokemon.append(pokemon)

    def add_pokecenter(self, pokecenter: PokeCenter) -> None:
        """Add pokecenter to this world.

        Appends the pokecenter to _pokecenters if pokecenter is
        not in _pokecenter. If the pokecenter is already in _pokecenters,
        do nothing.

        >>> player = Trainer("CSC148-trainer", 1, 5, 15)
        >>> world = World(player)
        >>> pokecenter = PokeCenter("PC1", 10)
        >>> world.add_pokecenter(pokecenter)
        """
        # This method is implemented for you. Do NOT change it!
        if pokecenter not in self._pokecenters:
            self._pokecenters.append(pokecenter)

    def get_wild_pokemon(self) -> List[Pokemon]:
        """Return a list of the wild pokemon. A wild pokemon is one that doesn't
        have an owner.

        >>> player = Trainer("CSC148-trainer", 1, 5, 15)
        >>> world = World(player)
        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> world.add_trainer(ash)
        >>> world.add_pokemon(pikachu)
        >>> len(world.get_wild_pokemon())
        1
        >>> ash.add_pokemon(pikachu)
        >>> len(world.get_wild_pokemon())
        0
        """
        # This method is implemented for you. Do NOT change it!
        res = []
        for poke in self._pokemon:
            if not poke.owner:
                res.append(poke)
        return res

    def rank_trainers(self) -> List[List[Trainer]]:
        """Return a tier list of trainer ranks.

        Each sublist represents the Trainers with a particular win rate,
        with the sublists ordered from highest to lowest win rate.

        For example, if the trainer ash has a win rate of 50%,
        Trainer misty has a win rate of 50%, and trainer brock has a win rate
        of 10%, this method should return [[ash, misty], [brock]].

        The example below is more concrete and separate from the verbal one
        provided above.

        >>> player = Trainer("CSC148-trainer", 1, 5, 15)
        >>> world = World(player)
        >>> ash = Trainer("Ash", 1, 5, 15)
        >>> misty = Trainer("Misty", 1, 5, 15)
        >>> brock = Trainer("Brock", 1, 5, 15)
        >>> world.add_trainer(ash)
        >>> world.add_trainer(misty)
        >>> world.add_trainer(brock)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> ash.add_pokemon(pikachu)
        >>> butterfree = Pokemon(
        ...     "Butterfree", "bug", {"fire": 1.0, "flying": 0.5, "rock": 0.2},
        ...     1, 100, 10, 5
        ... )
        >>> misty.add_pokemon(butterfree)
        >>> ash.record_battle_outcome(misty, True)
        >>> misty.record_battle_outcome(ash, False)
        >>> misty.record_battle_outcome(ash, True)
        >>> ash.record_battle_outcome(misty, False)
        >>> result = world.rank_trainers()
        >>> len(result)
        1
        >>> len(result[0])
        2
        >>> ash in result[0]
        True
        >>> misty in result[0]
        True
        >>> brock in result[0]
        False
        """
        # lst1_0 = []
        # for trner in self._trainers:
        #     if trner.get_win_rate() is 1.0:
        #         lst1_0.append(trner)

        b = []
        for i in range(0, 11):
            d = (10 - i) / 10
            a = []
            for trner in self._trainers:
                w_r = trner.get_win_rate()
                if w_r == d:
                    a.append(trner)
            if a:
                b.append(a)
        return b

    def get_available_pokecenters(self) -> List[PokeCenter]:
        """Return a list of pokecenters that have available spaces.

        A pokecenter has available spaces if it has fewer pokemon in
        _admitted_pokemon than its max_capacity.

        >>> player = Trainer("CSC148-trainer", 1, 5, 15)
        >>> world = World(player)
        >>> pokecenter1 = PokeCenter("PC1", 1)
        >>> pokecenter2 = PokeCenter("PC2", 1)
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5
        ... )
        >>> world.add_pokecenter(pokecenter1)
        >>> world.add_pokecenter(pokecenter2)
        >>> world.add_pokemon(pikachu)
        >>> pikachu.curr_hp = int(0.5 * pikachu.max_hp)
        >>> len(world.get_available_pokecenters())
        2
        >>> pokecenter1.admit_pokemon(pikachu)
        True
        >>> len(world.get_available_pokecenters())
        1
        """
        # This method is implemented for you. Do NOT change it!
        result = []
        for pokecenter in self._pokecenters:
            if pokecenter.get_availability() > 0:
                result.append(pokecenter)
        return result

    def admit_all_npc_pokemon(self, limit: int) -> None:
        """Send sick, non-hospitalized pokemon owned by non-player trainers
        to the available pokecenters, while accounting for the capacity of the
        pokecenters as well as the limit of hospitalized pokemon per trainer.

        For the purposes of this assignment, a sick pokemon is either
        fainted or has less health points than the maximum possible value.

        Prioritize the Pokemon that are admitted using the following rules:
        - alphabetical order of the trainer name, followed by
        - the pokemon's current hp, in non-descending order,
        - in the case of a tie for the current hp, use alphabetical order
          of the pokemon's name.

        Fill out Pokecenters in ascending order of available spaces.

        Does NOT change self._trainers, self._pokecenters or self._pokemon

        HINT: You may wish to create a helper Trainer method to get candidate
        pokemon for admission, and sort them in some order...

        >>> player = Trainer("CSC148-trainer")
        >>> world = World(player)
        >>> pokecenter1 = PokeCenter("PC1", 1)
        >>> pokecenter2 = PokeCenter("PC2", 0)
        >>> world.add_pokecenter(pokecenter1)
        >>> world.add_pokecenter(pokecenter2)
        >>> ash = Trainer("Ash")
        >>> pikachu = Pokemon(
        ...     "Pikachu", "electric", {"ground": 1.0}, 1, 100, 10, 5)
        >>> squirtle = Pokemon(
        ...     "Squirtle", "water", {"grass" : 0.5, "electric": 0.7}, 1, 100,
        ...     10, 5)
        >>> bulbasaur = Pokemon(
        ...     "Bulbasaur", "grass",
        ...     {"fire" : 1.0, "psychic": 0.5, "flying": 0.3, "ice": 0.1},
        ...     1, 100, 10, 5
        ... )
        >>> world.add_trainer(ash)
        >>> world.add_pokemon(squirtle)
        >>> world.add_pokemon(pikachu)
        >>> world.add_pokemon(bulbasaur)
        >>> ash.add_pokemon(squirtle)
        >>> ash.add_pokemon(pikachu)
        >>> player.add_pokemon(bulbasaur)
        >>> pikachu.curr_hp = 0
        >>> pikachu.fainted = True
        >>> squirtle.curr_hp = 0
        >>> squirtle.fainted = True
        >>> bulbasaur.curr_hp = 0
        >>> bulbasaur.fainted = True
        >>> world.admit_all_npc_pokemon(3)
        >>> pikachu.in_hospital
        True
        >>> pokecenter1.is_admitted(pikachu)
        True
        >>> squirtle.in_hospital  # tied for hp, admit in alphabetical order
        False
        >>> bulbasaur.in_hospital  # owned by player
        False
        >>> pokecenter1.get_availability()
        0
        >>> pokecenter2.get_availability()
        0
        """
        non_player_list = []  # Returns List of Trainers who are not _player
        for player in self._trainers:
            if player is not self._player:
                non_player_list.append(player)
        #
        avle_pokecenters = self.get_available_pokecenters()
        avle_pokecenters.sort(key=lambda s: s.get_availability())

        non_player_list.sort(key=lambda p: p.name)  # Alphabetical Order
        #
        for trainer in non_player_list:
            sick_pokemon = candidate_pokemon(trainer)
            sick_pokemon = sick_pokemon[0:limit]
            for s_p in sick_pokemon:
                if avle_pokecenters:
                    avle_pokecenters[0].admit_pokemon(s_p)
                    avle_pokecenters = self.get_available_pokecenters()
                    avle_pokecenters.sort(key=lambda s: s.get_availability())


def candidate_pokemon(t: Trainer) -> List[Pokemon]:
    """Returns a List of Pokemon who are sick in a non-descending
    order.

    """
    sick = []
    all_pokemon = t.get_all_pokemon()
    for pokemon in all_pokemon:
        if pokemon.fainted is True or pokemon.curr_hp < pokemon.max_hp:
            sick.append(pokemon)
    sick.sort(key=lambda p: p.name)

    # List of all hp's of sick pokemon, use that list to get a dict with hp key
    # and
    # value being the corresponding pokemon
    # return sick
    hp_list = []
    for pkm in sick:
        hp_list.append(pkm.curr_hp)
    hp_list = list(set(hp_list))
    b = []
    for val in hp_list:
        a = []
        for pkmn in sick:
            if pkmn.curr_hp == val:
                a.append(pkmn)
        b.append(a)

    result = []
    for sublist in b:
        for item in sublist:
            result.append(item)
    return result


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'disable': ['E1136', 'R0913', 'R0902'],
        'max-nested-blocks': 5
    })

    import doctest

    doctest.testmod()
