from tkinter import Tk, Canvas, Frame, BOTH

class Place:
    '''
        A place is a passive nodes of Petri Net
        Properties:
            - label: name of a place
            - token: number of token holding
            - (visualize)
        Method:
    '''
    def __init__(self,label,token):
        self.label = label
        self.token = token

    
class Arc:
    '''

    '''
    def __init__(self,place,amount=1):
        self.place = place
        self.amount = amount

class Out(Arc):
    def trigger(self):
        self.place.token -= self.amount

class In(Arc):
    def trigger(self): 
        self.place.token += self.amount


class Transition:
    '''

    '''
    def __init__(self,label,out_arcs,in_arcs):
        self.label = label
        self.out_arcs = set(out_arcs)
        self.arcs = self.out_arcs.union(in_arcs)

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
 
class PetriNet:
    def __init__(self,transitions):
        self.transitions = transitions

    def deadlock_free(self):
        return sum([self.transitions[i].enabled() for i in self.transitions]) != 0

    def run(self,firing_sequence,places):
        print("start {}\n".format([pl.token for pl in places]))
        for name in firing_sequence:
            t = self.transitions[name]
            if self.deadlock_free():
                if t.fire() :

                    print("{} firing!".format(self.transitions[name].label))
                    print(" => {}\n".format([pl.token for pl in places]))
                else:
                    print("{} stucked. Switching...".format(self.transitions[name].label))

        print("final {}\n".format([pl.token for pl in places]))




def make_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--firings', type=int)
    parser.add_argument('--marking', type=int, nargs='+')
    return parser

def problem1(firings):
    places = [Place('wait', 5), Place('inside', 0),Place('done', 1)]
    trans = dict(
        t1=Transition('start', [Out(places[0])], [In(places[1])]),
        t2=Transition('change', [Out(places[1])], [In(places[2])]),
    )

    # non-determistic choice:
    from random import choice
    firing_sequence = [choice(list(trans.keys())) for _ in range(firings)]
    petri_net = PetriNet(trans)
    petri_net.run(firing_sequence, places)

def problem3(firings):
    places = [Place('wait', 3), Place('inside', 0),Place('done', 1), Place('free', 1), Place('busy', 0),Place('docu', 0)]
    trans = dict(
        t1=Transition('start', [Out(places[0]),Out(places[3])], [In(places[1]),In(places[4])]),
        t2=Transition('change', [Out(places[1]),Out(places[4])], [In(places[2]),In(places[5])]),
        t3=Transition('end', [Out(places[5])], [In(places[3])]),
    )

    # non-determistic choice:
    from random import choice
    firing_sequence = [choice(list(trans.keys())) for _ in range(firings)]
    petri_net = PetriNet(trans)
    petri_net.run(firing_sequence, places)


if __name__ == '__main__':
    # args = make_parser().parse_args()

    # places = [Place('p', p) for p in args.marking]

    # trans = dict(
    #     t1=Transition('', [Out(places[0])], [In(places[1]),In(places[2])]),
    #     t2=Transition('', [In(places[1]),In(places[2])], [In(places[3]),In(places[0])]),
    # )

    # # from random import choice
    # # firing_sequence = [choice(list(trans.keys())) for _ in range(args.firings)]
    # firing_sequence = ["t1", "t1", "t2", "t1"]

    # petri_net = PetriNet(trans)
    # petri_net.run(firing_sequence, places)
    problem1(100)
    print('__________________________________________')
    problem3(100)

