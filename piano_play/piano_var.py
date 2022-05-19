import pygame
import play

# define game class


class Game():  # two variables - ready and instrument (replacing with a global variable)
    def __init__(self):
        self.ready = False
        self.instrument = 0

    def set_instrument(self, val):
        self.instrument = val

    def get_instrument(self):
        return self.instrument

    def start(self):
        self.ready = True

    def paused(self):  # the object is given a specific instruction "the game is paused"
        self.ready = False

    def is_ready(self):
        return self.ready


# interface - tips, control buttons:
play.set_backdrop('light blue')
introduce1 = play.new_text(words='Piano for fun!', x=0, y=250)
introduce2 = play.new_text(
    words='Create your melody by pressing the keys', x=0, y=200)

key_play_melody = play.new_box(
    color='light green', border_color='black', border_width=1,
    x=-140, y=-80, width=120, height=50)
kpm = play.new_text(words='play melody', x=-140, y=-80, font_size=20)

key_repeat_melody = play.new_box(
    color='light yellow', border_color='black', border_width=1,
    x=-5, y=-80, width=120, height=50)
krm = play.new_text(words='repeat melody', x=-5, y=-80, font_size=20)

key_clear_melody = play.new_box(
    color='light pink', border_color='black', border_width=1,
    x=130, y=-80, width=120, height=50)
kcm = play.new_text(words='clear melody', x=130, y=-80, font_size=20)
sound_clear_melody = pygame.mixer.Sound('clear_melody.wav')

# instrument switches:
ch_p = play.new_circle(
    color='black', x=-180, y=-150, radius=10,
    border_color='black', border_width=2)
txt_p = play.new_text(words='piano', x=-145, y=-150, font_size=20)
ch_g = play.new_circle(
    color='light blue', x=-80, y=-150, radius=10,
    border_color='black', border_width=2)
txt_g = play.new_text(words='guitar', x=-45, y=-150, font_size=20)
ch_v = play.new_circle(
    color='light blue', x=20, y=-150, radius=10,
    border_color='black', border_width=2)
txt_v = play.new_text(words='violin', x=55, y=-150, font_size=20)
ch_f = play.new_circle(
    color='light blue', x=120, y=-150, radius=10,
    border_color='black', border_width=2)
txt_f = play.new_text(words='flute', x=155, y=-150, font_size=20)
# keys and sounds for them:
keys = []
sounds = []
# we have 4 instruments:
for i in range(4):
    sounds.append([])

for i in range(8):
    key_x = -180 + i * 50  # 40 - key width, 10 - distance between them
    key = play.new_box(color='white', border_color='black',
                       border_width=3, x=key_x, y=50, width=40, height=100)
    keys.append(key)
    # all the sounds for all the instruments are stored in 1 list
    sound = pygame.mixer.Sound(str(i+1) + '.ogg')
    sounds[0].append(sound)
    sound = pygame.mixer.Sound('g' + str(i+1) + '.ogg')
    sounds[1].append(sound)
    sound = pygame.mixer.Sound('v' + str(i+1) + '.ogg')
    sounds[2].append(sound)
    sound = pygame.mixer.Sound('f' + str(i+1) + '.ogg')
    sounds[3].append(sound)

# melody not yet recorded:
melody = []
game = Game()


@play.when_program_starts
async def start():
    pygame.mixer_music.load('hello.mp3')
    pygame.mixer_music.play()
    await play.timer(seconds=4.5)
    game.start()


@ch_p.when_clicked
def set_piano():
    game.set_instrument(0)
    ch_p.color = 'black'
    ch_g.color = 'light blue'
    ch_v.color = 'light blue'
    ch_f.color = 'light blue'


@ch_g.when_clicked
def set_guitar():
    game.set_instrument(1)
    ch_p.color = 'light blue'
    ch_g.color = 'black'
    ch_v.color = 'light blue'
    ch_f.color = 'light blue'


@ch_v.when_clicked
def set_violin():
    game.set_instrument(2)
    ch_p.color = 'light blue'
    ch_g.color = 'light blue'
    ch_v.color = 'black'
    ch_f.color = 'light blue'


@ch_f.when_clicked
def set_flute():
    game.set_instrument(3)
    ch_p.color = 'light blue'
    ch_g.color = 'light blue'
    ch_v.color = 'light blue'
    ch_f.color = 'black'


@key_clear_melody.when_clicked
def clear():
    if game.is_ready():
        melody.clear()
        sound_clear_melody.play()
    else:
        game.start()


@key_play_melody.when_clicked
# play recorded melody:
async def play_m():
    if game.is_ready():
        inst = game.get_instrument()  # number of the instrument in the list
        game.paused()
        for i in range(len(melody)):
            await play.timer(seconds=0.5)
            # play the note of the instrument we need “list of lists”
            sounds[inst][melody[i]].play()
        game.start()


@key_repeat_melody.when_clicked
async def repeat_m():
    if game.is_ready():
        key_repeat_melody.color = 'light grey'
        key_clear_melody.color = 'light red'
        kcm.words = 'stop'
        game.paused()
        inst = game.get_instrument()
        i = 0
        while not game.is_ready():
            sounds[inst][melody[i]].play()
            await play.timer(seconds=0.5)
            i += 1
            if len(melody) == i:
                await play.timer(seconds=0.5)  # pause at the end of the phrase
                i = 0
        key_repeat_melody.color = 'light yellow'
        key_clear_melody.color = 'light pink'
        kcm.words = 'clear melody'


@play.repeat_forever
async def play_piano():
    for i in range(len(keys)):
        if keys[i].is_clicked and game.is_ready():
            keys[i].color = 'light grey'
            sounds[0][i].play()  # have the piano always sound on the keys
            await play.timer(seconds=0.3)
            keys[i].color = 'white'
            melody.append(i)

play.start_program()
