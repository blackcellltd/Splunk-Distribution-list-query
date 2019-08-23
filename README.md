# Splunk Distribution list query

This script is a Splunk implemented command which queries the Active Directory to get members of Distribution Lists.

### Requirements
 - ldapsearch
 - bash
 - Python3-paramiko


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

After the scripts are in place we should set up our exchdl.py script to be able to connect to the Active Directory for the query.

If you user different server as the Splunk server to query the Active Directory you should connect with SSH to that server.
Give your credentials below.
```sh
Line 11 -> ssh.connect("<IP address>", username = "<username>", key_filename = "<filepath>")
```

After this step you need to setup the query command.
```sh
Line 27 -> channel.exec_command('/bin/bash -c cat /dev/stdin | xargs -I{} /opt/ldap/ldapsearch -LLL -E pr=1000/noprompt -H <dc_hostname> -D "CN=<the user who query the DC>,OU=<OUinfo1>,OU=<OUinfo2>,OU=<OUinfo3>,OU=<OUinfo4>,DC=<domain>,DC=<domain2>" -b "DC=<domain>,DC=<domain2>" -o ldif-wrap=no -w "<password>" "{}"')
```
In this section you need to giveyour Domain Controller hostname, the canonical name of the user who perform the query and other domain related informations (see in the angle brackets).

Now we are ready to go:

Right now you need to put exchangedl command to the end of your Splunk search which give results about distribution list names and we will see the members of the groups which included.


