import random
from game.hero import Hero
from game.monsters import Monster, Skeleton, Zombie


class DungeonRoom:

    def __init__(self, room_type: str):
        self.room_type = room_type
        self.monster = None
        self.is_searched = False
        self.description = self._generate_description()
        if random.random() < 0.7:
            self.monster = random.choice([Skeleton(), Zombie()])

    def _generate_description(self):
        descriptions = {
            'corridor': 'A long corridor lit by dim glowing stones.',
            'hall': 'A spacious hall with towering columns.',
            'treasury': 'The treasury of ancient rulers.',
            'entrance': 'The entrance to the dungeon. At first glance, it seems safe...',
            'exit': 'The exit from the dungeon! Salvation is near.',
        }
        return descriptions.get(self.room_type, 'An ordinary room.')

    def search_room(self, hero: Hero):
        if not hero or not hero.alive:
            return 'You do not have a living character!'
        if self.is_searched:
            return 'This room has already been searched.\nAvailable commands:\n/next, /flee'
        self.is_searched = True
        gold_found = random.randint(0, 40)
        hero.stats.coins += gold_found
        return f'You found {gold_found} gold coins!\nAvailable commands:\n/next, /flee'


class Dungeon:

    def __init__(self, dungeon_type: str):
        self.dungeon_type = dungeon_type
        self.rooms = self.generate_rooms(dungeon_type)
        self.current_room = 0

    def generate_rooms(self, dungeon_type: str):
        rooms = []
        room_count = random.randint(5, 8)
        room_types = ['corridor', 'hall', 'treasury']
        selected_types = ['entrance'] + random.choices(room_types, k=room_count - 2) + ['exit']
        for room_type in selected_types:
            rooms.append(DungeonRoom(room_type))
        return rooms

    def enter(self, hero: Hero) -> str:
        self.current_room = 0
        first_room = self.rooms[0]
        response = [
            f'You enter the {self.dungeon_type} dungeon. It has {len(self.rooms)} rooms.',
            f'You are now in room 1. {first_room.description}'
        ]
        if first_room.monster:
            monster_type = 'Skeleton' if isinstance(first_room.monster, Skeleton) else 'Zombie'
            response.append(f'A {monster_type} appears in the room!')
            response.append(first_room.monster.get_taunt())
        return '\n'.join(response)
