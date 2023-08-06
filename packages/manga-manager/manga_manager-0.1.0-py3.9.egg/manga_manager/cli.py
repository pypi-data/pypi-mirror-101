"""Console script for manga_manager."""
import sys

import manga_manager.manga_manager as mm
from manga_manager.util import argument_parser


def main():
    """Console script for manga_manager."""
    if len(sys.argv) < 2:
        mm.start_menu()
    else:
        parser = argument_parser()
        mm.print_welcome()
        mm.list_manga()

        args = parser.parse_args()
        args.title = " ".join(args.title)
        if args.action == "add":
            mm.add_manga(
                title=args.title,
                provider=eval(f"{args.provider}()"),
                download_mode=args.download_mode,
            )
            mm.save()
        elif args.action == "remove":
            mm.remove_manga(mm.fuzzy_find_title(args.title))
            mm.save()
        elif args.action == "edit":
            mm.edit_manga(mm.fuzzy_find_title(args.title))
            mm.save()
        elif args.action == "read":
            mm.read_manga(
                title=mm.fuzzy_find_title(args.title),
                chapter=int(args.chapters) - 1 if args.chapters else None,
            )
            mm.save()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
