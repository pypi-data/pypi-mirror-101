.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================
collective.expandcollapse.tile
==============================

Javascript plugin that enable expand/collapse behavior in tiles.


Usage
-----

To enable expand/collapse feature in a tile, you only need to add a specific CSS class to it.

Some tiles like `collective.tiles.advancedstatic <https://github.com/collective/collective.tiles.advancedstatic>`_ or `collective.tiles.collection <https://github.com/collective/collective.tiles.collection>`_ 
have a field in their configuration that allows to add custom CSS classes.

Possible classes are:

- **collapsible-desktop**: enable expand/collapse feature for Desktop displays (width > 991px)
- **collapsible**: enable expand/collapse for small screens only (width < 991px)

In addition to these two mutually exclusive classes, you can also add the class **accordion** so
when one of them is opened, the others will be closed.

Installation
------------

Install collective.expandcollapse.tile by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.expandcollapse.tile


and then running ``bin/buildout``

After that, you need to install the product "Expand/Collapse tile" in your Plone site.

Development
-----------

All resources are compiled with grunt.

First of all, you need to setup your development environment inside project root::

    > npm install

Then, you need to activate grunt in watch-mode::
    
    > npm run develop

After that, you can edit *expand_collapse.js* or *styles.scss* files and resources will be automatically compiled in *dist* folder.

You can also force compilation with this command::

    > npm run compile


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.expandcollapse.tile/issues
- Source Code: https://github.com/collective/collective.expandcollapse.tile


License
-------

The project is licensed under the GPLv2.

Dependencies
------------

This product has been tested on Plone 5.1

Credits
-------

Developed with the support of `Regione Emilia Romagna <http://www.regione.emilia-romagna.it/>`_;

Regione Emilia Romagna supports the `PloneGov initiative <http://www.plonegov.it/>`_.


Authors
-------

This product was developed by RedTurtle Technology team.

.. image:: https://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: https://www.redturtle.it/
