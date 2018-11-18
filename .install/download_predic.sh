#!/bin/bash

if [ -z $1 ] ; then
    echo usage:
    echo "    download_predic.sh  master | another_branch"
    echo
    exit 0
fi
branch=$1

# Prepare temp directory
mkdir /home/predic/tmp > /dev/null 2>&1
cd /home/predic/tmp

# Removes any existent master.zip or predic directory for this branch:
rm $branch.zip
rm -r pre.di.c-$branch

# Downloads the zip
wget https://github.com/rsantct/pre.di.c/archive/$branch.zip

# Unzip
unzip $branch.zip
rm $branch.zip

# Drops install scripts into tmp/ to be accesible
cp -f pre.di.c-$branch/.install/*sh .

# And back to home
cd