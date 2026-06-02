from dataclasses import dataclass
from typing import List, Dict, Tuple, Any
from game.enums import DamageType


@dataclass
class ActiveEffect:
    effect_type: DamageType
    base_damage: float
    duration: int = 0
    stacks: int = 1
    chance: float = 0.2
    stun: bool = False
    slow: bool = False
    damage_reduction: float = 1.0
    is_finished: bool = False

    @property
    def current_damage(self) -> float:
        if self.effect_type == DamageType.POISON:
            return self.base_damage * self.stacks
        return self.base_damage

    def tick(self, target, messages: List[str], owner_name: str, end_effects: List[str]) -> None:
        damage_dealt = 0.0

        if self.effect_type == DamageType.POISON:
            damage_dealt = self.base_damage * self.stacks
        elif self.effect_type in (
            DamageType.FIRE,
            DamageType.FROST,
            DamageType.LIGHTNING,
            DamageType.BLEEDING,
        ):
            damage_dealt = self.base_damage

        if damage_dealt > 0:
            action_messages = {
                DamageType.FIRE: f"{owner_name} is burning and takes {damage_dealt:.1f} damage!",
                DamageType.FROST: f"{owner_name} is freezing and takes {damage_dealt:.1f} damage!",
                DamageType.LIGHTNING: f"{owner_name} trembles from the lightning strike and takes {damage_dealt:.1f} damage!",
                DamageType.BLEEDING: f"{owner_name} is bleeding and loses {damage_dealt:.1f} health!",
                DamageType.POISON: f"{owner_name} suffers from poison and loses {damage_dealt:.1f} health!",
            }
            messages.append(
                action_messages.get(
                    self.effect_type,
                    f"{owner_name} takes {damage_dealt:.1f} damage."
                )
            )
            target.health = max(0, round(target.health - damage_dealt, 1))

        if self.stun:
            target.is_stunned = True
            messages.append(f"{owner_name} is stunned and skips a turn!")

        if self.slow:
            target.is_slowed = True
            target.damage_reduction *= self.damage_reduction
            messages.append(f"{owner_name} is slowed! Damage is reduced.")

        self.duration -= 1

        if self.duration <= 0:
            end_effects.append(f"The {self.effect_type.value} effect has ended on {owner_name}.")
            self.is_finished = True

    def apply(self) -> Tuple[float, str, bool, Dict[str, Any]]:
        effect_data = {
            'stun': False,
            'slow': False,
            'damage_reduction': 1.0
        }

        if self.effect_type == DamageType.FIRE:
            self.duration = 2
            effect_message = (
                f"The monster is affected by Fire "
                f"({self.base_damage:.1f} damage each round for {self.duration} rounds)"
            )
        elif self.effect_type == DamageType.FROST:
            self.duration = 2
            effect_data['slow'] = True
            effect_data['damage_reduction'] = 0.7
            effect_message = (
                f"The monster is affected by Frost "
                f"({self.base_damage * 0.5:.1f} damage each round for {self.duration} rounds, speed reduced)"
            )
        elif self.effect_type == DamageType.LIGHTNING:
            self.duration = 1
            effect_data['stun'] = True
            effect_message = (
                f"The monster is struck by Lightning! "
                f"({self.base_damage:.1f} damage for {self.duration} round, stunned)"
            )
        elif self.effect_type == DamageType.POISON:
            self.duration = 2
            effect_message = (
                f"The monster is poisoned "
                f"({self.base_damage:.1f} damage each round for {self.duration} rounds, {self.stacks} stack(s))"
            )
        elif self.effect_type == DamageType.BLEEDING:
            self.duration = 2
            effect_message = (
                f"The monster is bleeding "
                f"({self.base_damage * 1.2:.1f} damage each round for {self.duration} rounds)"
            )

        return (self.current_damage, effect_message, True, effect_data)

    def stack_up(self):
        if self.effect_type in (DamageType.POISON, DamageType.BLEEDING):
            self.stacks += 1


@dataclass
class BleedingEffect(ActiveEffect):
    def __init__(self, damage: float, duration: int, chance: float):
        super().__init__(
            effect_type=DamageType.BLEEDING,
            base_damage=damage,
            duration=duration,
            stacks=1,
            chance=chance
        )
