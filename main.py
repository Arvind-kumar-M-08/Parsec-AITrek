"""This specially named module makes the package runnable."""

from ViewController import ViewController
from models.Environement import Environment


def main() -> None:
    """Entrypoint of simulation."""
    model = Environment()
    vc = ViewController(model)
    vc.start_simulation()


if __name__ == "__main__":
    main()
