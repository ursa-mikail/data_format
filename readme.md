
Data types must be tagged for proper management, e.g. if the data is in {}
1. SQL, there is criteria of SQL injection defense/countermeasures.
2. Server apps, there are criteria of XSS protection and vulnerability scans.
3. System configs, there are criteria of local file inclusion protection. If data is tied to sys with loc that updates and upgrades, there has to be vulnerability scans to check odeon on arbitrary file up/downloads (system in/outgress), including path access traversal, trusted and vulnerable component(s), etc. 

Data can be typed as:
1. Field-tagged: i.e. there is a field tag and value (SQL, forms, etc)
	- Key:value
	- HTML form
	- List (linked, graphQL syntax, tree, graph, etc)* graphs and trees are considered specific forms of linked lists

2. File (known)
	- Text (syntax known: formatted forms, e.g. json, yaml, cvs, xml, latex, html, etc)
	- Mixed (pdf, windoc, etc)
	- Image (jpg, png, svg, etc)
	- Audio (mp3, etc)
	- Video (mp4, etc)
	- Data frames (canonized, e.g. GPS, python `pickle`, etc)

3. File (unknown)
	- Binary (blob, volumes, unknown executables (must be marked trusted or untrusted), etc)
	- Streamed payloads

* all data are to be tagged with data classification (secret, sensitive, non-sensitive, public, etc)

	- 