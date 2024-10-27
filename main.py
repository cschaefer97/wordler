from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import keyboard
import tkinter as tk
import textsender

class WordleSolver:
    def __init__(self):
        """
        Declares word list, opens NYT Wordle website and clicks through popup options
        until we can start solving the game.
        """

        self.first_guess = "aeros"
        self.word_list = self.read_file("sgb-words.txt")
        self.alphabet = self.read_file("letters.txt")
        self.weighted_alphabet = dict.fromkeys(self.alphabet, 0)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

        play_button_xpath = "/html/body/div[2]/div/div/div/div/div[2]/button[2]"
        close_tutorial_xpath = "//*[@id=\"help-dialog\"]/div/div/button"
        worlde_url = "https://www.nytimes.com/games/wordle/index.html"

        self.driver.get(worlde_url)
        self.driver.find_element(By.XPATH, play_button_xpath).click()
        tutorial_skip = self.wait.until(expected_conditions.element_to_be_clickable((
            By.XPATH, close_tutorial_xpath)))
        tutorial_skip.click()

        self.play_wordle()
        self.driver.quit()
        
    def play_wordle(self):
        """
        Interacts with the actual game board, inputting the optimal guess and scraping the page for the result
        """
        gameboard_xpath = "//*[@id=\"wordle-app-game\"]/div[1]/div"
        for num_guess in range(1,7):
            
            if num_guess == 1:
                # first run through we have to click the Wordle board so it will take our inputs
                guess = self.first_guess
                self.driver.find_element(By.XPATH, gameboard_xpath).click()
            
            keyboard.write(guess)
            keyboard.press_and_release('Enter')
            time.sleep(2)   # wait necessary for guess to populate gameboard
            
            result = self.get_wordle_results(num_guess)

            if result == [2,2,2,2,2]:
                self.win_condition(guess)
                break

            self.update_word_list(result, guess)
            new_guess = self.generate_best_guess()
            guess = new_guess
        
    def get_wordle_results(self, num_guess):
        """
        gets results of Wordle guess and returns an array containing enums of correct, present, and incorrect.
        """
        row = self.driver.find_element(By.CSS_SELECTOR,"[aria-label='Row " + str(num_guess) + "']")
        raw_results = row.find_elements(By.CSS_SELECTOR, "[aria-label*='letter']")
        results = []
        for i in range(5):
            tile = raw_results[i].accessible_name
            if "correct" in tile:
                results += [2]
            elif "present" in tile:
                results += [1]
            elif "absent" in tile:
                results += [0]
            else:
                print("ERROR, UNABLE TO PARSE. RESULTS INVALID")
                
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

    def win_condition(self, winning_word):
        """
        Copies results to clipboard and sends the user their results!
        """
        share_button = "//*[@id=\"regiwallModal-dialog\"]/div/div[1]/div[2]/div/div[5]/div/button"
        exit_popup = "//*[@id=\"loginPrompt-dialog\"]/div/div/div[1]/div/button/div"
        
        self.wait.until(expected_conditions.element_to_be_clickable((
            By.XPATH, exit_popup))).click()

        self.wait.until(expected_conditions.element_to_be_clickable((
            By.XPATH, share_button))).click()

        root = tk.Tk()
        root.withdraw()  # to hide the window
        victory_message = root.clipboard_get()
        victory_message += "\n " + winning_word
        textsender.send_text(victory_message)

    def read_file(self, name):
        file = open(name, "r")
        obj = file.read().splitlines()
        file.close()
        return obj

if __name__ == "__main__":
    wordler = WordleSolver()
    