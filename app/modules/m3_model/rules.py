from collections import defaultdict
from app.reasons import issue

def deduplicate(rows):
    groups=defaultdict(list)
    for row in rows:groups[(row['area'],row['category'])].append(row)
    good=[];bad=[]
    ids=defaultdict(set)
    for row in rows:ids[row['cell_id']].add((row['area'],row['category']))
    for key,group in sorted(groups.items()):
        if any(len(ids[x['cell_id']])>1 for x in group):bad.extend(issue(x,'CONFLICT') for x in group);continue
        variants={(x['count'],x['weight'],x['row_total'],x['column_total']) for x in group}
        if len(variants)>1:bad.extend(issue(x,'CONFLICT') for x in group)
        else:good.append(group[0]);bad.extend(issue(x,'DUPLICATE') for x in group[1:])
    return good,bad

def totals(rows):
    rowsum=defaultdict(int);colsum=defaultdict(int)
    for r in rows:rowsum[r['area']]+=r['count'];colsum[r['category']]+=r['count']
    mismatches=[]
    for r in rows:
        if rowsum[r['area']]!=r['row_total']:mismatches.append({'line':r['line'],'axis':'行','key':r['area'],'expected':r['row_total'],'actual':rowsum[r['area']]})
        if colsum[r['category']]!=r['column_total']:mismatches.append({'line':r['line'],'axis':'列','key':r['category'],'expected':r['column_total'],'actual':colsum[r['category']]})
    expected={(a,c) for a in rowsum for c in colsum}
    missing=sorted(expected-{(r['area'],r['category']) for r in rows})
    return {'row_totals':dict(rowsum),'column_totals':dict(colsum),'total':sum(rowsum.values()),'mismatches':mismatches,'missing':[{'area':a,'category':c} for a,c in missing],'complete':bool(rows) and not missing and not mismatches}
