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
        jsonresp['trigger'] = ""
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
        jsonresp['parameters']['ids_stated'] = ','.join(ids)
    else:
        jsonresp['parameters']['ids_stated'] = ids

    if not jsonresp['filled']:
        del jsonresp['parameters']['ids_stated']

    if jsonresp['partially_filled']:
        jsonresp['trigger'] = invalid_trigger
    else:
        jsonresp['trigger'] = ""
    
    return jsonresp