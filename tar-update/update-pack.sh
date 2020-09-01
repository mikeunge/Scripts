#!/bin/bash
#
# Module that updates a given .tar file.
#
if [ -z $1 ]; then
    echo "No '.tar' file provided. Exiting."
    exit 1
fi
if ! [ -f $1 ]; then
    echo "File ($1) does not exist! Exiting."
    exit 1
fi

# Set the .tar file to update.
to_update=$1

# Create a "PATHS" array where all the paths will get added.
declare -a PATHS

# Loop over the different elements.
for elem in $(tar --diff -Pf $to_update)
do
    if [[ $elem == /* ]]; then
        if [[ ! " ${PATHS[@]} " =~ " ${elem%:} " ]]; then
            PATHS+=(${elem%:})
        fi
    fi
done

# Delete the path from the '.tar' file.
for path in ${PATHS[@]}
do
    echo "Working on file: $path"
    {
        tar --delete -Pf $to_update $path
        echo "Deleted '$path' from '$to_update'."
    } || {
        echo "Could not delete '$path' from '$to_update'. Skipped."
        continue
    }

    {
        tar -rPf $to_update $path
        echo "Appended '$path' to '$to_update'."
    } || {
        echo "Could not append '$path' to '$to_update'. Next."
        continue
    }
done
