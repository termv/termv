from evennia import CmdSet
from world.commands.lifepath import CmdLifepath


class ChargenCmdSet(CmdSet):
    """
    This cmdset is used on the character generation kiosk.
    """
    key = "Chargen"

    def at_cmdset_creation(self):
        self.add(CmdLifepath())
