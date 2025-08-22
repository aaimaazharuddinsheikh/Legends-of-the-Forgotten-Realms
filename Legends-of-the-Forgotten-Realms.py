import time
import random

# --------- UTILS ---------
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def divider(sticker="✨"):
    print(sticker * 40)

def menu(options):
    for key, (desc, _) in options.items():
        print(f"{key}. {desc}")
    while True:
        choice = input("> ").strip()
        if choice in options:
            return options[choice][1]
        slow_print("❌ Invalid choice, try again.")

# --------- PLAYER STATE ---------
player = {
    "name": "",
    "class": "",
    "health": 100,
    "base_dmg": 15,
    "inventory": [],
    "quests": {
        "Find Key": False, 
        "Defeat Dragon": False, 
        "Treasure Hunt": False,
        "Help Traveler": False
    },
    "gold": 0,
    "location": "Start"
}

# --------- SCORE SYSTEM ---------
def calculate_score():
    score = 0
    breakdown = []

    for q, done in player["quests"].items():
        if done:
            score += 50
            breakdown.append(f"📜 {q}: +50")

    score += player["gold"] // 2
    breakdown.append(f"💰 Gold ({player['gold']}): +{player['gold']//2}")

    score += len(player["inventory"]) * 5
    breakdown.append(f"🎒 Items ({len(player['inventory'])}): +{len(player['inventory'])*5}")

    score += player["health"] // 2
    breakdown.append(f"❤️ Health ({player['health']}): +{player['health']//2}")

    return score, breakdown

def medal(score):
    if score >= 400:
        return "🏆 LEGENDARY HERO OF REALMS"
    elif score >= 300:
        return "🥇 GOLDEN CHAMPION"
    elif score >= 200:
        return "🥈 SILVER ADVENTURER"
    elif score >= 100:
        return "🥉 BRONZE EXPLORER"
    else:
        return "🪙 NOVICE WANDERER"

def show_score():
    divider("🏆")
    slow_print("📊 YOUR LEGENDARY SCORE 📊")
    score, breakdown = calculate_score()
    for b in breakdown:
        slow_print(b)
    divider("➡️")
    slow_print(f"TOTAL SCORE: {score} 🏅")
    slow_print(f"TITLE: {medal(score)}")
    divider("🏆")

# --------- COMBAT ---------
def combat(enemy, health, dmg):
    divider("⚔️")
    slow_print(f"A wild {enemy} appears! ⚔️")
    while health > 0 and player["health"] > 0:
        slow_print(f"❤️ Your HP: {player['health']} | {enemy} HP: {health}")
        action = input("[A]ttack / [R]un: ").lower()
        if action == "a":
            hit = random.randint(player["base_dmg"], player["base_dmg"] + 10)
            slow_print(f"💥 You strike for {hit} damage!")
            health -= hit
            if health <= 0:
                slow_print(f"🎉 You defeated the {enemy}!")
                player["gold"] += 20
                return True
            enemy_hit = random.randint(5, dmg)
            player["health"] -= enemy_hit
            slow_print(f"⚠️ {enemy} hits you for {enemy_hit} damage!")
        elif action == "r":
            chance = 0.5
            if player["class"] == "Rogue":
                chance = 0.8  # Rogues escape easier
            if random.random() < chance:
                slow_print("🏃 You fled the battle!")
                return False
            else:
                slow_print("❌ Failed to escape!")
                enemy_hit = random.randint(5, dmg)
                player["health"] -= enemy_hit
        else:
            slow_print("❌ Invalid choice!")
    if player["health"] <= 0:
        game_over()
    return False

# --------- SIDE QUESTS ---------
def side_quest():
    divider("🎲")
    slow_print("🌌 A side quest unfolds...")
    event = random.choice(["treasure", "traveler", "riddle", "ambush"])

    if event == "treasure":
        reward = random.choice(["Ancient Coin", "Mystic Gem", "Healing Potion"])
        player["inventory"].append(reward)
        gold_bonus = 15
        if player["class"] == "Rogue":
            gold_bonus += 10  # Rogues get more treasure
        player["gold"] += gold_bonus
        slow_print(f"💎 You discovered a hidden chest! You gain {reward} & {gold_bonus} gold!")

    elif event == "traveler":
        slow_print("🚶 A lost traveler asks for your help.")
        choice = input("[H]elp / [I]gnore: ").lower()
        if choice == "h":
            player["quests"]["Help Traveler"] = True
            player["gold"] += 30
            slow_print("✨ The traveler rewards you with 30 gold!")
        else:
            slow_print("❌ You walk away, leaving the traveler behind...")

    elif event == "riddle":
        slow_print("🧙 A mysterious sage asks a riddle:")
        slow_print("'What has cities, but no houses; mountains, but no trees; and water, but no fish?'")
        options = {
            "1": "A map",
            "2": "A dream",
            "3": "An ocean",
            "4": "A kingdom"
        }
        for k, v in options.items():
            print(f"{k}. {v}")
        ans = input("> ")
        if ans == "1":
            bonus = 25
            if player["class"] == "Mage":
                bonus += 15  # Mages get bonus gold for riddles
            player["gold"] += bonus
            slow_print(f"✅ Correct! The sage gives you {bonus} gold.")
        else:
            slow_print("❌ Wrong! The sage disappears...")

    elif event == "ambush":
        slow_print("⚠️ Bandits ambush you!")
        combat("Bandit", 50, 15)

# --------- LOCATIONS ---------
def dark_cave():
    player["location"] = "Cave"
    divider("🌌")
    slow_print("You step into the Dark Cave... echoes whisper your name.")

    if "torch" not in player["inventory"]:
        slow_print("🔥 You found a Torch!")
        player["inventory"].append("torch")

    combat("Goblin", 40, 12)

    divider("❓ RIDDLE ❓")
    slow_print("🔮 'I run but never move. What am I?'")
    riddle_options = {
        "1": ("A river", True),
        "2": ("A shadow", False),
        "3": ("The wind", False),
        "4": ("Time", True)
    }
    for key, (txt, _) in riddle_options.items():
        print(f"{key}. {txt}")
    choice = input("> ")
    if choice in riddle_options and riddle_options[choice][1]:
        if not player["quests"]["Find Key"]:
            player["inventory"].append("magical key")
            player["quests"]["Find Key"] = True
            slow_print("✨ Correct! You gained the Magical Key!")
    else:
        slow_print("❌ Wrong! The cave rumbles but spares you...")

    crossroads()

def castle_gate():
    player["location"] = "Castle"
    divider("🏰")
    if "magical key" in player["inventory"]:
        slow_print("🔑 You unlock the Castle Gates...")
        combat("Dragon", 80, 20)
        player["quests"]["Defeat Dragon"] = True
        slow_print("👑 Inside lies the Eternal Crown!")
        player["quests"]["Treasure Hunt"] = True
        ending()
    else:
        slow_print("🚪 The gate is sealed. You need a Magical Key.")
        crossroads()

def village_square():
    player["location"] = "Village"
    divider("🌳")
    slow_print("Welcome to the Village Square 🏘️.")
    slow_print("💰 A merchant offers you a healing potion for 10 gold.")
    choice = input("[B]uy / [L]eave: ").lower()
    if choice == "b" and player["gold"] >= 10:
        player["gold"] -= 10
        player["inventory"].append("potion")
        slow_print("🍷 Potion added to inventory!")
    elif choice == "b":
        slow_print("❌ Not enough gold!")

    if random.random() < 0.5:
        side_quest()

    crossroads()

# --------- MENUS ---------
def crossroads():
    player["location"] = "Crossroads"
    divider("🧭")
    slow_print("You stand at the Crossroads of Destiny.")
    next_action = menu({
        "1": ("Enter the Cave 🌌", dark_cave),
        "2": ("Travel to Castle 🏰", castle_gate),
        "3": ("Visit Village 🌳", village_square),
        "4": ("Take a Side Quest 🎲", side_quest),
        "5": ("Check Score 🏆", show_score),
        "6": ("Quit ❌", quit_game)
    })
    next_action()

# --------- ENDINGS ---------
def ending():
    divider("🌟")
    slow_print("✨ Your legend is complete! ✨")
    show_score()
    slow_print("🌌 YOUR LEGEND LIVES ON IN THE FORGOTTEN REALMS 🌌")
    quit()

def game_over():
    divider("💀")
    slow_print("You have fallen... 💀")
    show_score()
    slow_print("But perhaps your tale will be told in taverns...")
    quit()

# --------- START ---------
def choose_class():
    divider("⚔️")
    slow_print("Choose your Hero Class:")
    options = {
        "1": ("🛡️ Warrior – Strong & Tough", "Warrior"),
        "2": ("✨ Mage – Wise & Clever", "Mage"),
        "3": ("🗡️ Rogue – Sneaky & Lucky", "Rogue"),
    }
    for k, (desc, _) in options.items():
        print(f"{k}. {desc}")
    while True:
        choice = input("> ")
        if choice in options:
            player["class"] = options[choice][1]
            if player["class"] == "Warrior":
                player["health"] = 120
                player["base_dmg"] = 20
                player["gold"] = 10
            elif player["class"] == "Mage":
                player["health"] = 90
                player["base_dmg"] = 15
                player["gold"] = 20
            elif player["class"] == "Rogue":
                player["health"] = 100
                player["base_dmg"] = 15
                player["gold"] = 15
            slow_print(f"✅ You are now a {player['class']}!")
            break
        else:
            slow_print("❌ Invalid choice.")

def intro():
    divider("⚔️")
    title = r"""
██╗     ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗██████╗ ███████╗
██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝
██║     █████╗  ██║   ██║██║  ██║█████╗  ██╔██╗ ██║██║  ██║█████╗  
██║     ██╔══╝  ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  
███████╗███████╗╚██████╔╝██████╔╝███████╗██║ ╚████║██████╔╝███████╗
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
"""
    print(title)
    slow_print("🌌 Welcome, Adventurer, to the Legends of the Forgotten Realms ⚔️")
    player["name"] = input("Enter your hero name: ")
    choose_class()
    slow_print(f"✨ Brave {player['name']} the {player['class']}, your story begins...")
    crossroads()

def quit_game():
    slow_print("Thanks for playing! Farewell, adventurer 👋")
    quit()

# --------- RUN GAME ---------
if __name__ == "__main__":
    intro()
