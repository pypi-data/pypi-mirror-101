from processdat import preprocess

def test_preprocess():
	retval = preprocess('Data.csv')
	assert len(retval) == 4