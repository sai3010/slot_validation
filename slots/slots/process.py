from typing import List, Dict, Callable, Tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                invalid_trigger: str = None, key: str = None,
                                support_multiple: bool = True, pick_first: bool = False, **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    jsonresp = {}
    jsonresp['parameters']={}
    ids = []
    if not values:
        jsonresp['filled'] = False
        jsonresp['partially_filled'] = False
        jsonresp['trigger'] = invalid_trigger
        return  jsonresp
        
    for val in values:
        if val['value'] in supported_values:
            jsonresp['filled'] = True
            jsonresp['partially_filled'] = False
            ids.append(val['value'].upper())
        else:
            jsonresp['filled'] = False
            jsonresp['partially_filled'] = True

    if pick_first:
        jsonresp['parameters'][key] = ','.join(ids)
    else:
        jsonresp['parameters'][key] = ids

    if not support_multiple:
        if not jsonresp['filled']:
            del jsonresp['parameters'][key]

    if jsonresp['partially_filled']:
        jsonresp['trigger'] = invalid_trigger
    else:
        jsonresp['trigger'] = ""
    
    return jsonresp

def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    jsonresp={}
    jsonresp['parameters']={}
    age_stated = []
    if constraint == '' or not values:
        jsonresp['filled'] = False
        jsonresp['partially_filled'] = False
        jsonresp['trigger'] = invalid_trigger
        return jsonresp

    for val in values:
        x = val['value']
        if eval(constraint.replace(var_name,str(val['value']))):
            jsonresp['filled'] = True
            jsonresp['partially_filled'] = False
            age_stated.append(x)
        else:
            jsonresp['filled'] = False
            jsonresp['partially_filled'] = True
    if pick_first:
        jsonresp['parameters'][key] = str(",".join(map(str, age_stated))) 
    else:
        jsonresp['parameters'][key] = age_stated

    if not support_multiple:
        if len(age_stated) == 0:
            del jsonresp['parameters'][key]
        elif type(jsonresp['parameters'][key]) == str:
            jsonresp['parameters'][key] = jsonresp['parameters'][key].split(",")[0]
        else:
            jsonresp['parameters'][key] = age_stated[0]

    if jsonresp['partially_filled']:
        jsonresp['trigger'] = invalid_trigger
    else:
        jsonresp['trigger'] = ""
    return jsonresp