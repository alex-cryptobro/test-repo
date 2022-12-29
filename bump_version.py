import re
from sys import argv

import tomli


VERSION_REGEX = re.compile(r"^\d+\.\d+[.\d]*?$")


def get_current_version():
    with open("pyproject.toml", mode="rb") as pyproject:
        return tomli.load(pyproject).get("tool", {}).get("poetry", {}).get("version", "0.0.0")


if __name__ == '__main__':
    if len(argv) < 2:
        print("Error: bump action required (major, minor, patch)")
        exit(1)
    if argv[1] not in ['major', 'minor', 'patch']:
        print("Error: unknown bump action passed. Allowed: major, minor, patch")
        exit(1)

    current_version = get_current_version()
    if not re.match(VERSION_REGEX, current_version):
        print("Error: incorrect version format. Expected [0-9]+.[0-9]+.[0-9]*?")
        exit(1)

    current_version_split = current_version.split(".")
    if len(current_version_split) < 3:
        current_version_split.append("0")
    current_version_prepared = ".".join(current_version_split)

    new_version_split = current_version_split.copy()
    if argv[1] == 'major':
        new_version_split[0] = str(int(new_version_split[0]) + 1)
        new_version_split[1] = "0"
        new_version_split[2] = "0"
    if argv[1] == "minor":
        new_version_split[1] = str(int(new_version_split[1]) + 1)
        new_version_split[2] = "0"
    if argv[1] == "patch":
        new_version_split[2] = str(int(new_version_split[2]) + 1)
    new_version = ".".join(new_version_split)

    print(f"Current version = {current_version_prepared}")
    print(f"Action = {argv[1]}")
    print(f"New version = {new_version}")
