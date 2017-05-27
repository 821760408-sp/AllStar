# Star them all

Programmatically stars all public repos from your following.

## Usage

To install dependencies:

```bash
pip install -r requirements.txt
```

To run:

```bash
python star_them_all.py --user=gvanrossum --threads=4
```
### Options

Use `--user` to specify a single user whose repos you'd like to star. If omitted, the repos from all the users you're currently following will be starred.

Use `--threads` to determine how many threads to use (default is 1 when omitted or when `--user` is set).
