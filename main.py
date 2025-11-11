import sys
from player_mode import PlayerMode
from algorithm_mode import AlgorithmMode

def main():
    argc = len(sys.argv)
    if argc not in [2, 4]:
        print("Missing command line arguments")
        print("First Usage:  python ./main.py level.csv")
        print("Second Usage: python ./main.py level.csv algorithm duration")
        sys.exit(1)
    level_file = f"levels/{sys.argv[1]}"
    try:
        if argc == 2:
            # * Player mode
            player_mode = PlayerMode(level_file)
            player_mode.run()
        else:
            # * Algorithm mode
            algorithm = sys.argv[2]
            duration = float(sys.argv[3])
            algorithm_mode = AlgorithmMode(level_file, algorithm, duration)
            algorithm_mode.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
