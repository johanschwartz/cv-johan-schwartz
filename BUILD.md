# Building the PDF

README.md is the CV. `build.py` turns it into `Johan Schwartz - CV.pdf`.

## One-time setup

1. Install [pandoc](https://pandoc.org/installing.html).
2. Install Playwright and its Chromium:

   ```
   pip install playwright
   python -m playwright install chromium
   ```

## Build

```
python build.py
```

## Files

- `README.md`: the CV itself. GitHub shows it on the repo's front page.
- `style.css`: layout and typography for the PDF. Each role is kept on one page.
- `fonts/`: Fira Sans, bundled so the PDF looks the same on every machine (SIL Open Font License, see `fonts/OFL.txt`).
- `build.py`: the build script.
