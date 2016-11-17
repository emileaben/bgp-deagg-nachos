DATE=2016-11-01

# BLOB: ripencc|RU|asn|206817|1|20161031|allocated

ido +dc RIR_STATS +xT $DATE +R -M AS* +M +T | egrep BLOB | perl -F\\\| -lane'$end=$F[3]+$F[4]-1;$start=$F[3]; for ($start..$end) { print "$_\t$F[1]" }'
