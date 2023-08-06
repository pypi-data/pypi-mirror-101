# Herd python client

Drafting a `project herd` client library

## Usage

Install the library:

```
	python3 -m pip install herdpy
```


Use the `new_report` helper to create and send reports to the herd server:

```
	from herdpy import new_report

	r = new_report()

	r.url = "http://nowhere.local"
	r.node_name = "testclient"
	r.group = "testgroup"
	r.status_code = "E200OK"

	r.add_tag("test")
	r.add_tag("dev")

	# Send the report to the server
	r.send()

```

More to come...


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Author

Steffen Park <dev@istherepie.com>
