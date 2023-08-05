import sys

from fnvstring.hasher import Fvn64StringHasher as Hash


def main() -> int:
    """Execute command line."""
    args = sys.argv
    command = args[0].split("/")[-1]
    countargs = len(args)

    USG_STR = (
        "Fowler–Noll–Vo hash generator\n\n"
        f"usage: {command} [-h] STRING [SALT]\n\n"
        "(C) 2020 David Vicente Ranz"
    )

    if not 2 <= countargs <= 3:
        print(USG_STR)
        return -1

    if args[1] == "-h":
        print(USG_STR)
        return 0

    string = args[1]
    salt = args[2] if len(args) == 3 else None

    print(Hash.as_base64(string, salt=salt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
