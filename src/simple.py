def documentize(d:dict, nominal:str)->dict:
  ''' Transforms a `dict` to a suitable MongoDB document.
  
  The function modifies the given object by removing the `nominal` field, and assigning its value to the `_id` field.
  
  Parameters:
    d (dict): The dictionary to transform
    nominal (str): The name of the field to use as the `_id`
  
  Returns:
    dict: The transformed dictionary
  '''
  d['_id'] = d.pop(nominal)
  return d

def pythonize(d: dict, nominal:str) ->dict:
  ''' Transforms a `dict` obtained from a MongoDB document into a `dict` represenation expected in python
  
  The function modifies the given MongoDB document `dict` by removing the `_id` field, and assigning its value to the `nominal` field.
  
  Parameters:
    d (dict): The MongoDB document as a dict
    nominal (str): The name of the field to use instead of `_id`
  
  Returns:
    dict: The transformed dictionary
  '''
  d[nominal]= d.pop('_id')
  return d
