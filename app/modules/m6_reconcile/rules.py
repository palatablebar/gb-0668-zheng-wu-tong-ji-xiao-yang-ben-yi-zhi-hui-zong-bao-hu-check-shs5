from app.modules.m4_calculate.rules import bridges

def verify(model,calculation):
    hidden=set(calculation['hidden'])
    unsafe=bridges(model['rows'],hidden)
    eq=[]
    for axis,key in [('行','area'),('列','category')]:
        labels=sorted({r[key] for r in model['rows']})
        for label in labels:
            records=[r for r in model['rows'] if r[key]==label];unknown=sum(r['cell_id'] in hidden for r in records)
            eq.append({'axis':axis,'key':label,'cells':len(records),'hidden':unknown,'status':'安全' if unknown!=1 else '可还原'})
    return {'rows':eq,'unsafe':unsafe,'total':model['total'],'row_sum':sum(model['row_totals'].values()),'column_sum':sum(model['column_totals'].values()),'balanced':model['complete'] and not unsafe}
