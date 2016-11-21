#!/usr/bin/env python2
import sys
import json
from collections import defaultdict

### first argument: input file
### second argument: 'asnsize', 'pfxcount', or 'country'


d = {'children': []}

# AS to country mapping:
as2cat = {}
cat_count = defaultdict(lambda : {"pfx_count":0, "te_count":0, "asnsize":0})
if sys.argv[2] == 'country':
    with open( "as2cc.txt", "r" ) as ccFile:
        for line in ccFile:
            w = line.split("\t")
            as2cat[w[0]] = w[1]

# AS to business type mapping:
if sys.argv[2] == 'business':
    with open( "as2business.txt", "r" ) as catFile:
        for line in catFile:
            w = line.split(" ")
            as2cat[w[0]] = w[1]



with open( sys.argv[1] ) as inf:
   for line in inf:
      line = line.rstrip('\n')
      asn,asnsize,pfx_count,te_count = line.split('\t')
      try:
         pfx_count = int( pfx_count )
         te_count = int( te_count ) 
         te_pct = 100.0 * te_count / pfx_count
         asnsize = int(asnsize)
         size = None
         if sys.argv[2] == 'asnsize':
            size = int(asnsize)
            d['children'].append(
            {
                'name': asn,
                'size': size,
                'pc': pfx_count,
                'as': asnsize,
                'pct': te_pct
                }
            )
         elif sys.argv[2] == 'pfxcount':
            size = pfx_count
            d['children'].append(
                {
                'name': asn,
                'size': size,
                'pc': pfx_count,
                'as': asnsize,
                'pct': te_pct
                }
            )
         elif sys.argv[2] == 'country' or sys.argv[2] == 'business':
            if asn in as2cat:
                cc = as2cat[asn]
            else:
                cc = "n/a"
            cat_count[cc]["pfx_count"] += pfx_count
            cat_count[cc]["te_count"] += te_count
            cat_count[cc]["asnsize"] += asnsize
         else:
            print >>sys.stderr, "fatal. 1st argument is inputfile, 2nd argument is 'asnsize' or 'pfxcount'"
            sys.exit(1)
      except Exception,e:
         print >>sys.stderr, "err on line: %s" % line
         print >>sys.stderr, e



# Compute percentage for countries:
for k, v in cat_count.iteritems():
    d["children"].append(
        {
        "name": k,
        "size": v["pfx_count"],
        "pc": v["pfx_count"],
        "as": v["asnsize"],
        "pct": 100.0*v["te_count"]/v["pfx_count"]
        }
    )

print json.dumps( d, indent=2 )
