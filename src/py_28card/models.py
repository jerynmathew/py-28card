from dataclasses import dataclass
from enum import StrEnum
from random import shuffle
from typing import Iterable, List

from rich.console import Console
from rich.table import Table

console = Console()


class IsEmptyError(Exception):
    pass


class NotInitializedError(Exception):
    pass


class Suit(StrEnum):
    HEARTS = "♥️"
    CLUBS = "♣️"
    SPADE = "♠️"
    DIAMOND = "♦️"


class Value(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    ACE = "A"
    KING = "K"
    QUEEN = "Q"
    JACK = "J"


VALID_4_PLAYER_VALUES = [
    Value.JACK,
    Value.QUEEN,
    Value.KING,
    Value.ACE,
    Value.TEN,
    Value.NINE,
    Value.EIGHT,
    Value.SEVEN,
]


@dataclass
class Card:
    suit: Suit
    value: Value

    def __repr__(self) -> str:
        return f"{self.value.value}{self.suit.value}"

    @property
    def score(self):
        if self.value:
            match self.value:
                case Value.JACK:
                    return 3
                case Value.NINE:
                    return 2
                case Value.ACE:
                    return 1
                case Value.TEN:
                    return 1
                case _:
                    return 0
        return None


@dataclass
class Deck:
    cards: List[Card] = None

    def add_card(self, card: Card) -> None:
        if self.cards is None:
            self.cards = []

        if isinstance(card, Card) and card not in self.cards:
            self.cards.append(card)

    @property
    def size(self) -> int:
        if self.cards:
            return len(self.cards)
        return None

    @property
    def top_card(self) -> Card:
        if self.cards:
            return self.cards[0]
        return None

    @property
    def bottom_card(self) -> Card:
        if self.cards:
            return self.cards[-1]
        return None

    def sort_cards(self):
        if self.cards:
            self.cards.sort(key=lambda card: card.suit and card.value)

    def clear_deck(self):
        if isinstance(self.cards, Iterable):
            self.cards.clear()

        if not self.cards:
            self.cards = []

    def shuffle_deck(self):
        if self.cards:
            new_deck = self.cards.copy()

            while True:
                shuffle(new_deck)
                if new_deck != self.cards:
                    self.cards = new_deck
                    return

    def draw_card(self) -> Card:
        if isinstance(self.cards, Iterable):
            if self.size > 0:
                return self.cards.pop(0)
            raise IsEmptyError
        raise NotInitializedError

    def show_cards(self):
        return self.cards

    def generate_deck(self):
        raise NotImplementedError

    @property
    def total_score(self) -> int:
        total = 0
        for card in self.cards:
            total += card.score

        return total


class FullDeck(Deck):
    def generate_deck(self, is_shuffle: bool = True):
        self.clear_deck()

        for suit in Suit.__members__.values():
            for val in Value.__members__.values():
                card = Card(suit, val)
                self.add_card(card)

        if is_shuffle:
            self.shuffle_deck()


class FourPlayerDeck(FullDeck):
    def generate_deck(self, values: List[Card] = VALID_4_PLAYER_VALUES, is_shuffle: bool = True):
        self.clear_deck()

        for suit in Suit.__members__.values():
            for val in values:
                card = Card(suit, val)
                self.add_card(card)

        if is_shuffle:
            self.shuffle_deck()


@dataclass
class Hand(Deck):
    def draw_card_from_deck(self, deck: Deck, count: int = 1):
        self.clear_deck()

        for _ in range(count):
            self.cards.append(deck.draw_card())

    def show_cards(self):
        if not self.cards:
            print("No cards drawn for this hand!")
            return

        table = Table(title="Your Hand")
        table.add_column("Number", justify="center")
        table.add_column("Card", justify="center")
        table.add_column("Score", justify="right", style="green")

        for index, card in enumerate(self.cards):
            table.add_row(f"{index + 1}", f"{card}", f"{card.score}")

        table.add_row("", "[bold]Total Score", f"[bold]{self.total_score}")
        console.print(table)

    def play_card(self, card_number: int):
        if self.card and card_number <= len(self.cards):
            return self.cards.pop(card_number - 1)

        raise Exception(msg="Invalid Card")


class Player:
    hand: Hand


class Rules:
    pass
