#!/usr/bin/env python3
"""Makes Codio assessment instructions collapsed by default.

Wraps each code test's instructions in <details><summary></summary> ... </details>.
Instructions that are already wrapped are left alone; <details open> is changed
to <details> so they start collapsed.
Only "test" (Advanced Code Test) and "code-output-compare" assessments are changed,
so questions in other types (e.g. multiple choice) are never hidden.

Run in the Codio terminal:
  python3 collapse-instructions.py           preview only, changes nothing
  python3 collapse-instructions.py --apply   back up, then change the files
"""
import glob, json, os, re, sys, tarfile, time

TYPES = ("test", "code-output-compare")

os.chdir(os.path.expanduser("~/workspace"))
apply = "--apply" in sys.argv

changes = []
for path in sorted(glob.glob(".guides/assessments/*.json")):
	with open(path, encoding="utf-8") as f:
		raw = f.read()
	try:
		data = json.loads(raw)
	except ValueError:
		print("  skipped (not valid JSON): " + path)
		continue
	source = data.get("source", {})
	text = source.get("instructions") or ""
	if data.get("type") not in TYPES or not text.strip():
		continue

	stripped = text.strip()
	if re.match(r"<details\b", stripped):
		new = re.sub(r"^<details\b[^>]*>", "<details>", stripped, count=1)
		if new == stripped:
			continue
		reason = "removed 'open' so it starts collapsed"
	else:
		new = "<details><summary>\n</summary>\n\n" + stripped + "\n</details>"
		reason = "wrapped in <details>"

	source["instructions"] = new
	name = source.get("name", "")
	changes.append((path, raw, data))
	print("  {} ({}): {}".format(path, name, reason))

if not changes:
	print("All code test instructions are already collapsed - nothing to do.")
	sys.exit(0)

if not apply:
	print("\nPreview only. Run again with --apply to change these files.")
	sys.exit(0)

backup = os.path.expanduser(time.strftime("~/instructions-backup-%Y%m%d-%H%M%S.tgz"))
with tarfile.open(backup, "w:gz") as tar:
	tar.add(".guides/assessments")
print("Backup saved: " + backup)
print("(restore with: cd ~/workspace && tar xzf " + backup + ")")

for path, raw, data in changes:
	# save in Codio's own format: tab indents, no trailing newline
	text = json.dumps(data, indent="\t", ensure_ascii=all(ord(c) < 128 for c in raw))
	with open(path, "w", encoding="utf-8", newline="\n") as f:
		f.write(text)
print("Done. {} file(s) changed. Reload the Codio page to see the result.".format(len(changes)))
