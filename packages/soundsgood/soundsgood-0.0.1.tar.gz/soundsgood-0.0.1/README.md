# soundsgood
Cos I don't think https://docs.python.org/3/tutorial/modules.html#packages is at all sound...


# Python Packaging Pandora

I couldn't get my nested `module -> submodule -> *.py` packaging working? 

After quite a painful hours of Google + Stackoverflowing, the results point to:


- https://stackoverflow.com/questions/33743880/what-does-from-future-import-absolute-import-actually-do
- https://stackoverflow.com/questions/63728242/importerror-cannot-import-name-unknown-location
- https://stackoverflow.com/questions/8953844/import-module-from-subfolder

- https://packaging.python.org/tutorials/packaging-projects/
- https://docs.python.org/3/reference/import.html#__path__
- https://docs.python.org/3/tutorial/modules.html#packages

Although the last link in the bullet above looks "sound", I've tried an hour worth of variation of how to write the `__init__.py` files and I'm giving up so I made this repo to replicate the tutorial and hopefully document what really should be in the `___init__.py` files from the https://docs.python.org/3/tutorial/modules.html#packages tutorial given the following file structure:

```
soundsgood/                     Top-level package
      __init__.py               Initialize the sound package
      formats/                  Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/                  Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/                  Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```
