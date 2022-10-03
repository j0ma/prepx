#!/usr/bin/env python

from pathlib import Path
import subprocess as sp

import click
from rich import print as pprint
from rich.tree import Tree
import prepx.experiment as exp

TMP = Path("/tmp")
STAGING = TMP / "staging"


def create_random_checkpoint_folder() -> None:
    raise NotImplementedError


@click.group()
def cli():
    pass


@cli.command("create")
@click.option("--experiment-name", help="Name of the experiment.")
@click.option("--train-name", help="Name of the model/train run.")
@click.option("--eval-name", help="Name of the eval run.")
@click.option(
    "--root-folder",
    type=click.Path(dir_okay=True, path_type=Path),
    help="Root experiments folder. Defaults to cwd.",
)
@click.option(
    "--raw-data-folder",
    type=click.Path(dir_okay=True, path_type=Path),
    help="Folder with relevant raw data.",
)
@click.option(
    "--binarized-data-folder",
    type=click.Path(dir_okay=True, path_type=Path),
    help="Folder with relevant binarized data.",
)
@click.option(
    "--checkpoints-folder",
    type=click.Path(dir_okay=True, path_type=Path),
    help="Folder with relevant checkpoints.",
)
@click.option(
    "--eval-checkpoint",
    type=click.Path(file_okay=True, dir_okay=False, exists=True, path_type=Path),
    help="Path to checkpoint if using --eval-only",
)
@click.option("--empty-only", is_flag=True, help="Only create empty experiment folder")
@click.option("--eval-only", is_flag=True, help="Only create eval folder of experiment")
def create_experiment(
    experiment_name,
    train_name,
    eval_name,
    root_folder,
    raw_data_folder,
    binarized_data_folder,
    checkpoints_folder,
    eval_checkpoint,
    empty_only,
    eval_only,
) -> None:

    root_folder = root_folder.resolve()
    raw_data_folder = raw_data_folder.resolve()
    if binarized_data_folder:
        binarized_data_folder = binarized_data_folder.resolve()

    if checkpoints_folder:
        checkpoints_folder = checkpoints_folder.resolve()

    if eval_checkpoint:
        eval_checkpoint = eval_checkpoint.resolve()

    ef = exp.ExperimentFolder(
        experiment_name=experiment_name,
        root_folder=root_folder,
    )

    root = ef.create_root(return_path=True)

    if not empty_only:
        create = ef.create_eval if eval_only else ef.create_train
        checkpoint_key = "checkpoint" if eval_only else "checkpoint_folder"
        checkpoint_value = eval_checkpoint if eval_only else checkpoints_folder

        args = {
            checkpoint_key: checkpoint_value,
            "name": eval_name if eval_only else train_name,
            "raw_data_folder": raw_data_folder,
            "binarized_data_folder": binarized_data_folder
        }

        create(**args)

    print(f"Path to created experiment: {str(root)}")


def traverse_path(path, tree=None, current_level=0, max_level=None):
    tree = tree or Tree(str(path))
    should_expand = max_level is None or current_level < max_level

    if should_expand:
        for child in path.glob("*"):

            # Recursively expand all directories

            if child.is_symlink():
                tree.add(f"{str(child.name)} -> {str(child.resolve())}")
            elif child.is_dir():
                st = tree.add(str(child.name))
                traverse_path(
                    child, st, current_level=current_level + 1, max_level=max_level
                )
            else:
                tree.add(str(child.name))

    return tree


@cli.command("analyze")
@click.option(
    "--max-level",
    help="Maximum number of levels to descend in directory hierarchy.",
    type=int,
)
@click.argument(
    "folder",
    type=click.Path(dir_okay=True, path_type=Path),
    nargs=1,
)
def analyze_experiment(max_level, folder, *args, **kwargs) -> None:

    tree = traverse_path(folder, max_level=max_level)
    pprint(tree)


if __name__ == "__main__":
    cli()
