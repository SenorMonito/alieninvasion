import click
from alieninvasion.InvasionSim import InvasionSim

@click.command()
@click.argument("in_file", required=True)
@click.argument("out_file", required=True)
@click.option("--debug", "-d", default=False, type=bool, required=False, help="debug")
@click.option("--aliens", "-N", default=5, type=int, required=False, help="number of aliens")
@click.option("--iterations", "-i", default=10000, type=int, required=False, help="number of iterations")
def cli(in_file: str, out_file: str, debug: bool, aliens: int, iterations: int) -> None:
   game = InvasionSim()
   game.read(in_file)
   game.deploy(aliens)
   print(str(game))
   game.run_sim(iterations)
   game.write(out_file)
   print("Goodbye world!")



if __name__ == "__main__":
   cli()
