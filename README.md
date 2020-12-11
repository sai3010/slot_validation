# slot_validation

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

## API to validate a slot with a numeric value extracted and constraints on the value extracted.

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