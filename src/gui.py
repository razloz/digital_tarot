#!../.env/bin/python3
#from panda3d.core import ConfigVariableManager
#print(ConfigVariableManager.getGlobalPtr().listVariables())
from panda3d.core import loadPrcFileData
loadPrcFileData("", "fullscreen 1")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename
from direct.gui.DirectGui import OnscreenText, DirectButton
from panda3d.core import TextNode
from panda3d.core import DirectionalLight, AmbientLight
from direct.controls.BattleWalker import BattleWalker
from os.path import abspath
from direct.fsm.FSM import FSM

get_path = lambda p: Filename.fromOsSpecific(abspath(p)).getFullpath()


class ControlAvatar(FSM):
    def __init__(self):
        FSM.__init__(self, 'AvatarFSM')

class GUI(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.setSceneGraphAnalyzerMeter(True)
        self.setFrameRateMeter(True)
        self.scene = self.loader.loadModel(get_path("../resources/scene.bam"))
        self.scene.reparentTo(self.render)
        #self.cam.setPos(8, -150, 8)
        #self.cam.setHpr(-8, 0, 0)
        self.walker = BattleWalker()
        self.walker.enableAvatarControls()
        #self.taskMgr.add(self.walker.handleAvatarControls, 'Avatar')
        self.light = DirectionalLight('Sun Light')
        self.light.setColorTemperature(3400)
        self.ambience = AmbientLight('Ambient Light')
        self.ambience.setColor((0.1, 0.1, 0.1, 1))
        self.light_node = self.render.attachNewNode(self.light)
        self.ambience_node = self.render.attachNewNode(self.ambience)
        self.render.setLight(self.light_node)
        self.render.setLight(self.ambience_node)
        self.msg = OnscreenText(text="", pos=(0, -0.95), scale=0.07,
                                fg=(0.8, 0, 0.8, 1), align=TextNode.ACenter,
                                mayChange=1)
        btn_txt = ("Click me!", "Again!", "Oooohhh", "Enable me...")
        self.btn = DirectButton(text=btn_txt, command=self.button_callback,
                                pos=(-1.15, 0, -0.95), scale=0.07)
        #self.res = self.getSize()
        #self.screen_height = self.res[0]
        #self.screen_width = self.res[1]
        #self.deck_count = 78
        #self.cards = list()
        #scalar = (self.screen_width * 0.0005, self.screen_height * 0.0005, 1)
        #card_path = get_path("../resources/card.gltf")
        #for i in range(self.deck_count):
            #self.create_card(card_mesh_path, self.render, scalar, pos, self.hpr)

    def create_card(self, r_path, r_parent, r_scale, r_position, r_hpr):
        card = self.loader.loadModel(r_path)
        card.setScale(r_scale)
        card.setPos(r_position)
        card.setHpr(r_hpr)
        card.reparentTo(r_parent)
        self.cards.append(card)

    def button_callback(self):
        self.msg.text = "Button Clicked!"
        print("Clicky Clicky Clicky")
        exit(1)


def start_engine():
    """Create and run the 3D engine."""
    app = GUI()
    app.run()


if __name__ == "__main__":
    start_engine()
