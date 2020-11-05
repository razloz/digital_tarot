#!../.env/bin/python3
from panda3d.core import loadPrcFileData
configData = """
win-size 1920 1080
fullscreen 1
textures-auto-power-2 False
textures-power-2 None
textures-square None
"""
loadPrcFileData("", configData)

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextureAttrib, Filename, TextNode, AmbientLight
from direct.gui.DirectGui import DirectButton
from os.path import abspath
import shuffles
from datetime import datetime as dt


get_path = lambda p: Filename.fromOsSpecific(abspath(p)).getFullpath()


class Card():
    def __init__(self, name, base, parent, pos, hpr, scale):
        """Create card object from local resources."""
        self._card_name = name
        self._scene_base = base
        self._parent_node = parent
        loadModel = self._scene_base.loader.loadModel
        loadTexture = self._scene_base.loader.loadTexture
        self._mesh_path = get_path("./resources/models/card.dae")
        self._card_mesh = loadModel(self._mesh_path)
        self._card_mesh.setPos(*pos)
        self._card_mesh.setHpr(*hpr)
        self._card_mesh.setScale(*scale)
        self._card_mesh.reparentTo(self._parent_node)
        self._stock_path = get_path("./resources/textures/card_stock.png")
        self._stock_texture = loadTexture(self._stock_path)
        self._stock_texture.setWrapU(self._stock_texture.WM_border_color)
        self._stock_texture.setWrapV(self._stock_texture.WM_border_color)
        self._stock_texture.setBorderColor((0.2, 0.2, 0.2, 1))
        self._stock_attrib = TextureAttrib.make(self._stock_texture)
        self._stock_geom = self._card_mesh.find("**/cardStock").node()
        self._stock_state = self._stock_geom.get_geom_state(0)
        self._stock_state = self._stock_state.add_attrib(self._stock_attrib)
        self._stock_geom.set_geom_state(0, self._stock_state)
        self._face_path = get_path(f"./resources/textures/{name}.jpg")
        self._face_texture = loadTexture(self._face_path)
        self._face_texture.setWrapU(self._face_texture.WM_clamp)
        self._face_texture.setWrapV(self._face_texture.WM_clamp)
        self._face_attrib = TextureAttrib.make(self._face_texture)
        self._face_geom = self._card_mesh.find("**/cardFace").node()
        self._face_state = self._face_geom.get_geom_state(0)
        self._face_state = self._face_state.add_attrib(self._face_attrib)
        self._face_geom.set_geom_state(0, self._face_state)

    def get_name(self):
        """Get card name."""
        return self._card_name

    def get_node(self):
        """Get card node object."""
        return self._card_mesh

    def set_pos(self, x, y, z):
        """Change card's position."""
        self._card_mesh.setPos(x, y, z)

    def set_hpr(self, h, p, r):
        """Change card's orientation."""
        self._card_mesh.setHpr(h, p, r)

    def set_scale(self, x, y, z):
        """Change card's size."""
        self._card_mesh.setScale(x, y, z)


class GUI(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.setBackgroundColor(0.1, 0.1, 0.1, 1)
        self.btn_spread = DirectButton(text="Draw", command=self.__spread__,
                                pos=(1.65, 0, -0.95), scale=(0.08, 0.1, 0.1))
        self.btn_shuffle = DirectButton(text="Shuffle", command=self.__shuffle__,
                                pos=(1.35, 0, -0.95), scale=(0.08, 0.1, 0.1))
        self.btn_cap = DirectButton(text="Screenshot", command=self.__save_png__,
                                pos=(1.35, 0, 0.9), scale=(0.08, 0.1, 0.1))
        self.btn_exit = DirectButton(text="Exit", command=self.__user_exit__,
                                pos=(1.7, 0, 0.9), scale=(0.08, 0.1, 0.1))
        self.camera.reparentTo(self.render)
        self.camera.setPos(0, 0, 45)
        self.cam.setHpr(0, -90, 0)
        self.ambience = AmbientLight('Ambient Light')
        self.ambience.setColorTemperature(5500)
        self.ambience_node = self.render.attachNewNode(self.ambience)
        self.render.setLight(self.ambience_node)
        self.render.setShaderAuto()
        self.cards = list()
        scalar = (1, 1, 1)
        pos = (14, 0, 0)
        hpr = (0, -90, 0)
        caste = list()
        for i in range(22):
            caste.append(f'Major0{i}' if i < 10 else f'Major{i}')
        for i in range(14):
            caste.append(f'Cups0{i+1}' if i < 9 else f'Cups{i+1}')
        for i in range(14):
            caste.append(f'Pents0{i+1}' if i < 9 else f'Pents{i+1}')
        for i in range(14):
            caste.append(f'Swords0{i+1}' if i < 9 else f'Swords{i+1}')
        for i in range(14):
            caste.append(f'Wands0{i+1}' if i < 9 else f'Wands{i+1}')
        for name in caste:
            self.cards.append(Card(name, self, self.render, pos, hpr, scalar))
        self.gen = shuffles.ShuffleGen(len(self.cards), None)
        for i in range(10):
            self.deck_state = self.gen.next_shuffle()

    def __shuffle__(self):
        for i in range(9):
            self.deck_state = self.gen.next_shuffle()

    def __spread__(self):
        for card in self.cards:
            card.set_pos(14, 0, 0)
            card.set_hpr(0, -90, 0)
        spread = [
            (-7, 0, 0),
            (0, 0, 0),
            (7, 0, 0),
            (-3, -7, 0),
            (3, 7, 0),
            (-14, 8, 0),
            (-14, 0, 0),
            (-14, -8, 0)
            ]
        i = 0
        e = len(spread)
        self.__shuffle__()
        for n in self.deck_state:
            self.cards[n].set_pos(*spread[i])
            if i == 3 or i == 4:
                self.cards[n].set_hpr(90, 90, 180)
            else:
                self.cards[n].set_hpr(0, 90, 180)
            i += 1
            if i == e: break

    def __show_buttons__(self, task):
        if task.time < 1.5: return task.cont
        self.btn_spread.show()
        self.btn_shuffle.show()
        self.btn_cap.show()
        self.btn_exit.show()
        return task.done

    def __save_png__(self):
        self.btn_spread.hide()
        self.btn_shuffle.hide()
        self.btn_cap.hide()
        self.btn_exit.hide()
        self.taskMgr.add(self.__do_screenshot__, 'screen_capture')

    def __do_screenshot__(self, task):
        if task.time < 1.5: return task.cont
        png_name = dt.today().strftime('%Y-%m-%d %H:%M:%S')
        self.screenshot(f"./capture/{png_name}.png", False)
        self.taskMgr.add(self.__show_buttons__, 'show_buttons')
        return task.done

    def __user_exit__(self):
        exit()

def start_engine():
    """Create and run the 3D engine."""
    app = GUI()
    app.run()


if __name__ == "__main__":
    start_engine()
