import pytest
from app.config import ROOT,COLUMNS
from app.modules.m1_intake.rules import parse
from app.errors import DomainError

def test_bom_sample(sample):
    # TRAP-02
    assert sample['intake']['input']==36

def test_gb18030_sample():
    # TRAP-01
    data=parse((ROOT/'sample_data/legacy.csv').read_bytes());assert data['encoding']=='gb18030';assert data['rows'][0]['raw']['note']=='就业培训统计'

def test_sample_raw_zero(sample):assert sample['intake']['rows'][2]['raw']['count']=='0'

def test_empty_three_states():
    # TRAP-18
    assert parse(b'')['state']=='EMPTY_FILE';assert parse(b'\n')['state']=='BLANK_ONLY';assert parse(','.join(COLUMNS).encode())['state']=='HEADER_ONLY'

def test_bad_column_isolated():assert parse((','.join(COLUMNS)+'\nx,y').encode())['quarantine'][0]['code']=='COLUMN_COUNT'

def test_duplicate_header_ignored():
    text=','.join(COLUMNS)+'\n';data=parse((text+text).encode());assert data['headers']==1;assert data['input']==0

def test_broken_csv_rejected():
    with pytest.raises(DomainError):parse((','.join(COLUMNS)+'\n"unterminated').encode())
