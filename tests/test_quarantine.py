from app.modules.m5_quarantine.service import execute
from app.modules.m5_quarantine.rules import filter_rows,classify

def test_sample_six_bad(sample):assert sample['quarantine']['count']==6

def test_sample_bad_have_evidence(sample):assert all(x['line']>1 and x['raw'] for x in sample['quarantine']['rows'])

def test_sample_bad_distribution(sample):assert sum(x['count'] for x in sample['quarantine']['reasons'])==6

def test_empty_quarantine():assert execute([])['count']==0

def test_reason_filter():assert filter_rows([{'code':'X'},{'code':'Y'}],'X')==[{'code':'X'}]

def test_counts_by_reason():assert classify([{'code':'X'},{'code':'X'}])[0]['count']==2

def test_repairable_missing():assert execute([{'code':'NULL_VALUE'}])['recoverable']==1
