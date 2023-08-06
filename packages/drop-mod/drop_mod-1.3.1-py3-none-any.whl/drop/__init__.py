__version__ = "1.3.1"


def licenses():
    license_list = [
        {
            "name": "Drop",
            "license": "Apache 2.0",
            "link": "https://github.com/AtlasC0R3/drop-moderation/blob/master/LICENSE",
            "changes": "no changes made"
        },
        {
            "name": "duckduckpy",
            "license": "MIT License",
            "link": "https://github.com/ivankliuk/duckduckpy/blob/master/LICENSE",
            "changes": None
        },
        {
            "name": "LyricsGenius",
            "license": "MIT License",
            "link": "https://github.com/johnwmillr/LyricsGenius/blob/master/LICENSE.txt",
            "changes": None
        },
        {
            "name": "Parsedatetime",
            "license": "Apache 2.0",
            "link": "https://github.com/bear/parsedatetime/blob/master/LICENSE.txt",
            "changes": "no changes made"
        },
        {
            "name": "Dear PyGui",
            "license": "MIT License",
            "link": "https://github.com/hoffstadt/DearPyGui/blob/master/LICENSE",
            "changes": None
        }
    ]
    # If you installed these from PyPI directly (or just ran setup.py or pip to install this), then no changes have been
    # made, so you don't need to stress out about that.
    license_str = ""
    for dep in license_list:
        to_add = f"{dep['name']}, licensed under {dep['license']}"
        if dep['changes']:
            to_add = to_add + ", " + dep['changes']
        license_str = license_str + to_add + f" ({dep['link']})\n"
    return license_str
