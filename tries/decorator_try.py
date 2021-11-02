from functools import wraps
from pathlib import Path
def path_handler(): # this is the "decorator creator"
    def helper_decorator(decorated_func): # this is returned and is the real decorator, called at function definition time
        @wraps(decorated_func) # sugar
        def new_func(*args, **kwargs): # and this is the function called on execution.
            match kwargs.keys():
                    case ["src_file", "dest_file", *others]:
                        src_file = kwargs["src_file"]
                        dest_file = kwargs["dest_file"]
                        if src_file is not isinstance(Path) and dest_file is not isinstance(Path):
                            raise TypeError("Arguments src_file and dest_file have to by Path instance")
                        if not src_file.is_file():
                            raise FileNotFoundError("Source file not found.")
                        if not dest_file.parent.is_dir(): # dest_file not exists for now, so check only parent folder
                            raise FileExistsError("Destination directory not '{dest_file}' exists.")
                    case ["file_list", "dest_folder", *others]:
                        for file in kwargs["file_list"]:
                            if not file.exists():
                                raise FileNotFoundError(f"{file} not found.")
                        dest_folder = kwargs["dest_folder"]
                        if not dest_folder.is_dir():
                            raise FileExistsError(f"Destination directory '{dest_folder}' not exists.")
            return decorated_func(*args, **kwargs)
        return new_func
    return helper_decorator

