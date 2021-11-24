# Petri Net (Project Bor)

## Reference:

- [Wikipedia](https://en.wikipedia.org/wiki/Petri_net)

## Technology:

- Python
-

## Notes

UML:

1. Place
    - label : string
    - token : int
    - 
    - coordinate (for visual)
2. Arc
    - place: Place
    - amount: int
    - trigger: 
    - coordinate (for visual)

3. Transition
    - label : string
    - input : list of input arc
    - output: list of output arc
    + enabled : determine a transition is ready to fire
    + fire : when enabled, tokens which are set amount to be taken in each input arc are distributed to each output arc
    - coordinate (for visual)
