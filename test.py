"""
THIS FILE EXISTS TO TEST THE ALGORITHM, INDEPENDENT OF WORDLE WEBSITE
"""
import time
import random

class WordleSolver:
    def __init__(self):
        """
        init function, opens NYT Wordle website and clicks through popup options
        until we can start solving the game.
        """

        self.first_guess = "aeros"
        self.word_list = self.read_file("wordle_words.txt")
        self.alphabet = self.read_file("letters.txt")
        self.weighted_alphabet = dict.fromkeys(self.alphabet, 0)
        self.answer = random.choice(self.word_list)
        # self.answer = "corer"
        self.play_wordle()
        
    def play_wordle(self):
    # def play_wordle(self, driver, first_guess):
        """
        Interacts with the actual game board, inputting the optimal guess and scraping the page for the result
        """
        all_guesses = []
        for num_guess in range(1,6):
            
            if num_guess == 1:
                guess = self.first_guess
            all_guesses += [guess]

            result = self.get_wordle_results(guess)

            if result == [2,2,2,2,2]:
                self.win_condition(num_guess, guess, all_guesses)

            self.update_word_list(result, guess)
            new_guess = self.generate_best_guess()
            guess = new_guess

        self.loss_condition(all_guesses)

    def get_wordle_results(self, guess):
        """
        gets results of Wordle guess and returns an array containing 
        """
        results = []
        for i in range(5):
            letter = guess[i]
            if self.answer[i] == letter:
                results += [2]
            elif letter in self.answer:
                results += [1]
            else:
                results +=[0]

        return results
    
    def update_word_list(self, result, guess):
        """
        removes all invalid letters and words from word list
        """
        for pos, letter in enumerate(guess):
            if result[pos] == 0:
                
                if letter in self.weighted_alphabet:
                    self.weighted_alphabet.pop(letter)
                for words in reversed(self.word_list):
                    if letter in words:
                        self.word_list.remove(words)

            if result[pos] == 1:
                for words in reversed(self.word_list):
                    if letter not in words or words[pos] == letter:
                        self.word_list.remove(words)

            if result[pos] == 2:
                for words in reversed(self.word_list):
                    if words[pos] != letter:
                        self.word_list.remove(words)

    def generate_best_guess(self):
        """
        Counts how many times each letter appears in the list of words that are left
        If the same letter appears multiple times in the a word, it still only counts it once.
        This algorithm could be much more opimal, but this is only a weekend project.
        """
        for keys in self.weighted_alphabet:
            self.weighted_alphabet[keys] = 0
        for words in self.word_list:
            for letters in words:
                self.weighted_alphabet[letters] += 1

        best_word = ["",0]
        for words in self.word_list:
            next_word = [words, 0]
            temp_word = words
            for letters in words:
                temp_word = temp_word[1:]
                if letters not in temp_word:
                    next_word[1] += self.weighted_alphabet[letters]

            if next_word[1] > best_word[1]:
                best_word = next_word
                
        return best_word[0]

    def win_condition(self, num_tries, winning_word, all_guesses):
        """
        Copies results to clipboard and sends the user their results!
        """
        win_statement = "Congrats: You won in {} tries. The word was: {}".format(str(num_tries), winning_word)

        print(win_statement)
        print("All guesses: ")
        for word in all_guesses:
            print(word)
        exit()

    def loss_condition(self, all_guesses):
        print("Correct word: {}".format(self.answer))
        print("All guesses: ")
        for word in all_guesses:
            print(word)
        print("Words left: ")
        for word in self.word_list:
            print(word)

    def read_file(self, name):
        file = open(name, "r")
        obj = file.read().splitlines()
        file.close()
        return obj

wordler = WordleSolver()
