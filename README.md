# Splunk Distribution list query

This script is a Splunk implemented command which queries the Active Directory to get members of Distribution Lists.

### Usage
Place exchdl.py anywhere you want in your filesystem but do not forget to change the path in exchangedl.py.
```sh
Line 10 -> p = subprocess.Popen(["$(PATH/exchdl.py)", mail], stdout = subprocess.PIPE, stderr = subprocess.PIPE, env = e)
```
Then put exchangedl.py to $SPLUNK_HOME/etc/apps/{YOUR APP}/bin/ folder.
