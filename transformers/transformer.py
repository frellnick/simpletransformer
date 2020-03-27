"""
Transformer
    Base class for transforms
"""
import pandas as pd
import numpy as np

# Base Class
class Transformer():
    def __init__(self, name, report=None):
        self.name = name
        self.input_shape = []
        self.output_shape = []
        self.message = ''
        self.report = report
        
    def __str__(self):
        add_info = ''
        if hasattr(self, '__input_shape'):
            add_info = f':Input: {self.input_shape}, Output: {self.output_shape}'
        
        return f'<Transformer> {self.name}' + add_info
        
    def transform(self, data, message=None):
        # Set report components
        if message is None:
            self.message = 'Nothing to Report'
        else:
            self.message = message
        
        self.output = data
    
    @property
    def report(self):        
        if len(self.input_shape) < 1:
            self.__report = {'message': 'empty'}
        else:
            self.__report = {
                'Transformer': self.name,
                'input_shape': self.input_shape,
                'output_shape': self.output_shape,
                'message': self.message,
            }
        return self.__report
    
    @report.setter
    def report(self, report):
        if report is None:
            self.__report = self.report
        else:
            self.__report = report


#####################
## Derived Classes ##
#####################


class SplitTransform(Transformer):
    def __init__(self, n=2, size=None, data: pd.DataFrame = None):
        super().__init__(name='split')
        self.transform(data, n, size)
    
    def transform(self, data, n, size):
        assert type(data) == pd.DataFrame
        if size is not None:
            assert sum(size) == 1, 'Split fractions must sum to 1.0'
            assert len(size) == n, 'Must provide fractions for all splits'
        # Get data length
        dlen = len(data)
        # Define breakpoints
        if size is None:
            size = [1/n for _ in range(n)]
        
        breakpoints = []
        for count, fraction in enumerate(size):
            if count == 0:
                point = fraction * dlen
            else:
                point = fraction * dlen + breakpoints[count - 1]
            
            breakpoints.append(int(point))
        
        # Fix breakpoints :(\)
        breakpoints.insert(0, 0)
        breakpoints.pop()
            
        # print('Breakpoints: ', breakpoints)  # DEBUG
            
        # Bin dataframe at breakpoints
        new_data = {}
        for index in range(len(breakpoints)):
            if index < len(breakpoints) - 1:
                # print('{}:{}'.format(breakpoints[index], breakpoints[index+1]))  # DEBUG
                temp = data.iloc[breakpoints[index]:breakpoints[index+1]]
            else:
                temp = data.iloc[breakpoints[index]:dlen]
                      
            new_data[index] = temp
        
        
        # Create report components
        self.input_shape = data.shape
        self.output_shape = {key: new_data[key].shape for key in new_data}
        message = f'Data successfully split into {len(new_data)} pieces'
        
        # print(len(new_data))  # DEBUG
        
        return super().transform(data=new_data, message=message)


class InsertNullTransform(Transformer):
    def __init__(self, n=0, column=None, column_index=0, fraction=0.1, data = None):
        super().__init__(name='insert_null')
        self.transform(data=data, n=n, column=column, column_index=column_index, fraction=fraction)
        
    def transform(self, data, n, column, column_index, fraction):
        # Standardize access to data
        try:
            new_data = self.standardize_data(data)
            mod_data = new_data[n].copy()
        except:
            print('n is too large.  Pick an n < {}'.format(len(self.standardize_data(data))))
            raise
        
        # Infer column selection
        iloc_list = self.infer_column(mod_data, column, column_index)

        # Replace fraction of values in mod_column with np.nan
        mod_columns = self.inject_nan(
            columns = mod_data.iloc[:, iloc_list],
            fraction = fraction
        )

        # Update mod_data 
        mod_data.iloc[:, iloc_list] = mod_columns
        print(mod_data)
        
        # Replace dataset with modified dataset
        new_data[n] = mod_data

        # Create report components
        self.input_shape = data.shape
        self.output_shape = {key: new_data[key].shape for key in new_data}
        message = f'Nulls successfully inserted into set {n}, column{iloc_list}'
        
        return super().transform(data=new_data, message=message)
    
    def standardize_data(self, data):
        if type(data) == pd.DataFrame:
            new_data = {0: data}
        elif type(data) == dict:
            new_data= data
            
        return new_data

    def infer_column(self, data, column, column_index):
        assert type(data) == pd.DataFrame, "Data must be type Pandas DataFrame for inference"
        # Test All Columns Case
        if column is None and column_index is None:
            iloc_list = [True]*len(data.columns)
            raise NotImplementedError
        # Test Named Column(s) Case
        elif column is not None:
            raise NotImplementedError
        # Test column_index case
        elif column_index is not None:
            iloc_list = [False] * len(data.columns)
            if type(column_index) == int:
                iloc_list = [column_index]
            elif type(column_index) == list:
                raise NotImplementedError
                for index in column_index:
                    iloc_list[index] = True
        return iloc_list


    def inject_nan(self, columns, fraction):
        nulled_indices = np.random.choice(
            a = range(len(columns)),
            size = int(len(columns) * fraction),
            replace = False
        )
        new_columns = columns.copy()
        new_columns.iloc[nulled_indices] = np.nan
        return new_columns
