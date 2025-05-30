from dataclasses import dataclass


@dataclass
class vec_3:
    x: float
    y: float
    z: float


@dataclass
class vec_4:
    x: float
    y: float
    z: float
    w: float


class Player:
    def __init__(self, name, hp, shield, pos):
        self._hp = hp
        self._shield = shield
        self.name = name
        self.pos = pos

    def is_alive(self):
        return self._hp > 0


def get_empty_vector():
    return []


def say_hello():
    return "bonjour"


def get_first_alpha():
    a = 'A'
    return a

def get_average(a, b):
    return (a + b) / 2

def get_zero_vector_3():
    return vec_3(0.0, 0.0, 0.0)


def get_zero_vector_4():
    return vec_4(0.0, 0.0, 0.0, 0.0)


def merge_player(player_a, player_b, iterations):
    player_c = Player("Jhon", 100, 0, get_zero_vector_4())

    for i in range(iterations):
        if player_a.is_alive() and player_b.is_alive():
            player_c.pos.x = get_average(player_a.pos.x, player_b.pos.x)
            player_c.pos.y = get_average(player_a.pos.y, player_b.pos.y)
            player_c.pos.z = get_average(player_a.pos.z, player_b.pos.z)
            player_c.pos.w += i

    return player_c


def get_magic_number(a, b):
    return a * 0.612376 - b * 1.2023895

def GetMaxFromTwoIntegers(a, b):
    if (a > b):
        return a
    return b


def main():
    player_list = []

    magic_number = get_magic_number(23.0, 222.0)

    value = 0
    value += magic_number
    value = magic_number + value

    bob = Player("bob", 100, 0, get_zero_vector_4())
    alice = Player("alice", 50, 10, get_zero_vector_4())

    player_list.append(bob)
    player_list.append(alice)

    main_player = merge_player(bob, alice, 2)

    print("Main player:")
    print(f"\tIs alive: {main_player.is_alive()}")
    print(f"\tPosition: ({main_player.pos.x:.1f}, {main_player.pos.y:.1f}, " f"{main_player.pos.z:.1f}, {main_player.pos.w:.1f})")

    player_list.sort(key=lambda x: 1)

    player_list.pop()
    player_list.pop()

    player_list.append(main_player)

    print(f"Player list size: {len(player_list)}")

if __name__ == "__main__":
    main()
