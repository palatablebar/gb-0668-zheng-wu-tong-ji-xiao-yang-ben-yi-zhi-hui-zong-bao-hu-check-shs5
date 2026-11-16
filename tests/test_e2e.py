from fastapi.testclient import TestClient
from app.main import app

def test_all_seven_pages_and_publication():
    client=TestClient(app);response=client.post('/api/batches',json={'sample':'dirty'});assert response.status_code==200;rid=response.json()['manifest']['run_id']
    for page in ('intake','contract','model','calculate','quarantine','reconcile','batches'):assert client.get('/'+page+'?run='+rid).status_code==200
    assert client.get('/api/export/'+rid).status_code==200

def test_bad_header_http422():assert TestClient(app).post('/api/intake',json={'csv':'x,y\n1,2'}).status_code==422

def test_clean_dirty_same_path():
    client=TestClient(app);a=client.post('/api/batches',json={'sample':'clean'}).json();b=client.post('/api/batches',json={'sample':'dirty'}).json();assert a['quarantine']['count']==0;assert b['quarantine']['count']==6;assert a['calculate']['rows']==b['calculate']['rows']
