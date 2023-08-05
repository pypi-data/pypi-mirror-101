# pyquotes

This is a quote style checker for use with pylama.

For now this is hard-coded check for:

* Double-quote style on doc strings, e.g. `"""Hello World."""`
* Single-quote style on everything else, e.g.
  `d['key'] = 'value {}:{}'.format('Hello', 42)`

## Installing

Since this is a pretty personal repo, I usually just install using pip from this directory:
`pip3 install --user --upgrade .`

However, if you to install without cloning a repo to your drive, you can just:
`pip3 install --user --upgrade -e git+https://github.com/CraigKelly/pyquotes#egg=pylama_quotes`

If you are hacking on this module, you can also add the `-e` switch to that: 
`pip3 install --user --upgrade -e .`


## One day it would be nice to:

* Allow specifying style options
* Be in PyPI (and so pip installable by name instead of fs location)

## License

This package is licensed under the MIT license. See `./LICENSE` for details.
