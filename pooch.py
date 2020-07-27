import random

class player:
    def __init__(self):
        self.name = None
        self.cards = []
        self.bet = 0
        self.current_wins =  0
        self.score = 0


class card:
    def __init__(self):
        self.suit = None
        self.number = None
        self.actual = None
class deck:
    def __init__(self):
        suit_table = {}
        suit_table[0] = 'hearts'
        suit_table[1] = 'spades'
        suit_table[2] = 'clubs'
        suit_table[3] = 'diamonds'


        self.pack = []
        for i in range(1, 14):
            for j in range(4):
                temp = card()
                temp.suit = suit_table[j]
                number = card_converter(i)
                actual = card_converter_reverse(number)
                temp.number = number
                temp.actual = actual
                self.pack.append(temp)

def card_converter(number):
    final = number
    if number == 1:
        final = 'ace'
    elif number == 11:
        final = 'jack'
    elif number == 12:
        final = 'queen'
    elif number == 13:
        final = 'king'
    return final
def card_converter_reverse(number):
    final = number
    if number == 'ace':
        final = 13
    if number == 'jack':
        final = 10
    if number == 'queen':
        final = 11
    if number == 'king':
        final = 12
    return final

class master():
    def __init__(self):
        print('#############################')
        print('hello, get ready to play pooch! ')
        print('#############################')
        self.amt = int(input('amount of players:'))
        while(self.amt <2):
            self.amt = int(input('sorry! need more than one player to play. How many players:'))
        self.deck_cards = deck()
        self.round = None
        self.player_list = []
        self.first = 0
        self.eighth = False
        self.played = []
        self.trump_card = None
        self.lead = None

        for i in range(self.amt):
            temp = player()
            self.player_list.append(temp)
        for i in range(self.amt):
            print(i, 'player name:')
            self.player_list[i].name = input()


        self.__master_deal(False)
        self.__master_deal(True)
        self.__final_winner()


    def __master_deal(self, backward):
        start = 1
        end = 9
        incr = 1
        if backward:
            start = 7
            end = 0
            incr = -1
        # For each round
        self.first = 0
        for i in range(start,end,incr):
            print('#############################')
            print('Round ', i)
            print('#############################')
            self.round = i
            # Deal out the cards
            for j in range(self.amt):
                for k in range(i):
                    index = random.randrange(len(self.deck_cards.pack))
                    self.player_list[j].cards.append(self.deck_cards.pack[index])
                    self.deck_cards.pack.pop(index)

            if i <= 6 and not backward:
                index = random.randrange(len(self.deck_cards.pack))
                self.trump_card = self.deck_cards.pack.pop(index)
                print('trump card:', self.trump_card.number, 'of', self.trump_card.suit)
            else:
                self.eighth = True
            self.__single_round()
            self.first += (self.first +1) % self.amt

            # Reset for new round
            self.trump_card = None
            self.eighth = False
            for elem in self.player_list:
                elem.cards = []
                elem.bet = 0
                elem.current_wins = 0
            self.deck_cards = deck()


    def __single_round(self):
        length = len(self.player_list)

        #Make bets
        for i in range(length):
            print('#################')
            print(self.player_list[(i + self.first) % length].name,', it is your turn to bet! here are your cards:')
            for elem in self.player_list[(i + self.first) % length].cards:
                print(elem.number, 'of', elem.suit)

            bet  = int(input('how much you want to bet:'))
            while(bet > self.round):
                bet = int(input('Too high of a bid; how much do you want to bet:'))
            if i == length - 1:
                sum = 0
                for elem in self.player_list:
                    sum += elem.bet
                while (sum + bet == self.round ):
                    print('sorry, since your the last player, you cannot bet that. You can bet anything but', bet)
                    bet = int(input('Try again, how much you want to bet:'))
                    print('sum', sum, bet)
                    while (bet > self.round):
                        bet = int(input('Too high of a bid; how much do you want to bet:'))

            self.player_list[(self.first + i) % length].bet = bet
        # playing cards
        for i in range(self.round):
            print('#############################')
            print('hand number', i + 1)
            print('#############################')
            pile = []
            for j in range(length):
                player = self.player_list[(j+ self.first)  % length]

                # print player's cards
                print(player.name, 'it is your turn to play; here are your cards:')
                for elem in self.player_list[(j + self.first) % length].cards:
                    print(elem.number,'of' , elem.suit)

                print(player.name, ',what card do you want to play? (e.g. king of spades')

                card = self.__input_converter(input('card:'), player)
                card = self.__valid(card,self.player_list[(j + self.first) % length].cards, player)

                if j == 0:
                    self.lead = card

                pile.append((card, player))

                for elem in self.player_list[j % length].cards:
                    if elem.suit == card.suit and elem.number == card.number:
                        self.player_list[j % length].cards.remove(elem)
                        break
            winner= self.__check(pile)[1]
            print('the winner of this hand is', winner.name,'!')
            input1 = input('enter anything to continue to the next hand')
            winner.current_wins += 1
            index = self.player_list.index(winner)
            self.first = index

        self.__check_bets()

    def __valid(self, card1, player_cards, player):

        if card1[0] == 0:
            card1 = self.__input_converter(
                input('input is invalid, please try again (e.g. king of spades):'), player)
            card1 = self.__valid(card, player_cards, player)

        if card1[0] == 1:
            print('you do not have that card, here are your cards:')
            for elem in player_cards:
                print(elem.number, 'of', elem.suit)
            card1 = self.__input_converter(input('Try again (e.g. king of spades):'), player)
            card1 = self.__valid(card, player_cards, player)

        return card1[1]

    def __input_converter(self, string, player1):
        index = 0
        for i in range(len(string)):
            if string[i] == ' ':
                index = i
                break

        if len(string[0: index]) <= 2:
            number = int(string[0: index])
        else:
            number = string[0: index]

        suit = string[index+4:len(string)]

        temp_card = card()
        temp_card.suit = suit
        temp_card.number = number
        temp_card.actual = card_converter_reverse(number)
        temp_deck = deck()

        flag = False
        for elem in temp_deck.pack:

            if elem.number == temp_card.number and elem.suit == temp_card.suit:

                flag = True
        if not flag:
            return 0, None
        flag = False
        for elem in player1.cards:
            if elem.suit == temp_card.suit and elem.number == temp_card.number:
                flag = True
        if not flag:
            return 1, None
        return 2, temp_card

    def __check_bets(self):
        print('#############################')
        print('here is the scores from this round!')
        print('#############################')
        for elem in self.player_list:
            flag = False
            if elem.current_wins == elem.bet:
                elem.score += 10 + elem.bet
                flag = True
            if not flag:
                print(elem.name , 'pooched! no points for you :(')
            else:
                print(elem.name ,'got', 10 + elem.bet, 'points', 'for a cumulative total of', elem.score)
        input1 = input('type anything to continue to the next round! ')



    def __check(self,pile):
        winner = None
        trump_suit = self.trump_card.suit
        lead_suit = self.lead.suit

        for elem in pile:
            if not winner:
                winner = elem
            if elem[0].suit == lead_suit or elem[0].suit == trump_suit:
                if self.eighth:
                    if winner[0].suit != trump_suit and elem[0].suit == trump_suit:
                        winner = elem
                    if elem[0].suit == trump_suit and winner[0].suit == trump_suit:
                        if elem[0].actual > winner[0].actual:
                            winner = elem
                if elem[0].suit == lead_suit and winner[0].suit == lead_suit:
                    if elem[0].actual > winner[0].actual:
                        winner = elem

        return winner

    def __final_winner(self):
        print('the final scores are...')
        total = []
        for elem in self.player_list:
            print(elem.name, 'got', elem.score, 'points')
            total.append(elem.score)
        index =  total.index(max(total))
        print('so the winner is ', self.player_list[index].name, 'with', self.player_list[index], 'points! ')


master = master()


