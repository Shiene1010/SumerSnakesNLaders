import random
import time

class GameEngine:
    def __init__(self, board_size=100):
        self.board_size = board_size
        self.player_pos = 1
        self.karma = 0
        self.gold = 10
        self.stamina = 10
        self.inventory = []
        self.game_over = False
        
        # Ladders and Snakes
        self.ladders = {2: 38, 7: 14, 8: 31, 15: 26, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 78: 98, 87: 94}
        self.snakes = {16: 6, 46: 25, 49: 11, 62: 19, 64: 60, 74: 53, 89: 68, 92: 88, 95: 75, 99: 80}
        
        # Branching Paths: {start_pos: {choice_a: target_range, choice_b: target_range}}
        # This is a bit complex for a simple board, let's simplify to "Path Choice Events"
        
        self.narrative_events = {
            1: ("You stand before the gates of Ur. A beggar asks for gold.", 
                [("Give 2 Gold (+2 Karma)", "karma", 2, "gold", -2), 
                 ("Ignore them (-1 Karma)", "karma", -1, None, 0), 
                 ("Ask for a blessing (Costs 1 Stamina, +1 Karma)", "karma", 1, "stamina", -1)]),
            12: ("The road splits. The 'Serpent's Pass' is shorter but dangerous. The 'Merchant's Way' is long but safe.",
                 [("Serpent's Pass (Risky, +3 to dice)", "dice_bonus", 3, "stamina", -1), 
                  ("Merchant's Way (Safe, -1 to dice)", "dice_bonus", -1, "gold", -1)]),
            30: ("A mystical oasis appears. You can rest or search for treasure.",
                 [("Rest (+5 Stamina)", "stamina", 5, "gold", 0), 
                  ("Search for loot (Chance for Gold, costs 2 Stamina)", "gold_chance", 5, "stamina", -2)])
        }
        
        # Narrative bridges based on region
        self.regions = {
            (1, 20): "the dusty plains of Mesopotamia",
            (21, 50): "the dense palm groves along the Euphrates",
            (51, 80): "the treacherous mountain foothills",
            (81, 100): "the holy ascent to the Ziggurat summit"
        }

    def get_region_text(self, pos):
        for (start, end), text in self.regions.items():
            if start <= pos <= end:
                return text
        return "the unknown lands"

    def roll_dice(self, bonus=0):
        roll = random.randint(1, 6) + bonus
        return max(1, roll)

    def handle_hazard(self, pos, type="SNAKE"):
        if type == "SNAKE":
            print(f"\n[HAZARD] A giant serpent blocks your path at square {pos}!")
            print("1. Try to charm it (Roll 4+ to pass, using Karma)")
            print("2. Sacrifice 2 Gold to distract it")
            print("3. Accept your fate and fall back")
            
            try:
                choice = int(input("What do you do? "))
                if choice == 1:
                    success_threshold = 4 - (self.karma // 3)
                    roll = random.randint(1, 6)
                    print(f">> Rolled {roll} (Needed {max(2, success_threshold)})")
                    if roll >= success_threshold:
                        print(">> You charmed the serpent! You stay where you are.")
                        return False # Don't fall
                elif choice == 2 and self.gold >= 2:
                    self.gold -= 2
                    print(">> You threw gold at it. It seemed confused but let you pass.")
                    return False
            except: pass
            return True # Fall down
        return False

    def move_player(self, steps):
        self.stamina -= 1
        if self.stamina <= 0:
            print("\n[EXHAUSTION] You are too tired to move fast. (Dice -2)")
            steps = max(1, steps - 2)
            self.stamina = 2 # Partial recovery

        start_pos = self.player_pos
        new_pos = self.player_pos + steps
        
        region = self.get_region_text(new_pos)
        print(f"\n>> You travel through {region}...")

        if new_pos >= self.board_size:
            self.player_pos = self.board_size
            self.game_over = True
            return f"Rolled {steps}. You finally reached Square 100!"

        self.player_pos = new_pos
        msg = f"Rolled {steps}. Position: {self.player_pos}"

        # Hazard Checks
        if self.player_pos in self.snakes:
            if self.handle_hazard(self.player_pos, "SNAKE"):
                fall = self.snakes[self.player_pos]
                msg += f"\n[SNAKE] You fell to {fall}."
                self.player_pos = fall
        
        elif self.player_pos in self.ladders:
            jump = self.ladders[self.player_pos]
            print(f"\n[LADDER] You found a hidden path at square {self.player_pos}!")
            print("Expend 2 Stamina to climb? (y/n)")
            if input().lower() == 'y' and self.stamina >= 2:
                self.stamina -= 2
                msg += f"\n[LADDER] You climbed to {jump}."
                self.player_pos = jump
            else:
                print(">> You chose to stay on the ground.")
            
        return msg

def main():
    game = GameEngine()
    print("=== Sumerian Snakes & Ladders (CYOA v2.0) ===\n")
    
    while not game.game_over:
        print(f"\n--- [Pos: {game.player_pos}] [Gold: {game.gold}] [Stamina: {game.stamina}] [Karma: {game.karma}] ---")
        
        event = game.narrative_events.get(game.player_pos)
        dice_bonus = 0
        
        if event:
            text, choices = event
            print(f"\n[EVENT] {text}")
            for i, (c_text, *_) in enumerate(choices):
                print(f"{i+1}. {c_text}")
            
            try:
                c_idx = int(input("Choose: ")) - 1
                choice = choices[c_idx]
                print(f">> {choice[0]}")
                
                # Apply effects: (type, val, type2, val2)
                type1, val1, type2, val2 = choice[1], choice[2], choice[3], choice[4]
                if type1 == "karma": game.karma += val1
                elif type1 == "dice_bonus": dice_bonus = val1
                elif type1 == "stamina": game.stamina += val1
                elif type1 == "gold_chance": 
                    earned = random.randint(1, val1)
                    game.gold += earned
                    print(f">> Found {earned} Gold!")
                
                if type2 == "gold": game.gold += val2
                elif type2 == "stamina": game.stamina += val2
            except: pass
        else:
            input("Press Enter to roll...")

        print(game.move_player(game.roll_dice(dice_bonus)))
        time.sleep(0.3)

    if game.game_over:
        print("\n[FINISH] Legend has it, your journey will be sung for generations.")

if __name__ == "__main__":
    main()
