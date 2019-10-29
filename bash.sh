#!/bin/bash
# Build new version automatically
py=$1
old_version=$2
new_version=$3
if [ -d dist/ ]; then
    echo =================
    echo 'Cleaning dist/'
    echo =================
    rm -rf dist/*
else 
    echo =================
    echo 'Not in the project root directory!'
    echo 'exiting...'
    exit 1
fi
echo =========================
echo 'Updating version number'
if [ -z $py ]; then
    echo =================
    echo 'Error: Please input python command: python or python3'
    echo 'exit...'
    exit 1
fi
if [ -z $old_version ]; then
    echo =================
    echo 'Error: Please input old version'
    echo 'exit...'
    exit 1
fi
if [ -z $new_version ]; then
    echo =================
    echo 'Error: Please input new version'
    echo 'exit...'
    exit 1
fi
echo =========================
echo old version: $old_version
echo new version: $new_version
echo =========================
sed -i '' -e "s/$old_version/$new_version/" src/loon/__init__.py
echo ======================
echo 'Creating new version'
echo ======================
cp README.md docs/README.md
git add .
git commit -m "Release $new_version"
git tag $new_version
echo =========================
echo 'Creating some distributions'
echo =========================
$py setup.py sdist bdist_wheel
echo =========================
echo 'Uploading distributions'
echo =========================
twine upload dist/*
echo =========================
echo 'Uploading release to GitHub'
echo =========================
git push --tags
git push