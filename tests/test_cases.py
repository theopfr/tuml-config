
success_case_1 = {
    "input": '''
        testString: "test string";
        testInt: 10;
        testFloat: -2e-3;
        testTrue: true;
        testFalse: false;
        testSection: (
            sectionString: "test string";
            sectionList: [1, 2, 3];
        );
        testList: [1, 2, "test string", (
            listSectionInt: 3;
            listSectionBool: true;
        )];
        lastTestFloat: .3E-7;
        listOfLists: [[1], [2], [3]];
    ''',
    "expected": {
        "testString": "test string",
        "testInt": 10,
        "testFloat": -0.002,
        "testTrue": True,
        "testFalse": False,
        "testSection": {
            "sectionString": "test string",
            "sectionList": [1, 2, 3]
        },
        "testList": [1, 2, "test string", {
            "listSectionInt": 3,
            "listSectionBool": True,
        }],
        "lastTestFloat": 3e-8,
        "listOfLists": [[1], [2], [3]]
    }
}


success_case_2 = {
    "input": '''
        employees: [
            (
                name: "ted";
                age: 43;
            ),
            (
                name: "bill";
                age: 54;
            )
        ];
        section: (
            subSection: (
                subSubSection: (
                    list: [true, false, -20, +10];
                );
            );
        );
    ''',
    "expected": {
        "employees": [
            {
                "name": "ted",
                "age": 43,
            },
            {
                "name": "bill",
                "age": 54,
            }
        ],
        "section": {
            "subSection": {
                "subSubSection": {
                    "list": [True, False, -20, 10]
                }
            }
        }
    }
}
