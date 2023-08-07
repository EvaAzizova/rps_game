import sys
import random
import hashlib
import hmac

class KeyGenerator:
    @staticmethod
    def generate_key():
        return random.randint(0, 2**256 - 1)

class HMACGenerator:
    @staticmethod
    def generate_hmac(key, data):
        return hmac.new(key.to_bytes(32, 'big'), data.encode(), hashlib.sha256).hexdigest()

class GameRules:
    @staticmethod
    def determine_winner(player_choice, computer_choice, num_choices):
        half_num_choices = num_choices // 2
        if player_choice == computer_choice:
            return "Draw"
        elif (player_choice + half_num_choices) % num_choices == computer_choice:
            return "Computer wins"
        else:
            return "Player wins"

class HelpTableGenerator:
    @staticmethod
    def generate_help_table(choices):
        table = [[""] + choices]
        for player_choice in choices:
            row = [player_choice]
            for computer_choice in choices:
                result = GameRules.determine_winner(choices.index(player_choice), choices.index(computer_choice), len(choices))
                row.append(result)
            table.append(row)
        return table

class RockPaperScissors:
    def __init__(self, choices):
        self.choices = choices
        self.key = KeyGenerator.generate_key()
        self.computer_choice = random.randint(0, len(choices) - 1)
    
    def play(self):
        print(f"HMAC key: {self.key}")
        player_choice = self.get_player_choice()
        computer_choice = self.computer_choice
        hmac_result = HMACGenerator.generate_hmac(self.key, self.choices[computer_choice])
        
        print(f"Computer choice: {self.choices[computer_choice]}")
        print(f"HMAC: {hmac_result}")
        
        result = GameRules.determine_winner(player_choice, computer_choice, len(self.choices))
        print(result)
    
    def get_player_choice(self):
        while True:
            print("\nChoose your move:")
            for i, choice in enumerate(self.choices):
                print(f"{i + 1} - {choice}")
            try:
                player_choice = int(input("Your choice: ")) - 1
                if 0 <= player_choice < len(self.choices):
                    return player_choice
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) % 2 == 0:
        print("Usage: python script.py choice1 choice2 ...")
        sys.exit(1)

    choices = sys.argv[1:]
    game = RockPaperScissors(choices)
    game.play()
    help_table = HelpTableGenerator.generate_help_table(choices)
    print("\nHelp Table:")
    for row in help_table:
        print("\t".join(row))
