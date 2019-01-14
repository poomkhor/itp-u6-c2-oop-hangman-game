import random
from .exceptions import *

class GuessAttempt(object):
    def __init__(self, guess_letter, hit=None, miss=None):
        self.guess = guess_letter
        self.hit = hit
        self.miss = miss
        if self.hit == self.miss:
            raise InvalidGuessAttempt
        
    def is_hit(self):
        if self.hit:
            return True
        return False
    
    def is_miss(self):
        if self.miss:
            return True
        return False

class GuessWord(object):
    def __init__(self, word):
        self.answer = word
        self.masked = '*' * len(word)
        if not word:
            raise InvalidWordException        
            
    def perform_attempt(self, guess_letter):
        if len(guess_letter) > 1:
            raise InvalidGuessedLetterException
        
        if guess_letter.lower() in self.answer.lower():           
            attempt = GuessAttempt(guess_letter, hit=True)
            self.masked = self.unmasked_answer(guess_letter)
        else:
            attempt = GuessAttempt(guess_letter, miss=True)
        return attempt
    
    def unmasked_answer(self, guess_letter):
        answer = ''
        for i in range(len(self.answer)):
            answer_letter = self.answer[i].lower()
            masked_letter = self.masked[i].lower()
            
            if masked_letter != '*':
                answer += answer_letter
            elif answer_letter == guess_letter.lower():
                answer += answer_letter
            else:
                answer += '*'
        return answer
                 
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, list_of_words=None, number_of_guesses=5):
        if not list_of_words:
            list_of_words = self.WORD_LIST
        select_word = self.select_random_word(list_of_words)
        self.word = GuessWord(select_word)
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        
    def guess(self, guess_letter):
        if self.is_finished():
            raise GameFinishedException()
        attempt = self.word.perform_attempt(guess_letter)
        self.previous_guesses.append(guess_letter.lower())
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
        if self.is_won():
            raise GameWonException()
        return attempt
    
    def is_won(self):   
        if self.word.answer == self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    @classmethod
    def select_random_word(self, list_of_words):
        if len(list_of_words) == 0:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)
        
        
        
        
        