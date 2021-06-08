# Built-in
from typing import List

# ----------------------------------------------- #
# Current version of runup                        #
# ----------------------------------------------- #
# Al lanzar la version 0.1.0 nos pasamos a SemVer #
# ----------------------------------------------- #
runup_version:str = '0.1.dev7'

# ----------------------------------------------------- #
# List of versions supported when reading the YAML file #
# ----------------------------------------------------- #
# Format: 2 numbers. Example: 1 and 1.0 but not 1.0.0   #
#                                                       #
# On every major release add a version X and a X.0      #
#                                                       #
# Until the release 2.0, a test is going to fail every  #
# time a new version is released. Just search for:      #
# "Update major to latest until 2.0 is released"        #
# without quotes.                                       #
# ----------------------------------------------------- #
yaml_versions:List[str] = ['1', '1.0',]
