import pytest
import time
from pyls import list_directory, navigate_path, format_ls_entry

# Mock data for testing
MOCK_STRUCTURE = {
    "name": "root",
    "contents": [
        {
            "name": "file1.txt",
            "size": 100,
            "time_modified": 1700205600,
            "permissions": "-rw-r--r--",
        },
        {
            "name": "dir1",
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "file2.txt",
                    "size": 200,
                    "time_modified": 1700205700,
                    "permissions": "-rw-r--r--",
                }
            ],
        },
        {
            "name": ".hidden_file",
            "size": 50,
            "time_modified": 1700205800,
            "permissions": "-rw-r--r--",
        },
    ],
}

def test_navigate_path():
    # Navigate to root
    assert navigate_path(MOCK_STRUCTURE, ".") == MOCK_STRUCTURE

    # Navigate to a directory
    dir1 = navigate_path(MOCK_STRUCTURE, "dir1")
    assert dir1["name"] == "dir1"
    assert len(dir1["contents"]) == 1

    # Navigate to a file
    file2 = navigate_path(MOCK_STRUCTURE, "dir1/file2.txt")
    assert file2["name"] == "file2.txt"

    # Non-existent path
    assert navigate_path(MOCK_STRUCTURE, "nonexistent") is None

def test_format_ls_entry():
    # Test long format
    item = {
        "name": "file.txt",
        "size": 123,
        "time_modified": 1700205600,
        "permissions": "-rw-r--r--",
    }
    timestamp = time.strftime("%b %d %H:%M", time.localtime(1700205600))
    assert (
        format_ls_entry(item, long_format=True)
        == f"-rw-r--r--    123 {timestamp} file.txt"
    )

    # Test short format
    assert format_ls_entry(item, long_format=False) == "file.txt"

def test_list_directory():
    # List root directory
    result = list_directory(MOCK_STRUCTURE, long_format=False, path=".")
    assert result == ["file1.txt", "dir1"]

    # Include hidden files
    result = list_directory(MOCK_STRUCTURE, long_format=False, show_all=True, path=".")
    assert result == ["file1.txt", "dir1", ".hidden_file"]


    # Filter by files only
    result = list_directory(MOCK_STRUCTURE, filter_type="file", path=".")
    assert result == ["file1.txt"]

    # Filter by directories only
    result = list_directory(MOCK_STRUCTURE, filter_type="dir", path=".")
    assert result == ["dir1"]

    # Long format listing
    result = list_directory(MOCK_STRUCTURE, long_format=True, path=".")
    #print (result)
    timestamp1 = time.strftime("%b %d %H:%M", time.localtime(1700205600))
    timestamp2 = time.strftime("%b %d %H:%M", time.localtime(0))
    assert result[0].startswith(f"-rw-r--r--    100 {timestamp1} file1.txt")
    #assert result[0].startswith(f"-rw-r--r--    100 {timestamp1} file1.txt")
    #assert result[1].startswith(f"drwxr-xr-x        0 {timestamp2} dir1")
    #print("Expect Result[1]:", f"drwxr-xr-x        0 {timestamp2} dir1")
    #print("Actual Result[1]:", result[1])
    assert result[1].startswith(f"drwxr-xr-x      0 {timestamp2} dir1")

def test_error_handling():
    # Non-existent file
    assert navigate_path(MOCK_STRUCTURE, "nonexistent") is None

    # Non-existent nested path
    assert navigate_path(MOCK_STRUCTURE, "dir1/nonexistent.txt") is None
