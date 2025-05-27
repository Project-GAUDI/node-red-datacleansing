import standard_converter
from lib import converter_tester
import sys


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

    tester.converter_test_caller("2-35-1", CodeKey, 00, None, None)
    tester.converter_test_caller("2-35-2", CodeKey, "!!", None, None)
    tester.converter_test_caller("2-35-3", CodeKey, "aa", None, None)
    tester.converter_test_caller("2-35-4", CodeKey, "ｱｱ", None, None)
    tester.converter_test_caller("2-35-5", CodeKey, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-35-6", CodeKey, "1000", None, None)
    tester.converter_test_caller("2-35-7", CodeKey, "100 200", None, None)
    tester.converter_test_caller("2-35-8", CodeKey, None, None, None)
    tester.converter_test_caller("2-35-9", CodeKey, ["ABC",5384,1295,8752,2], None, "ABC2108051534482")
    tester.converter_test_caller("2-35-10", CodeKey, [123,5384,1295,8752,2], None, "1232108051534482")
    tester.converter_test_caller("2-35-11", CodeKey, [None,5384,1295,8752,2], None, None)
    tester.converter_test_caller("2-35-12", CodeKey, ["ABC","5384","1295","8752","3"], None, "ABC2108051534483")
    tester.converter_test_caller("2-35-13", CodeKey, ["ABC",None,1295,8752,2], None, None)
    tester.converter_test_caller("2-35-14", CodeKey, ["ABC",5384,"DEF",8752,2], None, None)
    tester.converter_test_caller("2-35-15", CodeKey, ["ABC",5384,1295,"/?<",2], None, None)
    tester.converter_test_caller("2-35-16", CodeKey, ["ABC",5384,1295,8752,None], None, None)
    tester.converter_test_caller("2-35-17", CodeKey, ["ABC", sys.maxsize-2, sys.maxsize-1, sys.maxsize, 2], None, "ABC1271271271271271272")
    tester.converter_test_caller("2-35-18", CodeKey, ["ABC", sys.maxsize-1, sys.maxsize, sys.maxsize+1, 2], None, "ABC12712712712700002")
    tester.converter_test_caller("2-35-19", CodeKey, ["ABC",5384,1295,8752,2], 00, "ABC2108051534482")
    tester.converter_test_caller("2-35-20", CodeKey, ["ABC",5384,1295,8752,2], "!!", "ABC2108051534482")
    tester.converter_test_caller("2-35-21", CodeKey, ["ABC",5384,1295,8752,2], [1, "aa"], "ABC2108051534482")
    tester.converter_test_caller("2-35-22", CodeKey, ["ABC",5384,1295,8752,2], None, "ABC2108051534482")

    tester.converter_test_caller("2-36-1", CodeKeySwap, 00, None, None)
    tester.converter_test_caller("2-36-2", CodeKeySwap, "!!", None, None)
    tester.converter_test_caller("2-36-3", CodeKeySwap, "aa", None, None)
    tester.converter_test_caller("2-36-4", CodeKeySwap, "ｱｱ", None, None)
    tester.converter_test_caller("2-36-5", CodeKeySwap, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-36-6", CodeKeySwap, "1000", None, None)
    tester.converter_test_caller("2-36-7", CodeKeySwap, "100 200", None, None)
    tester.converter_test_caller("2-36-8", CodeKeySwap, None, None, None)
    tester.converter_test_caller("2-36-9", CodeKeySwap, ["ABC",2069,3845,12322,2], None, "ABC2108051534482")
    tester.converter_test_caller("2-36-10", CodeKeySwap, [123,2069,3845,12322,2], None, "1232108051534482")
    tester.converter_test_caller("2-36-11", CodeKeySwap, [None,2069,3845,12322,2], None, None)
    tester.converter_test_caller("2-36-12", CodeKeySwap, ["ABC","2069","3845","12322","3"], None, "ABC2108051534483")
    tester.converter_test_caller("2-36-13", CodeKeySwap, ["ABC",None,3845,12322,2], None, None)
    tester.converter_test_caller("2-36-14", CodeKeySwap, ["ABC",2069,"DEF",12322,2], None, None)
    tester.converter_test_caller("2-36-15", CodeKeySwap, ["ABC",2069,3845,"/?<",2], None, None)
    tester.converter_test_caller("2-36-16", CodeKeySwap, ["ABC",2069,3845,12322,None], None, None)
    tester.converter_test_caller("2-36-17", CodeKeySwap, ["ABC", sys.maxsize-2, sys.maxsize-1, sys.maxsize, 2], None, "ABC1271271271271271272")
    tester.converter_test_caller("2-36-18", CodeKeySwap, ["ABC", sys.maxsize-1, sys.maxsize, sys.maxsize+1, 2], None, "ABC12712712712700002")
    tester.converter_test_caller("2-36-19", CodeKeySwap, ["ABC",2069,3845,12322,2], 00, "ABC2108051534482")
    tester.converter_test_caller("2-36-20", CodeKeySwap, ["ABC",2069,3845,12322,2], "!!", "ABC2108051534482")
    tester.converter_test_caller("2-36-21", CodeKeySwap, ["ABC",2069,3845,12322,2], [1, "aa"], "ABC2108051534482")
    tester.converter_test_caller("2-36-22", CodeKeySwap, ["ABC",2069,3845,12322,2], None, "ABC2108051534482")

    tester.converter_test_caller("old", undersub_converter_tester_old, None, None, "All Test Finished Normally.")

    return "All Test Finished Normally."


def undersub_converter_tester_old(input, option):
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