#region imports
from delog.constants import (
    QUIET,
)
#endregion imports



#region module
def console_log(
    text: str,
):
    if not QUIET:
        print(text)
#endregion module
