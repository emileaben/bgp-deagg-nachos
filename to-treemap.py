#!/usr/bin/env python
import sys
import json

d = {'children': []}

with open( sys.argv[1] ) as inf:
   for line in inf:
      line = line.rstrip('\n')
      asn,size,pfx_count,te_count = line.split('\t')
      try:
         size = int(size)
         pfx_count = int( pfx_count )
         te_count = int( te_count ) 
         te_pct = 100.0 * te_count / pfx_count
         d['children'].append(
            {
               'name': asn,
               #'size': size,
               'size': pfx_count,
               'pct': te_pct
            }
         )
      except:
         print >>sys.stderr, "err on line: %s" % line

print json.dumps( d, indent=2 )
