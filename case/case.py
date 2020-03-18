""" Handles report compilation, tranform, and export """
import pandas as pd

class Case():
    def __init__(self, source: pd.DataFrame=None, transformers: list = [], report=None):
        self.source = source
        self.transformers = transformers
        self.report = report
    
    def transform(self, transformer):
        # TODO: add split handling
        self._transformed_data = self.source
        for transformer in self.transformers:
            self._transfomed_data = transformer(self._transformed_data)
            assert self._transformed_data is not None
            
    def compile_report(self):
        report = [transformer.report for transformer in self.transformers]
        return '\n'.join(report)
        
    def export_csv(self, path):
        self._transformed_data.to_csv(path, index=False)
        
    @property
    def report(self):
        if len(self.transformers) < 1:
            self.__report = {'message': 'empty'}
        else:
            self.__report = self.compile_report()
        return self.__report
    
    @report.setter
    def report(self, report):
        if len(self.transformers) < 1:
            self.__report = {'message': 'empty'}
        else:
            self.__report = self.compile_report()
