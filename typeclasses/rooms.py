"""
Room

Rooms are simple containers that has no location of their own.

"""
from collections import defaultdict

from evennia import DefaultRoom
from evennia.utils import wrap, time_format


def format_time(idle_time, param):
    pass


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """

        def char_string(con, char):
            """
            Format the display from the character object to show some information about each character in the room
            when one does a look command.
            """
            output = ""
            if con.is_superuser:
                output += " |h|y*|n "
            else:
                output += "   "
            output += con.get_display_name(char).ljust(20)
            if con == char:
                output += "0s".rjust(5)
            else:
                output += time_format(con.idle_time, 1).rjust(5)
            output += "  "
            if con.db.shotdesc:
                output += (con.db.shortdesc[:45] + "...") if len(con.db.shortdesc) > 48 else con.db.shortdesc
            else:
                output += "|h|xUse '+shortdesc <desc>' to set this field.|n"
            output += "\n"
            return output

        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(con)
            elif con.has_account:
                users.append(char_string(con, looker))
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        string = f"--->> |h{self.get_display_name(looker)}|n >>".ljust(82, "-") + "\n\n"
        desc = wrap(self.db.desc, width=78)
        if desc:
            string += "%s\n\n" % desc
        string += "--->> |hCharacters|n >>".ljust(82, "-") + "\n"
        string += "|hName|n".ljust(28) + "|hIdle|n".rjust(5) + "  " + "|hShort Description|n\n"
        for user in users:
            string += user
        string += "\n"
        if things:
            string += "--->> |hObjects|n >>".ljust(82, "-") + "\n"
            for k, v in things:
                string += f"{'x' + str(len(v)) + ' A ' if len(v) > 1 else 'A '} " \
                          f"{v[0].get_display_name(looker)} " \
                          f"{v[0].db.placement if v[0].db.placement else 'sits here'}\n"
        if exits:
            string += "--->> |hExits|n >>".ljust(82, "-") + "\n"
            for ext in exits:
                aliases = ext.aliases.all()
                aliases.sort()
                string += f"|h{ext.get_display_name(looker)}|n-<|h{aliases[0].upper()}|n>\n"
        return string
