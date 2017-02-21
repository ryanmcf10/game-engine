import json

class CharacterBuilder():
    """
    CHARACTER BUILDER
    
    """
    def __init__(self, directory):
        self.directory = directory

    """
    Build a new character from a json file

    Example formatting of a valid json file:

    !! All characters must have "meta" token, all other tokens are optional
    {
        "meta":
        {
            "name":"string",
        }
        "overworld":
        {
            "spritesheet":"filename",
            "num_cols":int,
            "num_rows":int,
            "animated":bool,
            "animation_dictionary":
            {
                "UP":[1, 2, 3],
                "DOWN":[4, 5 , 6]
            }
        }
        "battle":
        {
            "spritesheet":"filename",
            "animated":bool,
            "animation_dictionary":
            {
                "ATTACK1":[0, 1, 2],
                "ATTACK2":[3, 4, 5]
            }
        }
    }
    """
    def build_character_from_json(self, filename):
        pass

    def _build_overworld_representation(self, data):
        pass
