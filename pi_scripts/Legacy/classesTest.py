# classesTest.py
# a file to test the test file...

class TestClass:
    name = ''
    testInstanceVar = ''

    #def __init__(self, name):
    #    self.name = name

#test = TestClass('heyy')
test = TestClass()
test.name = 'heyy1'
print(test.name)
test.testInstanceVar = 123
test.testInstanceVar += 5
print(test.testInstanceVar)