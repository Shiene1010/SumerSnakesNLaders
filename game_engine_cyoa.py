import time
import sys

class CYOAEngine:
    def __init__(self):
        self.gold = 10
        self.stamina = 10
        self.karma = 0
        self.current_node = "start"
        self.game_over = False
        
        # Scenario Nodes: {node_id: {description: str, options: [ (text, next_node, effects) ]}}
        # Effects: {stat: change}
        self.scenarios = {
            "start": {
                "description": "You stand before the ancient gates of Ur. Your journey to the Ziggurat begins here.",
                "options": [
                    ("Give 2 Gold to the gate beggar (+Karma)", "plains_intro", {"gold": -2, "karma": 2}),
                    ("Sneak past the guards (Costs 2 Stamina)", "plains_intro", {"stamina": -2}),
                    ("Ask for a merchant's blessing (Costs 2 Gold, +1 Bonus step later)", "plains_intro", {"gold": -2, "karma": 1})
                ]
            },
            "plains_intro": {
                "description": "You enter the dusty plains of Mesopotamia. The sun is harsh.",
                "options": [
                    ("Sprint across (Fast, -3 Stamina)", "palm_groves", {"stamina": -3}),
                    ("Walk slowly (Conserves energy, -1 Stamina)", "lowlands_enc", {"stamina": -1}),
                    ("Search for water (-1 Stamina, +2 Stamina if lucky)", "water_find", {"stamina": -1})
                ]
            },
            "water_find": {
                "description": "You find a small well. It's refreshing!",
                "options": [
                    ("Continue to the palm groves", "palm_groves", {"stamina": 3})
                ]
            },
            "lowlands_enc": {
                "description": "In the lowlands, you encounter a traveling scribe.",
                "options": [
                    ("Buy a map (Costs 5 Gold, jump to Foothills)", "foothills_intro", {"gold": -5}),
                    ("Ignoring him, continue walking", "palm_groves", {"stamina": -1})
                ]
            },
            "palm_groves": {
                "description": "The dense palm groves provide shade, but hide danger.",
                "options": [
                    ("Take the 'Serpent's Shortcut' (Fast but risky)", "snake_hazard", {"stamina": -1}),
                    ("Stay on the main road (Safe but long)", "oasis", {"stamina": -2})
                ]
            },
            "snake_hazard": {
                "description": "[SNAKE] A giant cobra blocks the shortcut!",
                "options": [
                    ("Try to charm it (Requirement: Karma > 1)", "foothills_intro", {"karma": 1}), # Logic will handle failure
                    ("Pay 3 Gold to distract it", "foothills_intro", {"gold": -3}),
                    ("Retreat in fear (Reset to start of groves)", "palm_groves", {"stamina": -1})
                ]
            },
            "oasis": {
                "description": "You've reached a beautiful oasis. A perfect place to recover.",
                "options": [
                    ("Rest deeply (+5 Stamina)", "foothills_intro", {"stamina": 5}),
                    ("Trade with merchants (Spend Gold for Stamina)", "foothills_intro", {"gold": -3, "stamina": 3})
                ]
            },
            "foothills_intro": {
                "description": "The mountain foothills are steep. The Ziggurat is visible now.",
                "options": [
                    ("Climb the 'Ladder of Heaven' (Costs 5 Stamina, huge jump)", "summit", {"stamina": -5}),
                    ("Take the winding path (-2 Stamina)", "hermit_cave", {"stamina": -2})
                ]
            },
            "hermit_cave": {
                "description": "An old hermit offers you a final riddle before the summit.",
                "options": [
                    ("Solve the riddle (Requires 2 Karma)", "summit", {"karma": 1}),
                    ("Ignore him and climb alone", "summit", {"stamina": -3})
                ]
            },
            "summit": {
                "description": "You reached the pinnacle of the Ziggurat! The gods smile upon you.",
                "options": [] # End state
            }
        }

    def apply_effects(self, effects):
        for stat, change in effects.items():
            if stat == "gold": self.gold += change
            elif stat == "stamina": self.stamina += change
            elif stat == "karma": self.karma += change

    def play(self):
        print("=== Sumerian Legend: The Path to Ur (Pure CYOA) ===\n")
        
        while not self.game_over:
            node = self.scenarios[self.current_node]
            print(f"\n--- [Gold: {self.gold}] [Stamina: {self.stamina}] [Karma: {self.karma}] ---")
            print(f"\n{node['description']}")
            
            if not node['options']:
                print("\n[FINISH] Your journey is complete.")
                self.game_over = True
                break
                
            for i, (opt_text, *_) in enumerate(node['options']):
                print(f"{i+1}. {opt_text}")
                
            try:
                choice_idx = int(input("\nWhat is your choice? ")) - 1
                selected_opt = node['options'][choice_idx]
                
                # Special Logic for Requirement checks (e.g., Snake Charm)
                if self.current_node == "snake_hazard" and choice_idx == 0:
                    if self.karma <= 1:
                        print("\n>> You failed to charm the snake! It bites you. (Stamina -5, retreating)")
                        self.apply_effects({"stamina": -5})
                        self.current_node = "palm_groves"
                        continue

                # Normal transition
                self.current_node = selected_opt[1]
                self.apply_effects(selected_opt[2])
                
                if self.stamina <= 0:
                    print("\n[DEFEAT] You collapsed from exhaustion in the desert.")
                    self.game_over = True
                    break
                    
            except (ValueError, IndexError):
                print(">> You hesitated. Please choose a valid path.")

if __name__ == "__main__":
    game = CYOAEngine()
    game.play()
