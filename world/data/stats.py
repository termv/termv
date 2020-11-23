from math import floor

STATS = ["INT", "REF", "DEX", "TECH",
         "COOL", "WILL", "LUCK", "MOVE", "BODY", "EMP"]

TECH_STAT_MATRIX = {
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
}


class StatHandler():
    """
    StatHandler houses all of the in-game information about a character's 
    statistics.  
    """

    def __init__(self, stats, base=0):
        """
        Initialize the stat object and handle setting base and derived stats.
        """
        self.stats = {}
        self.init(stats=stats, base=base)
        self.hp = DerivedStat(
            lambda body, will: 10 + floor((body + will)/2))
        self.humanity = DerivedStat(lambda emp: 10 * emp)

    def init(self, stats, base=0, temp=0):
        """
        init() takes in a list of stat names, and optional initial
        settings and adds them to the stats object.
        """
        for stat in STATS and not self.stats[stat]:
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
        self.stats[stat]["effects"].append(
            {"name": eff_name, "mod": mod, "desc": desc})
        if remove:
            for effect in self.stats[stat]["effects"]:
                if effect["name"].lower() == eff_name.lower():
                    self.stats[stat]["effects"].remove(effect)

    def set_derived_stats(self):
        # Check for the existance of pre-req stats then calculate derived.
        if self.stats["EMP"]:
            self.humanity.calc(self.stats["EMP"])

        if self.stats["BODY"] and self.stats["WILL"]:
            self.hp.calc(self.stats["BODY"]["base"],
                         self.stats["WILL"]["base"])

    def get_current(self, stat):
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

    def __init__(self, calc):
        self.base = 0
        self.temp = 0
        self.calc = calc

    @property
    def current(self):
        """
        Get the current value of a derived stat.
        """
        if self.temp:
            return self.temp
        else:
            return self.base
