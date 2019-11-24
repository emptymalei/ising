import numpy as np

class Ising():
    def __init__(self, params):
        self.width = params.get('width') or 20
        self.height = params.get('height') or 20
        self.states = params.get('states') or [-1,1]


    def initialize(self, state=None):
        if state is None:
            state = np.random.choice(
                self.states, size=(self.height, self.width)
            )

        self.state = state

    def _neighbours(self, coords):
        i = coords[0]
        j = coords[1]
        neighbour_coords = (
            ((i-1)%self.height, j),
            ((i+1)%self.height, j),
            (i, (j-1)%self.width),
            (i, (j+1)%self.width)
        )

        neighbours = self.state[neighbour_coords]

        return neighbours

    def delta_energy(self, coord):
        neighbour_states = self._neighbours(coord)
        coord_state = self.state[coord]
        return 2 * coord_state * np.sum(neighbour_states)


if __name__ == "__main__":
    ising_param = {
        'width': 20,
        'height': 20
    }

    ising = Ising(ising_param)
    ising.initialize()

    print(
        ising.state
    )

    print(
        np.random.choice(
            [-1,1], size=(10,10)
        )
    )

    print('END of GAME')