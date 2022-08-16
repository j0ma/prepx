#!/usr/bin/env python

from pathlib import Path
import subprocess as sp

import click
from rich import print as pprint
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
    "--checkpoints-folder",
    type=click.Path(dir_okay=True, path_type=Path),
    help="Folder with relevant checkpoints.",
)
@click.option(
    "--train-folder",
    type=click.Path(dir_okay=True, path_type=Path),
    help="Folder of train run if using --eval-only",
)
@click.option(
    "--eval-checkpoint",
    type=click.Path(file_okay=True, dir_okay=False, exists=True, path_type=Path),
    help="Path to checkpoint if using --eval-only",
)
@click.option("--root-only", is_flag=True, help="Only create root of experiment")
@click.option("--eval-only", is_flag=True, help="Only create eval folder of experiment")
def create_experiment(
    experiment_name,
    train_name,
    eval_name,
    root_folder,
    raw_data_folder,
    checkpoints_folder,
    train_folder,
    eval_checkpoint,
    root_only,
    eval_only,
) -> None:

    root_folder = root_folder.resolve()
    raw_data_folder = raw_data_folder.resolve()

    if checkpoints_folder:
        checkpoints_folder = checkpoints_folder.resolve()

    if train_folder:
        train_folder = train_folder.resolve()

    if eval_checkpoint:
        eval_checkpoint = eval_checkpoint.resolve()

    ef = exp.ExperimentFolder(
        experiment_name=experiment_name,
        root_folder=root_folder,
    )

    root = ef.create_root(return_path=True)

    if root_only:
        print(f"Path to created experiment: {str(root)}")

        return
    elif eval_only:
        assert (
            train_folder is not None
        ), "If using --eval-only, the --train-folder argument is mandatory."
        ef.create_eval(
            eval_name=eval_name,
            checkpoint=eval_checkpoint,
            raw_data_folder=raw_data_folder,
            train_folder=train_folder,
        )
    else:
        ef.create_train(
            train_name=train_name,
            checkpoint_folder=checkpoints_folder,
            raw_data_folder=raw_data_folder,
        )

    print(f"Path to created experiment: {str(root)}")


@cli.command("analyze")
@click.argument(
    "folder",
    type=click.Path(dir_okay=True, path_type=Path),
    nargs=1,
)
def analyze_experiment(folder, *args, **kwargs) -> None:

    args_ = ["tree", str(folder)]
    pid = sp.run(args_, capture_output=True)
    pprint(pid.stdout.decode("utf-8"))


if __name__ == "__main__":
    cli()
