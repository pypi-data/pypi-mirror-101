# Knights Tour 0.1.x

A very simple implementation of the knights tour. Intended to create a lot of data work with a little bit of code.

## Installation

Use poetry to install package

```bash
poetry install knightstour-lucasmcgregor
```

## Usage

```python
from knightstour.Chessboard import Chessboard
from knightstour.TourReporter import TourReporter

tours = TourReporter()
board = Chessboard(x_size=8, y_size=8, reporter=tours)
board.solve_board()

print("moves checked: {0}".format(tours.moves))
print("we found {0} tours".format(tours.tours_count))
```

## License
[MIT](https://choosealicense.com/licenses/mit/)