# co_snap

...is a utility for generating conducto screenshots.
Unless you care about conducto docs as much as I do, you probably don't need this.

## Prerequisites

It assumes you're using [i3wm](i3wm.org) because that's what I use.  All of that code is in [i3.py](co_snap/i3.py)--should be fairly easy to hook in your window manager of choice too.

You'll also need python3.6 or higher.

## Setup

eval the output of `co_snap_init` to stage necessary env vars


```bash
pip install -e .
eval "$(co_snap_init)"
```
## Usage

- Ensure your pipeline is running and make note of its url
- Automate the creation of your screenshot like in [sample.py](sample.py)
- Run the screenshot automation script like so:
```python
python sample.py --url https://conducto.com/app/p/the-pip
```
- Expect images to be created
![Sample Screenshot](sample.png)
