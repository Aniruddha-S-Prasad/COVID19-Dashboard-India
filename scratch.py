import numpy as np


def generate_matrix(x: np.ndarray, j: int) -> np.ndarray:
    n = x.size - j + 1
    return np.array([x[i:i + j] for i in range(n)])


def main():
    rand = np.arange(8)
    # print(rand[2:4])
    print(generate_matrix(rand, 4))
    return 0


if __name__ == '__main__':
    main()
