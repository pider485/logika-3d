
from ursina import load_texture
import os

chunk_size=5
world_size=10
detail_distanke = 5

block_textures = []
BASE_DIR= os.getcwd()
IMG_DIR = os.path.join(BASE_DIR, 'aset/block_textures')
file_list = os.listdir(IMG_DIR)
for image in file_list:
    texture = load_texture('aset/block_textures'+ os.sep + image)
    block_textures.append(texture)
