from ursina import *
from settings import *
# from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
from perlin_noise import PerlinNoise
from random import randint
import pickle

# player = FirstPersonController()

scene.trees = {}

class Tree(Entity):
    def __init__(self,pos, **kwargs):
        super().__init__(
            parent=scene,
            model='aset\\tree\\scene',
            scale=8,
            collider='box',
            position=pos,
            color=color.white,
            # shader=lit_with_shadows_shader,
            **kwargs)
        scene.trees[(self.x,self.y,self.z)] = self


class Block(Button):
    id = 3


    def __init__(self,pos,parent_world ,block_id=3, **kwargs):
        super().__init__(
            parent = parent_world,
            model='cube',
            texture=block_textures[block_id],
            scale=1,
            collider='box',
            position=pos,
            color=color.white,
            # shader=lit_with_shadows_shader,
            highlight_color=color.gray,
            **kwargs)
        self.id = block_id
        parent_world.blocks[(self.x, self.y,self.z)] = self

class Chunk(Entity):
    def __init__(self, chunk_pos,**kwargs):
        super().__init__(model=None,collider=None,**kwargs)
        self.chunk_pos = chunk_pos
        self.is_simplify = False
        self.default_texture = 3
        self.blocks = {}
        self.noise = PerlinNoise(octaves=2, seed=228)

    def simplify_chunk(self):
        if self.simplify_chunk:
            return

        self.model = self.combine()
        self.collider = 'mesh'
        self.texture = block_textures[self.default_texture]

        for block in self.blocks.values():
            destroy(block)
        self.is_simplify = True
    
    def detail_chunk(self):
        if not self.simplify_chunk:
            return
        self.model = None
        self.collider = None
        self.texture = None

        for pos, block in self.blocks.items():
            new_block = Block(pos, self, block_id = block.id)
        self.is_simplify = False

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
                    tree = Tree((block_x,y-3,block_z))


class WorldEdit(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.blocks = {}
        self.noise = PerlinNoise(octaves=2, seed=228)
        self.chunks={}
        self.curret_chunk = None
        self.player = player

    def generate_world(self):
        for z in range(world_size):
            for x in range(world_size):
                chunk_pos = (x,z)
                if chunk_pos not in self.chunks:
                    chunk = Chunk(chunk_pos)
                    chunk.generate_chunk()
                # rand_num=randint(0,100)
                # if rand_num == 52:
                #     tree = Tree((z-(chunk_size/2)-0.5,y-3,x-(chunk_size/2)-0.5), self)
    def save_game(self):
        game_data = {
            "player_pos":(self.player.x, self.player.y, self.player.z),
            "chunks":[],
            "trees":[],

        }
        for chunk_pos, chunk in self.chunks.items():
            blocks_data = []
            for block_pos, block in chunk.block.items():
                blocks_data.append((block_pos,block.id))
            game_data["chunks"].append((chunk_pos, blocks_data))

        for tree_pos, tree in scene.trees.items():
            game_data['trees'].append((tree_pos))
        with open('save.dat', 'wb')as file:
            pickle.dump(game_data, file)
    def clear_wrold(self):
        for chunk in self.chunks.values():
            for block in chunk.blocks.values():
                destroy(block)
            destroy(chunk)
        for tree in scene.trees.values():
            destroy(tree)
        scene.trees.clear()
        self.chunks.clear()
    def load_world(self, chunk_data, tree_data):
        for chunk_pos, blocks in chunk_data:
            chunk = Chunk(chunk_pos)
            for block_pos, block_id in blocks:
                Block(block_pos, chunk,block_id)
            self.chunks[chunk_pos] = chunk
        for tree_pos in tree_data :
            tree = Tree(tree_pos)
    def load_game(self):
        with open('save.dat', 'rb')as file:
            game_data = pickle.load(file)

            self.clear_wrold()
            self.load_world(game_data['chunks'],game_data['trees'])
            self.player.x, self.player.y, self.player.z = game_data['player_pos']
  
    def input(self, key):
        if key == 'k':
            self.save_game()
            print("гру збережено")
        if key == 'l':
            self.load_game()
            print("гру завантажено")
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                block = Block(hit_info.entity.position + hit_info.normal, hit_info.entity.parent, Block.id)
        if key == 'left mouse down' and mouse.hovered_entity:
            if isinstance(mouse.hovered_entity, Block):
                block = mouse.hovered_entity
                chunk = block.parent
                del chunk.blocks[(block.x,block.y,block.z)]
                destroy(mouse.hovered_entity)
        if key == 'left mouse down' and mouse.hovered_entity:
            if isinstance(mouse.hovered_entity, Tree):
                tree = mouse.hovered_entity
                del scene.trees[(tree.x,tree.y,tree.z)]
                destroy(mouse.hovered_entity)
        if key == "scroll up":
            Block.id+=1
            if len(block_textures)<=Block.id:
                Block.id = 0
        if key == "scroll down":
            Block.id-=1
            if Block.id<0:
                Block.id = len(block_textures)-1
    def update(self):
        players_pos = self.player.position
        for chunk_pos, chunk in self.chunks.items():
            chunk_world_pos = Vec3(chunk_pos[0]*chunk_size, 0, chunk_pos[1]*chunk_size)
            d = distance(players_pos, chunk_world_pos)
            if d < detail_distanke and chunk.is_simplyfi:
                chunk.detail_chunk()
            if d > detail_distanke and not chunk.is_simplyfi:
                chunk.simplify_chunk()