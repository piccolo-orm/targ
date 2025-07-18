Changes
=======

0.6.0
-----

Modernised the type annotations used in the ``targ`` codebase (e.g. using
``list[str]`` instead of ``List[str]``). This is possible because we no longer
support Python 3.8. Thanks to @sinisaos for this.

Added support for the new union syntax (e.g. ``str | None``). So targ now
works with both of these:

.. code-block:: python

    def say_hello(name: Optional[str] = None):
        print(f'Hello {name}' if name else 'Hello')

    def say_hello(name: str | None = None):
        print(f'Hello {name}' if name else 'Hello')

0.5.0
-----

General maintenance - dropping Python 3.8 support, adding Python 3.13, and
updating dependencies.

0.4.0
-----

General maintenance - dropping Python 3.7 support, adding Python 3.12, updating
dependencies, and fixing linter errors.

0.3.8
-----
Slackened dependencies to avoid clashes with other libraries, like ``fastkafka``.

0.3.7
-----
If an exception is raised when running a command, mention the ``--trace``
option, which will show a full stack trace.

Added docstring to ``Command``.

0.3.6
-----
Added Python 3.10 support.

0.3.5
-----
Fixing a bug with the ``--trace`` option, which outputs a traceback if an
exception occurs.

0.3.4
-----
Commands will now work if the type annotation of an argument is missing - in
this case the type of the argument is assumed to be a string.

0.3.3
-----
Small help formatting change when a command has no args.

0.3.2
-----
Add back `CLI.command_exists` - required by Piccolo.

0.3.1
-----
Show aliases in command help text.

0.3.0
-----
Added aliases for commands.

0.2.0
-----
Added support for ``Optional`` and ``Decimal``.

0.1.9
-----
Added solo mode.

0.1.8
-----
Fixing py.typed.

0.1.7
-----
Loosening colorama dependency version.

0.1.6
-----
Improving appearance when a command has no args.

0.1.5
-----
Added --trace argument for getting Python traceback on error.

0.1.4
-----
Can override the command name.

0.1.3
-----
Removed cached_property to support Python 3.7.

0.1.2
-----
Added support for groups and coroutines.

0.1.1
-----
Add support for flag arguments, and improved help output.

0.1.0
-----
Initial release.
