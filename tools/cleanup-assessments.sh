#!/bin/bash
# Lists, or deletes, Codio assessments that no Guide page uses.
# An assessment is "used" if a Guide page has {...|assessment}(its id).
#
# Run in the Codio terminal:
#   bash cleanup-assessments.sh            preview only, deletes nothing
#   bash cleanup-assessments.sh --delete   back up, ask, then delete

cd ~/workspace || exit 1

if [ ! -d .guides/assessments ]; then
	echo "No .guides/assessments folder - nothing to do."
	exit 0
fi

used=$(grep -rhoE '\{[^}]*\|[[:space:]]*assessment[[:space:]]*\}\([^)]+\)' .guides/content 2>/dev/null | sed -E 's/.*\(([^)]+)\)/\1/' | sort -u)

if [ -z "$used" ]; then
	echo "No assessments found in the Guide - stopping so nothing is deleted by mistake."
	exit 1
fi

echo "Used by the Guide:"
echo "$used" | sed 's/^/  /'

unused=()
for f in .guides/assessments/*; do
	[ -e "$f" ] || continue
	# an assessment's files are <id>.json and sometimes <id>-parameters.py
	id=$(basename "$f" | sed -E 's/(-parameters\.py|\.json)$//')
	echo "$used" | grep -qxF "$id" || unused+=("$f")
done

if [ ${#unused[@]} -eq 0 ]; then
	echo "No unused assessment files."
	exit 0
fi

echo "Not used:"
printf '  %s\n' "${unused[@]}"

if [ "$1" != "--delete" ]; then
	echo
	echo "Preview only. Run again with --delete to remove these files."
	exit 0
fi

read -r -p "Delete these ${#unused[@]} files? (y/n) " answer
if [ "$answer" != "y" ]; then
	echo "Nothing deleted."
	exit 0
fi

backup=~/assessments-backup-$(date +%Y%m%d-%H%M%S).tgz
if ! tar czf "$backup" .guides/assessments; then
	echo "Backup failed - nothing deleted."
	exit 1
fi
echo "Backup saved: $backup"
echo "(restore with: cd ~/workspace && tar xzf $backup)"

rm -v "${unused[@]}"
echo "Done. Reload the Codio page to update the assessment list."
