#!/usr/bin/env python3
# Brodderick Rodriguez
# Auburn University - CSSE
# 19 Mar. 2019

from TexasHoldem_ReinforcementLearning.env0.player import Player
from enum import Enum
from treys import Evaluator, Deck, Card
import logging


# describes the current stage of the Texas Hold'em game
class GameStage(Enum):
    INITIAL, FLOP, TURN, RIVER, SHOWDOWN, HAND_COMPLETE = 0, 1, 2, 3, 4, 5

    # simply increments the game stage to the next stage
    def increment(self):
        return GameStage(self.value + 1)


class TexasHoldem:
    def __init__(self, players):
        # if len(players) < 2:
        #     raise RuntimeError('number of players must be at least two')

        # initialize variables and assign their respective values in reset()
        self.deck, self.table_cards, self.players, self.game_stage = [], [], players, GameStage.INITIAL
        self.reset()

    def reset(self):
        self.deck = Deck()
        self.table_cards = []
        self.game_stage = GameStage.INITIAL

        logging.info('dealing initial cards')
        for player in self.players:
            player.cards = self.deck.draw(n=2)
            logging.info(str(player) + Card.print_pretty_cards(player.cards))

    def step(self, actions):
        # check if hand is complete
        if self.game_stage == GameStage.HAND_COMPLETE:
            return self.game_stage

        # if not, increment the game's stage
        self.game_stage = self.game_stage.increment()

        # log some helpful output
        logging.info(self.game_stage)

        # if game stage is flop, put three cards on the table
        if self.game_stage == GameStage.FLOP:
            self.table_cards = self.deck.draw(n=3)

        # if game stage is turn or river, add another card to the table
        elif self.game_stage in [GameStage.TURN, GameStage.RIVER]:
            self.table_cards.append(self.deck.draw(n=1))

        # if all cards for this hand have been delt, evaluate each players hands
        # and return a list of winning players
        elif self.game_stage == GameStage.SHOWDOWN:
            return self.evaluate_hands()

        # if we accidentally call TexasHoldem.step() after the hand is over,
        # this will catch it
        elif self.game_stage == GameStage.HAND_COMPLETE:
            return self.game_stage

        # log some helpful output
        logging.info(Card.print_pretty_cards(self.table_cards))

        # lastly, return the game stage
        return self.game_stage

    def evaluate_hands(self):
        evaluator = Evaluator()

        # for each player, evaluate their hand and store its value
        # in player.hand_score
        for player in self.players:
            player.hand_score = evaluator.evaluate(player.cards, self.table_cards)
            print(player, player.hand_score)

        # sorts players in descending over respective to their hand_score
        # see Player.__lt__()
        self.players.sort(reverse=True)
        winners = [self.players[0]]
        idx = 0

        # check if there are ties for first place
        while idx + 1 < len(self.players) and self.players[idx].hand_score == self.players[idx + 1].hand_score:
            winners.append(self.players[idx + 1])
            idx += 1

        return winners


# a test class to make sure everything in this file works
class Tests:
    def __init__(self):
        pass

    @staticmethod
    def game_stage_test():
        players = [Player() for _ in range(3)]
        game = TexasHoldem(players)

        game.step()  # initial
        game.step()  # flop
        game.step()  # turn
        game.step()  # river
        game.step()  # showdown
        # game.step()  # game over
        # game.step()  # test -- this shouldn't cause a runtime error


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Tests.game_stage_test()