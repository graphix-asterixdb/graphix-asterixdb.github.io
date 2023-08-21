# Graphix AsterixDB
A little website for the Graphix project. Check it out [here](https://graphix.ics.uci.edu)!

## Contributing to Docs

### Site Generation
This website uses the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme for Jekyll, a static site generator.

### Image Standards
Please try to use SVG files when adding images. :-)

### Grammar File Generation
To generate the grammar SVG files...
1. Use the [Railroad Diagram Generator](https://www.bottlecaps.de/rr/ui) to produce an XHTML+SVG zip (not embedded).
2. Run `python3 tools/bottlecaps.py` to copy the images _and_ image sizes to your local repository.
