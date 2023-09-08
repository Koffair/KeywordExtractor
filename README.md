# Keyword Extractor for Tilos Radio

## General Remarks
+ If the Hungarian model is not available on the
machine, the script downloads it from the web
+ this means the first run of this script requires
a stable internet connection AND
+ it takes severa minutes to download the model, so
be patient

## How to run
Simply provide an input and an output folder.
The input folder must contain txt files, the output
folder will contain files with the same name and
extension.
```bash
python main.py --input tests/data/ --output tests/data/out/
```