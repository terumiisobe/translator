pidstat -p $1 -u 1 60 > samples/REST\(t\)/shopping/$2/CPU/sample_$3.txt &
pidstat -p $1 -r 1 60 > samples/REST\(t\)/shopping/$2/mem/sample_$3.txt &
sar -n DEV 1 60 > samples/REST\(t\)/shopping/$2/net/sample_$3.txt &
sar -d 1 60 > samples/REST\(t\)/shopping/$2/disk/sample_$3.txt &&
cat samples/REST\(t\)/shopping/$2/CPU/sample_$3.txt
