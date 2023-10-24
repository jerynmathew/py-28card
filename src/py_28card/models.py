from dataclasses import dataclass
from enum import StrEnum
from typing import List, Iterable
from random import shuffle


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
    Value.JACK, Value.QUEEN, Value.KING, Value.ACE,
    Value.TEN, Value.NINE, Value.EIGHT, Value.SEVEN
]


@dataclass
class Card:
    suit: Suit
    value: Value

    def __repr__(self) -> str:
        return f"{self.value.value}{self.suit.value}"


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

    @property
    def top_card(self) -> Card:
        if self.cards:
            return self.cards[0]

    @property
    def bottom_card(self) -> Card:
        if self.cards:
            return self.cards[-1]

    def sort_cards(self):
        if self.cards:
            self.cards.sort(key=lambda card: card.suit and card.value)

    def clear_deck(self):
        if isinstance(self.cards, Iterable):
            self.cards.clear()

    def shuffle_deck(self):
        if self.cards:
            shuffle(self.cards)

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
        self.cards.append(deck.draw_card())

    def show_cards(self):
        pass

    def play_card(self, card_number: int):
        pass


class Player:
    hand: Hand



class Rules:
    pass
