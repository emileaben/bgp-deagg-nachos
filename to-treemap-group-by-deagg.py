#!/usr/bin/env python
import sys
import json

### first argument: input file
### second argument: 'asnsize' or 'pfxcount'


data = []

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
         elif sys.argv[2] == 'pfxcount':
            size = pfx_count
         else:
            print >>sys.stderr, "fatal. 1st argument is inputfile, 2nd argument is 'asnsize' or 'pfxcount'"
            sys.exit(1)
         data.append(
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


data = sorted( data, key=lambda x:x['pct'] )

'''
# chunked into evenly sized pieces

def chunks(l, n):
    """split l in n chunks"""
    size = int( len(l) / n )
    for i in range(0, n):
        yield l[size*i:size*(i+1)-1]

d = {'children': []}
chunk_idx = 0
chunk_count = 9
for chunk in chunks( data, chunk_count ):
   chunk_idx += 1
   chunk_data = {
      #DEBUG 'name': u'chunk {}/{}'.format(chunk_idx,chunk_count),
      'children': []
   }
   for leaf in chunk:
      #DEBUG leaf['chunk'] = chunk_idx
      chunk_data['children'].append( leaf )
   d['children'].append( chunk_data )
'''

#chunked into pieces based on percentage 'categories'
d = {'children': []}
chunk_count = 9
chunk_idx = 0
min_pct = 0
max_pct = 100.0
for idx in range( 0 , chunk_count + 1 ):
   d['children'].append(
      {
         'name': u'chunk {}/{}'.format(idx,chunk_count),
         'children': []
      }
   )
chunk_size = max_pct / chunk_count
this_chunk_max = chunk_size * ( chunk_idx + 1 )
for unit in data:
   if unit['pct'] <= this_chunk_max:
      d['children'][ chunk_idx ]['children'].append( unit )
   else:
      chunk_idx += 1
      this_chunk_max = chunk_size * ( chunk_idx + 1 )
   
print json.dumps( d, indent=2 )
