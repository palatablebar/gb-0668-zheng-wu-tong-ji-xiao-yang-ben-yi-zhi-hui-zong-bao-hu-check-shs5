from copy import deepcopy
from app.modules.m3_model.service import execute
from app.modules.m3_model.rules import totals

def test_sample_rectangular(sample):assert sample['model']['complete'];assert len(sample['model']['rows'])==30

def test_sample_total(sample):assert sample['model']['total']==273

def test_sample_conflicts_isolated(sample):
    # TRAP-14
    assert [r['code'] for r in sample['model']['quarantine']].count('CONFLICT')==2

def test_missing_cell_detected(normalized):assert execute(normalized[1:])['missing']==[{'area':'001','category':'C01'}]

def test_source_total_mismatch(normalized):
    # TRAP-21
    rows=deepcopy(normalized);rows[0]['row_total']=999;assert not execute(rows)['complete'];assert execute(rows)['mismatches'][0]['expected']==999

def test_shuffle_equivalent(normalized):
    # TRAP-19
    assert execute(normalized)['rows']==execute(list(reversed(normalized)))['rows']

def test_both_axes_conserve(normalized):
    result=totals(normalized);assert sum(result['row_totals'].values())==sum(result['column_totals'].values())==273


def test_same_cell_id_cannot_name_two_positions(normalized):
    rows=deepcopy(normalized)
    rows[1]['cell_id']=rows[0]['cell_id']
    result=execute(rows)
    assert len([r for r in result['quarantine'] if r['code']=='CONFLICT'])==2
    assert not result['complete']
