from setuptools import setup

setup(
    name="co_snap",
    version="0.1.0.dev1",
    description="screenshots of conducto pipelines",
    author="Matt Rixman",
    author_email="mrixman@conducto.com",
    packages=["co_snap"],
    python_requires=">=3.6",
    install_requires=["i3ipc", "selenium", "Selenium-Screenshot", "Pillow", "OpenCV-Python"],
    entry_points={
        "console_scripts": [
            # sync a billing-slice of meta from source to dest, clobbering dest data
            "co_snap_init = co_snap.cli:init"
        ]
    },
)
