#!/usr/bin/env python3
from co_snap import browser, i3, xpath, url, cli, png

args = cli.get_args("make a screenshot")
name = url.get_name(args.url)
i3.prepare(name)
dom = browser.pipeline(args)
i3.resize(name)

# select first child node
root = dom.find_element_by_id("root")
root.find_element_by_xpath(xpath.first_child).click()

# delete absolute path
browser.wait_for_stdout(dom)
browser.delete(dom, xpath.abspath)

# filenames for intermediate image steps
step = [ "sample.guts.partial.png",
         "sample.cropped.partial.png",
         "sample.arrow.partial.png",
         "sample.png" ]

# create the screenshot
middle = root.find_element_by_xpath(xpath.two_columns)
png.screenshot_element(dom, middle, step[0])
png.top_only(step[0], 245, step[1])
png.arrow_from_to(step[1], (700,40), (820, 40), step[2])
png.text_at(step[2], "copy a debug command", (550,40), step[3])
