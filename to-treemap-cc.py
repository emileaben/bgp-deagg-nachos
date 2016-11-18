#!/usr/bin/env python
import sys
import json

### first argument: input file
### second argument: 'asnsize' or 'pfxcount'
### 3rd argument output dir

asn2cc = {}
ccset = set()
with open('as2cc.txt') as inf:
   for line in inf:
      line = line.rstrip('\n')
      asn,cc = line.split('\t')
      asn2cc[asn] = cc
      ccset.add( cc )

# first level will be ASN:
d = {} # d ={'children': []}
for cc in ccset:
   d[cc] = {'children': []}

outdir = sys.argv[3]

with open( sys.argv[1] ) as inf:
   for line in inf:
      line = line.rstrip('\n')
      asn,asnsize,pfx_count,te_count = line.split('\t')
      try:
         cc = asn2cc[ asn ]
         pfx_count = int( pfx_count )
         te_count = int( te_count ) 
         te_pct = 100.0 * te_count / pfx_count
         asnsize = int(asnsize)
         size = None
         if sys.argv[2] == 'asnsize':
            size = int(asnsize)
         elif sys.argv[2] == 'pfxcount':
            size = pfx_count
         else:
            print >>sys.stderr, "fatal. 1st argument is inputfile, 2nd argument is 'asnsize' or 'pfxcount'"
            sys.exit(1)
         d[cc]['children'].append(
            {
               'name': asn,
               'size': size,
               'pc': pfx_count,
               'as': asnsize,
               'pct': te_pct
            }
         )
      except:
         print >>sys.stderr, "err on line: %s" % line

for cc in d.keys():
   with open("{}/{}.{}.json".format( outdir, cc, sys.argv[2] ), 'w') as outf:
      print >>outf, json.dumps( d[cc], indent=2 )
