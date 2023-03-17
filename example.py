from tuml import tuml

parsed = tuml.load("./config.tuml")
print(parsed)



config2 = '''
myKey: "myValue";
myList: ["myItem", 2];
mySection: (
    mySectionKey: "mySectionValue";
    mySectionList: [1, 2, [(a: 1;)]];
);
'''

config1 = '''
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
# myList: [1, [2, 3, (a: "0"; b: (u: "1"; u2: "2"; u3: ["l", "o", "l"];);)]]

config0 = '''
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

config = '''
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

