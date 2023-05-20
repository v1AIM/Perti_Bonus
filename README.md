# Perti_Bonus

This is a Perti Net project that checks the soundness of a given workflow and outputs the rechability graph.

## How to Run
```bash
python index.py
```


### How to enter input

This example is in slides petri net page 52

![Example_Sound](https://github.com/v1AIM/Perti_Bonus/assets/70938961/a10c854a-f25f-4139-b248-4ab9e7b4803b)




```
Number of places : 6
--> it will print the places with there i (intial) and o (last place) 
i p1 p2 p3 p4 o

Intial marking (separated by spaces): 1 0 0 0 0 0 

Number of transitions: 6
--> it will print the transitions 
t1 t2 t3 t4 t5 t6

#### Now the Important part (the outgoing and the Ingoing arcs)

Outgoing arcs means the flow from i to a transition
Ingoing arcs means the flow from the transition to a place 

to continue if there was no in or out going just press Enter in blank"

so we will enter the input as follow
Outgoing arcs for t1:i 
Ingoing arcs for t1: p2 p3
Outgoing arcs for t2: p2
Ingoing arcs for t2: p1
Outgoing arcs for t3: p1
Ingoing arcs for t3: p2
Outgoing arcs for t4: p4
Ingoing arcs for t4: p3
Outgoing arcs for t5: p3
Ingoing arcs for t5: p4
Outgoing arcs for t6: p2 p3
Ingoing arcs for t6: o

Sound: True "printing the Soundness"


"representation of the Reachability Graph"

Reachability Graph: 
('i',) -> t1 -> ('p2', 'p3')
('p2', 'p3') -> t2 -> ('p1', 'p3')
('p1', 'p3') -> t3 -> ('p2', 'p3')
('p2', 'p3') -> t5 -> ('p2', 'p4')
('p2', 'p4') -> t2 -> ('p1', 'p4')
('p1', 'p4') -> t3 -> ('p2', 'p4')
('p2', 'p4') -> t4 -> ('p2', 'p3')
('p2', 'p3') -> t6 -> ('o',)
('p1', 'p4') -> t4 -> ('p1', 'p3')
('p1', 'p3') -> t5 -> ('p1', 'p4')



 

```
