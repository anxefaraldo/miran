#!/bin/sh

mydir=`dirname "$0"`
infile="$1"
outfile="$2"

if [ t"$infile" = "t" ] || [ t"$outfile" = "t" ]; then
    echo "Usage: $0 infile.wav outfile.txt"
    exit 2
fi

mkdir -p "$mydir"/out || exit 1

echo "Processing input WAV file $infile, writing results to $outfile..." 1>&2

# We want output like
#
# Bb<TAB>minor
#
# Our Sonic Annotator output gives us something like that for each
# detected key change (the feature label, in column 4), but we want
# the modal key (modal in the statistical rather than the musical
# sense!) and Sonic Annotator doesn't retain labels for summaries.  So
# let's write to a temporary file, retrieve the modal value, then pick
# the label (from earlier in the file) whose value corresponds to it.

VAMP_PATH="$mydir" "$mydir"/sonic-annotator \
    -t "$mydir"/qm-keydetector.ttl \
    -w csv --csv-separator ";" \
    --csv-basedir "$mydir/out" \
    --csv-force \
    -S mode \
    "$infile" || exit 1

inbase=`basename "$infile"`
inbase=${inbase%.*}
tempfile="$mydir/out/${inbase}_vamp_qm-vamp-plugins_qm-keydetector_key.csv"
if [ ! -f "$tempfile" ]; then
    echo "Key output file $tempfile not found! bailing out"; exit 1
fi

mode=`grep ';mode;' "$tempfile" | awk -F';' '{ print $4; }'`

cat "$tempfile" | \
    awk -F';' '{ print $2, $3 }' | \
    grep "^$mode \"" | \
    head -n 1 | \
    sed -e 's/^[^"]*"//' -e 's/"[^"]*$//' -e 's,/ [^ ]* ,,' -e 's/ /\ /' \
    > "$outfile"




