import neat
import os
from main import eval_genomes
from neat.config import Config

# Path to the NEAT configuration file
config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')

def run_neat(config_file):
    # Load configuration for NEAT
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_file
    )

    # Create the population
    population = neat.Population(config)

    # Add reporters to show progress in the console
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    # Run NEAT with the evaluation function defined in `game.py`
    winner = population.run(eval_genomes, 50)

    print(f'\nBest genome:\n{winner}')

if __name__ == "__main__":
    run_neat(config_path)