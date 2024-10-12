from ursina import *

Text.default_font = "aset\\F77MinecraftRegular-0VYv.ttf"


class MenuButton(Button):
    def __init__(self, text, action, x ,y ,parrent):
        super().__init__(text=text, on_click=action, x=x, y=y, parrent=parrent,
                         scale=(0.6, 0.1),
                         origin=(0,0),
                         ignore_paused=True,
                         texture = 'aset\\block_textures\\stone.png',
                         color=color.color(0,0, random.uniform(0.9, 1)),
                         highlight_color=color.gray,
                         pressed_scale=1.05,
                         
                         )


class Menu(Entity):
    def __init__(self, game , **kwargs):
        super().__init__(parent = camera.ui, **kwargs)
        self.bg = Sprite(texture="aset\\bg.jpg", parent=self, z=1,color=color.white, scale = 0.14)
        self.title = Text(text="UrsintaCraft", scale=2, parent=self, origin=(0,0),x=0,y=0.35)
        self.bg_music = Audio('aset\\StockTune-Midnight Forest Footsteps_1728725391.mp3', volume=0.3, loop=True, autoplay=True)
        game.menu=self
        MenuButton("Нова Гра", game.generate_world ,0,0.13,self)
        MenuButton("Завантажити гру", game.load_game ,0,0,self)
        MenuButton("Зберегти", game.save_game ,0,-0.13,self)
        MenuButton("Вихід", application.quit ,0,-0.26,self)
    def toggle_menu(self):
        application.paused = not application.paused
        self.enabled =   application.paused
        self.visible =  self.visible
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.visible

if __name__ == "__main__":
    app = Ursina()
    menu = Menu(app)
    app.run()