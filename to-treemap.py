#!/usr/bin/env python
import sys
import json

### first argument: input file
### second argument: 'asnsize' or 'pfxcount'


d = {'children': []}

with open( sys.argv[1] ) as inf:
   for line in inf:
      line = line.rstrip('\n')
      asn,asnsize,pfx_count,te_count = line.split('\t')
      try:
         pfx_count = int( pfx_count )
         te_count = int( te_count ) 
         te_pct = 100.0 * te_count / pfx_count
         size = None
         if sys.argv[2] == 'asnsize':
            size = int(asnsize)
         elif sys.argv[2] == 'pfxcount':
            size = pfx_count
         else:
            print >>sys.stderr, "fatal. 1st argument is inputfile, 2nd argument is 'asnsize' or 'pfxcount'"
            sys.exit(1)
         d['children'].append(
            {
               'name': asn,
               'size': size,
               'pct': te_pct
            }
         )
      except:
         print >>sys.stderr, "err on line: %s" % line

print json.dumps( d, indent=2 )
