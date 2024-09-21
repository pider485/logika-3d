from ursina import *
from settings import *
# from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
from perlin_noise import PerlinNoise
from random import randint
# player = FirstPersonController()

class Tree(Entity):
    id = 3
    def __init__(self,pos, parent_world, **kwargs):
        super().__init__(
            parent=parent_world,
            model='aset\\tree\\scene',
            scale=8,
            collider='box',
            position=pos,
            color=color.white,
            # shader=lit_with_shadows_shader,
            **kwargs)


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

class Chunk(Entity):
    def __init__(self, chunk_pos,**kwargs):
        super().__init__(model=None,collider=None,**kwargs)
        self.chunk_pos = chunk_pos
        self.blocks = {}
        self.noise = PerlinNoise(octaves=2, seed=228)
    def generate_chunk(self):
        cx,cz = self.chunk_pos
        for z in range(chunk_size):
            for x in range(chunk_size):
                block_x = cx * chunk_size + x
                block_z = cz * chunk_size + z
                y = floor(self.noise([block_x/24, block_z/24])*6)
                block = Block((block_x,y,block_z), self)
                self.blocks[(block_x,y,block_z)] = block

                rand_num=randint(0,100)
                if rand_num == 52:
                    tree = Tree((block_x,y-3,block_z), self)


class WorldEdit(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocks = {}
        self.noise = PerlinNoise(octaves=2, seed=228)
        self.chunks={}
        self.curret_chunk = None

    def generate_world(self):
        for z in range(world_size):
            for x in range(world_size):
                chunk_pos = (x,z)
                if chunk_pos not in self.chunks:
                    chunk = Chunk(chunk_pos)
                    chunk.generate_chunk()
                    self.chunks[chunk_pos] = chunk
                # rand_num=randint(0,100)
                # if rand_num == 52:
                #     tree = Tree((z-(chunk_size/2)-0.5,y-3,x-(chunk_size/2)-0.5), self)

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