"""coBib's List command.

This command simply lists the entries in the database:
```
cobib list
```

### Basic Options

It provides some very basic output manipulation options.

You can disable the shortening of the output:
```
cobib list --long
```
You can reverse the output:
```
cobib list --reverse
```
You can sort the list according to a database field:
```
cobib list --sort year
```
(In the TUI, this is available via the `s` key, by default.)


### Filters

However, the arguably most useful feature of this command are the *filters*.
These are a set of keyword arguments which are registered at runtime depending on the fields which
appear in your database.
To give an example, you can find the following filters in the output of `cobib list --help`:
```
++author AUTHOR
--author AUTHOR
++year YEAR
--year YEAR
```
As you can see, each field is used twice: once with a `++` and once with a `--` prefix.
These allow you two specify positive and negative matches, respectively.
For example:
```
cobib list ++year 2020
```
will list *only* entries whose `year` contains `2020`.
On the contrary:
```
cobib list --year 2020
```
will print all those entries whose `year` does *not* contain `2020`.

You can combine multiple filters to narrow your selection down further.
For example:
```
cobib list ++year 2020 ++author Rossmannek
```
will list entries whose `year` contains `2020` *and* whose `author` field contains `Rossmannek`.

Note, that you by default you can use the `f` key in the TUI to add filters to displayed list of
entries.

There are some aspects to take note of here:
1. By default, multiple filters are combined with logical `AND`s. You can specify `--or` to
   overwrite this to logical `OR`s. This will also apply to all filters of the specified command.
2. All entries are treated as `str`. Thus, `++year 20` will match anything *containing* `20`.
"""

from __future__ import annotations

import argparse
import logging
import sys
import textwrap
from collections import defaultdict
from operator import itemgetter
from typing import IO, TYPE_CHECKING, List, Optional

from cobib.database import Database

from .base_command import ArgumentParser, Command

LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from cobib.tui import TUI


class ListCommand(Command):
    """The List Command."""

    name = "list"

    def execute(self, args: List[str], out: IO = None) -> Optional[List[str]]:
        """Lists the entries in the database.

        This command simply lists the labels and titles of the entries in the database.
        By default, it lists them in the order in which they appear in the database.
        However, the order as well as selection of entries to be listed can be configured through
        additional arguments.
        Please refer to the [Filters](#filters) section above for more information.
        Note, that the filtering mechanisms leverages `cobib.database.Entry.matches` to do the
        actual filter-matching.

        Args:
            args: a sequence of additional arguments used for the execution. The following values
                are allowed for this command:
                    * `-l`, `--long`: if specified, the columns of the output table will be not be
                      shortened.
                    * `-r`, `--reverse`: if specified, the entries will be listed in reverse order.
                      This is especially useful in the TUI (where it is enabled by default) because
                      it puts the last added entries at the top of the window. When using the
                      command-line interface it is disabled by default, because this puts the last
                      added entries at the bottom, just above the new command-line prompt.
                    * `-x`, `--or`: if specified, multiple filters will be combined with logical OR
                      rather than the default logical AND.
                    * `-s`, `--sort`: you can specify an arbitrary `cobib.database.Entry.data` field
                      name which should be used for sorting the listed entries. This will
                      automatically include a column for this field in the output table.
                    * in addition to the options above, [Filter keyword arguments](#filters) are
                      registered at runtime based on the fields available in the database. Please
                      refer the that section for more information.
            out: the output IO stream. This defaults to `None`.

        Returns:
            A list with the filtered and sorted labels.
        """
        LOGGER.debug("Starting List command.")
        if "--" in args:
            args.remove("--")
        parser = ArgumentParser(
            prog="list", description="List subcommand parser.", prefix_chars="+-"
        )
        parser.add_argument(
            "-l",
            "--long",
            action="store_true",
            help="print table in long format (i.e. don't shorten lines)",
        )
        parser.add_argument(
            "-r", "--reverse", action="store_true", help="reverses the listing order"
        )
        parser.add_argument("-s", "--sort", help="specify column along which to sort the list")
        parser.add_argument(
            "-x",
            "--or",
            dest="OR",
            action="store_true",
            help="concatenate filters with OR instead of AND",
        )
        unique_keys = set()
        LOGGER.debug("Gathering possible filter arguments.")
        for entry in Database().values():
            unique_keys.update(entry.data.keys())
        for key in sorted(unique_keys):
            parser.add_argument(
                "++" + key, type=str, action="append", help="include elements with matching " + key
            )
            parser.add_argument(
                "--" + key, type=str, action="append", help="exclude elements with matching " + key
            )

        try:
            largs = parser.parse_args(args)
        except argparse.ArgumentError as exc:
            LOGGER.error(exc.message)
            print(exc.message, file=sys.stderr)
            return None

        LOGGER.debug("Constructing filter.")
        _filter = defaultdict(list)
        for key, val in largs.__dict__.items():
            if key in ["OR", "long", "sort", "reverse"] or val is None:
                continue
            if not isinstance(val, list):
                val = [val]
            for i in val:
                for idx, obj in enumerate(args):
                    if i == obj:
                        _filter[tuple([key, args[idx - 1][0] == "+"])].append(i)
                        break
        LOGGER.debug("Final filter configuration: %s", dict(_filter))
        if largs.OR:
            LOGGER.debug("Filters are combined with logical ORs!")

        columns = ["ID", "title"]
        if largs.sort and largs.sort not in columns:
            # insert columns which are sorted by at front of list view
            LOGGER.debug('Sorting by "%s".', largs.sort)
            columns.insert(1, largs.sort)
        # filtered columns are still appended
        columns.extend([arg[0] for arg in _filter.keys() if arg[0] not in columns])
        widths = [0] * len(columns)
        labels = []
        table = []
        for key, entry in Database().items():
            if entry.matches(_filter, largs.OR):
                LOGGER.debug('Entry "%s" matches the filter.', key)
                labels.append(key)
                table.append([entry.data.get(c, "") for c in columns])
                if largs.long:
                    table[-1][1] = table[-1][1]
                else:
                    table[-1][1] = textwrap.shorten(table[-1][1], 80, placeholder="...")
                widths = [max(widths[col], len(table[-1][col])) for col in range(len(widths))]
        LOGGER.debug("Column widths determined to be: %s", widths)
        if largs.sort:
            LOGGER.debug("Sorting table in %s order.", "reverse" if largs.reverse else "normal")
            labels, table = zip(
                *sorted(
                    zip(labels, table),
                    reverse=largs.reverse,
                    key=itemgetter(columns.index(largs.sort)),
                )
            )
        elif largs.reverse:
            # do not sort, but reverse
            LOGGER.debug("Reversing order.")
            labels, table = labels[::-1], table[::-1]
        for row in table:
            print("  ".join([f"{col: <{wid}}" for col, wid in zip(row, widths)]), file=out)
        return list(labels)

    # TODO: refactor this command in order to unify the `tui` method (#66)
    @staticmethod
    def tui(tui: TUI, sort_mode: bool) -> None:  # type: ignore
        """TUI command interface.

        🛑 *WARNING*: this will be refactored in the future, ensuring a unified command syntax with
        the other commands!

        This function serves as the commands entry-point from the `cobib.tui.TUI` instance.
        It should take care of any pre- and/or post-processing before calling `execute` internally
        to do the actual work.

        The processing may involve handling of highlighting as well as general screen buffer
        contents.

        Args:
            tui: the runtime-instance of coBib's TUI.
            sort_mode: a boolean indicating whether the command was triggered from a sorted context.
        """
        LOGGER.debug("List command triggered from TUI.")
        LOGGER.debug("Clearing current buffer contents.")
        tui.viewport.clear()
        # update list prompt arguments
        if sort_mode:
            try:
                sort_arg_idx = tui.STATE.list_args.index("-s")
                LOGGER.debug(
                    'Removing previous sort argument: "%s"', tui.STATE.list_args[sort_arg_idx + 1]
                )
                tui.STATE.list_args.pop(sort_arg_idx + 1)
                tui.STATE.list_args.pop(sort_arg_idx)
            except ValueError:
                pass
            tui.STATE.list_args += ["-s"]
        # handle input via prompt
        command, _ = tui.execute_command(
            "list " + " ".join(tui.STATE.list_args), out=tui.viewport.buffer
        )
        # after the command has been executed n the prompt handler, the `command` variable will
        # contain the contents of the prompt
        LOGGER.debug("Post-process ListCommand arguments for consistent prompt.")
        if command:
            # always ensure the 'reverse' and 'or' keyword arguments are consistent
            if "-r" in command and "-r" not in tui.STATE.list_args:
                LOGGER.debug('Adding "reverse" list argument.')
                tui.STATE.list_args.insert(1, "-r")
            elif "-r" not in command and "-r" in tui.STATE.list_args:
                LOGGER.debug('Removing "reverse" list argument.')
                tui.STATE.list_args.remove("-r")
            if "-x" in command and "-x" not in tui.STATE.list_args:
                LOGGER.debug('Adding "OR" list argument.')
                tui.STATE.list_args.insert(1, "-x")
            elif "-x" not in command and "-x" in tui.STATE.list_args:
                LOGGER.debug('Removing "OR" list argument.')
                tui.STATE.list_args.remove("-x")

            if sort_mode:
                try:
                    sort_arg_idx = command.index("-s")
                    if sort_arg_idx + 1 >= len(command):
                        raise ValueError
                    tui.STATE.list_args += [command[sort_arg_idx + 1]]
                    LOGGER.debug('Using sort argument: "%s"', tui.STATE.list_args[-1])
                except ValueError:
                    tui.STATE.list_args.remove("-s")
            else:
                # first, pop all filters from tui.STATE.list_args
                indices_to_pop = []
                # enumerate words in current list arguments
                prev_args = list(enumerate(tui.STATE.list_args))
                # iterate in reverse to ensure popping indices remain correct after popping a few
                prev_args.reverse()
                for idx, p_arg in prev_args:
                    if p_arg[:2] in ("++", "--"):
                        # matches a filter: current index is type and one larger is the key
                        LOGGER.debug(prev_args)
                        LOGGER.debug(
                            'Removing filter from prompt: "%s"',
                            " ".join(tui.STATE.list_args[idx : idx + 2]),
                        )
                        indices_to_pop.extend([idx + 1, idx])
                for idx in indices_to_pop:
                    tui.STATE.list_args.pop(idx)
                # then, add all new filter (type, key) pairs
                for idx, n_arg in enumerate(command):
                    if n_arg[:2] in ("++", "--"):
                        LOGGER.debug(
                            'Adding filter to prompt: "%s"', " ".join(command[idx : idx + 2])
                        )
                        tui.STATE.list_args.extend(command[idx : idx + 2])
                # reset current line position to top
                tui.STATE.current_line = 0
        # populate buffer with the list
        LOGGER.debug("Populating buffer with ListCommand results.")
        tui.STATE.mode = "list"
        tui.STATE.previous_line = -1
        tui.STATE.inactive_commands = []
        tui.viewport.view()
        # update database list
        tui.viewport.update_list()
