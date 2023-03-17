# TUML: Theo's Ugly Markup Language

## What?
TUML is a configuration/markup language very similar to JSON and YAML.


## Why?
I just wanted to write a parser...


## Properties:
- root level keys are allowed (like in YAML, unlike in JSON)
- whitespace is ignored, each expression is ended by a semicolon
- in keys only the characters a-z, A-Z, 0-9 and "_" are allowed
- boolean values are represented as "true" and "false"
- sections are encapsulated by "(" and ")"
- lists are encapsulated by "[" and "]"
- all possible values: String, Integer, Float, Boolean, List, Section
- example:
    ```
    companyName: "Tuml Inc.";
    comanySince: 2023;
    employees: [
        (
            name: "bill";
            age: 43;
            hobbies: ["tennis", "warhammer", "design"];
            isSenior: true;
            salaryPerHour: 40.5;
        ),
        (
            name: "ted";
            age: 32;
            hobbies: ["fitness", "coding", "DnD"];
            isSenior: false;
            salaryPerHour: 35.5;
        )
    ];
    ```


## Parsing:
Loading and parsing a TUML file to a Python dict:
```python
import tuml

parsed = tuml.load("./example.tuml")
```

Parsing a TUML string to a Python dict:
```python
import tuml

config_string = '''
    myKey: "myValue";
    myList: ["myItem", 2];
    mySection: (
        mySectionKey: "mySectionValue";
        mySectionList: [1, 2, [(a: 1;)]];
    );
'''

parsed = tuml.loads(config_string)
```

---

## Todos:
- [ ] add null/none type value
- [ ] add comments
- [ ] dump dict to TUML file
