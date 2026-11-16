import csv
import io
import json
from app.manifest import manifest

def finalize(raw,params,elapsed,summary):
    info=manifest(raw,params,elapsed)
    return info,{'rows':[{'run_id':info['run_id'],'sha256':info['sha256'],'version':info['rule_version'],'elapsed_ms':info['elapsed_ms'],'status':'通过' if summary['balanced'] else '待复核'}],'params':params}

def evidence_csv(result):
    from app.errors import DomainError
    if not result['reconcile']['balanced']:raise DomainError('UNSAFE_RELEASE','发布检查未通过',409)
    out=io.StringIO(newline='');writer=csv.writer(out)
    writer.writerow(['地区','类别','发布人数','发布状态'])
    for row in result['calculate']['rows']:writer.writerow([row['area'],row['category'],row['published'],row['status']])
    return '\ufeff'+out.getvalue()
