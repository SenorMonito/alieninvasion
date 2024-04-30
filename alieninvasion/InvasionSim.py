from random import sample
from networkx import DiGraph, to_dict_of_dicts
from typing import List


class InvasionSim:
    def __init__(self):
        self.__world = DiGraph()

    def __str__(self):
        return f"cities = {self.__world.nodes.data()}\nroutes = {self.__world.edges.data()}"

    def add_city(self, city:str) -> None:
        self.__world.add_node(city, aliens=[])

    def add_route(self, city:str, sibling: str, dir:str) -> None:
        self.__world.add_edge(city, sibling, dir=dir)

    def deploy_alien(self, city:str, id: int) -> None:
        self.__world.nodes[city]["aliens"].append(id)

    def pop_alien(self, city:str) -> int:
        return self.__world.nodes[city]["aliens"].pop(0)
    
    @property
    def cities(self) -> List[str]:
        return list(self.__world.nodes)
    
    def aliens(self, city:str) -> List[int]:
        return self.__world.nodes[city]["aliens"]
    
    def is_overwhelmed(self, city: str) -> bool:
        return len(self.aliens(city)) > 1

    def destroy(self, city: str) -> None:
        # will remove city, aliens and edges
        print(f"{city} destroyed by aliens {self.aliens(city)}")
        self.__world.remove_node(city)



    def deploy(self, n: int) -> None:
        """Deploy aliens randomly on world, without overlapping"""
        for i, city in enumerate(sample(self.cities, n)):
            self.deploy_alien(city, i)

    def move_aliens(self) -> None:
        """Go through cities and move aliens randomly"""
        moves = 0
        for city in self.cities:
            has_aliens = len(self.aliens(city)) > 0
            nbrs = list(self.__world.neighbors(city))
            if has_aliens and len(nbrs) > 0:
                # select first random neighbor
                nbr = sample(nbrs, 1)[0]
                et = self.pop_alien(city)
                self.deploy_alien(nbr, et)
                print(f"alien {et} moved from {city} to {nbr}")
                moves += 1

        if moves < 1:
            print("Stalemate. All aliens trapped. Finish")
            exit()

    def run_sim(self, iterations: int) -> None:
        """
        Run the simulation through
        Do this by moving the aliens into position, then destroy overwhelmed cities
        """
        for i in range(iterations):
            print(f"Day {i} of invasion")
            self.move_aliens()
            # If city is overwhelmed one alien nuke everything
            for city in [city for city in self.cities if self.is_overwhelmed(city)]:
                self.destroy(city)

    """
    File read/write
    """
    
    def read(self, fh: str) -> None:
        """
        Read world from file. This has a defined format:
        ```
        Foo north=Bar west=Baz south=Qu-ux
        Bar south=Foo west=Bee
        ```
        """
        with open(fh, 'r') as f:
            for line in f.readlines():
                    city, _, neighbors  = line.strip().partition(" ")
                    self.add_city(city)
                    for neighbor in neighbors.split(" "):
                        direction, sister = neighbor.split("=")
                        self.add_city(sister)
                        self.add_route(city, sister, dir=direction)

    def write(self, out: str) -> None:
        """
        Write world out to file using defined format"
        ```
        Foo north=Bar west=Baz south=Qu-ux
        Bar south=Foo west=Bee
        ```
        """
        d = to_dict_of_dicts(self.__world)
        with open(out, 'w') as file:
            for city, neighbours in d.items():
                if neighbours:
                    ln = [city]
                    for neighbour, direction in neighbours.items():
                        ln.append(direction["dir"] + ":" + neighbour)
                        file.write(" ".join(ln)+"\n")
