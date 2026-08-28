from pathlib import Path

def getFileList(path: str,
                filterstr: str) -> list:
    if path == '' or path == '.':
        files = [f for f in Path('.').iterdir() if f.is_file() and filterstr in f.name]
    else:
        directory = Path(path)
        files = ["./"+str(g).replace('\\','/') for g in directory.iterdir() if g.is_file() and filterstr in getOnlyFileName(str(g))]
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
    directory = str(p.parent) + '/'   # или str(p.parent) + os.sep
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
        print(f"Директория {dirpath} создана.")
    

def savestrtofile(s: str,
                  savefilename: str) -> None:
    with open(savefilename,"wt") as f:
        f.write(s)
    print("Файл ",savefilename, " успешно сохранён!")


def test1():
    filename = "/1/2/3/k/filename.txt"
    parentdir = getFullPathWithouFilename(filename)
    print(parentdir)
    print("Все проверки успешны!")

if __name__ == "__main__":
    test1()