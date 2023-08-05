# cvsser
**cvsser** is a simple library for interpreting CVSS vector strings and converting their metrics into ready-to-publish formats.

```
>>> import cvsser
>>> import json
>>> sample = "CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C"
>>> vs = cvsser.VectorString(sample)
>>> print(vs.privileges_required)
N
>>> print(json.dumps(vs.to_dict(style="verbose", parentheticals="values", include="mandatory"), indent=2))
{
  "AV": {
    "metric": "Attack Vector",
    "value": "Local (L)"
  },
  "AC": {
    "metric": "Attack Complexity",
    "value": "High (H)"
  },
  "PR": {
    "metric": "Privileges Required",
    "value": "None (N)"
  },
  "UI": {
    "metric": "User Interaction",
    "value": "Required (R)"
  },
  "S": {
    "metric": "Scope",
    "value": "Unchanged (U)"
  },
  "C": {
    "metric": "Confidentiality Impact",
    "value": "High (H)"
  },
  "I": {
    "metric": "Integrity Impact",
    "value": "High (H)"
  },
  "A": {
    "metric": "Availability Impact",
    "value": "High (H)"
  }
}
>>> print(json.dumps(vs.guide, indent=2))
{
  "v2.0": {
    "AV": {
      "name": "Access Vector",
      "values": {
        "L": "Local",
        "A": "Adjacent Network",
        "N": "Network"
      },
      "type": "Base",
      "mandatory": true
    },
    "AC": {
      "name": "Access Complexity",
      "values": {
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Base",
      "mandatory": true
    },
...
```

## Installing cvsser
cvsser is available on PyPI:

```console
$ python -m pip install cvsser
```
