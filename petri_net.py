from tkinter import Tk, Canvas, Frame, BOTH, constants, FIRST, LAST
import time
from math import cos, sin, sqrt, acos

HEIGH = 486
WIDTH = 864
OPENING_TIME = 2000
TRANSITION_TIME = 1000

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
        self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        dir_x = [0,0.5, 0,-0.5,0,1, 0,-1]
        dir_y = [0.5,0,-0.5, 0,1,0,-1, 0]
        self.tks = [self.canvas.create_oval(self.x - 5 + dir_x[i%8] * 20, self.y - 5 + dir_y[i%8] * 20, self.x + 5 + dir_x[i%8] * 20, self.y + 5 + dir_y[i%8] * 20,fill='red') for i in range(0, self.token)]

    def show(self):
        if self.tks: self.tks = [self.canvas.delete(tk) for tk in self.tks]
        dir_x = [0,0.5, 0,-0.5,0,1, 0,-1]
        dir_y = [0.5,0,-0.5, 0,1,0,-1, 0]
        self.tks = [self.canvas.create_oval(self.x - 5 + dir_x[i%8] * 20, self.y - 5 + dir_y[i%8] * 20, self.x + 5 + dir_x[i%8] * 20, self.y + 5 + dir_y[i%8] * 20,fill='red') for i in range(0, self.token)]
        self.loop = self.canvas.after(1,self.show)


class Arc:
    '''
        An arc connects a place and a transition.
        Properties:
            - place: place in a petri net
            - amount: set throughput limit
    '''
    def __init__(self,place,amount=1):
        self.place = place
        self.amount = amount

class Out(Arc):
    '''
        An output arc derives 
    '''
    def trigger(self):
        self.place.token -= self.amount

    def show(self,canvas,x,y):
        angle = acos(abs(x - self.place.x) / sqrt((x - self.place.x)**2 + (y - self.place.y)**2))
        x0_offset = Place.radius * cos(angle) * (1 if (x - self.place.x >= 0) else -1)
        y0_offset = Place.radius * sin(angle) * (1 if (y - self.place.y >= 0) else -1)
        x_offset = Transition.w * cos(angle) * (1 if (x - self.place.x >= 0) else -1)
        y_offset = Transition.h * sin(angle) * (1 if (y - self.place.y >= 0) else -1)

        canvas.create_line(self.place.x + x0_offset, self.place.y + y0_offset, x - x_offset, y - y_offset, arrow=LAST)

class In(Arc):
    def trigger(self): 
        self.place.token += self.amount
    
    def show(self,canvas,x,y):
        angle = acos(abs(x - self.place.x) / sqrt((x - self.place.x)**2 + (y - self.place.y)**2))
        x0_offset = Place.radius * cos(angle) * (1 if (x - self.place.x >= 0) else -1)
        y0_offset = Place.radius * sin(angle) * (1 if (y - self.place.y >= 0) else -1)
        x_offset = Transition.w * cos(angle) * (1 if (x - self.place.x >= 0) else -1)
        y_offset = Transition.h * sin(angle) * (1 if (y - self.place.y >= 0) else -1)

        canvas.create_line(self.place.x + x0_offset, self.place.y + y0_offset,x - x_offset, y - y_offset, arrow=FIRST)

class Transition:
    '''

    '''
    h = 30
    w = 30

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
            self.y + self.h, self.x + self.w, self.y + self.h, self.x + self.w, self.y - self.h, fill = 'blue')
        for i in self.arcs:
            i.show(self.canvas,self.x,self.y)
 
class PetriNet:
    def __init__(self,transitions,places,canvas):
        self.transitions = transitions
        self.places = places
        self.canvas = canvas

    def deadlock_free(self):
        return sum([self.transitions[i].enabled() for i in self.transitions]) != 0

    def run(self,windows,firing_sequence,i,auto_close=True,done=False):
        if i == 0: print("start {}\n".format([pl.token for pl in self.places]))
        if i >= len(firing_sequence): return
        name = firing_sequence[i]
        t = self.transitions[name]
        if self.deadlock_free():
            if t.fire() :
                print("{} firing!".format(t.label))
                print(" => {}\n".format([pl.token for pl in self.places]))
                self.canvas.after(TRANSITION_TIME,self.run,windows,firing_sequence,i + 1,auto_close,done)
            else:
                print("{} stucked. Switching...".format(t.label))
                self.canvas.after(TRANSITION_TIME / 2,self.run,windows,firing_sequence,i + 1,auto_close,done)
        else:
            print("deadlock")
            print("final {}\n".format([p.token for p in self.places]))
            done = True
        if done and auto_close: windows.after(OPENING_TIME, windows.destroy)

    def reach(self, find_all=True):
        ts = []
        reachable_markings = []
        reachable_markings.append([p.token for p in self.places])
        while len(reachable_markings) != 0:
            front = reachable_markings[0]
            reachable_markings.pop(0)
            for name in self.transitions:
                for p,t in zip(self.places,front):
                    p.token = t
                t = self.transitions[name]
                if(t.fire()):
                    lst = [p.token for p in self.places]
                    print(front, "firing "+ name + " => ",lst )
                    if lst not in ts and lst not in reachable_markings: reachable_markings.append(lst)
            ts.append(front)
            if not find_all: break
        for p,t in zip(self.places,ts[0]):
            p.token = t           
        return ts

def make_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--firings', type=int)
    parser.add_argument('--marking', type=int, nargs='+')
    return parser

def problem1a():
    windows = Tk()
    canvas = Canvas(windows, bg="white",
           height=HEIGH, width=WIDTH)
    canvas.pack()
    places = [
        Place('free',  1, 200, 100, canvas), 
        Place('busy',  0, 400, 300, canvas),
        Place('docu',  0, 600, 100, canvas),
    ]

    trans = dict(
        start=Transition(
            'start', 
            [
                Out(places[0])
            ], 
            [
                In(places[1])
            ],
            200,
            300,
            canvas
        ),
        change=Transition(
            'change', 
            [
                Out(places[1])
            ], 
            [
                In(places[2])
            ],
            600,
            300,
            canvas
        ),
        end=Transition(
            'end', 
            [
                Out(places[2])
            ], 
            [
                In(places[0])
            ],
            400,
            100,
            canvas
        ),
    )

    # petri_net = PetriNet(trans,places,canvas)
    for i in trans: trans[i].show()
    windows.after(OPENING_TIME,windows.destroy)
    [p.show() for p in places]
    windows.mainloop()

def problem1b():
    windows = Tk()
    canvas = Canvas(windows, bg="white",
           height=HEIGH, width=WIDTH)
    canvas.pack()
    places = [
        Place('free',  0, 200, 100, canvas), 
        Place('busy',  0, 400, 300, canvas),
        Place('docu',  0, 600, 100, canvas),
    ]

    trans = dict(
        start=Transition(
            'start', 
            [
                Out(places[0])
            ], 
            [
                In(places[1])
            ],
            200,
            300,
            canvas
        ),
        change=Transition(
            'change', 
            [
                Out(places[1])
            ], 
            [
                In(places[2])
            ],
            600,
            300,
            canvas
        ),
        end=Transition(
            'end', 
            [
                Out(places[2])
            ], 
            [
                In(places[0])
            ],
            400,
            100,
            canvas
        ),
    )
    petri_net = PetriNet(trans,places,canvas)
    for i in trans: trans[i].show()
    try:
        sum = 0
        # Input
        for p in places:
            p.token = int(input()) 
            sum += p.token
        if sum == 1:
            petri_net.reach()
        else :
            print("Invalid Petri Net Needed")
    except:
        print('Invalid input')
    [p.show() for p in places]
    windows.after(OPENING_TIME,windows.destroy)
    windows.mainloop()

def problem1b_():
    windows = Tk()
    canvas = Canvas(windows, bg="white",
           height=HEIGH, width=WIDTH)
    canvas.pack()
    places = [
        Place('free',  0, 200, 100, canvas), 
        Place('busy',  0, 400, 300, canvas),
        Place('docu',  0, 600, 100, canvas),
    ]

    trans = dict(
        start=Transition(
            'start', 
            [
                Out(places[0])
            ], 
            [
                In(places[1])
            ],
            200,
            300,
            canvas
        ),
        change=Transition(
            'change', 
            [
                Out(places[1])
            ], 
            [
                In(places[2])
            ],
            600,
            300,
            canvas
        ),
        end=Transition(
            'end', 
            [
                Out(places[2])
            ], 
            [
                In(places[0])
            ],
            400,
            100,
            canvas
        ),
    )
    for i in trans: trans[i].show()
    petri_net = PetriNet(trans,places,canvas)
    try:
        for p in places:
            p.token = int(input()) 
    except:
        print('Invalid input')
    petri_net.reach()
    [p.show() for p in places]
    windows.after(OPENING_TIME,windows.destroy)
    windows.mainloop()

def problem1():
    print('Problem 1: ')
    print('+++++++++++++++++++++++++++++++++++')
    print('1 a: ')
    problem1a()
    print('1 b: ')
    problem1b()
    problem1b_()

def problem2(firings):
    print('Problem 2: ')
    print('+++++++++++++++++++++++++++++++++++')
    windows = Tk()
    canvas = Canvas(windows, bg="white",
        height=HEIGH, width=WIDTH)
    canvas.pack()
    places = [
        Place('wait',   5, 200, 100, canvas), 
        Place('inside', 0, 400, 100, canvas),
        Place('done',   1, 600, 100, canvas),
    ]
    trans = dict(
        start=Transition(
            'start', 
            [
                Out(places[0])
            ], 
            [
                In(places[1])
            ],
            300,
            100,
            canvas
        ),
        change=Transition(
            'change', 
            [
                Out(places[1])
            ], 
            [
                In(places[2])
            ],
            500,
            100,
            canvas
        ),
    )

    [p.show() for p in places]
    for i in trans: trans[i].show()
    # non-determistic choice:
    from random import choice
    firing_sequence = [choice(list(trans.keys())) for _ in range(firings)]
    petri_net = PetriNet(trans,places,canvas)
    print(petri_net.reach())
    petri_net.run(windows,firing_sequence, 0)
    windows.mainloop()

def problem3(firings):
    print('Problem 3: ')
    print('+++++++++++++++++++++++++++++++++++')
    windows = Tk()
    canvas = Canvas(windows, bg="white",
        height=HEIGH, width=WIDTH)
    canvas.pack()
    places = [  
                Place('wait',   3, 200, 200, canvas), 
                Place('inside', 0, 400, 300, canvas),
                Place('done',   1, 600, 200, canvas),
                Place('free',   1, 300, 100, canvas), 
                Place('busy',   0, 400, 200, canvas),
                Place('docu',   0, 500, 100, canvas),
            ]

    trans = dict(
        start=Transition(
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
            200,
            canvas
        ),
        change=Transition(
            'change', 
            [
                Out(places[1]),    
                Out(places[4])
            ], 
            [
                In(places[2]),    
                In(places[5])
            ],
            500,
            200,
            canvas
        ),
        end=Transition(
            'end', 
            [
                Out(places[5])
            ], 
            [
                In(places[3])
            ],
            400,
            100,
            canvas
        ),
    )

    [p.show() for p in places]
    for i in trans: trans[i].show()

    # non-determistic choice:
    from random import choice
    firing_sequence = [choice(list(trans.keys())) for _ in range(firings)]

    petri_net = PetriNet(trans,places,canvas)
    petri_net.run(windows,firing_sequence, 0)
    windows.mainloop()

def problem4():
    print('Problem 4: ')
    print('+++++++++++++++++++++++++++++++++++')
    windows = Tk()
    canvas = Canvas(windows, bg="white",
        height=HEIGH, width=WIDTH)
    canvas.pack()
    places = [  
                Place('wait',   3, 200, 200, canvas), 
                Place('inside', 0, 400, 300, canvas),
                Place('done',   1, 600, 200, canvas),
                Place('free',   1, 300, 100, canvas), 
                Place('busy',   0, 400, 200, canvas),
                Place('docu',   0, 500, 100, canvas),
            ]

    trans = dict(
        start=Transition(
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
            200,
            canvas
        ),
        change=Transition(
            'change', 
            [
                Out(places[1]),    
                Out(places[4])
            ], 
            [
                In(places[2]),    
                In(places[5])
            ],
            500,
            200,
            canvas
        ),
        end=Transition(
            'end', 
            [
                Out(places[5])
            ], 
            [
                In(places[3])
            ],
            400,
            100,
            canvas
        ),
    )

    for i in trans: trans[i].show()

    petri_net = PetriNet(trans,places,canvas)
    petri_net.reach(False)
    windows.after(OPENING_TIME,windows.destroy)
    [p.show() for p in places]
    windows.mainloop()


if __name__ == '__main__':
    problem1()
    print('__________________________________________')
    problem2(100)
    print('__________________________________________')
    problem3(100)
    print('__________________________________________')
    problem4()
