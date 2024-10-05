from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
# from perlin_noise import PerlinNoise
from numpy import floor
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
import os


app = Ursina()

from settings import *
from models import Block , WorldEdit


player = FirstPersonController()
player.x= chunk_size /2
player.z= chunk_size /2
player.gravity = 0
def input(key):
    player.gravity = 0.5
# picaxe = Entity(color=color.gray,scale=2, texture='grass' ,collider='box')

Sky = Sky()
light=DirectionalLight(shadows=True)
light.look_at(Vec3(1,-2,1))

world = WorldEdit(player)
world.generate_world()

# scene.fog_density = (7, 10)   # sets linear density start and end

# camera.clip_plane_far = 30

app.run()