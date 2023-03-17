import tuml


# example of loading a tuml file
parsed = tuml.load("./example.tuml")
print(parsed, "\n")


# example of parsing a tuml string
config_string = '''
myKey: "myValue";
myList: ["myItem", 2];
mySection: (
    mySectionKey: "mySectionValue";
    mySectionList: [1, 2, [(a: 1;)]];
);
'''

parsed = tuml.loads(config_string)
print(parsed)


# more examples
config_string_1 = '''
myInt: 9;
mySection: (
    mySectionString: "sub";
    mySubSection: (
        mySubInt: false;
        gett: "hi";
    );
    that: "this";
);
here: "there";

b: (
    inner: [
        (
            name: "ted";
            age: 21;
        ),
        (
            name: "bill";
            age: 33;
        )
    ];
    mhm: -1;
); 
'''

config_string_2 = '''
section1: (
    section2: (
        section3: (
            section4: (
                inner: "lol";
                list: [
                    [
                        [

                        ]
                    ]
                ];
            );
        );
    );
);
'''

config_string_3 = '''
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
    l: [[1], [2], [3]];
    l2: [
        [
            [2]
        ]
    ];
'''

