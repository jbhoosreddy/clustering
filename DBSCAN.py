from helper import load_data


INPUT_FILE = 'cho.txt'
CLUSTERS = 5















if __name__ == "__main__":
    epsilon = 1
    min_points = 3
    D = load_data(INPUT_FILE)
    print D