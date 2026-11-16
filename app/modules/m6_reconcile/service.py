from .rules import verify

def execute(intake,model,calculation,quarantine):
    check=verify(model,calculation)
    accepted=model['accepted'];isolated=quarantine['count'];row_delta=intake['input']-accepted-isolated
    return check|{'input':intake['input'],'accepted':accepted,'isolated':isolated,'row_delta':row_delta,'balanced':check['balanced'] and row_delta==0,'mismatches':model['mismatches'],'missing':model['missing']}
