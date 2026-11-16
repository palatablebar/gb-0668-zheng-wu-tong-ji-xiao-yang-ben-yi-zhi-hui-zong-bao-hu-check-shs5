from copy import deepcopy
from app.modules.m3_model.service import execute as model
from app.modules.m4_calculate.service import execute as calculate
from app.modules.m6_reconcile.rules import verify

def test_sample_balanced(sample):assert sample['reconcile']['balanced']

def test_sample_rows_conserve(sample):assert sample['reconcile']['input']==36;assert sample['reconcile']['accepted']==30;assert sample['reconcile']['isolated']==6

def test_sample_equations_all_safe(sample):assert all(r['hidden']!=1 for r in sample['reconcile']['rows'])

def test_bad_total_blocks_release(normalized):
    rows=deepcopy(normalized);rows[0]['row_total']=0;m=model(rows);a=calculate(m,5);assert not verify(m,a)['balanced']

def test_primary_only_is_reconstructible(normalized):
    m=model(normalized);a=calculate(m,5);a['hidden']=a['primary'];assert verify(m,a)['unsafe']

def test_equations_include_every_axis(normalized):
    m=model(normalized);a=calculate(m,5);assert len(verify(m,a)['rows'])==11

def test_missing_cell_blocks_release(normalized):
    m=model(normalized[1:]);assert not verify(m,calculate(m,5))['balanced']
