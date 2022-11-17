from typing import Optional, List
from pathlib import Path

from attr import define, field
from rich import print


@define
class TrainFolder:

    # Every train folder needs these
    name: str = field()
    path: Path = field()
    raw_data_folder: Path = field()
    parent: "ExperimentFolder" = field(repr=False)
    binarized_data_folder: Optional[Path] = field(default=None)
    with_tensorboard: bool = field(default=False)

    # These can optionally be set. The default behavior is:
    # 1) checkpoint folder is symlinked to it exists, else created here using
    # default template 2) eval folder is symlinked to if it exists, else
    # created in parent using default template
    checkpoint_folder: Optional[Path] = field(default=None)
    eval_folder: Optional[Path] = field(default=None)

    # Templates for raw data, checkpoint and eval folder names
    default_raw_data_template = field(default="raw_data", repr=False)
    default_binarized_data_template = field(default="binarized_data", repr=False)
    default_checkpoint_folder_template = field(default="checkpoints", repr=False)
    default_checkpoint_template = field(default="checkpoint_best.pt", repr=False)
    default_eval_template = field(default="eval_{}", repr=False)
    default_tensorboard_folder_template = field(default="tensorboard", repr=False)

    raw_data_link: Optional[Path] = field(default=None)
    binarized_data_link: Optional[Path] = field(default=None)
    checkpoint_link: Optional[Path] = field(default=None)
    checkpoint_best_link: Optional[Path] = field(default=None)
    eval_link: Optional[Path] = field(default=None)
    tensorboard_link: Optional[Path] = field(default=None)

    def __attrs_post_init__(self):
        self.raw_data_link: Path = Path(self.path / self.default_raw_data_template)
        self.binarized_data_link: Path = Path(
            self.path / self.default_binarized_data_template
        )
        self.checkpoint_link: Path = Path(
            self.path / self.default_checkpoint_folder_template
        )
        self.checkpoint_best_link = (
            self.checkpoint_link / self.default_checkpoint_template
        )
        self.tensorboard_link: Path = Path(
            self.path / self.default_tensorboard_folder_template
        )

    def create(self):

        if not self.path.exists():
            self.path.mkdir(parents=True)

        # Raw data
        print(f"Linking: {self.raw_data_link} -> {self.raw_data_folder}")
        self.raw_data_link.symlink_to(self.raw_data_folder)

        # Bin data if given

        if self.binarized_data_folder:
            print(
                f"Linking: {self.binarized_data_link} -> {self.binarized_data_folder}"
            )
            self.binarized_data_link.symlink_to(self.binarized_data_folder)

        # Checkpoints

        if self.checkpoint_folder:
            print(f"Linking: {self.checkpoint_link} -> {self.checkpoint_folder}")
            self.checkpoint_link.symlink_to(self.checkpoint_folder)
        else:
            print(f"Creating non-existent checkpoint folder:\n{self.checkpoint_link}")
            self.checkpoint_link.mkdir(parents=True, exist_ok=True)

        if self.with_tensorboard:
            print(f"Creating non-existent tensorboard folder:\n{self.tensorboard_link}")
            self.tensorboard_link.mkdir(parents=True, exist_ok=True)

        # Evaluation
        default_eval_name = self.default_eval_template.format(self.name)
        self.eval_link = Path(self.path / "eval")

        if self.eval_folder is None or not self.eval_folder.exists():
            self.eval_folder = self.parent.create_eval(
                name=default_eval_name,
                checkpoint=self.checkpoint_best_link,
                raw_data_folder=self.raw_data_link,
                binarized_data_folder=self.binarized_data_link,
                return_path=True,
            )
        print(f"Linking: {self.eval_link} -> {self.eval_folder}")
        self.eval_link.symlink_to(self.eval_folder)


@define
class EvalFolder:

    # Every eval folder needs these
    name: str = field()
    path: Path = field()
    checkpoint: Path = field()
    raw_data_folder: Path = field()
    parent: "ExperimentFolder" = field(repr=False)
    binarized_data_folder: Optional[Path] = field(default=None)

    # This can optionally be set.
    train_folder: Optional[Path] = field(default=None)

    # Templates for raw data, checkpoint and eval folder names
    default_raw_data_template = field(default="raw_data", repr=False)
    default_binarized_data_template = field(default="binarized_data", repr=False)
    default_checkpoint_template = field(default="checkpoint", repr=False)
    default_train_template = field(default="train", repr=False)

    raw_data_link: Optional[Path] = field(default=None)
    binarized_data_link: Optional[Path] = field(default=None)
    checkpoint_link: Optional[Path] = field(default=None)
    train_link: Optional[Path] = field(default=None)

    def __attrs_post_init__(self):
        self.raw_data_link: Path = Path(self.path / self.default_raw_data_template)
        self.binarized_data_link: Path = Path(
            self.path / self.default_binarized_data_template
        )
        self.checkpoint_link: Path = Path(self.path / self.default_checkpoint_template)

    def create(self):

        if not self.path.exists():
            self.path.mkdir(parents=True)

        # Create checkpoint folder
        print(f"Linking: {self.checkpoint_link} -> {self.checkpoint}")
        self.checkpoint_link.symlink_to(self.checkpoint)

        # Link to raw data folder
        print(f"Linking: {self.raw_data_link} -> {self.raw_data_folder}")
        self.raw_data_link.symlink_to(self.raw_data_folder)

        # Link to binarized data folder if given (e.g. when working with fairseq)

        if (
            self.binarized_data_folder is not None
            and self.binarized_data_folder.resolve().exists()
        ):
            print(
                f"Linking: {self.binarized_data_link} -> {self.binarized_data_folder}"
            )
            self.binarized_data_link.symlink_to(self.binarized_data_folder)


@define
class ExperimentFolder:

    experiment_name: str

    # Root folder, e.g. "experiments" with all experiment folders inside it.
    root_folder: Optional[str] = field(default=None, repr=False)

    # Name for train/eval folders
    train_root_folder_name: str = field(repr=False, default="train")
    eval_root_folder_name: str = field(repr=False, default="eval")

    # Full path placeholder
    full_path: Optional[Path] = None

    with_tensorboard: bool = field(default=False)

    def __attrs_post_init__(self):

        if not self.root_folder:

            # Default to working directory
            self.root_folder = Path.cwd()

        self.root_folder = Path(self.root_folder)

        self.full_path = self.root_folder / self.experiment_name

    @property
    def train_root_folder(self) -> Path:
        return self.full_path / self.train_root_folder_name

    @property
    def eval_root_folder(self) -> Path:
        return self.full_path / self.eval_root_folder_name

    @property
    def trains(self) -> List[str]:
        return [f.name for f in self.train_root_folder.glob("*")]

    def create_root(self, return_path: bool = False) -> Optional[Path]:
        self.full_path.mkdir(parents=True, exist_ok=True)

        if return_path:
            return self.full_path

    def create_train(
        self,
        name: str,
        checkpoint_folder: Path,
        raw_data_folder: Path,
        binarized_data_folder: Optional[Path],
        return_path: bool = False,
        with_tensorboard: bool = True,
    ) -> Optional[Path]:

        if name in self.trains:
            raise FileExistsError(f"A train folder named '{name}' already exists!")

        root = self.train_root_folder / name

        train_folder = TrainFolder(
            parent=self,
            path=root,
            name=name,
            checkpoint_folder=checkpoint_folder,
            raw_data_folder=raw_data_folder,
            binarized_data_folder=binarized_data_folder,
            with_tensorboard=with_tensorboard,
        )

        train_folder.create()

        if return_path:
            return root

    def create_eval(
        self,
        name: str,
        checkpoint: Path,
        raw_data_folder: Path,
        binarized_data_folder: Optional[Path] = None,
        return_path: bool = False,
        *args, **kwargs
    ) -> Optional[Path]:

        root = self.eval_root_folder / name

        eval_folder = EvalFolder(
            name=name,
            parent=self,
            path=root,
            checkpoint=checkpoint,
            raw_data_folder=raw_data_folder,
            binarized_data_folder=binarized_data_folder,
            train_folder=None,
        )

        eval_folder.create()

        if return_path:
            return root
