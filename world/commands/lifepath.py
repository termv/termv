from random import randint

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils import list_to_string
from world.data.lifepath import BASIC_LIFEPATH

class CmdLifepath(MuxCommand):
    """
    View and generate a character's lifepath.

    Usage:  +lifepath [<name>]
            +lifepath/generate [<name>]
    """

    key="+lifepath"
    aliases=["+lp", "+lpath"]

    def func(self):

        if "generate" in self.switches:

            # Check if there's a name given.  If so, check to make sure the caller is an admin.
            if not self.args or self.args and self.caller.locks.check_lockstring(self.caller, "dummy:perm(Admin)"):
                path = {}
                for k, v in BASIC_LIFEPATH:
                    path[k] = v[randint(1, 10)]


