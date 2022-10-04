# this file contains only testing functions and helper functions for testing

# imports needed for testing
import pytest
import asyncio
from aiofile import async_open
from pathlib import Path
from string import ascii_letters, punctuation
from random import choice, randint, sample
from functools import cache

# internal imports
from easyfile.backend import hash_file, _copy_one_file, copy
# END OF IMPORTS

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

# pytest fixtures (helper functions for tests)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """We need only one asyncio loop for all fixtures, because is better to create test files only once."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@cache
@pytest.fixture(scope="session")
async def giga_file(event_looper, tmp_path_factory):
    """This corutine will create one file named test.file.giga in folder files"""
    giga_file_path = tmp_path_factory.mktemp("files") / "test.file.giga"
    char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
    async with async_open(giga_file_path, "wb") as dest:
        # create 1GB file
        await dest.write(char_to_file * (1024 * 1024 * 1024))
    return giga_file_path


@cache
@pytest.fixture(scope="session")
async def hundred_files(event_loop, tmp_path_factory):
    """This corutine will create 100 files with random size and random content, every file named test.file.NUM in folder files"""
    hundred_files_path = tmp_path_factory.mktemp("files")
    for file_number in range(1, 101):
        file_number = str(file_number).zfill(3)
        char_to_file = bytes(choice(ascii_letters + punctuation), 'utf-8')
        async with async_open(hundred_files_path / f"test.file.{file_number}", "wb") as dest:
            # create 100 files of random size to 1MB
            await dest.write(char_to_file * randint(0, 1024 * 1024))
    return hundred_files_path

# thats the end of fixtures

# TESTS


async def test_successful_copy_one_file(hundred_files: Path):
    """Testing function, where we test copy one file and test, if the copied file is same like source file"""
    # src_file = files_path.joinpath(f"test.file.{str(randint(1, 100)).zfill(3)}") # randomly choose one file for copy
    src_file = hundred_files / f"test.file.{str(randint(1, 100)).zfill(3)}"
    dest_file = src_file.with_name(
        str(src_file.name) + "_copied")  # name of destination file
    await _copy_one_file(src_file, dest_file)  # make a copy of file
    src_hash = await hash_file(src_file)  # hash of source file
    dest_hash = await hash_file(dest_file)  # hash of destination file
    # print(src_file, ":", src_hash, "\n", dest_file, ":", dest_hash) # only for visual testing of hashes
    assert src_hash == dest_hash  # hashes have to be same


async def test_copy_one_file_but_dir(hundred_files: Path, tmp_path: Path):
    """Testing function, where we test copy one directory and not file."""
    src_dir = tmp_path / "src_dir"
    src_dir.mkdir()
    dest_file = tmp_path / "some.file"
    with pytest.raises(IsADirectoryError):
        await _copy_one_file(src_dir, dest_file)


async def test_copy_one_non_existent_file(tmp_path: Path):
    """Testing function, where we test copy one non-existent file."""
    src_file = tmp_path / "XXXXXXX"
    dest_file = tmp_path / "XXXXXXX"
    with pytest.raises(FileNotFoundError):
        await _copy_one_file(src_file, dest_file)


async def test_copy_one_file_to_dir_except_of_file(hundred_files: Path, tmp_path: Path):
    """Testing function, where we test copy one file to existing directory except of file."""
    src_file = hundred_files / f"test.file.{str(randint(1, 100)).zfill(3)}"
    dest_file = tmp_path / "XXXXXXX"
    dest_file.mkdir()
    with pytest.raises(IsADirectoryError):
        await _copy_one_file(src_file, dest_file)


async def test_copy_to_existing_file(hundred_files: Path, tmp_path: Path):
    """Testing function, where we test copy to already existing file."""
    src_file = hundred_files / f"test.file.{str(randint(1, 50)).zfill(3)}"
    dest_file = hundred_files / f"test.file.{str(randint(50, 100)).zfill(3)}"
    with pytest.raises(FileExistsError):
        await _copy_one_file(src_file, dest_file)


async def test_copy_file_list(hundred_files):
    """Testing function, where we copy ten random files and test, if the copied files are same like source files"""
    file_list = [
        f"test.file.{str(number).zfill(3)}" for number in sample(range(1, 101), 10)]
    dest_folder = hundred_files / "dest_folder"
    # we need to create that directory, if not exists
    dest_folder.mkdir(parents=True, exist_ok=True)
    await copy([hundred_files / file for file in file_list], dest_folder)
    for file in file_list:
        file_hash_src = await hash_file(hundred_files / file)
        file_hash_dest = await hash_file(dest_folder / file)
        assert file_hash_src == file_hash_dest

# test for hash function
