import pytest
from app.modules.m2_contract.rules import integer,convert
from app.errors import DomainError

def test_sample_contract_count(sample):assert sample['contract']['accepted']==33

def test_sample_missing_not_zero(sample):
    # TRAP-07
    assert any(x['code']=='NULL_VALUE' for x in sample['contract']['quarantine'])

def test_sample_leading_zero(sample):
    # TRAP-08
    assert sample['contract']['rows'][0]['area']=='001'

def test_fullwidth_thousands():
    # TRAP-06
    assert integer('１,２３４','人数')==1234

def test_non_integer_rejected():
    with pytest.raises(DomainError):integer('1.01','人数')

def test_negative_rejected():
    with pytest.raises(DomainError):integer('-1','人数')

def test_zero_count_allowed():assert integer('0','人数')==0

def test_weight_zero_rejected():
    with pytest.raises(DomainError) as exc:integer('0','权重',True)
    assert exc.value.code=='WEIGHT'


def test_extreme_count_rejected():
    with pytest.raises(DomainError):integer('1e1000000','人数')
