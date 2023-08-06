# HeaderBreakdown
flattens a collection of HTTP headers into a JSON structure for automated analysis

### Installation
```
pip install headerbreakdown
```

### Example Output
![headerbreakdown-summary-output.PNG](https://github.com/bonifield/HeaderBreakdown/raw/main/images/headerbreakdown-summary-output.PNG)
- this is the summary; each of these items are accessible directly as attributes; see below

### Example Usage
```
from headerbreakdown import HeaderBreakdown
import json
# sample header with multiple Host and User-Agent values
H1 = "GET /?gws_rd=ssl HTTP/1.1\r\nHost: www.google.com\r\nHost: www.bing.com\r\nHost: www.yahoo.com\r\nConnection: keep-alive\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/99.0\r\nCookie: 1P_JAR=2021-03-13-04"
# create the object
h = HeaderBreakdown(H1)
# utilize attributes
print(h.output) # dictionary
print(h.json) # string
print(h.summary)
# etc
```

### Available Attributes (all except summary included in output and json)
```
# main attributes (also listed below)
	output (dictionary)
	json (string)
	nested_*
# dictionaries
	output
	nested_output # all objects nested under 'headers', ex. {'headers':{...}}
	nested_direction_output # all objects nested under "headers"+direction, ex. {'headers':{'request':{...}}}
# lists
	notices
# strings
	json
	nested_json # all objects nested under "headers", ex. {"headers":{...}}
	nested_direction_json # all objects nested under "headers"+direction, ex. {"headers":{"request":{...}}}
	direction
	http_version
	method
	host
	path
	user_agent
	response_code
	response_phrase
	summary
```

### Releases and Updates
- 2021-04-06
	- added nested_direction_json/output, ex. {"headers":{"request":{...}}}
	- so direction gets captured and headers do not get overwritten if processing a capture with both sides of the communication
	- the nested_direction_* attributes will be type None when processing a single, direction-ambiguous header (ex. "Set-Cookie: k1=v1;k2=v2")
- 2021-04-01
	- minor fix for HTTP/ detection
- 2021-03-23
	- minor edits, added summary and nested_output/nested_json attributes, ex. {"headers":{...}}
- 2021-03-13
	- first release
