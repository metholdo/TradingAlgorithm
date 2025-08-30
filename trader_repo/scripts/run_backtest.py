
import argparse
from trader.__main__ import backtest_run

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", default="sma_crossover")
    args = parser.parse_args()
    backtest_run(strategy=args.strategy)
