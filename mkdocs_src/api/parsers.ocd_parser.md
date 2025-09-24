# Module `parsers.ocd_parser`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

Raises:
    OSError: If directory cannot be created.

### `run(storage_path: str | pathlib.Path, config: dict) -> str`

Clone or update the OCD Divisions repository.

If the repository does not exist locally in the given storage path, it will be cloned.
If it already exists, it will pull latest changes from remote.

Args:
    storage_path (str | Path): Local storage path for this polling run.
    config (dict): Loaded configuration containing 'ocd_repo_url'.

Returns:
    str: Status message confirming repository update.
