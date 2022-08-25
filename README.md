# prepx

A library to create experiment folders according to a common schema.

## Schema
- An  *experiment* is a collection of *train* and *eval* runs
- Each train run represents a trained model and has attributes:
    - Checkpoint folder
    - Eval folder
    - Data folder
    - Log folder
- Each eval run represents a model applied to some data:
    - Notably, this includes ones with no associated training runs
    - Covers e.g. applying a pre-trained model on a given dataset
    - Checkpoint folder
    - Eval folder
    - Data folder
    - Log folder

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

### Create

This command supports several scenarios:

#### 1. Create an empty experiment folder

```
prepx create --empty-only \
             --experiment-name <desired-experiment-name> \
             --root-folder <your-desired-root-name>
             --experime
```

Doing this manually is not mandatory.

#### 2. Create a train run under an experiment

- Note: a default eval run will also be created under `eval_<train-name>`

```
prepx create \
    --experiment-name <desired-experiment-name> \
    --root-folder <your-desired-root-name> \
    --train-name <desired-name-of-model> \
    --raw-data-folder <path-to-evaluation-data>
```

#### 3. Only create an eval run under an experiment

```
prepx create \
    --eval-only \
    --experiment-name <desired-experiment-name> \
    --root-folder <your-desired-root-name> \
    --eval-name <desired-eval-name> \
    --eval-checkpoint <path-to-eval-checkpoint> \
    --raw-data-folder <path-to-evaluation-data>
```

Overall help:

```
Usage: prepx create [OPTIONS]

Options:
  --experiment-name TEXT     Name of the experiment.
  --train-name TEXT          Name of the model/train run.
  --eval-name TEXT           Name of the eval run.
  --root-folder PATH         Root experiments folder. Defaults to cwd.
  --raw-data-folder PATH     Folder with relevant raw data.
  --checkpoints-folder PATH  Folder with relevant checkpoints.
  --eval-checkpoint FILE     Path to checkpoint if using --eval-only
  --empty-only               Only create empty experiment folder
  --eval-only                Only create eval folder of experiment
  --help                     Show this message and exit.
```

### Analyze
```
Usage: prepx analyze [OPTIONS] FOLDER

Options:
  --help  Show this message and exit.
```
