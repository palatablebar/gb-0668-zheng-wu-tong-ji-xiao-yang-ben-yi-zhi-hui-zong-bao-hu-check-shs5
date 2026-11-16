import unicodedata
from decimal import Decimal,InvalidOperation
from app.config import NULLS
from app.errors import DomainError

def integer(value,key,positive=False):
    text=unicodedata.normalize('NFKC',value).strip().replace(',','')
    if text in NULLS:raise DomainError('NULL_VALUE',key+'缺失')
    try:number=Decimal(text)
    except InvalidOperation:raise DomainError('NUMBER',key+'不是整数')
    if not number.is_finite() or number>Decimal('1000000000000') or number!=number.to_integral_value() or number<0:raise DomainError('NUMBER',key+'须为非负整数')
    if positive and number==0:raise DomainError('WEIGHT','权重须大于0')
    return int(number)

def convert(row):
    r={k:v.strip() for k,v in row['raw'].items()}
    if any(r[k] in NULLS for k in ('cell_id','area','category')):raise DomainError('NULL_VALUE','分类编码缺失')
    return r|{'line':row['line'],'raw':row['raw'],'count':integer(r['count'],'计数'),'weight':integer(r['weight'],'权重',True),'row_total':integer(r['row_total'],'行合计'),'column_total':integer(r['column_total'],'列合计')}
