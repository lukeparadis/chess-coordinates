from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

import random
import sys
import os
import pickle

Window.clearcolor = (1, 1, 1, 1)

SIZE = 1024
STEP = SIZE // 8
FLIP_COUNT_MAX = 50

Window.size = (SIZE//2,SIZE//2)

RANKS = [ letter for letter in 'abcdefgh' ]
FILES = list(range(1,9))

BOARD_FILENAME = 'resources/board-2048.png'
BOARD_FLIPPED_FILENAME = 'resources/board-flipped=2048.png'

SQUARE_TO_LOCATION = {}
LOCATION_TO_SQUARE = {}

for x in range(8):
    for y in range(8):
        location = (x,y)
        square = '{}{}'.format(RANKS[x],FILES[y])
        LOCATION_TO_SQUARE[location] = square
        SQUARE_TO_LOCATION[square] = location

class Scorer(object):

    def __init__(self):
        super().__init__()

        self.stats = {}
        self.noise = .001
        self.filename = 'data/scores.pkl'

        if not os.path.exists(self.filename):
            self.init_stats()
        else:
            self.load_stats()

    def init_stats(self):
        self.stats = {}

        for flipped in (True,False):
            self.stats[flipped] = {}
            for square in SQUARE_TO_LOCATION:
                self.stats[flipped][square] = { 'correct': 0, 'attempts': 0 }

    def load_stats(self):
        with open(self.filename, 'rb') as fh:
            self.stats = pickle.load(fh)

    def save_stats(self):
        with open(self.filename, 'wb') as fh:
            pickle.dump(self.stats, fh)

    def random_square(self, flipped):

        scores = []
        total_score = 0

        for square,stats in self.stats[flipped].items():

            # potential for more complicated scoring function
            score = stats['correct']
            total_score += score
            scores.append({ 'square': square, 'score': score })

        scores = sorted(scores, key=lambda k: k['score'])

        if total_score == 0:
            total_score = 1

        for item in scores:
            item['score'] = item['score'] / total_score + random.gauss(0,self.noise)

        scores = sorted(scores, key=lambda k: k['score'])

        return scores[0]['square']

    def update_score(self, flipped, square, misses):
        self.stats[flipped][square]['attempts'] += 1 
        if misses == 0:
            self.stats[flipped][square]['correct'] += 1

def point_to_square(flipped, x, y):

    x = int(x / STEP)
    y = int(y / STEP)

    if flipped:
        x = 7 - x
        y = 7 - y

    location = (x,y)
    square = LOCATION_TO_SQUARE[location] 
    
    return square

class CoordinatesWidget(AnchorLayout):
    def __init__(self):

        #super().__init__(orientation='horizontal')
        super().__init__(anchor_x='center', anchor_y='center')

        #self.left_pane = AnchorLayout(anchor_x='center', anchor_y='center')
        #self.right_pane = AnchorLayout(anchor_x='center', anchor_y='center')

        #self.add_widget(self.left_pane)
        #self.add_widget(self.right_pane)

        self.image = Image(source=BOARD_FILENAME)
        #self.image = Image(source=BOARD_FLIPPED_FILENAME)
        self.add_widget(self.image)

        self.flipped = False
        self.scorer = Scorer()
        self.square = self.scorer.random_square(self.flipped)
        self.misses = 0
        self.flip_count = 0

        self.label = Label(text=self.square, font_size='120', color=(0,0,0,1))
        self.add_widget(self.label)

    def on_touch_down(self, touch):

        if touch.pos[0] < SIZE:

            location = point_to_square(self.flipped, touch.pos[0], touch.pos[1])

            if location == self.square:
                self.scorer.update_score(self.flipped, self.square, self.misses)
                self.square = self.scorer.random_square(self.flipped)
                self.label.text = self.square
                self.misses = 0
                self.scorer.save_stats()
                self.flip_count += 1

                if self.flip_count == FLIP_COUNT_MAX:
                    self.flipped = not self.flipped
                    if not self.flipped:
                        self.image.source = BOARD_FILENAME
                    else:
                        self.image.source = BOARD_FLIPPED_FILENAME
                    self.flip_count = 0
            else:
                self.misses += 1

class CoordinatesApp(App):
    
    def build(self):
        return CoordinatesWidget()

if __name__ == '__main__':

    CoordinatesApp().run()

