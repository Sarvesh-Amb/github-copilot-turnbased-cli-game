import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Character:
    name: str
    max_hp: int
    attack: int
    special: str
    special_damage: int


ROSTER = [
    Character("Lee Yung", 100, 12, "Dragon Kick", 24),
    Character("Ellie Shade", 90, 14, "Shadow Strike", 26),
    Character("Jax", 110, 11, "Thunder Smash", 23),
    Character("Kageyama", 95, 13, "Void Slash", 25),
]


@dataclass
class Fighter:
    character: Character
    hp: int
    guarding: bool = False
    special_cooldown: int = 0

    @classmethod
    def create(cls, character):
        return cls(character=character, hp=character.max_hp)


def choose_fighter():
    print("\nChoose your fighter:")
    for index, character in enumerate(ROSTER, start=1):
        print(
            f"  {index}. {character.name}  "
            f"HP {character.max_hp} | Attack {character.attack} | "
            f"Special: {character.special} ({character.special_damage} damage)"
        )

    while True:
        choice = input("Enter 1-4: ").strip()
        if choice in {"1", "2", "3", "4"}:
            return ROSTER[int(choice) - 1]
        print("Please enter a number from 1 to 4.")


def deal_damage(target, damage):
    if target.guarding:
        damage = max(1, damage // 2)
        target.guarding = False
        print(f"The guard absorbs part of the hit! {target.character.name} takes {damage}.")
    else:
        print(f"{target.character.name} takes {damage} damage.")
    target.hp = max(0, target.hp - damage)


def show_health(player, rival):
    print(f"\n{player.character.name}: {player.hp}/{player.character.max_hp} HP")
    print(f"{rival.character.name}: {rival.hp}/{rival.character.max_hp} HP")


def player_turn(player, rival):
    print("\nYour move:")
    print("  1. Attack")
    print("  2. Guard")
    special_status = (
        "ready" if player.special_cooldown == 0
        else f"cooldown: {player.special_cooldown} turn(s)"
    )
    print(f"  3. {player.character.special} ({special_status})")

    while True:
        choice = input("Choose 1-3: ").strip()
        if choice == "1":
            damage = random.randint(player.character.attack - 2, player.character.attack + 2)
            print(f"You strike {rival.character.name}!")
            deal_damage(rival, damage)
            return
        if choice == "2":
            player.guarding = True
            print("You brace for the next hit.")
            return
        if choice == "3":
            if player.special_cooldown:
                print("Your special move is still recharging.")
                continue
            print(f"You use {player.character.special}!")
            deal_damage(rival, player.character.special_damage)
            player.special_cooldown = 2
            return
        print("Please enter 1, 2, or 3.")


def rival_turn(rival, player):
    if rival.special_cooldown == 0 and random.random() < 0.35:
        print(f"\n{rival.character.name} uses {rival.character.special}!")
        deal_damage(player, rival.character.special_damage)
        rival.special_cooldown = 2
    elif random.random() < 0.2:
        rival.guarding = True
        print(f"\n{rival.character.name} takes a guarded stance.")
    else:
        damage = random.randint(rival.character.attack - 2, rival.character.attack + 2)
        print(f"\n{rival.character.name} attacks!")
        deal_damage(player, damage)


def duel(player_character):
    rival_character = random.choice(
        [character for character in ROSTER if character != player_character]
    )
    player = Fighter.create(player_character)
    rival = Fighter.create(rival_character)

    print(f"\nA challenger appears: {rival.character.name}!")
    print("Defeat your rival to win. Guards reduce the next hit; specials recharge after two turns.")

    while player.hp > 0 and rival.hp > 0:
        show_health(player, rival)
        player_turn(player, rival)
        if rival.hp == 0:
            break
        rival_turn(rival, player)
        player.special_cooldown = max(0, player.special_cooldown - 1)
        rival.special_cooldown = max(0, rival.special_cooldown - 1)

    show_health(player, rival)
    if player.hp > 0:
        print(f"\nVictory! {player.character.name} defeats {rival.character.name}!")
    else:
        print(f"\nDefeat! {rival.character.name} wins this time.")


def main():
    print("=== TURNBASED: CLI FIGHTER ===")
    while True:
        duel(choose_fighter())
        if input("\nFight again? (y/n): ").strip().lower() not in {"y", "yes"}:
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()