#!/bin/bash

name="@project-gaudi\/node-red-datacleansing"
description="Node-RED-DataCleansing"
target="package.json"
author="Toyota Industries Corporation"
lisence="MIT"
version=${VERSION}

sed -i 's/\"name\": \".*\",/\"name\": \"'"${name}"'\",/g' "${target}"
sed -i 's/\"version\": \".*\",/\"version\": \"'"${version}"'\",/g' "${target}"
sed -i 's/\"description\": \".*\",/\"description\": \"'"${description}"'\",/g' "${target}"
sed -i 's|"author": ".*",|"author": "'"${author}"'", |g' "${target}"
sed -i 's|"license": ".*"|"license": "'"${lisence}"'"|g' "${target}"

grep -q '"repository"' "${target}" || \
sed -i '/"node-red": {/i \
    "repository": { \
        "type": "git",\
        "url": "git+https://github.com/Project-GAUDI/node-red-datacleansing" \
    },' "${target}"

grep -q '"bugs"' "${target}" || \
sed -i '/"node-red": {/i \
    "bugs": { \
        "url": "https://github.com/Project-GAUDI/node-red-datacleansing/issues" \
    },' "${target}"

grep -q '"homepage"' "${target}" || \
sed -i '/"node-red": {/i \
    "homepage": "https://github.com/Project-GAUDI/node-red-datacleansing#readme",' "${target}"