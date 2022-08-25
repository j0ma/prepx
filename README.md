# prepx

It prepares experiments. :)

## Installation
```bash
pip install -e .
```

## Usage

There are two commands: `analyze` and `create`:

```
Usage: prepx [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  analyze
  create
```

### Analyze
```
Usage: prepx analyze [OPTIONS] FOLDER

Options:
  --help  Show this message and exit.
```

### Create
```
Usage: prepx create [OPTIONS]

Options:
  --experiment-name TEXT     Name of the experiment.
  --train-name TEXT          Name of the model/train run.
  --eval-name TEXT           Name of the eval run.
  --root-folder PATH         Root experiments folder. Defaults to cwd.
  --raw-data-folder PATH     Folder with relevant raw data.
  --checkpoints-folder PATH  Folder with relevant checkpoints.
  --train-folder PATH        Folder of train run if using --eval-only
  --eval-checkpoint FILE     Path to checkpoint if using --eval-only
  --root-only                Only create root of experiment
  --eval-only                Only create eval folder of experiment
  --help                     Show this message and exit.
```
