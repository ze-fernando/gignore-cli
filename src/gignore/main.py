from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path

from rich.prompt import Prompt

from gignore.utils import *


def create_parser() -> tuple[ArgumentParser, Namespace]:
    parser = ArgumentParser(
        prog="gignore",
        description="Generate a .gitignore file based on templates from donotcommit.com",
        epilog=("Examples:\n  gignore python,node\n  gignore -f python,node\n"),
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "templates",
        help="Comma-separated .gitignore templates. Ex: python,linux,vscode",
        nargs="?",
    )

    parser.add_argument(
        "-l", "--list", help="List available .gitignore templates", action="store_true"
    )

    parser.add_argument("-f", "--find", help="Search available .gitignore templates")

    parser.add_argument(
        "-o",
        "--override",
        help="Force overwrite of the .gitignore file",
        action="store_true",
    )

    parser.add_argument(
        "-p", "--path", help="Set the destination directory for the .gitignore file"
    )

    return parser, parser.parse_args()


def main() -> None:
    parser, args = create_parser()

    if args.list:
        content = get_templates()
        console.print(content)
    elif args.find:
        content = find_templates(args.find.split(","))  # type: ignore[assignment]
        console.print(content)
    elif args.templates:
        path = Path().cwd() / ".gitignore"
        content = get_data(args.templates)

        if args.path:
            path = Path(args.path) / ".gitignore"

        if not args.override and path.exists():
            choice = Prompt.ask(
                "A .gitignore file already exists at the current path. Do you want to add the new templates to it?\nUse -o or --override to overwrite it instead.",
                choices=["y", "n"],
                default="y",
            )
            match choice:
                case "y":
                    edit_file(content, path)
                    return
                case "n":
                    return

        create_file(content, path)

    else:
        parser.print_help()


# def run() -> None:
#     asyncio.run(main())


if __name__ == "__main__":
    main()
