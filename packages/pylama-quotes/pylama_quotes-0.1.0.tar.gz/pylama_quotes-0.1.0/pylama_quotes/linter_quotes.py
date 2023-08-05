import tokenize

from pylama.lint import Linter as BaseLinter

# pylama:ignore=E501


def _check(token):
    if token.type != tokenize.STRING:
        return None
    s = token.string.lstrip('flrubLRUB')  # don't look at prefixes, e.g. r'cc\c' becomes 'cc\c' 
    if s.startswith('"""'):
        return None  # triple-quote/docstring - using double quotes is OK
    if s.startswith("'") and not s.startswith("'''"):
        return None  # normal string - single quotes OK
    if s.startswith('"'):
        # normal string with double-quotes - OK IFF it contains a single quote
        if "'" in s.strip('"'):
            return None

    # If we're here then we know there's an issue
    if s.startswith("'''"):
        msg = 'Docstrings (and multi-line strings) should be delimited with double quotes'
    else:
        msg = 'Normal strings should be single-quote unless they contain single quotes'

    ln, col = token.start
    return {
        'lnum': ln,
        'col': col,
        'text': msg,
        'type': 'QUOTE',
    }


class Linter(BaseLinter):
    """Linter for quote style."""

    def run(self, path, **meta):
        try:
            return list(self.run_iter(path, **meta))
        except Exception as e:
            raise
            return [{
                'lnum': 1,
                'col': 1,
                'type': 'QUOTE_ERR',
                'text': 'Error parsing file: ' + repr(e)
            }]

    def run_iter(self, path, **meta):
        with open(path, 'rb') as f:
            for token in tokenize.tokenize(f.readline):
                found = _check(token)
                if found:
                    yield found
