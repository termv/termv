
CYBERWARE = {
    "name": {
        "install": "mall",
        "location": "Neural Link",
        "slots": 0,
        "size": 1,
        "cost": 100,
        "HL": [0, 1, 6]
    }
}


class CyberHandler:

    def __init__(self):
        """
        Set a character up to use the cyberware system.
        """
        self.cyberware = [
            {
                "name": "fashionware",
                "location": "meta",
                "slots": [7, 0],
                "spaces": 0,
                "size": 0,
                "notes": ""
            },
            {
                "name": "internal",
                "location": "meta",
                "slots": [7, 0],
                "spaces": 0,
                "size": 0,
                "notes": ""
            },
            {
                "name": "external",
                "location": "meta",
                "slots": [7, 0],
                "spaces": 0,
                "size": 0,
                "notes": ""
            }
        ]

    def install(self, name, location, slots, size, notes=""):
        "Add a new piece of cyberware"
        ware = {
            "name": name,
            "location": location,
            "slots": slots,
            "size": size,
            "notes": notes
        }

        self.cyberware.append(ware)

    def remove(self, name):
        self.cyberware = [
            ware for ware in self.cyberware if ware["name"] != name]

    def get(self, cyber):
        for ware in self.cyberware:
            if ware["name"].lower() == cyber.lower():
                return ware
