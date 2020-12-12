# slot_validation
Django REST Api to validate slot values.

# Running locally
- Make sure to have python 3.6 version installed along with latest pip version.
- Run `pip3 install -r req.txt` to install the dependencies.
- Run `python3 manage.py runserver 0.0.0.0:8000` to start the server
- Server will run on port `8000`

# Running it using docker
- `docker build -t <tagname of your choice> . `
- `docker run -p 8000:8000 -it <tagname>`
- Server will run on port `8000` , use the apis below to test the same
- Docker image size is `173 MB`

# Assumptions
### In Api `/slot_values` (To validate a slot with a finite set of values.)
- `pick_first` & `support_multiple` is contradicting when both are true , hence priority is given to `pick_first`. So if both are set to True in the sample request, the `ids_stated` in params will be a string instead of a list.
- When subset of values are valid and `support_multiple` is true the `ids_stated` is a list of supported IDs returned, otherwise `parameters` is a empty dictionary. | **Note : `pick_first` is given priority here as well.** |

### In Api `/slot_numeric` (To validate a slot with a numeric value extracted and constraints on the value extracted.)
- `pick_first` & `support_multiple` is contradicting when both are true , hence priority is given to `pick_first`. So if both are set to True in the sample request, the `ids_stated` in params will be a string instead of a list.
- If all are valid sending only the first element that has satisfied the constraint as per the example testcase stated below :
```
[                              | true,                  |
|   {                          | false,                 |
|     "entity_type": "number", | "",                    |
|     "value": 24              | {'age_stated': 24}     |
|   },                         |                        |
|   {                          |                        |
|     "entity_type": "number", |                        |
|     "value": 22              |                        |
|   }                          |                        |
| ]                            |   
```
even though both 24 and 22 are valid numbers , only 24 is returned assuming that it is the first value validated.
- If `support_multiple` is true all values satisfying the constraint are returned, Otherwise only the first element that has satisfied the constraint is returned.

# API's
## To validate a slot with a finite set of values.
```bash
curl --location --request POST 'http://localhost:8000/slot_values' \
--header 'Content-Type: application/json' \
--data-raw '{
  "invalid_trigger": "invalid_ids_stated",
  "key": "ids_stated",
  "name": "govt_id",
  "reuse": true,
  "support_multiple": true,
  "pick_first": false,
  "supported_values": [
    "pan",
    "aadhaar",
    "college",
    "corporate",
    "dl",
    "voter",
    "passport",
    "local"
  ],
  "type": [
    "id"
  ],
  "validation_parser": "finite_values_entity",
  "values": [
    {
      "entity_type": "id",
      "value": "college"
    },
    {
      "entity_type": "id",
      "value": "aadhaar"
    }
  ]
}'
```

## To validate a slot with a numeric value extracted and constraints on the value extracted.

```bash
curl --location --request POST 'http://localhost:8000/slot_numeric' \
--header 'Content-Type: application/json' \
--data-raw '{
  "invalid_trigger": "invalid_age",
  "key": "age_stated",
  "name": "age",
  "support_multiple": true,
  "reuse": true,
  "pick_first": true,
  "type": [
    "number"
  ],
  "validation_parser": "numeric_values_entity",
  "constraint": "x>=18 and x<=30",
  "var_name": "x",
  "values": [
    {
      "entity_type": "number",
      "value": 20
    }, {
      "entity_type": "number",
      "value": -2
    }
  ]
}'
```