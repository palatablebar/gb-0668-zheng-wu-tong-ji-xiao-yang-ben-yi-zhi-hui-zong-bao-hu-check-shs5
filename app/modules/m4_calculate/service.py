from .rules import suppress

def execute(model,threshold):
    result=suppress(model['rows'],threshold)
    return result|{'threshold':threshold,'release_ready':model['complete'] and result['safe'],'published_count':len(model['rows'])-len(result['hidden'])}
