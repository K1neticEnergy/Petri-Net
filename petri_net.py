from tkinter import Tk, Canvas, Frame, BOTH, constants, FIRST, LAST
import time
from math import sqrt

class Place:
    '''
        A place is a passive nodes of Petri Net
        Properties:
            - label: name of a place
            - token: number of token holding
            - (visualize)
        Method:
    '''
    radius = 30

    def __init__(self,label,token,x,y,canvas):
        self.label = label
        self.token = token
        self.canvas = canvas
        self.x = x
        self.y = y
        self.tks = None
        self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)

    def show(self):
        if self.tks: self.tks = [self.canvas.delete(tk) for tk in self.tks]
        dir_x = [0,0.5, 0,-0.5,0,1, 0,-1]
        dir_y = [0.5,0,-0.5, 0,1,0,-1, 0]
        self.tks = [self.canvas.create_oval(self.x - 5 + dir_x[i%8] * 20, self.y - 5 + dir_y[i%8] * 20, self.x + 5 + dir_x[i%8] * 20, self.y + 5 + dir_y[i%8] * 20,fill='red') for i in range(0, self.token)]
        self.canvas.after(1,self.show)


class Arc:
    '''

    '''
    def __init__(self,place,amount=1):
        self.place = place
        self.amount = amount

class Out(Arc):
    def trigger(self):
        self.place.token -= self.amount

    def show(self,canvas,trans_coor):
        ratio = (trans_coor[0] - self.place.x)**2 / ((trans_coor[1] - self.place.y)**2 + (trans_coor[0] - self.place.x)**2)
        x_offset = Place.radius * sqrt(ratio)
        y_offset = Place.radius * sqrt(1 - ratio)
        canvas.create_line(self.place.x, self.place.y, trans_coor[0], trans_coor[1], arrow=LAST)

class In(Arc):
    def trigger(self): 
        self.place.token += self.amount
    
    def show(self,canvas,trans_coor):
        canvas.create_line(self.place.x, self.place.y, trans_coor[0], trans_coor[1], arrow=FIRST)

class Transition:
    '''

    '''
    h = 30
    w = 15

    def __init__(self,label,out_arcs,in_arcs,x,y,canvas):
        self.label = label
        self.out_arcs = set(out_arcs)
        self.arcs = self.out_arcs.union(in_arcs)
        self.x = x
        self.y = y
        self.canvas = canvas


    def enabled(self):
        for i in self.out_arcs:
            if i.place.token == 0: 
                return False
        return True
    
    def fire(self):
        for i in self.out_arcs:
            if i.place.token == 0: 
                return False
        
        [i.trigger() for i in self.arcs]    
        return True

    def show(self):

        self.canvas.create_polygon( self.x - self.w, self.y - self.h, self.x - self.w, 
            self.y + self.h, self.x + self.w, self.y + self.h, self.x + self.w, self.y - self.h )
        for i in self.arcs:
            i.show(self.canvas,[self.x,self.y])
 
class PetriNet:
    def __init__(self,transitions,places,canvas):
        self.transitions = transitions
        self.places = places
        self.canvas = canvas

    def deadlock_free(self):
        return sum([self.transitions[i].enabled() for i in self.transitions]) != 0

    def run(self,firing_sequence,i):
        # print("start {}\n".format([pl.token for pl in places]))
        if i >= len(firing_sequence): return
        name = firing_sequence[i]
        t = self.transitions[name]
        if self.deadlock_free():
            if t.fire() :
                print("{} firing!".format(t.label))
                print(" => {}\n".format([pl.token for pl in self.places]))
            else:
                print("{} stucked. Switching...".format(t.label))
            self.canvas.after(1000,self.run,firing_sequence,i + 1)
        else:
            print("deadlock")


def make_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--firings', type=int)
    parser.add_argument('--marking', type=int, nargs='+')
    return parser

def problem2(firings):
    windows = Tk()
    canvas = Canvas(windows, bg="white",
           height=720, width=1280)
    canvas.pack()
    places = [
        Place('wait',   5, 100, 100, canvas), 
        Place('inside', 0, 300, 100, canvas),
        Place('done',   1, 500, 100, canvas),
    ]
    trans = dict(
        t1=Transition(
            'start', 
            [
                Out(places[0])
            ], 
            [
                In(places[1])
            ],
            200,
            100,
            canvas
        ),
        t2=Transition(
            'change', 
            [
                Out(places[1])
            ], 
            [
                In(places[2])
            ],
            400,
            100,
            canvas
        ),
    )

    for i in trans: trans[i].show()
    [p.show() for p in places]

    # non-determistic choice:
    from random import choice
    firing_sequence = [choice(list(trans.keys())) for _ in range(firings)]
    petri_net = PetriNet(trans,places,canvas)

    petri_net.run(firing_sequence, 0)
    windows.mainloop()

def problem3(firings):
    windows = Tk()
    canvas = Canvas(windows, bg="white",
           height=720, width=1280)
    canvas.pack()
    places = [  
                Place('wait',   3, 200, 400, canvas), 
                Place('inside', 0, 400, 500, canvas),
                Place('done',   1, 600, 400, canvas),
                Place('free',   1, 300, 200, canvas), 
                Place('busy',   0, 400, 300, canvas),
                Place('docu',   0, 500, 200, canvas),
            ]

    trans = dict(
        t1=Transition(
            'start', 
            [
                Out(places[0]),
                Out(places[3])
            ], 
            [
                In(places[1]),
                In(places[4])
            ],
            300,
            400,
            canvas
        ),
        t2=Transition(
            'change', 
            [
                Out(places[1]),    
                Out(places[4])], 
            [
                In(places[2]),    
                In(places[5])
            ],
            500,
            400,
            canvas
        ),
        t3=Transition(
            'end', 
            [
                Out(places[5])
            ], 
            [
                In(places[3])
            ],
            400,
            200,
            canvas
        ),
    )

    for i in trans: trans[i].show()
    [p.show() for p in places]

    # non-determistic choice:
    from random import choice
    firing_sequence = [choice(list(trans.keys())) for _ in range(firings)]

    petri_net = PetriNet(trans,places,canvas)
    petri_net.run(firing_sequence, 0)
    windows.mainloop()


if __name__ == '__main__':
    # windows = Tk()
    # canvas = Canvas(windows, bg="white",
    #        height=720, width=1280)
    # args = make_parser().parse_args()
    # canvas.pack()

    # places = [Place('p',p,canvas) for p in args.marking]

    # places[0].set_coor(100,200)
    # places[1].set_coor(300,100)
    # places[2].set_coor(300,300)
    # places[3].set_coor(600,200)

    # [p.show() for p in places]


    # trans = dict(
    #     t1=Transition('a', [Out(places[0])], [In(places[1]),In(places[2])]),
    #     t2=Transition('b', [In(places[1]),In(places[2])], [In(places[3]),In(places[0])]),
    # )

    # trans['t1'].show(canvas,200,200)
    # trans['t2'].show(canvas,400,400)

    # from random import choice
    # firing_sequence = [choice(list(trans.keys())) for _ in range(args.firings)]
    #firing_sequence = ["t1", "t1", "t2", "t1"]

    # problem2(100)
    print('__________________________________________')
    problem3(100)
    # petri_net = PetriNet(trans,places,canvas)
    # petri_net.run(firing_sequence,0)
    # windows.mainloop()
