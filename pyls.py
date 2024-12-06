import argparse
import json
import time
from typing import List, Dict, Optional


def format_ls_entry(item: Dict, long_format: bool, path: str = "") -> str:
    """Formats a single item for display."""
    if long_format:
        permissions = item.get("permissions", "---------")
        size = item.get("size", 0)
        timestamp = time.strftime(
            "%b %d %H:%M", time.localtime(item.get("time_modified", 0))
        )
        # Ensure proper relative path formatting
        #full_path = f"./{path}/{item['name']}".strip("./")
        if item['name'] in path:
            full_path = f"./{path}".strip("./")
        else:
            full_path = f"./{path}/{item['name']}".strip("./")
        return f"{permissions} {size:>6} {timestamp} {full_path}"
    return item["name"]


def list_directory(
    directory: Dict,
    long_format: bool = False,
    show_all: bool = False,
    recursive: bool = False,
    sort_by_time: bool = False,
    reverse: bool = False,
    filter_type: Optional[str] = None,
    single_line: bool = False,
    path: str = "",
) -> List[str]:
    """Lists the contents of a directory."""
    result = []
    items = directory.get("contents", [])

    if not show_all:
        # Filter out hidden files
        items = [item for item in items if not item["name"].startswith(".")]

    if filter_type == "dir":
        # Show directories only
        items = [item for item in items if "contents" in item]
    elif filter_type == "file":
        # Show files only
        items = [item for item in items if "contents" not in item]

    if sort_by_time:
        items.sort(key=lambda x: x.get("time_modified", 0))

    if reverse and not sort_by_time:
        items.reverse()

    for item in items:
        result.append(format_ls_entry(item, long_format, path))
        # Recursively list contents of directories
        if recursive and "contents" in item:
            subdir_result = list_directory(
                item,
                long_format,
                show_all,
                recursive,
                sort_by_time,
                reverse,
                filter_type,
                path=f"{path}/{item['name']}".strip("/"),
            )
            result.extend(subdir_result)

    if single_line and not long_format:
        return [" ".join(result)]

    return result


def navigate_path(directory: Dict, path: str) -> Optional[Dict]:
    """Navigates the JSON structure based on the path."""
    if path in (".", ""):
        return directory

    parts = path.strip("./").split("/")
    current = directory
    for part in parts:
        if "contents" not in current:
            return None  # Reached a file before finishing navigation
        next_item = next((item for item in current["contents"] if item["name"] == part), None)
        if not next_item:
            return None  # Path not found
        current = next_item

    return current


def load_structure() -> Dict:
    """Loads the default directory structure from a local file."""
    filepath = "structure.json"
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'.")
        exit(1)


def main():
    parser = argparse.ArgumentParser(description="List directory contents from JSON.")
    parser.add_argument(
        "-l", "--long", action="store_true", help="Use a long listing format"
    )
    parser.add_argument(
        "-A",
        "--all",
        action="store_true",
        help="Include all files, including hidden files (starting with '.')",
    )
    parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        help="Recursively list directory contents",
    )
    parser.add_argument(
        "-t",
        "--sort-time",
        action="store_true",
        help="Sort output by time_modified (newest first)",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Reverse the sort order",
    )
    parser.add_argument(
        "--filter",
        choices=["file", "dir"],
        help="Filter results to show only files or directories",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to navigate within the JSON structure (default: current directory)",
    )
    args = parser.parse_args()

    directory = load_structure()
    target = navigate_path(directory, args.path)

    if target is None:
        print(f"error: cannot access '{args.path}': No such file or directory")
        exit(1)

    entries = []
    if "contents" in target:
        # Target is a directory
        entries = list_directory(
            target,
            long_format=args.long,
            show_all=args.all,
            recursive=args.recursive,
            sort_by_time=args.sort_time,
            reverse=args.reverse,
            filter_type=args.filter,
            single_line=not args.long,  # Space-separated output unless -l is used
            path=args.path.strip("/"),
        )
    else:
        # Target is a file
        entries = [format_ls_entry(target, args.long, path=args.path.strip("/"))]

    print("\n".join(entries))


if __name__ == "__main__":
    main()
