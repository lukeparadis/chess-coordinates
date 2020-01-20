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

import common

Window.clearcolor = (1, 1, 1, 1)
Window.size = (common.SIZE//2,common.SIZE//2)

class Scorer(object):

    def __init__(self):
        super().__init__()

        self.stats = {}
        self.noise = .001
        self.filename = common.STATS_FILENAME

        if not os.path.exists(self.filename):
            self.init_stats()
        else:
            self.load_stats()

    def init_stats(self):

        self.stats = {}

        for side in ('white', 'black'):
            self.stats[side] = {}
            for square in common.SQUARE_TO_LOCATION:
                self.stats[side][square] = { 'correct': 0, 'total': 0 }

    def load_stats(self):
        with open(self.filename, 'rb') as fh:
            self.stats = pickle.load(fh)

    def save_stats(self):
        with open(self.filename, 'wb') as fh:
            pickle.dump(self.stats, fh)

    def random_square(self, side):

        scores = []
        total_score = 0

        for square,stats in self.stats[side].items():

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

    def update_score(self, side, square, misses):
        self.stats[side][square]['total'] += 1 
        if misses == 0:
            self.stats[side][square]['correct'] += 1

def point_to_square(side, x, y):

    x = int(x / common.STEP)
    y = int(y / common.STEP)

    if side == 'black':
        x = 7 - x
        y = 7 - y

    location = (x,y)
    square = common.LOCATION_TO_SQUARE[location] 
    
    return square

class CoordinatesWidget(AnchorLayout):
    def __init__(self):
        super().__init__(anchor_x='center', anchor_y='center')

        self.side = random.choice(['white','black'])
        if self.side == 'white':
            self.image = Image(source=common.BOARD_WHITE_FILENAME)
        else:
            self.image = Image(source=common.BOARD_BLACK_FILENAME)

        self.add_widget(self.image)

        self.scorer = Scorer()
        self.square = self.scorer.random_square(self.side)
        self.misses = 0
        self.flip_count = 0

        self.label = Label(text=self.square, font_size='120', color=(0,0,0,1))
        self.add_widget(self.label)

    def on_touch_down(self, touch):

        if touch.pos[0] < common.SIZE:

            location = point_to_square(self.side, touch.pos[0], touch.pos[1])

            if location == self.square:
                self.scorer.update_score(self.side, self.square, self.misses)
                self.square = self.scorer.random_square(self.side)
                self.label.text = self.square
                self.misses = 0
                self.scorer.save_stats()
                self.flip_count += 1

                if self.flip_count == common.FLIP_COUNT_MAX:
                    self.side = 'white' if self.side == 'black' else 'black'
                    if self.side == 'white':
                        self.image.source = common.BOARD_WHITE_FILENAME
                    else:
                        self.image.source = common.BOARD_BLACK_FILENAME
                    self.flip_count = 0
            else:
                self.misses += 1

class CoordinatesApp(App):
    
    def build(self):
        return CoordinatesWidget()

if __name__ == '__main__':

    CoordinatesApp().run()

