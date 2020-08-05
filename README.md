# co_snap

...is a utility for generating conducto screenshots.
Unless you care about conducto docs as much as I do, you probably don't need this.

## Prerequisites

It assumes you're using [i3wm](https://www.i3wm.org) because that's what I use.
Maybe one day I'll explore `chrome_options.add_argument("--headless")` and make it portable, but it scratches my itch for now.

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
