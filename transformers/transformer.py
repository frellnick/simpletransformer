"""
Transformer
    Base class for transforms
"""
import pandas as pd

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
        return data
    
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
            
        print('Breakpoints: ', breakpoints)
            
        # Bin dataframe at breakpoints
        new_data = {}
        for index in range(len(breakpoints)):
            if index < len(breakpoints) - 1:
                print('{}:{}'.format(breakpoints[index], breakpoints[index+1]))
                temp = data.iloc[breakpoints[index]:breakpoints[index+1]]
            else:
                temp = data.iloc[breakpoints[index]:dlen]
                      
            new_data[index] = temp
        
        
        # Create report components
        self.input_shape = data.shape
        self.output_shape = {key: new_data[key].shape for key in new_data}
        message = f'Data successfully split into {len(new_data)} pieces'
        
        print(len(new_data))
        
        super().transform(data=new_data, message=message)
