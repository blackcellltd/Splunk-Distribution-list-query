# Splunk Distribution list query

This script is a Splunk implemented command which queries the Active Directory to get members of Distribution Lists.

### Usage
Place exchdl.py anywhere you want in your filesystem but do not forget to change the path in exchangedl.py.
```sh
Line 10 -> p = subprocess.Popen(["$(PATH/exchdl.py)", mail], stdout = subprocess.PIPE, stderr = subprocess.PIPE, env = e)
```
Then put exchangedl.py to $SPLUNK_HOME/etc/apps/{YOUR APP}/bin/ folder.
For example if you put the python script to your search apps bin folder then you need to edit (if not exist create) the commands.conf file into $SPLUNK_HOME/etc/apps/search/local folder.
After this put these lines into the file.

```sh
[exchangedl]
filename = exchangedl.py
retainsevents = true
streaming = true
overrides_timeorder = false
is_risky = false
```
