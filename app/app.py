from utils.model import Ising



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

    print('End of Game')