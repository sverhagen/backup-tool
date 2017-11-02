# backup-tool
Simple scripts to backup my computer

<hr/>

**What computer is this for?** &mdash; I'm a proud and stubborn Windows user, currently on Windows 7. Clearly that's the
 only environment that this is tested on.

**Why does it fail without elevation?** &mdash; In order to pull stuff from the registry, it needs to be elevated (i.e.
 "Run As Administrator").

**Why did you build this yourself?** &mdash; I could not find a simple and straightforward tool that could do this to
 me, but I'm still open to suggestions.

**You seriously expect *takers* for this?** &mdash; No, I don't. This is for my own, personal use. With GitHub at least
 I have a backup of my backup tool.
 
## Requirements

The scripts assume you're running within [Cygwin](https://cygwin.com/). Windows Command Prompt is horror, Cygwin rocks.

For Cygwin `python3-dev` is required.

Requirements:

- Python 3-ish
- `pip install --upgrade pip`
- `pip install --upgrade setuptools`
- Python package `Fabric`
- Python package `PyYAML`
