class Place:
    '''
        A place is a passive nodes of Petri Net
        Properties:
            - label: name of a place
            - token: number of token holding
            - (visualize)
        Method:
    '''
    def __init__(self,token):
        self.token = token

class ArcBase:
	def __init__(self,place,amount=1):
		self.place = place
		self.amount = amount

class Out(ArcBase):
	def trigger(self):
		self.place.token -= self.amount
	

class In(ArcBase):
	def trigger(self):
		self.place.token += self.amount

class Transition:
	def __init__(self,out_arcs,in_arcs):
		self.out_arcs = out_arcs
		self.in_arcs = in_arcs
		self.arcs = set(out_arcs)
		self.arcs = self.arcs.union(set(in_arcs))
	
	def enabled(self):
		for i in self.out_arcs:
			if i.place.token == 0: 
				return False
		return True

	def fire(self):
		if self.enabled():
			for arc in self.arcs:
				arc.trigger()
			return True
		return False

class  PetriNet:
	def __init__(self,transitions,places):
		self.transition = transitions
		self.place =  places
	def run(self,firing_sequence):
		#print("Using firing sequence:\n" + " => ".join(firing_sequence))
		print("start {}\n".format([p.token for p in self.place.values()]))

		for name in firing_sequence:
			t = self.transition[name]
			if t.fire():
				print("{} firing!".format(name))
				print(" => {}".format([p.token for p in self.place.values()]))
			else:
				print("{} fizzled.... :/".format(name))

		print("final {}\n".format([p.token for p in self.place.values()]))
	#this method is used for problem 1b
	def reach(self,marking):
		if len(self.place) != len(marking): return []
		reachable_marking = []
		
		for name in self.transition.keys() :
			i = 0
			for v in self.place.values():
				v.token = marking[i]
				i += 1
			t = self.transition[name] 
			if(t.fire()):
				lst = [p.token for p in self.place.values()]
				print(marking, "firing "+ name + " => ",lst )
				reachable_marking.append(lst)
				
		return reachable_marking
	
	def display(self):
		print("Places : {" + " , ".join(self.place.keys()) + "}")
		print("Transitions : {" + " , ".join(self.transition.keys()) + "}")
		print("init {}\n".format([p.token for p in self.place.values()]))

def problem1():
	marking1 = [1,0,0]
	ps1 = dict(
			free = Place(marking1[0]),
			busy = Place(marking1[1]),
			docu = Place(marking1[2])
	     )
	ts1 = dict(
			start = Transition([Out(ps1['free'])],[In(ps1['busy'])]),
			change = Transition([Out(ps1['busy'])],[In(ps1['docu'])]),
			end = Transition([Out(ps1['docu'])],[In(ps1['free'])])
		)
	petri_net1 = PetriNet(ts1,ps1)
	print("1a --------------------------")
	petri_net1.display()
	print("1bi------------------------------")
	init = []
	for i in range(1,4):
		init.append(int(input()))
	print("initial marking :",init)
	sum = 0
	for i in init:
		sum += i
	if sum == 1 :
		reachable_marking = []
		reachable_marking.append(init)

		for marking in reachable_marking:
			new_reachable_marking = petri_net1.reach(marking)
			for i in new_reachable_marking:
				checkDuplicate = False
				for j in reachable_marking:
					if i == j:
						checkDuplicate = True
						break
				if checkDuplicate == False:
					reachable_marking.append(i)

			
			
			
	else :
		print("PetriNet khong hop le")
	print("1bii--------------------------------")
	init = []
	for i in range(1,4):
		init.append(int(input()))
	print("initial marking :",init)

	reachable_marking = []
	reachable_marking.append(init)

	for marking in reachable_marking:
		new_reachable_marking = petri_net1.reach(marking)
		for i in new_reachable_marking:
			checkDuplicate = False
			for j in reachable_marking:
				if i == j:
					checkDuplicate = True
					break
			if checkDuplicate == False:
				reachable_marking.append(i)
	print("---------------------------------------")

			
			
			


problem1()
marking2 = [5,0,1]
ps2 = dict(
			wait = Place(marking2[0]),
			inside = Place(marking2[1]),
			done = Place(marking2[2])
	     )
ts2 = dict(
			start = Transition([Out(ps2['wait'])],[In(ps2['inside'])]),
			change = Transition([Out(ps2['inside'])],[In(ps2['done'])])
		)

	#firing_sequence  = ["t1","t1","t2","t1"]


firing_sequence = []

petri_net2 = PetriNet(ts2,ps2)
petri_net2.display()

print("----------------------------------")

marking3 = [4,1,0,0,1,0]
ps3 = dict(
			wait = Place(marking3[0]),
			free = Place(marking3[1]),
			inside = Place(marking3[2]),
			busy = Place(marking3[3]),
			done = Place(marking3[4]),
			docu = Place(marking3[5])
	     )

ts3 = dict(
			start = Transition([Out(ps3['wait']),Out(ps3['free'])],[In(ps3['inside']),In(ps3['busy'])]),
			change = Transition([Out(ps3['inside']),Out(ps3['busy'])],[In(ps3['done']),In(ps3['docu'])]),
			end = Transition([Out(ps3['docu'])],[In(ps3['free'])])
		)


	#firing_sequence  = ["t1","t1","t2","t1"]


firing_sequence = ts3.keys()

petri_net3 = PetriNet(ts3,ps3)
petri_net3.run(firing_sequence)