# this file contains only testing functions and helper functions for testing

# imports needed for testing
import pytest
import asyncio
from anyio import Path
from anyio.streams.file import FileWriteStream
from string import ascii_letters, punctuation
from random import choice, randint, sample
from functools import cache
from os import walk

# internal imports
from easyfile.backend import EasyFile, hash_file, PathNotFoundError
# END OF IMPORTS

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.anyio

# pytest fixtures (helper functions for tests)

@pytest.fixture(scope='module')
def anyio_backend():
    return 'asyncio'

@pytest.fixture()
def ef():
    return EasyFile()

# @pytest.fixture(scope="session", autouse=True)
# def event_loop():
#     """We need only one asyncio loop for all fixtures, because is better to create test files only once."""
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


@cache
@pytest.fixture(scope="module")
async def giga_file(tmp_path_factory):
    """This corutine will create one file named test.file.giga in folder files"""
    giga_file_path = Path(tmp_path_factory.mktemp("files") / "test.file.giga")
    char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
    async with await FileWriteStream.from_path(giga_file_path) as dest:
        # create 1GB file
        await dest.send(char_to_file * (1024 * 1024 * 1024))
    return giga_file_path


@cache
@pytest.fixture(scope="module")
async def hundred_files(tmp_path_factory):
    """This corutine will create 100 files with random size and random content, every file named test.file.NUM in folder files"""
    hundred_files_path = Path(tmp_path_factory.mktemp("files"))
    # create 100 files of random size to 1MB
    for file_number in range(1, 101):
        file_number = str(file_number).zfill(3)
        char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
        async with await FileWriteStream.from_path(hundred_files_path / f"test.file.{file_number}") as dest:
            await dest.send(char_to_file * randint(0, 1024 * 1024))
    return hundred_files_path

@cache
@pytest.fixture()
async def atmp_path(tmp_path):
    return Path(tmp_path)

# thats the end of fixtures

# TESTS

async def test_successful_copy_one_file(ef, hundred_files: Path, atmp_path: Path):
    """Testing function, where we test copy one file and test, if the copied file is same like source file"""
    src_file = hundred_files / f"test.file.{str(randint(1, 100)).zfill(3)}"
    dest_file = atmp_path / src_file.with_name(
        src_file.name + "_copied").name  # name of destination file
    await ef._copy_one_file(src_file, dest_file)  # make a copy of file
    src_hash = await hash_file(src_file)  # hash of source file
    dest_hash = await hash_file(dest_file)  # hash of destination file
    # print(src_file, ":", src_hash, "\n", dest_file, ":", dest_hash) # only for visual testing of hashes
    assert src_hash == dest_hash  # hashes have to be same


@pytest.mark.skip(reason="it takes a few second more ...")
async def test_successful_copy_giga_file(ef, giga_file: Path, atmp_path: Path):
    """Testing function, where we test copy one big file with size 1GB and test, if the copied file is same like source file."""
    dest_file = atmp_path / giga_file.with_name(
        giga_file.name + "_copied").name  # name of destination file
    await ef._copy_one_file(giga_file, dest_file)  # make a copy of file
    src_hash = await hash_file(giga_file)  # hash of source file
    dest_hash = await hash_file(dest_file)  # hash of destination file
    # print(src_file, ":", src_hash, "\n", dest_file, ":", dest_hash) # only for visual testing of hashes
    assert src_hash == dest_hash  # hashes have to be same


async def test_copy_one_file_but_dir(ef, hundred_files: Path, atmp_path: Path):
    """Testing function, where we test copy one directory and not file."""
    src_dir = atmp_path / "src_dir"
    await src_dir.mkdir()
    dest_file = atmp_path / "some.file"
    with pytest.raises(IsADirectoryError):
        await ef._copy_one_file(src_dir, dest_file)


async def test_copy_one_non_existent_file(ef, atmp_path: Path):
    """Testing function, where we test copy one non-existent file."""
    src_file = atmp_path / "XXXXXXX"
    dest_file = atmp_path / "XXXXXXX_copied"
    with pytest.raises(FileNotFoundError):
        await ef._copy_one_file(src_file, dest_file)


async def test_copy_one_file_to_dir_except_of_file(ef, hundred_files: Path, atmp_path: Path):
    """Testing function, where we test copy one file to existing directory except of file."""
    src_file = hundred_files / f"test.file.{str(randint(1, 100)).zfill(3)}"
    dest_file = atmp_path / "XXXXXXX"
    await dest_file.mkdir()
    with pytest.raises(IsADirectoryError):
        await ef._copy_one_file(src_file, dest_file)


async def test_copy_to_existing_file(ef, hundred_files: Path, atmp_path: Path):
    """Testing function, where we test copy to already existing file."""
    src_file = hundred_files / f"test.file.{str(randint(1, 50)).zfill(3)}"
    dest_file = hundred_files / f"test.file.{str(randint(50, 100)).zfill(3)}"
    with pytest.raises(FileExistsError):
        await ef._copy_one_file(src_file, dest_file)


async def test_copy_non_existent_path(ef, atmp_path: Path):
    src_path = atmp_path / "src_path"
    dest_path = atmp_path / "dest_folder"
    await dest_path.mkdir(exist_ok=True)
    with pytest.raises(PathNotFoundError, match="src path has to exist!"):
        await ef._copy_path(src_path, dest_path)


async def test_copy_to_non_existent_path(ef, atmp_path: Path):
    src_path = atmp_path / "XXXXXXX"
    await src_path.mkdir(exist_ok=True)
    dest_path = atmp_path / "dest_folder"
    with pytest.raises(PathNotFoundError, match="dest path has to exist!"):
        await ef._copy_path(src_path, dest_path)


async def test_copy_only_files_in_list(ef, hundred_files: Path, atmp_path: Path):
    """Testing function, where we copy ten random files and test, if the copied files are same like source files"""
    file_list = [
        f"test.file.{str(number).zfill(3)}" for number in sample(range(1, 101), 10)]
    dest_folder = atmp_path / "dest_folder"
    # we need to create that directory, if not exists
    await dest_folder.mkdir(parents=True, exist_ok=True)
    await ef.copy([hundred_files / file for file in file_list], dest_folder)
    for file in file_list:
        file_hash_src = await hash_file(hundred_files / file)
        file_hash_dest = await hash_file(dest_folder / file)
        assert file_hash_src == file_hash_dest


async def test_copy_files_and_dirs_in_list(ef, hundred_files: Path, atmp_path: Path):
    """Testing function, where we copy random files and dirs and test, if the copied files and dirs are same like source files"""
    folder_to_copy = atmp_path / "folder_to_copy"
    folder1 = folder_to_copy / "src_folder1"
    subfolder1 = folder1 / "src_subfolder1"
    subsubfolder = subfolder1 / "subsubfolder"
    folder2 = folder_to_copy / "src_folder2"
    subfolder2 = folder2 / "src_subfolder2"
    await subsubfolder.mkdir(parents=True, exist_ok=True)
    await subfolder2.mkdir(parents=True, exist_ok=True)
    folders = [folder_to_copy, folder1, subfolder1, folder2, subfolder2, subsubfolder]
    file_list = sample([path async for path in hundred_files.iterdir()], 20)
    dest_folder = atmp_path / "dest_folder"
    await dest_folder.mkdir(parents=True, exist_ok=True)
    for file in file_list:
        # copy random files to random folders
        await ef._copy_one_file(file, choice(folders) / file.name)
    await ef.copy([folder_to_copy], dest_folder)
    for src_walk_output, dest_walk_output in zip(walk(folder_to_copy), walk(dest_folder / folder_to_copy)):
        src_dirpath, src_dirnames, src_filenames = src_walk_output
        dest_dirpath, dest_dirnames, dest_filenames = dest_walk_output
        assert src_dirpath == dest_dirpath
        for src_dirname, des_dirname in zip(src_dirnames, dest_dirnames):
            assert src_dirname == des_dirname
        for src_filename, des_filename in zip(src_filenames, dest_filenames):
            assert src_filename == des_filename


async def test_copy_empty_file_list(ef, atmp_path: Path):
    file_list = []
    with pytest.raises(ValueError):
        await ef.copy(file_list, atmp_path)


async def test_copy_list_with_no_paths_or_strings(ef, atmp_path: Path):
    file_list = [1,2,3]
    with pytest.raises(TypeError):
        await ef.copy(file_list, atmp_path)


async def test_copy_list_of_strings(ef, hundred_files: Path, atmp_path: Path):
    file_list = sample([path async for path in hundred_files.iterdir()], 3)
    str_file_list = [str(file) for file in file_list]
    dest_folder = atmp_path / "dest_folder"
    await dest_folder.mkdir(parents=True, exist_ok=True)
    str_dest_folder = str(dest_folder)
    await ef.copy(str_file_list, str_dest_folder)
    for file in file_list:
        assert await (dest_folder / file.name).exists()



# test for hash function
