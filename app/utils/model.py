import logging
import numpy as np
from itertools import product as _product

logger = logging.getLogger('model')
logger.setLevel(logging.DEBUG)

class Ising():
    def __init__(self, params):
        self.width = params.get('width') or 20
        self.height = params.get('height') or 20
        self.states = params.get('states') or [-1,1]
        self.max_steps = params.get('max_steps') or 100000
        self.observables = params.get('observables') or []


    def distribution(self):
        """
        distribution calculates the number of microstates for each energy level.
        """


        # generate possible combinations out of the states
        list_of_states_at_row = [self.states] * self.height
        rows = list(
            _product(*list_of_states_at_row)
        )

        list_of_rows = [rows] * self.width

        all_states = list(
            _product(*list_of_rows)
        )

        all_states_count = len(all_states)

        distribution = []
        for state_i in all_states:
            self.state = state_i
            ene = self._observe__energy(state_i, dist=True)
            single_particle_state_ct = self._single_particle_state_count(state_i)
            distribution.append(
                {
                    'energy': ene.get('energy'),
                    'state': state_i,
                    'dist': ene.get('dist'),
                    'spin_dist': single_particle_state_ct
                }
            )

        self.dist = {
            'total_states': all_states_count,
            'states': distribution
        }

    def _single_particle_state_count(self, state=None):

        if state is None:
            state = self.state

        flatten_state = [s for row in state for s in row]

        res = {}

        for st in self.states:
            res[st] = flatten_state.count(st)

        return res

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

        neighbours = []
        for i in neighbour_coords:
            neighbours.append(self.state[i])

        return neighbours

    def delta_energy(self, coord):
        """
        delta_energy calculates the energy different between the new state and the current state

        :param coord: coordnates
        :type coord: [list, tuple]
        :return: energy change
        :rtype: [float]
        """
        neighbour_states = self._neighbours(coord)
        coord_state = self.state[coord]
        return 2 * coord_state * np.sum(neighbour_states)

    def evolve_one(self, beta):
        """
        evolve one step forward of system
        """

        random_coord = (
            np.random.randint(self.height),
            np.random.randint(self.width)
            )
        current_state_at_coord = self.state[random_coord]
        delta_e = self.delta_energy(random_coord)
        if (delta_e < 0) or (np.random.rand() < np.exp(-delta_e/beta)):
            new_state_at_coord = -1 * current_state_at_coord
        else:
            new_state_at_coord = current_state_at_coord

        self.state[random_coord] = new_state_at_coord

    def evolve(self, beta, steps=None, observe_counts=None):
        """
        evolve evolves the system step by step

        :param beta: beta from statistical mechanics
        :type beta: float
        :param steps: number of steps to run, defaults to None
        :type steps: int, optional
        """
        if steps is None:
            steps = 100
        if observe_counts is None:
            observe_counts = 10

        observe_interval = int(steps/observe_counts)
        if observe_interval < 1:
            observe_interval = 1

        logger.debug('using observe_interval', observe_interval)
        print('using observe_interval', observe_interval)

        step = 0
        observe_count = 0
        for i in range(steps):
            self.evolve_one(beta)
            if observe_count%observe_interval == 0:
                self.observables.append(
                    self.observe(step)
                )
            if step > steps:
                break
            step += 1

    def observe(self, step):

        obser_energy = self._observe__energy()

        res = {
            "step": step,
            "energy": obser_energy.get('energy'),
            "state": self.state
        }

        return res

    def _observe__energy(self, state=None, dist=None):
        """
        _observe__energy calcualates the observables of the grid
        """
        if state is None:
            state = self.state
        if dist is None:
            dist = False
        if isinstance(state, (list, tuple)):
            state = np.asarray(state)

        res = {}

        total_energy = 0
        single_partile_energy_dist = {}
        for i in range(self.height):
            for j in range(self.width):
                mag_i_j = state[(i,j)]

                ip1 = (i + 1)%self.height
                im1 = (i - 1)%self.height
                jp1 = (j + 1)%self.width
                jm1 = (j - 1)%self.width

                mag_neighbours =  state[(
                        ip1, j
                    )] + state[(
                        i, jp1
                    )] +  state[(
                        im1, j
                        )] +  state[(
                            i,jm1
                            )]

                e_ij = -mag_i_j * mag_neighbours
                total_energy += e_ij
                if dist:
                    e_ij_dist = single_partile_energy_dist.get(e_ij,0)
                    single_partile_energy_dist[e_ij] = e_ij_dist + 1

        # the energy calculation has been repeated for four times
        total_energy = total_energy / 4
        res['energy'] = total_energy
        if dist:
            res['dist'] = single_partile_energy_dist

        return res



if __name__ == "__main__":
    ising_param = {
        'width': 2,
        'height': 2
    }

    ising = Ising(ising_param)

    ising.distribution()
    print(ising.dist)

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