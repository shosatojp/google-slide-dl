# Download google slides as SVG

- Download view only slides as svg files

## Usage

```sh
# install requirements
pip install -r requirements.txt

# run
python3 google-slide-dl.py 'https://docs.google.com/presentation/d/e/.../pub'
```

## Convert and concatenate as PDF (vector based)

```sh
cairosvg -f pdf 1.svg -o 1.svg.pdf
cairosvg -f pdf 2.svg -o 2.svg.pdf
cairosvg -f pdf 3.svg -o 3.svg.pdf
pdftk *.svg.pdf cat output slide.pdf
```
