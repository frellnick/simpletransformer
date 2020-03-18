"""
Transformer
    Base class for transforms
"""

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
        # Override with actual transformer.  Default Null transormation
        output = data
        
        # Create report components
        self.input_shape = data.shape
        self.output_shape = output.shape
        if message is None:
            self.message = 'Nothing to Report'
        else:
            self.message = message

        return output
    
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