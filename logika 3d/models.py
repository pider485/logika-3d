from ursina import *
from settings import *
# from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
from perlin_noise import PerlinNoise

# player = FirstPersonController()

class Block(Button):
    id = 3


    def __init__(self,pos, parent_world, **kwargs):
        super().__init__(
            parent=parent_world,
            model='cube',
            texture=block_textures[Block.id],
            scale=1,
            collider='box',
            position=pos,
            color=color.white,
            # shader=lit_with_shadows_shader,
            highlight_color=color.gray,
            **kwargs)



class WorldEdit(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocks = {}
        self.noise = PerlinNoise(octaves=2, seed=228)

    def generate_world(self):
        for z in range(map_size):
            for x in range(map_size):
                y = floor(self.noise([x/24, z/24])*6)
                block = Block((z-(map_size/2),y,x-(map_size/2)), self)
                self.blocks[(x,y,z)] = block

    def input(self, key):
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                block = Block(hit_info.entity.position + hit_info.normal,self)
        if key == 'left mouse down' and mouse.hovered_entity:
            destroy(mouse.hovered_entity)
        if key == "scroll up":
            Block.id+=1
            if len(block_textures)<=Block.id:
                Block.id = 0
        if key == "scroll down":
            Block.id-=1
            if Block.id<0:
                Block.id = len(block_textures)-1