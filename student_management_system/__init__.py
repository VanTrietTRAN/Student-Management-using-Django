"""Project package initializer.

On Windows it's common to use PyMySQL (pure-Python) instead of the
`mysqlclient`/MySQLdb C extension. This module tries to make PyMySQL act
as MySQLdb so Django's MySQL backend can import it without requiring a
compiled mysqlclient installation.

If PyMySQL isn't installed yet, import will raise ImportError and a
helpful install instruction is provided in the README below or in CLI
instructions.
"""

try:
	
	import pymysql
	pymysql.install_as_MySQLdb()
except ImportError:
	# PyMySQL not installed; install it into the active virtualenv with:
	# python -m pip install pymysql
	# We intentionally don't raise here so the app can still show a clear
	# error later if the DB backend is used without the driver.
	pass
