from ursina import *
from ursina import Default, camera
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
import os

map_size=25

app = Ursina()

class Block(Button):
    id = 0


    def __init__(self,pos, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            texture=block_textures[Block.id],
            scale=1,
            collider='box',
            position=pos,
            color=color.white,
            # shader=lit_with_shadows_shader,
            highlight_color=color.gray,
            **kwargs)
    def input(self, key):
        d = distance(player,self)
        if self.hovered:
            if key == "left mouse down" and d<10:
                destroy(self)
            if key == "right mouse down" and d<10:
                block = Block(self.position + mouse.normal)
        if key == "scroll up":
            Block.id+=1
            if len(block_textures)<=Block.id:
                Block.id = 0
        if key == "scroll down":
            Block.id-=1
            if Block.id<0:
                Block.id = len(block_textures)-1
player = FirstPersonController()
noise = PerlinNoise(octaves=2, seed=228)

block_textures = []
BASE_DIR= os.getcwd()
IMG_DIR = os.path.join(BASE_DIR, 'aset/block_textures')
file_list = os.listdir(IMG_DIR)
for image in file_list:
    texture = load_texture('aset/block_textures'+ os.sep + image)
    block_textures.append(texture)
print(block_textures)
for z in range(map_size):
    for x in range(map_size):
        y = floor(noise([x/24, z/24])*6)
        block = Block((z-(map_size/2),y,x-(map_size/2)))


# picaxe = Entity(color=color.gray,scale=2, texture='grass' ,collider='box')

Sky = Sky(texture='sky_sunset')
light=DirectionalLight(shadows=True)
light.look_at(Vec3(1,-2,1))

# scene.fog_density = .8          # sets exponential density
scene.fog_density = (1, 10)   # sets linear density start and end

app.run()