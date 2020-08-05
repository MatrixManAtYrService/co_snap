#! /usr/bin/env python3
from i3ipc import Connection
import sys
import re
from co_snap.cli import yes_or_no

# Resizes a container whose name matches query to size_px
# for consistency in screenshotting
# (i3 only, sorry)

query = "^[a-z]{3}-[a-z]{3}.*Conducto"
size_px = 1000

i3 = Connection()

# walk the container tree, look for matches
def leaves_named(node, name_regex):
    if not node.nodes:
        if re.search(name_regex, node.name):
            yield node
    else:
        for n in node.nodes:
            for leaf in leaves_named(n, name_regex):
                yield leaf


def _collect(query, ignore):

    leaves = leaves_named(i3.get_tree(), query)

    if not ignore:
        leaves = list(leaves)
    else:
        leaves = list(filter(lambda x: not re.search(ignore, x.name), leaves))

    return leaves


# called before launching a window--make sure it ends up in a vertical-resizable location and has a unique name
def prepare(query, ignore="--url"):

    leaves = _collect(query, ignore)
    if leaves:
        print("The new window has a name collision:")
        for i, node in enumerate(leaves):
            print(f'    [{i}]: "{node.name}"')

        if yes_or_no("Shall I close these?"):
            for node in leaves:
                node.command("kill")

    # place new window to the right of this one
    i3.get_tree().find_focused().command("split horizontal")


def resize(query, size_px=1000, ignore="--url"):

    leaves = _collect(query, ignore)

    # handle too few or too many
    if not leaves:
        print("no containers found with name:", query)
        print("doing nothing")
        sys.exit(1)
    elif len(leaves) > 1:
        print("multiple containers found matching name:", query)
        for i, node in enumerate(leaves):
            print(f'    [{i}]: "{node.name}"')
        print("which one should I resize?")
        idx = int(input())
        target = leaves[idx]
    else:
        target = leaves[0]

    # do it
    print("resizing: ", target.name)
    print("current width: ", target.rect.x)
    target.command(f"resize set {size_px} px")
    print(f"window {target.id} resized to {size_px}")
    return target.id


if __name__ == "__main__":
    resize(query)
