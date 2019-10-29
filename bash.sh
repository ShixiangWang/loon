#!/bin/bash
# Build new version automatically
py=$1
old_version=$2
new_version=$3
if [ -d dist/ ]; then
    echo 'Cleaning dist/'
    rm -rf dist/*
else 
    echo 'Not in the project root directory!'
    echo 'exiting...'
    exit 1
fi
echo 'Updating version number'
if [ -z $py ]; then
    echo 'Error: Please input python command: python or python3'
    echo 'exit...'
    exit 1
fi
if [ -z $old_version ]; then
    echo 'Error: Please input old version'
    echo 'exit...'
    exit 1
fi
if [ -z $new_version ]; then
    echo 'Error: Please input new version'
    echo 'exit...'
    exit 1
fi
echo old version: $old_version
echo new version: $new_version
sed -i '' -e "s/$old_version/$new_version/" src/loon/__init__.py
echo 'Creating new version'
git add .
git commit -m "Release $new_version"
git tag $new_version
echo 'Creating some distributions'
$py setup.py sdist bdist_wheel
echo 'Uploading distributions'
twine upload dist/*
echo 'Uploading release to GitHub'
git push --tags
