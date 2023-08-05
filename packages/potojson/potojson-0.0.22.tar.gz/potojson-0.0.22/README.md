# 📦 potojson

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]

Pofile to JSON conversion without pain.

## Status

[![Tests][tests-image]][tests-link]
[![coverage-image]][coverage-link]

## Installation

```bash
pip install potojson
```

## Documentation

### API

<a name="pofile_to_json" href="#pofile_to_json">#</a> <b>pofile_to_json</b>(<i>content</i>, <i>fallback_to_msgid=False</i>, <i>fuzzy=False</i>, <i>pretty=False</i>, <i>indent=2</i>, <i>language=None</i>, <i>plural_forms=None</i>, <i>as_dict=False</i>) ⇒ `str`

Converts a pofile passed as string or filepath and returns a JSON formatted
output. Given this pofile:

```po
#

#, fuzzy
msgid ""
msgstr ""
"Language: es\n"
"Plural-Forms: nplurals=2; plural=n != 1;\n"

msgid "msgid"
msgstr "msgstr"

msgctxt "msgctxt"
msgid "msgid"
msgstr "msgstr"

msgid "msgid"
msgid_plural "msgid_plural"
msgstr[0] "msgstr[0]"
msgstr[1] "msgstr[1]"

msgctxt "msgctxt"
msgid "msgid"
msgid_plural "msgid_plural"
msgstr[0] "msgstr[0]"
msgstr[1] "msgstr[1]"
```

... the output will be:

```json
{
  "": {
    "language": "es",
    "plural-forms": "nplurals=2; plural=n != 1;",
  },
  "msgid": "msgstr",
  "msgctxt": {
    "msgid": "msgstr",
  },
  "msgid": ["msgstr[0]", "msgstr[1]"],
  "msgctxt": {
    "msgid": ["msgstr[0]", "msgstr[1]"],
  }
}
```

This output can be customized tuning the parameters of the function:

- **content** (str) Content or filepath of the pofile to convert.
- **fallback_to_msgid** (bool) Use msgid if translation is missing.
- **fuzzy** (bool) Include fuzzy messages.
- **pretty** (bool) Pretty-print JSON output.
- **sort_keys** (bool) Sort dictionary by key. Combined with `as_dict`
 parameter, returns an instance of [`collections.OrderedDict`][ordereddict].
- **indent** (int) Number of spaces for indentation used pretty-printing JSON
 output. Only takes effect if `pretty` is enabled.
- **language** (str) Language for the translations. Will be inserted in the
 empty key of the JSON output. If not provided and the passed pofile includes
 the "Language" header, will be extracted from it.
- **plural_forms** (str) Plural forms for the language of the translations.
 Will be inserted in the empty key of the JSON output. If not provided and the
 passed pofile includes the "Plural-Forms" header, will be extracted from it.
- **as_dict** (bool) Returns the output as a Python dictionary.
- **encoding** (str) The encoding to use reading the pofile. By default will
 be auto-detected.

### CLI

```
usage: potojson [-h] [-v] [-m] [-f] [-p] [-k] [-i N] [-l LANGUAGE] [-s PLURAL_FORMS] [-e ENCODING] [PO_FILEPATH_OR_CONTENT ...]

Pofile to JSON conversion without pain.

positional arguments:
  PO_FILEPATH_OR_CONTENT
                        Path to pofile or pofile content as string. If the input file stream is interactive, will be read from STDIN.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show program version number and exit.
  -m, --fallback-to-msgid
                        Use msgid if translation is missing.
  -f, --fuzzy           Include fuzzy messages.
  -p, --pretty          Pretty-print JSON output.
  -k, --sort-keys       Sort JSON output by keys.
  -i N, --indent N      Number of spaces for indentation used pretty-printing JSON output. Only takes effect passing the "--pretty" option.
  -l LANGUAGE, --language LANGUAGE
                        Language for the translations. Will be inserted in the empty key of the JSON output. If not provided and the passed pofile includes the "Language" header, will be extracted from it.
  -s PLURAL_FORMS, --plural-forms PLURAL_FORMS
                        Plural forms for the language of the translations. Will be inserted in the empty key of the JSON output. If not provided and the passed pofile includes the "Plural-Forms" header, will be extracted from it.
  -e ENCODING, --encoding ENCODING
                        The encoding to use reading the pofile. By default will be auto-detected.
```

[pypi-link]: https://pypi.org/project/potojson
[pypi-version-badge-link]: https://img.shields.io/pypi/v/potojson
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/potojson
[license-image]: https://img.shields.io/pypi/l/potojson?color=light-green
[license-link]: https://github.com/mondeja/potojson/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/potojson/Test
[tests-link]: https://github.com/mondeja/potojson/actions?query=workflow%3ATest
[coverage-link]: https://coveralls.io/github/mondeja/potojson
[coverage-image]: https://img.shields.io/coveralls/github/mondeja/potojson

[ordereddict]: https://docs.python.org/3/library/collections.html#collections.OrderedDict
