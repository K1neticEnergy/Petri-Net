# Petri Net with Visualization

## Description

An implementation of a Petri Net in python with homework-solving visualization

## Prerequisites

- tkinter : a python library to create GUI 

- math: trigonometric calculation

Use ```pip``` command to install those libraries above.

```console
    pip install --upgrade pip
    pip install tkinter math
```

## Structure

### **UML Class Diagram** 
![UML class](./UML_class.png)


## Algorithm

### Find all reachable markings of a petri net (or construct a transition system from a petri net)

Strategy: Since each marking has at most n next markings in case of at most n enabled transitions, we will apply Greedy's algorithm in the form of Breadth-first Search (BFS) algorithm. A Queue stores next transitions of the front and iteratively pops front after finding all enabled markings until a queue is empty. 

Pseudo-code:
```code
Function reach()
    ts as a list
    transition as a dictionary
    reachable_marking as a queue
    Assign initial markings to the queue
    while reachable_marking is not empty
        front = reachable_marking.front()
        for name in transitions
            if transitions[name].fire():
                retrieve marking from places
                if marking is not in reachable_marking and ts:
                    reachable_marking.push(marking)
        reachable_marking.pop()
        ts.push(front)
    return ts
```

## Apply implementation into problemset
### Problem 1
