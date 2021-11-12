from ursina import *
from random import *
from ursina import curve
from ursina import texture
from ursina import text
from ursina.prefabs.first_person_controller import FirstPersonController


# -*- Encoding:UTF-8 -*- #
app=Ursina()

END_LINE=100


game_text = Text(text='',scale=4,position=(0,0.35,0),origin=0,color=color.black)
class Tagger(Entity): #술래
    def __init__(self,position):
        super().__init__(
            model='assets/robot',
            position=position,
            scale=1,
            origin=0,

            voice=Audio('assets/assets_sound',autoplay=False),
            status='idle'
        )

        invoke(self.start_game,delay=2) # 몇초뒤에 나오도록

    def start_game(self):
        game_text.text=u'START!!'

        invoke(game_text.disable,delay=2)
        
        self.look_back()
    
    def speak(self):
        self.status='speak'
        self.voice.play()

        invoke(self.look_forward,delay=4)

    def look_forward(self):
        self.status='forward'
        self.animate('rotation_y',0,duration=0.2,curve=curve.linear)

        invoke(self.look_back,delay=3)
    #술래가 뒤를 돌아보는 함수
    def look_back(self):
        self.status='back'
        self.animate('rotation_y',180,duration=3,curve=curve.linear) 

        invoke(self.speak,delay=3)

player = FirstPersonController()
tagger = Tagger(position=(0,0,END_LINE))

class Tree(Entity):
    def __init__(self,position,scale,rotation):
        super().__init__(
            model='assets/tree',
            position=position,
            scale=scale,
            origin=0,
            rotoation=rotation
        )
Sky()
PointLight(parent=camera,color=color.white,position=(0,10,-15)) # 카메라를 따라다니는 점광원
AmbientLight(color=color.rgba(100,100,100,0.1)) #은은한 빛
ground=Entity(model='cube',scale=(100,1,250), collider='box',color=color.gray,texture='white_cube')
line=Entity(model='cube',position=(0,0.1,END_LINE),scale=(100,1,1),color=color.red,texture='white_cube')
for _ in range(20):
    tree=Tree(
        position=(randint(-50,50),0.3,randint(-50,50)),
        scale=randint(20,40)/100,
        rotation=(randint(-5,5),randint(0,360),randint(-5,5))
    )

last_position=None


def update():
    global last_position
    if tagger.status=='forward':
        if last_position is None:
            last_position=player.position
        elif last_position !=player.position: #플레이어가 움직이면
            game_text.enable()
            game_text.color = color.red
            game_text.text="Died!!"
            player.disable()
        
    else:
        last_position=None
    
    if player.position.z > END_LINE:
        game_text.enable()
        game_text.color = color.azure
        game_text.text=u'WIN!'
app.run()