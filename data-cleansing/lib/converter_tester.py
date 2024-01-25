import json
import sys

class converter_tester():
    # エラーケースはexpectedResult: Noneで指定すること
    def converter_test_caller(self, label, func, inputs, options, expectedResult):

        testStatus = True
        result = None
        failedMsg = "test failed."
        unmacthMsg = "unmatch result."
        exceptMsg = "exception occurred."
        commonMsg = label + ": " + str(func.__name__) + "( " + str(inputs) + ", " + str(options) + " )" + " --> "

        try:
            result = func(inputs, options)

            expectedObject = {"result": expectedResult}
            resultObject = {"result": result}
            if not (json.dumps(expectedObject, ensure_ascii=True) == json.dumps(resultObject, ensure_ascii=True)):
                testStatus = False
                result = str(result) + " … " + unmacthMsg

        except Exception as e:
            if (expectedResult == None):
                result = str(e) + " … " + exceptMsg
            else:
                testStatus = False
                result = str(e) + " … " + failedMsg

        print(commonMsg + str(result), file=sys.stderr)

        if False == testStatus:
            raise Exception(result)
            # skip

        return
