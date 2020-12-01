from random import randint

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.evtable import EvTable
from world.data.lifepath import BASIC_LIFEPATH, FRIENDS, ENEMY, CAUSE, THROW_AT_YOU, REVENGE, TRAGIC_LOVE_AFFAIR, GOALS, \
    INDEX_DICTS, SECTIONS, INDEX_LISTS


class CmdLifepath(MuxCommand):
    """
    View and generate a character lifepath.  The first form of the command gives general information about a
    character's lifepath, if they've generated one, with a few quick glance fields.  When given the '/generate'
    flag, you'll generate an entire basic lifepath.  When given a <section> it will (re)generate that section.
    When given the '/section' flag, View a portion of the character's lifepath, or use 'all' to see the whole
    lifepwath at once (not recommended!).

    Usage:  +lifepath [<name>]
            +lifepath/generate [<section>]
            +lifepath/section [[<name>=] <section>]
    """

    key = "+lifepath"
    aliases = ["+lp", "+lpath"]

    def func(self):

        def get_rand(lst):
            return lst[randint(0, len(lst) - 1)]

        def rand_list(name, item_list, number):
            """Generate a random list"""
            tbl = EvTable(border="cells")
            tbl.reformat(width=78, align="l")
            items = []
            for itm in range(number):
                items.append(get_rand(item_list))
            for itm in items:
                tbl.add_row(f"|h{itm}|n")
            return [tbl, items]

        if "generate" in self.switches:
            # Check if there's a name given.  If so, check to make sure the caller is an admin.
            if not self.args:
                path = {}
                num_friends = randint(1, 10) - 7
                num_enemies = randint(1, 10) - 7
                num_lovers = randint(1, 10) - 7
                friends, enemies, lovers = [], [], []

                for k in BASIC_LIFEPATH:
                    path[k] = BASIC_LIFEPATH[k][randint(0, len(BASIC_LIFEPATH[k]) - 1)]

                path["What's Your Goal?"] = get_rand(GOALS)
                self.caller.db.lifepath_basic = path

                if num_friends > 0:
                    for friend in range(num_friends):
                        friends.append(get_rand(FRIENDS))
                    self.caller.db.lifepath_friends = friends

                if num_enemies > 0:
                    for enemy in range(num_enemies):
                        who = get_rand(ENEMY)
                        cause = get_rand(CAUSE)
                        what = get_rand(THROW_AT_YOU)
                        do = get_rand(REVENGE)
                        enemies.append(f"{who} {cause} {what} The next time you see them you'll {do}\n")
                    self.caller.db.lifepath_enemies = enemies

                if num_lovers > 0:
                    for lover in range(num_lovers):
                        lovers.append(get_rand(TRAGIC_LOVE_AFFAIR))
                    self.caller.db.lifepath_lovers = lovers

                self.caller.msg("|hBasic lifepath generated|n. Use '|h+lifepath/section <section>|n' to view it.")
            else:
                if self.args.lower() in INDEX_DICTS:
                    table = EvTable(border="cells")
                    table.reformat(width=78, align="l")
                    string = f"--->> |h{self.args.capitalize()}|n >>".ljust(82, "-")
                    for item in SECTIONS[self.args.lower()]:
                        table.add_row(f"|h{item}|n", self.caller.db.lifepath_basic[item])
                    self.caller.msg(string)
                    self.caller.msg(table)

                elif self.args.lower() == "friends":
                    results = rand_list("friends", FRIENDS, randint(1, 10) - 7)
                    self.caller.msg(f"--->> |h{self.args.capitalize()}|n >>".ljust(82, "-"))
                    self.caller.msg(results[0])
                    self.caller.db.lifepath_friends = results[1]

                elif self.args.lower() == "enemies":
                    table = EvTable(border="cells")
                    table.reformat(width=78, align="l")
                    num_enemies = randint(1, len(ENEMY) - 1) - 7
                    enemies = []
                    self.caller.msg(f"--->> |h{self.args.capitalize()}|n >>".ljust(82, "-"))
                    if num_enemies > 0:
                        for enemy in range(num_enemies):
                            who = get_rand(ENEMY)
                            cause = get_rand(CAUSE)
                            what = get_rand(THROW_AT_YOU)
                            do = get_rand(REVENGE)
                            enemies.append(f"{who} {cause} {what} The next time you see them you'll {do}\n")
                            table.add_row(f"{who} {cause} {what} The next time you see them you'll {do}\n")
                        self.caller.msg(table)
                        self.caller.db.lifepath_enemies = enemies

                elif self.args.lower() == "lovers":
                    results = rand_list("lovers", TRAGIC_LOVE_AFFAIR, randint(1, 10) - 7)
                    self.caller.msg(f"--->> |h{self.args.capitalize()}|n >>".ljust(82, "-"))
                    self.caller.msg(results[0])
                    self.caller.db.lifepath_lovers = results[1]
                else:
                    self.caller.msg(f"That's not a valid lifepath section.  For valid sections, see '|h+lifepath|n'.")

