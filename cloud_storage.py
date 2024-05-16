from abc import ABC




class CloudStorage(ABC):
    """
    `CloudStorage` interface.
    """


    def add_file(self, name: str, size: int) -> bool:
        """
        Should add a new file `name` to the storage.
        `size` is the amount of memory required in bytes.
        The current operation fails if a file with the same `name`
        already exists.
        Returns `True` if the file was added successfully or `False`
        otherwise.
        """
        # default implementation
        return False


    def copy_file(self, name_from: str, name_to: str) -> bool:
        """
        Should copy the file at `name_from` to `name_to`.
        The operation fails if `name_from` points to a file that
        does not exist or points to a directory.
        The operation fails if the specified file already exists at
        `name_to`.
        Returns `True` if the file was copied successfully or
        `False` otherwise.
        """
        # default implementation
        return False


    def get_file_size(self, name: str) -> int | None:
        """
        Should return the size of the file `name` if it exists, or
        `None` otherwise.
        """
        # default implementation
        return None
