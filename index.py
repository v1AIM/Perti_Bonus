
# Run using 'python index.py' in the terminal


class Place:
    def __init__(self, TokensHolding):

        # TokensHolding: Numer of token the place is initialized with.

        self.TokensHolding = TokensHolding

    def __repr__(self):
        return str(self.TokensHolding)

# representation of Flows in the Petri Net


class FlowBase:
    def __init__(self, place, amount=1):

        # place: The one place acting as source/target of the arc as arc in the net
        # amount: The amount of token removed/added from/to the place.

        self.place = place
        self.amount = amount


class Outgoing(FlowBase):

    # Removing token.
    def trigger(self):

        self.place.TokensHolding -= self.amount

    # Validate action of Outgoing arc is possible.
    def non_blocking(self):

        return self.place.TokensHolding >= self.amount


class InGoing(FlowBase):
    # Adding tokens.
    def trigger(self):

        self.place.TokensHolding += self.amount


class Transition:
    def __init__(self, Outgoing_arcs, InGoing_arcs):

        # Outgoing_arcs: Collection of ingoing arcs
        # InGoing_arcs: Collection of Outgoing arcs

        self.Outgoing_arcs = set(Outgoing_arcs)
        self.arcs = self.Outgoing_arcs.union(InGoing_arcs)

    def fire(self):
        # Check if transition is allowed
        not_blocked = all(arc.non_blocking() for arc in self.Outgoing_arcs)
        # Note: This would have to be checked differently for variants of
        # petri  nets that take more than once from a place, per transition.
        if not_blocked:
            for arc in self.arcs:
                arc.trigger()
        return not_blocked  # return if fired, for the sake of debuging


class PetriNet:
    def __init__(self, transitions, places: dict[str, Place]):
        self.places = places
        self.transitions = transitions
        # allowed[places] = [transitions]
        self.allowed = {
            tuple([
                p.TokensHolding for p in self.places.values()
            ]): [t for t in self.transitions.keys()]
        }
        # print(f"Allowed: {self.allowed}")
        self.fired = set()
        self.reachability_graph = []
        self.sound = True

    def run(self):
        for t, transition in self.transitions.items():
            # print(f"Current: {[p for p in self.places.values()]}")
            # keep a copy of the places, before transition fired
            places_before = {
                p: place.TokensHolding for p, place in self.places.items()
            }

            places_before_tuple = tuple([
                int(p > 0) for p in places_before.values()
            ])

            # Check if transition is allowed
            # print(f"Current Allowed: {self.allowed}")
            # print(f"Checking Transition: {t}")
            # print(f"Allowed of {tuple([p for p in places_before.values()])}: {self.allowed.get(tuple([p for p in places_before.values()]))}")

            if self.allowed.get(places_before_tuple) is None:
                # print(
                #     f"Couldn't find places {tuple([p for p in places_before.values()])} in Allowed")
                self.allowed[places_before_tuple] = [
                    t for t in self.transitions.keys()]
                # print(f"Now Current Allowed: {self.allowed}")

            if t not in self.allowed[places_before_tuple]:
                # print(f"Transition: {t} not allowed")
                continue

            success = transition.fire()

            if success:
                self.reachability_graph.append((places_before_tuple, t, tuple([
                    p.TokensHolding for p in self.places.values()
                ])))

                # print(f"Transition: {t} fired")
                # print(f"New: {[p for p in self.places.values()]}\n")

                # Condition 3: Check if every transition occurs in the reachability graph
                self.fired.add(t)

                self.allowed[places_before_tuple].remove(t)
                # print(
                #     f"Removed {t} from Allowed of {tuple([p for p in places_before.values()])}: {self.allowed}")

                # self.allowed[tuple([
                #     p.TokensHolding for p in self.places.values()
                # ])] = [t for t in self.transitions.keys()]

                # Check if the termination state is reached, only one token
                # exists in the workflow which is in the termination state.
                if not self.check_condition_2():
                    # print("NOT SOUND")
                    self.sound = False
                    return

                self.run()

                # Set places back to before transition fired
                for p, tokens in places_before.items():
                    self.places[p].TokensHolding = tokens
            else:
                # print(f"Transition: {t} not fired")
                pass

    def check_condition_2(self):
        last_key, last_value = list(self.places.items())[-1]
        if last_value.TokensHolding == 1:
            only_one_token = sum(
                [p.TokensHolding for p in self.places.values()]) == 1
            return only_one_token
        else:
            return True


def convert_to_string(places, row):
    places_before = row[0]
    transition = row[1]
    places_after = row[2]

    new_places_before = []

    for place, tokens in zip(places, places_before):
        if tokens != 0:
            new_places_before.append(
                f"{place}" + ("" if tokens == 1 else f":{tokens}"))

    new_places_after = []

    for place, tokens in zip(places, places_after):
        if tokens != 0:
            new_places_after.append(
                f"{place}" + ("" if tokens == 1 else f":{tokens}"))

    return f"{tuple(new_places_before)} -> {transition} -> {tuple(new_places_after)}"


def input_transitions(places):
    number_of_transitions = int(input("Number of transitions: "))

    transitions = {
        **{f"t{i}": None for i in range(1, number_of_transitions + 1)},
    }

    for t in transitions:
        print(t, end=" ")
    print()

    for t in transitions.keys():
        outgoing_arcs = [Outgoing(places[arc]) for arc in input(
            f"Outgoing arcs for {t}: ").split(" ")]
        ingoing_arcs = [InGoing(places[arc]) for arc in input(
            f"Ingoing arcs for {t}: ").split(" ")]

        transitions[t] = Transition(outgoing_arcs, ingoing_arcs)

    return transitions


def input_places():
    number_of_places = int(input("Number of places: "))

    places = {
        "i": Place(0),
        **{f"p{i}": Place(0) for i in range(1, number_of_places-1)},
        "o": Place(0)
    }

    return places


def input_initial_marking(places):
    new_places = {k: v for k, v in places.items()}

    initial_marking = input(
        "Initial marking (separated by spaces): ").split(" ")

    for place, tokens in zip(new_places.keys(), initial_marking):
        new_places[place].TokensHolding = int(tokens)

    return new_places


if __name__ == "__main__":
    # Example 1 Lab
    # places = dict(
    #     p0=Place(1),
    #     p1=Place(0),
    #     p2=Place(0),
    #     p3=Place(0),
    #     p4=Place(0),
    #     p5=Place(0),
    # )

    # Example 2 Lab
    # places = dict(
    #     p0=Place(1),
    #     p1=Place(0),
    #     p2=Place(0),
    #     p3=Place(0),
    #     p4=Place(0),
    #     p5=Place(0),
    # )
    # Example 3 Lab
    # places = dict(
    #     p0=Place(1),
    #     p1=Place(0),
    #     p2=Place(0),
    #     p3=Place(0),
    #     p4=Place(0),
    #     p5=Place(0),
    #     p6=Place(0),
    # )

    # Example 1 Lab
    # transitions = dict(
    #     t1=Transition(
    #         [Outgoing(places["p0"])],
    #         [InGoing(places["p1"]), InGoing(places["p2"])]
    #     ),
    #     t2=Transition(
    #         [Outgoing(places["p1"])],
    #         [InGoing(places["p3"])]
    #     ),
    #     t3=Transition(
    #         [Outgoing(places["p2"])],
    #         [InGoing(places["p4"])]
    #     ),
    #     t4=Transition(
    #         [Outgoing(places["p3"]), Outgoing(places["p4"])],
    #         [InGoing(places["p5"])]
    #     ),
    #     t5=Transition(
    #         [Outgoing(places["p1"]), Outgoing(places["p4"])],
    #         [InGoing(places["p5"])],
    #     )
    # )

    # transitions=dict(
    #     t1=Transition(
    #         [Outgoing(places["p0"])],
    #         [InGoing(places["p1"]), InGoing(places["p2"])]
    #     ),
    #     t2=Transition(
    #         [Outgoing(places["p4"])],
    #         [InGoing(places["p1"])]
    #     ),
    #     t3=Transition(
    #         [Outgoing(places["p2"])],
    #         [InGoing(places["p3"])]
    #     ),
    #     t4=Transition(
    #         [Outgoing(places["p1"])],
    #         [InGoing(places["p4"])]
    #     ),
    #     t5=Transition(
    #         [Outgoing(places["p1"]), Outgoing(places["p3"])],
    #         [InGoing(places["p5"])]
    #     ),
    # )

    # Example 3 Lab
    # transitions = dict(
    #     t1=Transition(
    # [Outgoing(places["p0"])],
    # [InGoing(places["p1"]), InGoing(places["p2"])]
    # ),
    # t2=Transition(
    #     [Outgoing(places["p4"])],
    #     [InGoing(places["p1"])]
    # ),
    # t3=Transition(
    #     [Outgoing(places["p1"])],
    #     [InGoing(places["p4"]), InGoing(places["p3"])]
    # ),
    # t4=Transition(
    #     [Outgoing(places["p2"]), Outgoing(places["p3"])],
    #     [InGoing(places["p5"])]
    # ),
    # t5=Transition(
    #     [Outgoing(places["p5"])],
    #     [InGoing(places["p2"])]
    # ),
    # t6=Transition(
    #     [Outgoing(places["p4"]), Outgoing(places["p5"])],
    #     [InGoing(places["p6"])]
    #     ),
    # )

    # Example 3 Lab
    # transitions=dict(
    #     t1=Transition(
    #         [Outgoing(places["p0"])],
    #         [InGoing(places["p1"]), InGoing(places["p2"])]
    #     ),
    #     t2=Transition(
    #         [Outgoing(places["p4"])],
    #         [InGoing(places["p1"])]
    #     ),
    #     t3=Transition(
    #         [Outgoing(places["p1"])],
    #         [InGoing(places["p4"]),InGoing(places["p3"])]
    #     ),
    #     t4=Transition(
    #         [Outgoing(places["p2"]),Outgoing(places["p3"])],
    #         [InGoing(places["p5"])]
    #     ),
    #     t5=Transition(
    #         [Outgoing(places["p5"])],
    #         [InGoing(places["p2"])]
    #     ),
    #      t6=Transition(
    #          [Outgoing(places["p4"]), Outgoing(places["p5"])],
    #          [InGoing(places["p6"])]
    #     ),

    places = input_places()
    for p in places:
        print(p, end=" ")
    print()
    places = input_initial_marking(places)
    transitions = input_transitions(places)

    petri_net = PetriNet(transitions, places)

    petri_net.run()
    print()
    print(f"Sound: {petri_net.sound}")
    print()
    print(f"Reachability Graph: ")
    for r in petri_net.reachability_graph:
        print(convert_to_string(places, r))
