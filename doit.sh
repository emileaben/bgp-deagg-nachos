DATE=2016-11-01
./to-treemap.py ../data/asnsize.$DATE.txt pfxcount | tee pfxcount/treemap.pfxcount.json 
./to-treemap.py ../data/asnsize.$DATE.txt asnsize | tee asnsize/treemap.asnsize.json 
