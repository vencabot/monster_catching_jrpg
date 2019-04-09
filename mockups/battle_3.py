import random

import dynamic_system_3

class Battle:
    def __init__(self):
        self.parties = []
        self.dynamic_rules = {"before": [], "after": []}

    def append_party(self, party):
        self.parties.append(party)
        party.battle = self

    def append_rule(self, rule):
        self.dynamic_rules[rule.check_phase].append(rule)


class BattleParty:
    def __init__(self, party_name):
        self.party_name = party_name
        self.units = []
        self.battle = None

    def append_unit(self, party_unit):
        self.units.append(party_unit)
        party_unit.party = self


class BattleUnit:
    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.hp = dynamic_system_3.DynamicAttribute(self, "hp", 10)
        self.atk = dynamic_system_3.DynamicAttribute(self, "atk", 5)
        self.mp = dynamic_system_3.DynamicAttribute(self, "mp", 5)
        self.abilities = {}
        self.party = None

    def learn_ability(self, ability_class):
        new_ability = ability_class(self)
        if new_ability.ability_name not in self.abilities:
            self.abilities[new_ability.ability_name] = []
        self.abilities[new_ability.ability_name].append(new_ability)


class UnitAbility:
    def __init__(self, ability_name, owner):
        self.ability_name = ability_name
        self.owner = owner

    def use(self, targets):
        glancing_chance = 15
        critical_chance = 15
        normal_chance = 100 - glancing_chance - critical_chance
        effectiveness_list = [
            self._use_glancing, self._use_normal, self._use_critical]
        effectiveness_weights = [
            glancing_chance, normal_chance, critical_chance]
        use_callables = random.choices(
                effectiveness_list, effectiveness_weights)
        if use_callables[0] == self._use_glancing:
            print(f"DIAGNOSTIC: {self.ability_name} was glancing.")
        elif use_callables[0] == self._use_critical:
            print(f"DIAGNOSTIC: {self.ability_name} was critical.")
        use_callables[0](targets)
        
    def _use_glancing(self, targets):
        self._use_normal(targets)

    def _use_normal(self, targets):
        pass

    def _use_critical(self, targets):
        self._use_normal(targets)
