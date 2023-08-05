#!/usr/bin/env python
# coding: utf-8

# In[3]:


class mortgageError(Exception):
    '''Mortgage subpackage custom exception class.'''
    pass

class FilterInputError(mortgageError):
    '''Raised when property filter receives a non dataframe object'''
    pass

class FormatError(mortgageError):
    '''Raised when a function's input has an improper format'''
    pass

class TermError(mortgageError):
    '''Raised if term length is is unavailable. Terms must range from (1,10) years.'''
    pass

class PovertyError(mortgageError):
    '''Raised when downpayment input value is too low to be legally considered'''
    pass

