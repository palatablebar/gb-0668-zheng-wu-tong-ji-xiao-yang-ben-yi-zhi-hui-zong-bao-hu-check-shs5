from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TITLE = '政务统计小样本抑制与汇总保护检查'
SHORT = 'statguard'
VERSION = '2026.11.1'
COLUMNS = ['cell_id', 'area', 'category', 'count', 'weight', 'row_total', 'column_total', 'note']
PAGES = [('intake', '底表采信'), ('contract', '发布契约'), ('model', '汇总建模'), ('calculate', '抑制求解'), ('quarantine', '质量隔离'), ('reconcile', '泄露复核'), ('batches', '发布归档')]
MAX_BYTES = 2_000_000
MAX_ROWS = 10000
NULLS = frozenset(['', '-', 'N/A', 'NULL', '未知'])
