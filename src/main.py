from nhl import NHL
from espn import ESPN


def main():
    for game in NHL().get_games():
        print(game)

    print()

    for game in ESPN().get_games():
        print(game)


if __name__ == "__main__":
    main()
