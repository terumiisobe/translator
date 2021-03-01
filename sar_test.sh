pidstat -p $1 -u 1 25 > samples/SOAP\(t\)/shopping/$2/CPU/sample_$3.txt &
pidstat -p $1 -r 1 25 > samples/SOAP\(t\)/shopping/$2/mem/sample_$3.txt &
sar -n DEV 1 25 > samples/SOAP\(t\)/shopping/$2/net/sample_$3.txt &
sar -d 1 25 > samples/SOAP\(t\)/shopping/$2/disk/sample_$3.txt &&
cat samples/SOAP\(t\)/shopping/$2/CPU/sample_$3.txt
