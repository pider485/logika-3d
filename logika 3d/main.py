from ursina import *
from ursina import Default, camera
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor

map_size=50

app = Ursina()

class Block(Button):
    def __init__(self, texture,pos, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            texture=texture,
            scale=1,
            collider='box',
            position=pos,
            color=color.white,
            **kwargs)
    

player = FirstPersonController()
block = Block('aset/block_textures/copper_ore.png',(0,2,2))
block = Block('aset/block_textures/crimson_planks.png',(0,3,2))
block = Block('aset/block_textures/glass.png',(1,2,2))
block = Block('aset/block_textures/gray_wool.png',(1,3,2))
block = Block('aset/block_textures/wood.png',(-1,3,2))
block = Block('aset/block_textures/stone.png',(-1,2,2))

noise = PerlinNoise(octaves=2, seed=228)


for z in range(map_size):
    for x in range(map_size):
        y = floor(noise([x/24, z/24])*6)
        block = Block('aset/block_textures/stone.png',(z-5,y,x-5))



cube = Entity(model='aset/da11/source/model', color=color.gray,scale=2, collider='box')
# picaxe = Entity(color=color.gray,scale=2, texture='grass' ,collider='box')

cube.position = (5,0,0)

# ground = Entity(model='quad', texture='grass',scale=100,texture_scale=(16,16),rotation=90,collider='box')
def spin():
    cube.animate('rotation_z', cube.rotation_z+360, duration=3, curve=curve.in_out_expo)
def input(key):
    if key == "y":
        cube.position=(0,5,0)

cube.on_click = spin
# EditorCamera()  # add camera controls for orbiting and moving the camera

Sky = Sky(texture='sky_sunset')


app.run()