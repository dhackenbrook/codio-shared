# codio-shared

Shared style and Run / Stop / Clear buttons for Codio Guide pages. Every assignment loads these files from here, so a change in this repo updates all assignments.

## Use in a Guide page

Put this at the top of the assignment's `.guides/content/Instructions-*.md`:

```html
<link href="https://cdn.jsdelivr.net/gh/dhackenbrook/codio-shared@main/python/guide-style.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<script src="https://codio.com/codio-client.js" type="text/javascript"></script>
<div id="RunCode">
<button id="runBtn" class="fa run">Run Code &#xf04b;</button>
<button id="stopBtn" class="fa stop">Stop Code &#xf04d;</button>
<button id="clearBtn" class="fa clear">Clear Terminal &#xf0e2;</button>
</div>
<script src="https://cdn.jsdelivr.net/gh/dhackenbrook/codio-shared@main/python/run-buttons.js" type="text/javascript"></script>
```

The Run button runs `python3 Main.py`, so the assignment's program must be in `Main.py`.

## After changing a file

jsDelivr caches files for up to 12 hours. To update right away, open these links once after pushing:

- https://purge.jsdelivr.net/gh/dhackenbrook/codio-shared@main/python/guide-style.css
- https://purge.jsdelivr.net/gh/dhackenbrook/codio-shared@main/python/run-buttons.js

Changes reach every assignment (including students already working), so test on one assignment first.

## Assignment tools

Run these in an assignment's Codio terminal. Each one previews first and only changes files when you add the flag, after saving a backup in your Codio home folder.

**Delete assessments no Guide page uses**

```bash
bash <(curl -s https://raw.githubusercontent.com/dhackenbrook/codio-shared/main/tools/cleanup-assessments.sh)
bash <(curl -s https://raw.githubusercontent.com/dhackenbrook/codio-shared/main/tools/cleanup-assessments.sh) --delete
```

**Make code test instructions collapsed by default**

```bash
python3 <(curl -s https://raw.githubusercontent.com/dhackenbrook/codio-shared/main/tools/collapse-instructions.py)
python3 <(curl -s https://raw.githubusercontent.com/dhackenbrook/codio-shared/main/tools/collapse-instructions.py) --apply
```

Run the cleanup first, so unused assessments aren't changed. Reload the Codio page afterwards.
