import sys
import os
import splunk.Intersplunk
import subprocess
import copy

def _expand(mail):
	e = copy.deepcopy(os.environ)
	e.pop("PYTHONPATH")
	p = subprocess.Popen(["/opt/exchdl.py", mail], stdout = subprocess.PIPE, stderr = subprocess.PIPE, env = e)
	out = p.communicate()
	sys.stderr.write(out[1])
	if p.returncode: exit(p.returncode)
	return out[0].decode()

results, _, settings = splunk.Intersplunk.getOrganizedResults()

newresults = []
for result in results:
	r = result["recipients"].split(" ")
	r2 = []
	r2 += _expand(" ".join(r)).split(" ")
	r2 = list(set(r2))
	r2.sort()
	result["recipients"] = "\n".join(r2)
	result["recnum"] = len(r2)
	newresults.append(result)

splunk.Intersplunk.outputResults(newresults)
