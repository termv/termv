from random import randint

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils import list_to_string
from evennia.utils.evtable import EvTable
from world.data.lifepath import BASIC_LIFEPATH, ROLE_PATHS, FRIENDS, ENEMY, CAUSE, THROW_AT_YOU, REVENGE, \
    TRAGIC_LOVE_AFFAIR, GOALS, \
    INDEX_DICTS, SECTIONS, INDEX_LISTS


class CmdLifepath(MuxCommand):
    """
    View and generate a character lifepath. When given the '/generate' flag,
    you'll generate an entire basic lifepath. When given a <section> it will
    (re)generate that section. When given the '/section' flag, View a portion
    of the character's lifepath. The '/role' flag along with a role will
    generate a character's professional lifepath.

    Usage:  +lifepath/generate [<section>]
            +lifepath/role <role>
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

        def send_list(caller, name, item_list):
            """Generate a title and table for a list abd send them to the caller"""
            tbl = EvTable(border="cells")
            tbl.reformat(width=78, align="l")
            caller.msg(f"--->> |h{name.capitalize()}|n >>".ljust(82, "-"))
            for itm in item_list:
                tbl.add_row(itm)
            caller.msg(tbl)

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

                table = EvTable(border="cells")
                table.reformat(width=78, align="l")
                string = f"--->> |hBasic Lifepath Quick View|n >>".ljust(82, "-")
                for item in SECTIONS["personality"]:
                    table.add_row(f"|h{item}|n", self.caller.db.lifepath_basic[item])
                self.caller.msg(string)
                self.caller.msg(table)
                self.caller.msg(f"Friends: |h{len(friends)}|n, Enemies: |h{len(enemies)}|n, Lovers: "
                                f"|h{len(lovers)}|n\n")
                self.caller.msg(f"Sections: {list_to_string(INDEX_DICTS + INDEX_LISTS)}.")
                self.caller.msg("Use '|h+lifepath/section <section>|n' to view a section.")

                self.caller.msg("Don't forget to use '|h+lifepath/role <path>|n' for your role lifepath!")
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
                    self.caller.msg(f"Unknown lifepath section. Valid "
                                    f"sections are {list_to_string(INDEX_DICTS + INDEX_LISTS)}.")
        elif "section" in self.switches:

            # If it's a section within the first part of basic lifepath generation, just show it.
            if self.args and self.args.lower() in INDEX_DICTS:
                table = EvTable(border="cells")
                table.reformat(width=78, align="l")
                self.caller.msg(f"--->> |h{self.args.capitalize()}|n >>".ljust(82, "-"))
                for item in SECTIONS[self.args.lower()]:
                    table.add_row(f"{item}", self.caller.db.lifepath_basic[item])
                self.caller.msg(table)
            elif self.args and self.args.lower() == "friends":
                send_list(self.caller, "Friends", self.caller.db.lifepath_friends)
            elif self.args and self.args.lower() == "enemies":
                send_list(self.caller, "enemies", self.caller.db.lifepath_enemies)
            elif self.args and self.args.lower() == "lovers":
                send_list(self.caller, "lovers", self.caller.db.lifepath_lovers)
            elif self.args and self.args.lower() == "role" and self.caller.db.lifepath_role:
                send_list(self.caller, f"Role: {self.caller.db.role}", self.caller.db.lifepath_role)
            else:
                self.caller.msg(f"Unknown lifepath section. Valid "
                                f"sections are {list_to_string((INDEX_DICTS + INDEX_LISTS + ['role']))}.")
        elif "role" in self.switches:
            try:
                if ROLE_PATHS[self.args.capitalize()]:
                    self.caller.msg(f"--->> |h{self.args.capitalize()} Lifepath Generation|n >>".ljust(82, "-"))
                    role = {}
                    table = EvTable(border="cells")
                    table.reformat(width=78, align="l")
                    for topic in ROLE_PATHS[self.args.capitalize()]:
                        role[topic] = get_rand(ROLE_PATHS[self.args.capitalize()][topic])
                        table.add_row(f"|h{topic}|n", role[topic])
                    self.caller.msg(table)
                    self.caller.db.lifepath_role = role
                    self.caller.db.role = self.args.capitalize()

                else:
                    roles = [x for x in ROLE_PATHS]
                    self.caller.msg(f"That's not a valid role. Valid roles are {list_to_string(roles)}")
            except KeyError:
                roles = [x for x in ROLE_PATHS]
                self.caller.msg(f"That's not a valid role. Valid roles are {list_to_string(roles)}")
        else:
            msg = "Unknown Option, valid commands are:\n\n" \
                  "+lifepath/generate [<section>]\n" \
                  "+lifepath/role <Role>\n" \
                  "+lifepath/section <section>\n"

            self.caller.msg(msg)
