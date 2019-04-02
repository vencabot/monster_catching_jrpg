class DynamicEvent:
    def __init__(
            self, target, attr_name, new_value, old_value, perpetrator):
        self.target = target
        self.attr_name = attr_name
        self.new_value = new_value
        self.old_value = old_value
        self.perpetrator = perpetrator
        self.prevented = False

class DynamicAttribute:
    def __init__(self, owner, attr_name, value):
        self.owner = owner
        self.attr_name = attr_name
        self.value = value

    def update(self, new_value, perpetrator):
        old_value = self.value
        dynamic_event = DynamicEvent(
                self.owner, self.attr_name, new_value, old_value,
                perpetrator)
        print(f"DIAGNOSTIC: Proposed value change to {new_value}.")
        if new_value == old_value:
            return
        rules = self.owner.party.battle.dynamic_rules
        for dynamic_rule in rules["preemption"]:
            dynamic_rule.check(dynamic_event)
        if dynamic_event.prevented:
            for dynamic_rule in rules["prevention"]:
                dynamic_rule.check(dynamic_event)
            return
        self.value = new_value
        for dynamic_rule in rules["reaction"]:
            dynamic_rule.check(dynamic_event)


class BattleUnit:
    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.hp = DynamicAttribute(self, "hp", 10)
        self.atk = DynamicAttribute(self, "atk", 5)
        self.party = None

    def slap(self, target_unit):
        print(f"{self.unit_name} slapped {target_unit.unit_name}!")
        new_hp = target_unit.hp.value - 2
        target_unit.hp.update(new_hp, self)


class BattleParty:
    def __init__(self, party_name):
        self.party_name = party_name
        self.units = []
        self.battle = None

    def append_unit(self, party_unit):
        self.units.append(party_unit)
        party_unit.party = self


class Battle:
    def __init__(self):
        self.parties = []
        self.dynamic_rules = {
                "preemption": [], "prevention": [], "reaction": []}

    def append_party(self, party):
        self.parties.append(party)
        party.battle = self

    def append_rule(self, rule):
        self.dynamic_rules[rule.check_phase].append(rule)


class DynamicRule:
    def __init__(self, rule_name, check_phase):
        self.rule_name = rule_name
        self.recurrence_counter = 0
        self._recurrence_limit = 1
        self.check_phase = check_phase

    def check(self, dynamic_event):
        if self.recurrence_counter >= self._recurrence_limit:
            self._at_limit(dynamic_event)
            return False
        if dynamic_event.prevented:
            self._fail(dynamic_event)
            return False
        elif self._check(dynamic_event):
            self.recurrence_counter += 1
            self._trigger(dynamic_event)
            return True

    def _check(self, dynamic_event):
        return False

    def _trigger(self, dynamic_event):
        pass

    def _at_limit(self, dynamic_event):
        #print(f"{self.rule_name} has reached its limit.")
        pass

    def _fail(self, dynamic_event):
        print(f"{self.rule_name} failed to trigger.")
