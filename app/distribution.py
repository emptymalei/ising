from utils.model import Ising
import logging

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)


def _dist_extraction(dist):
    """
    _dist_extraction extracts dist counts from the energy distribution dict
    """

    dist_keys = list(
        set(sum([
            list(i.keys()) for i in dist
        ],[]))
    )
    dist_keys.sort()

    dist_values = [
        [i.get(j,0) for j in dist_keys] for i in dist
    ]

    dist_counts = {}
    for i in dist_values:
        dist_counts[tuple(i)] = dist_values.count(i)

    dist_dict = {
        'states': tuple(dist_keys),
        'counts': dist_counts
    }

    return dist_dict


def _calc_ising_distribution(ising_param):
    """
    _calc_distribution calculates the distribution of Ising model
    """

    ising = Ising(ising_param)
    ising.distribution()
    states = ising.dist.get('states')
    total_states = ising.dist.get('total_states')
    energies = [i.get('energy') for i in states]
    dist = [i.get('dist') for i in states]
    spin_dist = [i.get('spin_dist') for i in states]

    return energies, total_states, _dist_extraction(dist), _dist_extraction(spin_dist)


if __name__ == "__main__":
    ising_param = {
        'width': 3,
        'height': 3
    }

    _calc_ising_distribution(ising_param)

    ising = Ising(ising_param)
    ising.distribution()

    print(
        ising.dist
    )

    import matplotlib.pyplot as plt


    print('End of Game')