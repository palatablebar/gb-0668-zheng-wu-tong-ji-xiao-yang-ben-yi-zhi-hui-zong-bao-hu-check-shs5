REASONS = {'COLUMN_COUNT': '字段数量错误', 'NULL_VALUE': '计数缺失', 'NUMBER': '计数必须为非负整数', 'WEIGHT': '权重必须为正整数', 'DUPLICATE': '相同单元格重复', 'CONFLICT': '单元格存在冲突', 'BALANCE': '合计不一致'}
def issue(row, code, detail=''):
    return {'line': row.get('line', 0), 'code': code, 'detail': detail or REASONS.get(code, code), 'raw': row.get('raw', row)}
