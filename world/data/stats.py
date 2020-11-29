from math import floor

STATS = ["INT", "REF", "DEX", "TECH",
         "COOL", "WILL", "LUCK", "MOVE", "BODY", "EMP"]

STAT_STREETRAT_MATRIX = {
    "Tech": {
        "INT":  [6, 7, 8, 7, 6, 8, 8, 8, 6, 8],
        "REF":  [7, 6, 6, 8, 6, 7, 6, 8, 6, 8],
        "DEX":  [7, 6, 5, 7, 7, 5, 7, 7, 7, 5],
        "TECH": [8, 7, 7, 8, 6, 6, 8, 8, 8, 6],
        "COOL": [4, 5, 5, 4, 4, 3, 4, 5, 3, 4],
        "WILL": [4, 3, 4, 4, 3, 3, 4, 4, 3, 4],
        "LUCK": [5, 7, 7, 6, 7, 7, 7, 6, 5, 6],
        "MOVE": [5, 7, 7, 5, 7, 6, 6, 5, 7, 5],
        "BODY": [7, 5, 5, 6, 6, 6, 7, 6, 7, 6],
        "EMP":  [6, 5, 7, 7, 6, 7, 6, 6, 7, 6]
    },
    "Rockerboy": {
        "INT":  [7, 3, 4, 4, 3, 5, 5, 5, 3, 4],
        "REF":  [6, 7, 5, 5, 7, 6, 6, 7, 5, 5],
        "DEX":  [6, 7, 7, 7, 7, 7, 6, 7, 5, 6],
        "TECH": [5, 7, 7, 7, 7, 5, 7, 5, 6, 5],
        "COOL": [6, 7, 6, 6, 6, 7, 7, 6, 7, 8],
        "WILL": [8, 6, 6, 8, 8, 8, 8, 6, 8, 8],
        "LUCK": [7, 7, 7, 7, 6, 5, 7, 6, 7, 7],
        "MOVE": [7, 7, 7, 6, 5, 7, 6, 6, 5, 6],
        "BODY": [7, 5, 5, 6, 6, 6, 7, 6, 7, 6],
        "EMP":  [8, 8, 8, 8, 7, 7, 6, 8, 7, 7]
    },
    "Solo": {
        "INT":  [6, 7, 5, 5, 6, 7, 7, 7, 7, 6],
        "REF":  [7, 8, 8, 8, 6, 7, 7, 8, 7, 6],
        "DEX":  [7, 6, 7, 6, 7, 6, 6, 7, 6, 8],
        "TECH": [3, 3, 4, 4, 5, 5, 5, 5, 4, 5],
        "COOL": [8, 6, 7, 6, 7, 7, 6, 6, 6, 6],
        "WILL": [6, 6, 7, 7, 6, 6, 7, 6, 6, 6],
        "LUCK": [5, 7, 6, 6, 7, 6, 7, 5, 6, 5],
        "MOVE": [5, 5, 7, 5, 6, 7, 6, 6, 5, 6],
        "BODY": [6, 6, 8, 7, 8, 7, 6, 8, 6, 6],
        "EMP":  [5, 6, 5, 6, 4, 5, 6, 4, 5, 5]
    },
    "Netrunner": {
        "INT":  [5, 5, 5, 5, 5, 6, 6, 5, 7, 7],
        "REF":  [8, 6, 6, 7, 8, 6, 6, 7, 6, 8],
        "DEX":  [8, 6, 6, 7, 8, 6, 6, 7, 6, 8],
        "TECH": [7, 5, 6, 7, 5, 7, 7, 6, 7, 6],
        "COOL": [7, 8, 6, 7, 7, 8, 6, 8, 6, 6],
        "WILL": [4, 3, 4, 5, 3, 4, 5, 4, 3, 4],
        "LUCK": [8, 8, 7, 8, 7, 7, 7, 8, 6, 7],
        "MOVE": [7, 7, 6, 6, 5, 7, 7, 5, 5, 7],
        "BODY": [7, 5, 7, 5, 5, 6, 7, 7, 6, 5],
        "EMP":  [4, 5, 4, 5, 6, 6, 6, 4, 5, 6]
    },
    "Medtech": {
        "INT":  [7, 6, 6, 8, 6, 8, 8, 6, 6, 8],
        "REF":  [5, 7, 5, 7, 7, 5, 6, 5, 6, 7],
        "DEX":  [6, 7, 5, 6, 5, 5, 5, 7, 7, 6],
        "TECH": [7, 7, 5, 5, 7, 5, 5, 7, 7, 6],
        "COOL": [5, 4, 5, 3, 5, 5, 5, 3, 5, 3],
        "WILL": [3, 4, 3, 5, 5, 5, 4, 5, 4, 4],
        "LUCK": [8, 6, 8, 6, 8, 6, 8, 8, 6, 8],
        "MOVE": [5, 7, 5, 6, 7, 6, 5, 5, 6, 7],
        "BODY": [5, 7, 7, 5, 6, 5, 7, 5, 5, 6],
        "EMP":  [7, 7, 8, 7, 8, 6, 7, 8, 6, 7]
    },
    "Media": {
        "INT":  [6, 8, 6, 6, 6, 7, 8, 6, 7, 7],
        "REF":  [6, 7, 7, 5, 6, 5, 5, 5, 7, 6],
        "DEX":  [5, 7, 7, 7, 7, 5, 6, 6, 5, 6],
        "TECH": [5, 3, 5, 5, 4, 4, 3, 5, 4, 3],
        "COOL": [8, 6, 6, 6, 8, 8, 7, 6, 6, 7],
        "WILL": [7, 6, 8, 7, 7, 7, 6, 8, 7, 6],
        "LUCK": [5, 6, 5, 5, 6, 6, 6, 6, 6, 7],
        "MOVE": [7, 5, 5, 5, 7, 7, 5, 6, 5, 6],
        "BODY": [5, 6, 5, 6, 5, 5, 6, 7, 6, 7],
        "EMP":  [7, 8, 7, 6, 8, 8, 7, 8, 7, 6]
    },
    "Lawman": {
        "INT":  [5, 6, 5, 6, 6, 7, 7, 5, 7, 6],
        "REF":  [6, 6, 7, 6, 6, 6, 8, 6, 7, 6],
        "DEX":  [7, 6, 7, 7, 7, 5, 7, 6, 5, 5],
        "TECH": [5, 5, 7, 6, 6, 5, 5, 5, 5, 6],
        "COOL": [7, 6, 6, 6, 7, 7, 6, 6, 7, 8],
        "WILL": [8, 8, 7, 8, 7, 8, 8, 8, 7, 7],
        "LUCK": [5, 5, 5, 5, 6, 5, 7, 5, 6, 5],
        "MOVE": [6, 7, 5, 7, 5, 6, 6, 7, 5, 7],
        "BODY": [5, 5, 7, 7, 5, 7, 5, 6, 5, 6],
        "EMP":  [6, 5, 6, 6, 6, 4, 4, 4, 6, 6]
    },
    "Exec": {
        "INT":  [8, 8, 8, 8, 7, 5, 6, 6, 7, 7],
        "REF":  [5, 6, 7, 5, 7, 7, 6, 7, 6, 7],
        "DEX":  [5, 6, 6, 7, 6, 7, 7, 7, 7, 5],
        "TECH": [3, 4, 3, 5, 5, 3, 5, 3, 5, 5],
        "COOL": [8, 7, 8, 6, 8, 6, 8, 7, 7, 8],
        "WILL": [6, 6, 6, 5, 5, 7, 7, 5, 5, 6],
        "LUCK": [6, 7, 7, 6, 7, 6, 6, 7, 7, 6],
        "MOVE": [5, 7, 6, 5, 7, 5, 7, 5, 6, 7],
        "BODY": [5, 5, 4, 5, 5, 5, 4, 5, 5, 4],
        "EMP":  [7, 7, 5, 7, 6, 7, 6, 7, 5, 7]
    },
    "Fixer": {
        "INT":  [8, 8, 6, 7, 8, 8, 8, 6, 8, 6],
        "REF":  [5, 5, 6, 7, 6, 7, 6, 6, 7, 5],
        "DEX":  [7, 5, 6, 5, 6, 5, 6, 7, 7, 6],
        "TECH": [4, 5, 4, 5, 3, 5, 5, 4, 5, 5],
        "COOL": [6, 6, 5, 7, 6, 6, 6, 7, 5, 5],
        "WILL": [5, 7, 6, 6, 5, 7, 5, 6, 5, 6],
        "LUCK": [8, 8, 8, 7, 8, 7, 6, 7, 7, 8],
        "MOVE": [5, 7, 6, 7, 7, 5, 7, 7, 6, 6],
        "BODY": [5, 5, 3, 5, 5, 3, 5, 4, 5, 4],
        "EMP":  [8, 7, 8, 8, 6, 6, 8, 7, 7, 7]
    },
    "Nomad": {
        "INT":  [6, 5, 5, 5, 6, 7, 6, 5, 6, 5],
        "REF":  [6, 7, 8, 8, 6, 6, 7, 7, 7, 6],
        "DEX":  [8, 6, 6, 7, 6, 8, 8, 8, 6, 7],
        "TECH": [3, 5, 3, 4, 3, 4, 4, 3, 4, 4],
        "COOL": [6, 8, 8, 8, 6, 6, 6, 8, 8, 7],
        "WILL": [7, 8, 7, 6, 7, 7, 6, 6, 6, 8],
        "LUCK": [6, 8, 6, 7, 6, 6, 7, 7, 6, 7],
        "MOVE": [6, 7, 5, 7, 7, 5, 5, 5, 6, 7],
        "BODY": [6, 5, 6, 7, 7, 6, 7, 5, 6, 7],
        "EMP":  [4, 4, 5, 5, 4, 5, 5, 5, 6, 4]
    }
}


class StatHandler():
    """
    StatHandler houses all of the in-game information about a character's
    statistics.
    """

    def __init__(self):
        """
        Initialize the stat object and handle setting base and derived stats.
        """
        self.stats = {}
        self.hp = DerivedStat()
        self.humanity = DerivedStat()
        self.init(stats=STATS, base=0)

    def init(self, stats, base=0, temp=0):
        """
        init() takes in a list of stat names, and optional initial
        settings and adds them to the stats object.
        """

        for stat in stats:
            self.stats[stat] = {"base": base, "temp": temp, "effects": []}
        self.set_derived_stats()

    def assign(self, stat="", base=0):
        """
        Assign a new stat, or re-assign an existing stat.
        """
        if stat:
            self.stats[stat]["base"] = base
            self.stats[stat]["temp"] = 0
            self.set_derived_stats()

    def effect(self, stat, eff_name, mod=0, desc="", remove=False):
        """
        Set a new effect on a stat, or remove an existing effect.
        """
        if remove:
            for effect in self.stats[stat]["effects"]:
                if effect["name"].lower() == eff_name.lower():
                    self.stats[stat]["effects"].remove(effect)
        else:
            self.stats[stat]["effects"].append(
                {"name": eff_name, "mod": mod, "desc": desc})

    def set_derived_stats(self):
        self.humanity.base = 10 * self.stats["EMP"]["base"]
        self.hp.base = 10 + \
            floor((self.stats["BODY"]["base"] + self.stats["WILL"]["base"])/2)

    def current(self, stat):
        """
        Get the current level of a stat, taking any effects into account.
        """
        mod = 0
        for effect in self.stats[stat]["effects"]:
            mod += effect["mod"]

        if self.stats[stat]["temp"]:
            return self.stats[stat]["temp"] + mod
        else:
            return self.stats[stat]["base"] + mod


class DerivedStat():
    """
    Handle stats that follow a formula.
    """

    def __init__(self):
        self.base = 0
        self.temp = 0

    @ property
    def current(self):
        """
        Get the current value of a derived stat.
        """
        if self.temp:
            return self.temp
        else:
            return self.base
