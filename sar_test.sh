pidstat -p $1 -u 1 15 > samples/REST\(t\)/$2/CPU/sample_$3.txt &
pidstat -p $1 -r 1 15 > samples/REST\(t\)/$2/mem/sample_$3.txt &
sar -n DEV 1 15 > samples/REST\(t\)/$2/net/sample_$3.txt &
sar -d 1 15 > samples/REST\(t\)/$2/disk/sample_$3.txt
