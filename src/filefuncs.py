from pathlib import Path

def getFileList(path: str, filterstr: str) -> list:
    """
    Returns a list of files in the specified directory,
    filtered by a substring in the filename.

    Args:
        path: path to the directory (relative or absolute)
        filterstr: substring for filtering filenames

    Returns:
        list: list of file paths as strings
    """
    # Determine the base directory
    if path == '' or path == '.':
        directory = Path('.')
    else:
        directory = Path(path)

    # If the directory does not exist, return an empty list
    if not directory.exists() or not directory.is_dir():
        return []

    # Collect files with filtering
    files = []
    for item in directory.iterdir():
        if item.is_file() and filterstr in item.name:
            # Return relative path relative to the current directory
            # or absolute path if an absolute path was passed
            if path == '' or path == '.':
                # For the current directory, use just the filename
                files.append(item.name)
            else:
                # For relative path, add './' and normalize slashes
                # Use os.path.relpath for correct handling
                import os
                rel_path = os.path.relpath(str(item), start='.')
                # Replace backslashes with forward slashes for consistency
                files.append(rel_path.replace('\\', '/'))

    return files

def getLastDirName(path_name):
    path = Path(path_name)
    last_dir = path.name
    return last_dir

def getRecursiveFileList(dirpath: str,
                         filterstr: str = "*.txt"):
    directory = Path(dirpath)
    files = [str(p) for p in directory.rglob(filterstr) if p.is_file()]
    return files

def getOnlyFileName(path: str):
    file_path = Path(path)
    file_name_without_ext = file_path.stem
    return file_name_without_ext

def getFullPathWithouFilename(fullpathstr: str):
    p = Path(fullpathstr)
    directory = str(p.parent) + '/'   # or str(p.parent) + os.sep
    return directory

def isFileExist(filename):
    if Path(filename).is_file():
        return True
    else:
        return False

def checkDir(dirpath: str,
             createIfNotExist: bool = True):
    dir_path_object = Path(dirpath)
    if not dir_path_object.exists():
        dir_path_object.mkdir()
        print(f"Directory {dirpath} created.")

def savestrtofile(s: str,
                  savefilename: str) -> None:
    with open(savefilename,"wt") as f:
        f.write(s)
    print("File ", savefilename, " successfully saved!")

def test1():
    filename = "/1/2/3/k/filename.txt"
    parentdir = getFullPathWithouFilename(filename)
    print(parentdir)
    print("All tests passed!")

if __name__ == "__main__":
    test1()