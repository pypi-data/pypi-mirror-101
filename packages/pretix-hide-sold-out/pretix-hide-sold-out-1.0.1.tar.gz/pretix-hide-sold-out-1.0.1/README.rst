Hide sold out events
====================

This is a plugin for `pretix`_.  It provides a cronjob that automatically sets ``is_public`` to ``False`` on any
event series as soon as all future dates in the series are sold out.

How to use
----------

- Install the plugin on the server, e.g. from ``pip install git+https://github.com/pretix-unofficial/pretix-hide-sold-out.git@main#egg=pretix-hide-sold-out``

- Enable the plugin in the events that you want to be affected.

- Set up a new cronjob that executes ``python -m pretix hide_sold_out``. Pass ``--allow-republish`` if you want the
  command to also re-publish events that are currently ``is_public=False`` but have available quota. Pass ``--dry-run``
  to see what the command would do without actually executing it.


Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed:

    pip install flake8 isort black docformatter

To check your plugin for rule violations, run:

    docformatter --check -r .
    black --check .
    isort -c .
    flake8 .

You can auto-fix some of these issues by running:

    docformatter -r .
    isort .
    black .

To automatically check for these issues before you commit, you can run ``.install-hooks``.


License
-------


Copyright 2020 pretix team

Released under the terms of the Apache License 2.0



.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
