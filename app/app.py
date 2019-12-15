from utils.model import Ising
import logging

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)


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

    ising.evolve(beta=1, steps=1000)

    print(
        ising._observe__energy()
    )

    print(
        ising.observables
    )

    print('End of Game')