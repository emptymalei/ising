from utils.model import Ising
import logging

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)



if __name__ == "__main__":
    ising_param = {
        'width': 3,
        'height': 3
    }

    ising = Ising(ising_param)
    ising.distribution()

    print(
        ising.dist
    )

    import matplotlib.pyplot as plt


    print('End of Game')