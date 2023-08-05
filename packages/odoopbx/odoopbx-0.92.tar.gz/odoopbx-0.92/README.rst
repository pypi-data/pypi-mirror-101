===============================
The OdooPBX Management Utility
===============================
Features:

* The Agent installation & configuration
* Asterisk installation management
* Odoo installation management

For more details visit the project homepage: https://odoopbx.com

*Latest* Odoo modules require the *latest* odoopbx utility. If you have outdates Odoo modules
see the release history for the corresponding odoopbx version and install it.

For example, to install version 0.80 enter the following command:

.. code::

    pip3 install odoopbx==0.80


ChangeLog
#########


0.92 (2021-04-05)
#################

* Fixed a bug with blackist list entry addition.
* Salt 2002.6 is set as dependency as there incompatible change in Salt 3003.
* Fixed a bug when manually added ipset entry to the banned list was not shown in the Odoo banned report.

