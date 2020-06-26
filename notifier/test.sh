# Check if a parameter is provided.
if [ -z "$1" ]; then
    limit=5
else
    limit=$1
fi
if [ -z "$2" ]; then
    sleep_time=5
else
    sleep_time=$2
fi

i=0
while true; do
    if (( $i == $limit )); then
        break
    else
        (( i=i+1 ))
        sleep $sleep_time
    fi
done
exit 0