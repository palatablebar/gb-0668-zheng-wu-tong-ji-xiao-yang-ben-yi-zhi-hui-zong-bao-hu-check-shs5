import pytest
from app.pipeline import run
from app.config import ROOT
from app.modules.m1_intake.rules import parse
from app.modules.m2_contract.service import execute

@pytest.fixture
def sample():return run({'sample':'dirty'})

@pytest.fixture
def normalized():return execute(parse((ROOT/'sample_data/clean.csv').read_bytes())['rows'])['rows']

@pytest.fixture(autouse=True)
def temporary_database(tmp_path,monkeypatch):monkeypatch.setenv('DB_PATH',str(tmp_path/'record.sqlite'))
