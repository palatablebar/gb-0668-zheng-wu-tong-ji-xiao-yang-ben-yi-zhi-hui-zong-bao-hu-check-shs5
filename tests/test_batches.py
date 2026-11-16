import pytest
from app import store
from app.errors import DomainError
from app.modules.m7_batches.service import evidence_csv
from app.modules.m7_batches.rules import validate

def test_sample_idempotency(sample):
    a=store.save(sample);b=store.save(sample);assert a['created'];assert not b['created'];assert len(store.history())==1

def test_sample_stale_review(sample):
    # TRAP-26
    a=store.save(sample);store.review(a['manifest']['run_id'],1)
    with pytest.raises(DomainError) as exc:store.review(a['manifest']['run_id'],1)
    assert exc.value.status==409

def test_sample_published_csv_hides_values(sample):
    exported=evidence_csv(sample);assert '主抑制' in exported;assert exported.count('—')==12;assert len(exported.splitlines())==31

def test_threshold_changes_run_id():
    from app.pipeline import run
    assert run({'sample':'clean','params':{'threshold':5}})['manifest']['run_id']!=run({'sample':'clean','params':{'threshold':3}})['manifest']['run_id']

def test_unsafe_export_rejected(sample):
    sample['reconcile']['balanced']=False
    with pytest.raises(DomainError):evidence_csv(sample)

def test_threshold_zero_rejected():
    with pytest.raises(DomainError):validate({'threshold':0},{'threshold':5})

def test_unknown_parameter_rejected():
    with pytest.raises(DomainError):validate({'random':5},{'threshold':5})
