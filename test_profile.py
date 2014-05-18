__author__ = 'andrew.sielen'

from system.calculate_inflation import get_inflation_rate

def main():
    set = input("What is the set number?: ")
    print(get_inflation_rate(set, 2014))
    main()


if __name__ == "__main__":
    main()