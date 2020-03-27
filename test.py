"""
Dev tests (Not full unit testing)
"""

import pandas as pd
from transformers import Transformer, SplitTransform, InsertNullTransform


# SetUp
source = pd.read_csv('source_complete.csv', encoding='latin-1').head(20)

# Instantiate a base class transformer
t = Transformer(name='test')
t.transform(source)
print('Null transform successful')

# Test split transformer
st = SplitTransform(n=4, size=[0.25, 0.5, 0.15, 0.1], data=source.copy())
assert(len(st.report['output_shape'])==4)
print(st.report)

# Test insert null transformer
nt = InsertNullTransform(n=0, column=None, column_index=1, fraction=0.5, data=source.copy())
print(nt.report)