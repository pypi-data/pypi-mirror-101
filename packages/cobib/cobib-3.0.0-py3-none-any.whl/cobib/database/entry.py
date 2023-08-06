"""coBib's Entry class."""

from __future__ import annotations

import logging
import os
import re
import subprocess
from typing import IO, TYPE_CHECKING, Any, Dict, List, Tuple, Type, Union, cast

from pylatexenc.latexencode import UnicodeToLatexEncoder

from cobib.config import config

LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    # The type annotation introduces a cyclic import dependency between the Parser and Entry classes
    from cobib.parsers.base_parser import Parser


class Entry:
    """coBib's bibliographic entry.

    coBib's `Database` stores the bibliographic information in entries which are instances of this
    class. This only contains a `label` which is a string used as a key to associate this entry as
    well as a free-form `data` dictionary, which can contain arbitrary key-value pairs.
    Two fields will *always* be present in the `data` dictionary:
    * `ID`: which must match the `label` of the entry.
    * `ENTRYTYPE`: which specifies the BibLaTex type of the entry.

    Only through the context imposed by BibLaTex will the other `data` fields be interpreted.

    However, some keys are exposed as properties in a special format to provide easy access to these
    meta-data fields not typically used by BibLaTex itself.

    Besides being a data container, this class also provides some utilities for data manipulation
    and querying.
    """

    def __init__(self, label: str, data: Dict[str, Any]) -> None:
        """Initializes a new Entry.

        Args:
            label: the ID associated with this entry in the `Database`.
            data: the actual bibliographic data stored as a dictionary mapping free-form field names
                (`str`) to any other data. Some fields are exposed as properties of this class for
                convenience.
        """
        label = str(label)

        LOGGER.debug("Initializing entry: %s", label)

        self._label: str = label

        self.data: Dict[str, Any] = data.copy()
        """The actual bibliographic data."""

        if self.data["ID"] != self._label:
            # sanity check for matching label and ID
            LOGGER.warning(
                "Mismatching label '%s' and ID '%s'. Overwriting ID with label.",
                self._label,
                self.data["ID"],
            )
            self.label = self._label

    def __eq__(self, other: object) -> bool:
        """Checks equality of two entries."""
        if not isinstance(other, Entry):
            return False
        return self.label == other.label and self.data == other.data

    @property
    def label(self) -> str:
        """The `Database` ID of this entry.

        The setter of this property also ensures that the `Entry.label` and `Entry.data["ID"]`
        fields are consistent.
        """
        return self._label

    @label.setter
    def label(self, label: str) -> None:
        """Sets the `Database` ID of this entry.

        Args:
            label: the ID of this entry. This property setter also ensures that the `Entry.label`
                and `Entry.data["ID"]` fields are consistent.
        """
        LOGGER.debug("Changing the label '%s' to '%s'.", self.label, label)
        self._label = label
        LOGGER.debug("Changing the ID '%s' to '%s'.", self.data["ID"], label)
        self.data["ID"] = label

    @property
    def tags(self) -> str:
        """The tags of this entry.

        The setter of this property will strip `+` symbols from the tags as these are an artifact of
        the command-line syntax. Internally, the list of tags is stored as a comma-separated list
        encoded in a string.
        """
        return self.data.get("tags", None)

    @tags.setter
    def tags(self, tags: List[str]) -> None:
        """Sets the tags of this entry.

        Args:
            tags: a list of tags. Tags will be stripped from `+` symbols as these are an artifact of
                the command-line syntax. Internally, the list of tags is stored as a comma-separated
                list encoded in a string.
        """
        self.data["tags"] = "".join(tag.strip("+") + ", " for tag in tags).strip(", ")
        LOGGER.debug("Adding the tags '%s' to '%s'.", self.data["tags"], self.label)

    @property
    def file(self) -> Union[str, List[str]]:
        # noqa: D402 (we skip this error because file(s) raises a false negative)
        """The associated file(s) of this entry.

        The setter of this property will be convert the strings to absolute paths. If multiple files
        are specified, they will be stored as a comma-separated list encoded in a string.
        """
        return self.data.get("file", None)

    @file.setter
    def file(self, file: Union[str, List[str]]) -> None:
        # noqa: D402 (we skip this error because file(s) raises a false negative)
        """Sets the associated file(s) of this entry.

        Args:
            file: can be either a single path (`str`) or a list thereof. In either case, the strings
                will be converted to absolute paths. If multiple files were specified, they will be
                stored as a comma-separated list encoded in a string.
        """
        if isinstance(file, list):
            file = ", ".join([os.path.abspath(f) for f in file])
        else:
            file = os.path.abspath(file)
        self.data["file"] = file
        LOGGER.debug("Adding '%s' as the file to '%s'.", self.data["file"], self.label)

    def convert_month(self, type_: Type[Union[int, str]] = config.database.format.month) -> None:
        """Converts the month into the specified type.

        The month field of an entry may be stored either in string or number format. This function
        is used to convert between the two options. The default can be configured via
        `config.database.format.month`.

        Args:
            type_: may be either `str` or `int` indicating the format of the month field.
        """
        month = self.data.get("month", None)
        if month is None:
            return
        try:
            month = int(month)
        except ValueError:
            pass
        if not isinstance(month, type_):
            LOGGER.debug("Converting month type for %s", self.label)
            months = [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec",
            ]
            if isinstance(month, str):
                self.data["month"] = str(months.index(month) + 1)
            elif isinstance(month, int):
                self.data["month"] = months[month - 1]

    def escape_special_chars(self, suppress_warnings: bool = True) -> None:
        """Escapes special characters in the bibliographic data.

        Special characters should be escaped to ensure proper rendering in LaTeX documents. This
        function leverages the existing implementation of the `pylatexenc` module to do said
        conversion. The only fields exempted from the conversion are the `ID` and `file` fields of
        the `Entry.data` dictionary.

        Args:
            suppress_warnings: if True, warnings generated by the `pylatexenc` modules will be
                suppressed. This argument will be overwritten if the logging level is set to
                `logging.DEBUG`.
        """
        enc = UnicodeToLatexEncoder(
            non_ascii_only=True,
            replacement_latex_protection="braces-all",
            unknown_char_policy="keep",
            unknown_char_warning=not suppress_warnings or LOGGER.isEnabledFor(logging.DEBUG),
        )
        for key, value in self.data.items():
            if key in ("ID", "file"):
                # do NOT these fields and keep any special characters
                self.data[key] = value
                continue
            if isinstance(value, str):
                self.data[key] = enc.unicode_to_latex(value)

    def save(self, parser: Parser = None) -> str:
        """Saves an entry using the parsers `dump` method.

        This method is mainly used by the `Database.save` method and takes care of some final
        conversions depending on the user's configuration. Applying such modifications (like e.g.
        month conversion and special character escaping) only before saving ensures a consistent
        state of the database while also providing a fast startup because these conversions are
        prevented at that time.

        Args:
            parser: the parser instance to use for dumping. If set to `None` it will default to a
                `cobib.parsers.YAMLParser`. Supplying a ready instance can improve efficiency
                significantly while saving many entries after one another.

        Returns:
            The string-representation of this entry as produced by the provided parser.
        """
        self.convert_month(config.database.format.month)
        self.escape_special_chars(config.database.format.suppress_latex_warnings)
        if parser is None:
            # pylint: disable=import-outside-toplevel,cyclic-import
            from cobib.parsers import YAMLParser

            parser = YAMLParser()
        return parser.dump(self) or ""  # `dump` may return `None`

    def matches(self, filter_: Dict[Tuple[str, bool], Any], or_: bool) -> bool:
        """Check whether this entry matches the supplied filter.

        coBib provides an extensive filtering implementation. The filter is specified in the form
        of a dictionary whose keys consist of pairs of `(str, bool)` entries where the string
        indicates the field to match against and the boolean whether a positive (`true`) or negative
        (`false`) match is required. The value obviously refers to what needs to be matched.

        Some examples:

        | `filter_`                                        | `or_`    | Meaning                    |
        | ------------------------------------------------ | -------- | -------------------------- |
        | `{('year', True): 2020}`                         | *either* | `year` identical to 2020   |
        | `{('year', False): 2020}`                        | *either* | `year` anything but 2020   |
        | `{('year', True): 2020, ('year', True): 2021}`   | True     | `year` either 2020 or 2021 |
        | `{('year', True): 2020, ('year', True): 2021}`   | False    | cannot match anything      |
        | `{('year', False): 2020, ('year', True): 2021}`  | False    | `year` identical to 2021   |
        | `{('year', False): 2020, ('year', False): 2021}` | False    | `year` is not 2020 or 2021 |

        Args:
            filter_: dictionary describing the filter as explained above.
            or_ : boolean indicating whether logical OR (`true`) or AND (`false`) is used to combine
                multiple filter items.

        Returns:
            Boolean indicating whether this entry matches the filter.
        """
        LOGGER.debug("Checking whether entry %s matches.", self.label)
        match_list = []
        for key, values in filter_.items():
            if key[0] not in self.data.keys():
                match_list.append(not key[1])
                continue
            for val in values:
                if val not in self.data[key[0]]:
                    match_list.append(not key[1])
                else:
                    match_list.append(key[1])
        if or_:
            return any(m for m in match_list)
        return all(m for m in match_list)

    def search(self, query: str, context: int = 1, ignore_case: bool = False) -> List[List[str]]:
        """Search entry contents for the query string.

        The entry will *always* be converted to a searchable string using the
        `cobib.parsers.BibtexParser.dump` method. This text will then be search for `query` which
        will be interpreted as a regex pattern.
        If a `file` is associated with this entry, the search will try its best to recursively query
        its contents, too. However, the success of this depends highly on the configured search
        tool, `config.commands.search.grep`.

        Args:
            query: the text to search for.
            context: the number of context lines to provide for each match. This behaves similarly
                to the *Context Line Control* available for the UNIX `grep` command (`--context`).
            ignore_case: if True, the search will be case-*in*sensitive.

        Returns:
            A list of lists containing the context for each match associated with this entry.
        """
        LOGGER.debug("Searching entry %s for %s.", self.label, query)
        matches: List[List[str]] = []
        # pylint: disable=import-outside-toplevel,cyclic-import
        from cobib.parsers import BibtexParser

        bibtex = BibtexParser().dump(self).split("\n")
        re_flags = re.IGNORECASE if ignore_case else 0
        for idx, line in enumerate(bibtex):
            if re.search(rf"{query}", line, flags=re_flags):
                # add new match
                matches.append([])
                # upper context; (we iterate in reverse in order to ensure that we abort on the
                # first previous occurrence of the query pattern)
                for string in reversed(bibtex[max(idx - context, 0) : min(idx, len(bibtex))]):
                    if re.search(rf"{query}", string, flags=re_flags):
                        break
                    matches[-1].insert(0, string)
                # matching line itself
                matches[-1].append(line)
                # lower context
                for string in bibtex[max(idx + 1, 0) : min(idx + context + 1, len(bibtex))]:
                    if re.search(rf"{query}", string, flags=re_flags):
                        break
                    matches[-1].append(string)

        if self.file:
            files = []
            if isinstance(self.file, list):
                files = self.file
            else:
                files = self.file.split(", ")

            for file_ in files:
                grep_prog = config.commands.search.grep
                LOGGER.debug("Searching associated file %s with %s", file_, grep_prog)
                grep = subprocess.Popen(
                    [grep_prog, f"-C{context}", query, file_], stdout=subprocess.PIPE
                )
                if grep.stdout is None:
                    continue
                stdout = cast(IO[bytes], grep.stdout)
                # extract results
                results = stdout.read().decode().split("\n--\n")
                for match in results:
                    if match:
                        matches.append([line.strip() for line in match.split("\n") if line.strip()])

        return matches
