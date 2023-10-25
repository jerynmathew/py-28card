from unittest import TestCase

from src.py_28card.models import Card, FourPlayerDeck, FullDeck, Suit, Value


class DeckTest(TestCase):

    def test_full_deck(self):
        deck = FullDeck()
        first_card = Card(Suit.HEARTS, Value.ONE)
        last_card = Card(Suit.DIAMOND, Value.JACK)

        deck.generate_deck(is_shuffle=False)

        assert deck.size == 56
        assert deck.top_card == first_card
        assert deck.bottom_card == last_card

        deck.generate_deck(is_shuffle=True)

        assert deck.size == 56
        assert deck.top_card != first_card
        assert deck.bottom_card != last_card

    def test_4p_deck(self):
        deck = FourPlayerDeck()
        first_card = Card(Suit.HEARTS, Value.JACK)
        last_card = Card(Suit.DIAMOND, Value.SEVEN)

        deck.generate_4_player_deck(is_shuffle=False)

        assert deck.size == 32
        assert deck.top_card == first_card
        assert deck.bottom_card == last_card

        deck.generate_4_player_deck(is_shuffle=True)

        assert deck.size == 32
        assert deck.top_card != first_card
        assert deck.bottom_card != last_card

