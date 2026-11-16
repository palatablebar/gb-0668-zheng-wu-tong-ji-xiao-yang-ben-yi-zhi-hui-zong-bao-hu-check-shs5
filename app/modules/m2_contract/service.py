from .rules import convert
from app.errors import DomainError
from app.reasons import issue

def execute(rows):
    accepted=[];bad=[]
    for row in rows:
        try:accepted.append(convert(row))
        except DomainError as exc:bad.append(issue(row,exc.code,exc.detail))
    return {'rows':accepted,'quarantine':bad,'accepted':len(accepted),'fields':[{'field':k,'definition':v} for k,v in [('count','非负整数，0不视为缺失'),('weight','补充抑制代价'),('area / category','保形文本'),('row_total / column_total','源系统合计')]]}
