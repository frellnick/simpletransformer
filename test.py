"""
Dev tests (Not full unit testing)
"""

import pandas as pd
from transformers import Transformer


# SetUp
source = pd.read_csv('source_complete.csv', encoding='latin-1')

# Instantiate a base class transformer
t = Transformer(name='test')
t.transform(source)
assert len(str(t).split()) < len(t.report)
print('Null transform successful')

