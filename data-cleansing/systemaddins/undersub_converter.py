import standard_converter
from lib import converter_tester


def CodeKey(input, option):
    """
    CodeKey生成
    　入力データを文字列化して連結する

    Args:
        input[0] (int): ラインNo.
        input[1] (int): 上位：年下２桁、下位：月
        input[2] (int): 上位：日、下位：時
        input[3] (int): 上位：分、下位：秒
        input[4] (int): 機種情報
        option (any): 未使用

    Returns:
        str: CodeKey文字列

    """
    retValue = ""
    joinList = []

    if None in input[0:5]:
        raise Exception("Input can not be None")

    joinList.append(str(input[0]))
    joinList.append(standard_converter.change_normal(int(input[1])))
    joinList.append(standard_converter.change_normal(int(input[2])))
    joinList.append(standard_converter.change_normal(int(input[3])))
    joinList.append(str(input[4]))

    retValue = "".join(joinList)

    return retValue


def CodeKeySwap(input, option):
    """
    CodeKey生成日付部swap付き
    　入力データを文字列化して連結する。
    　日時データ部は、上位・下位の入れ替えを行う

    Args:
        input[0] (int): ラインNo.
        input[1] (int): 下位：年下２桁、上位：月
        input[2] (int): 下位：日、上位：時
        input[3] (int): 下位：分、上位：秒
        input[4] (int): 機種情報
        option (any): 未使用

    Returns:
        str: CodeKey文字列

    """
    retValue = ""
    joinList = []

    if None in input[0:5]:
        raise Exception("Input can not be None")

    joinList.append(str(input[0]))
    joinList.append(standard_converter.change_normal_swap(int(input[1])))
    joinList.append(standard_converter.change_normal_swap(int(input[2])))
    joinList.append(standard_converter.change_normal_swap(int(input[3])))
    joinList.append(str(input[4]))

    retValue = "".join(joinList)

    return retValue


def undersub_converter_tester(input, option):
    tester = converter_tester.converter_tester()

    tester.converter_test_caller("2-2-1-1", CodeKey, [None,5384,1295,8752,2], None, None)
    tester.converter_test_caller("2-2-1-2", CodeKey, [1,5384,None,8752,2], None, None)
    tester.converter_test_caller("2-2-1-3", CodeKey, [1,5384,1295,8752,None], None, None)
    tester.converter_test_caller("2-2-1-4", CodeKey, ["ABC",5384,1295,8752,2], None, "ABC2108051534482")
    tester.converter_test_caller("2-2-1-5", CodeKey, [1,"ABC",1295,8752,2], None, None)
    tester.converter_test_caller("2-2-1-6", CodeKey, [1,5384,"ABC",8752,2], None, None)
    tester.converter_test_caller("2-2-1-7", CodeKey, [1,5384,1295,"ABC",2], None, None)
    tester.converter_test_caller("2-2-1-8", CodeKey, [1,5384,1295,8752,"ABC"], None, "1210805153448ABC")
    tester.converter_test_caller("2-2-1-9", CodeKey, [1,5384,1295,8752,2], None, "12108051534482")
    tester.converter_test_caller("2-2-1-10", CodeKey, ["1","5384","1295","8752","2"], None, "12108051534482")
    tester.converter_test_caller("2-2-1-11", CodeKey, [1,5384,1295,8752], None, None)

    tester.converter_test_caller("2-2-2-1", CodeKeySwap, [None,2069,3845,12322,2], None, None)
    tester.converter_test_caller("2-2-2-2", CodeKeySwap, [1,2069,None,12322,2], None, None)
    tester.converter_test_caller("2-2-2-3", CodeKeySwap, [1,2069,3845,12322,None], None, None)
    tester.converter_test_caller("2-2-2-4", CodeKeySwap, ["ABC",2069,3845,12322,2], None, "ABC2108051534482")
    tester.converter_test_caller("2-2-2-5", CodeKeySwap, [1,"ABC",3845,12322,2], None, None)
    tester.converter_test_caller("2-2-2-6", CodeKeySwap, [1,2069,"ABC",12322,2], None, None)
    tester.converter_test_caller("2-2-2-7", CodeKeySwap, [1,2069,3845,"ABC",2], None, None)
    tester.converter_test_caller("2-2-2-8", CodeKeySwap, [1,2069,3845,12322,"ABC"], None, "1210805153448ABC")
    tester.converter_test_caller("2-2-2-9", CodeKeySwap, [1,2069,3845,12322,2], None, "12108051534482")
    tester.converter_test_caller("2-2-2-10", CodeKeySwap, ["1","2069","3845","12322","2"], None, "12108051534482")
    tester.converter_test_caller("2-2-2-11", CodeKeySwap, [1,2069,3845,12322], None, None)

    return "All Test Finished Normally."
