from app.modules.m4_calculate.rules import suppress,bridges

def cell(key,area,category,count=10,weight=1):return {'cell_id':key,'area':area,'category':category,'count':count,'weight':weight,'line':1}

def test_sample_primary_six(sample):assert len(sample['calculate']['primary'])==6

def test_sample_secondary_six(sample):assert len(sample['calculate']['secondary'])==6

def test_sample_no_leaking_cells(sample):assert sample['calculate']['safe'];assert sample['calculate']['unsafe']==[]

def test_zero_not_primary():assert suppress([cell('a','a','a',0)],5)['primary']==[]

def test_single_small_cell_not_releasable():assert not suppress([cell('a','a','a',2)],5)['safe']

def test_secondary_makes_cycle():
    data=[cell('a','1','x',2),cell('b','1','y'),cell('c','2','x'),cell('d','2','y')];out=suppress(data,5);assert set(out['hidden'])==set('abcd');assert out['safe']

def test_bridge_between_cycles_is_leak():
    data=[cell('a','1','x'),cell('b','1','y'),cell('c','2','x'),cell('d','2','y'),cell('e','2','z'),cell('f','3','z'),cell('g','3','w'),cell('h','4','z'),cell('i','4','w')]
    assert bridges(data,set('abcdefghi'))==['e']

def test_threshold_boundary_public():assert suppress([cell('a','a','a',5)],5)['primary']==[]
