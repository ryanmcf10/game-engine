import env.components.character as character

class NpcCollection():
    def __init__():
        self.npc_list = []
        self.npc_collision_rects = []
        self.npc_action_handlers = []

    def add(self, npc):
        assert type(npc) is character.OverworldCharacter, "NPC must be of type OverworldCharacter"
        self.npc_list.append(npc)
        self.npc_collision_rects.append(npc.collision_rect)
        
    def update(self):
        self.npc_collision_rects = []

        for npc in self.npc_list:
            npc.update()
            self.npc_collision_rects.append(npc.collision_rect)

    def get_rects(self):
        return self.npc_collision_rects
