from lib import converter_tester

def tracer_tester(input, option):
    """
    Tracerクラスのテスト関数

    Args:
        input (any): 未使用
        option (any): 未使用

    Returns:
        str : 成功時："All Test Finished Normally."
        　　　失敗時は、失敗テストからの例外を発生。
    """
    tester = converter_tester.converter_tester()

    tester.converter_test_caller("2-37-1", tracer_tester1, None, None, [])
    tester.converter_test_caller("2-37-2", tracer_tester2, None, None, ["LABEL:DATA"])
    tester.converter_test_caller("2-37-3", tracer_tester3, None, None, ["LABEL:DATA"])
    tester.converter_test_caller("2-37-4", tracer_tester4, None, None, [])
    tester.converter_test_caller("2-37-5", tracer_tester5, None, None, ["LABEL:DATA"])
    tester.converter_test_caller("2-37-6", tracer_tester6, None, None, ["LABEL:DATA"])
    tester.converter_test_caller("2-37-7", tracer_tester7, None, None, ["DATA"])
    tester.converter_test_caller("2-37-8", tracer_tester8, None, None, ["1:DATA"])
    tester.converter_test_caller("2-37-9", tracer_tester9, None, None, ["None:DATA"])
    tester.converter_test_caller("2-37-10", tracer_tester10, None, None, ["[1, 2, 3]:DATA"])
    tester.converter_test_caller("2-37-11", tracer_tester11, None, None, ["LABEL:DATA"])
    tester.converter_test_caller("2-37-12", tracer_tester12, None, None, ["LABEL:"])
    tester.converter_test_caller("2-37-13", tracer_tester13, None, None, ["LABEL:1"])
    tester.converter_test_caller("2-37-14", tracer_tester14, None, None, ["LABEL:None"])
    tester.converter_test_caller("2-37-15", tracer_tester15, None, None, ["LABEL:[1, 2, 3]"])
    tester.converter_test_caller("2-37-16", tracer_tester16, None, None, [])
    tester.converter_test_caller("2-37-17", tracer_tester17, None, None, ["LABEL:[ 1, 2, 3 ]"])
    tester.converter_test_caller("2-37-18", tracer_tester18, None, None, ["[ 1, 2, 3 ]"])
    tester.converter_test_caller("2-37-19", tracer_tester19, None, None, ["1:[ 1, 2, 3 ]"])
    tester.converter_test_caller("2-37-20", tracer_tester20, None, None, ["None:[ 1, 2, 3 ]"])
    tester.converter_test_caller("2-37-21", tracer_tester21, None, None, ["[1, 2, 3]:[ 1, 2, 3 ]"])
    tester.converter_test_caller("2-37-22", tracer_tester22, None, None, ["LABEL:[ 1, 2, 3 ]"])
    tester.converter_test_caller("2-37-23", tracer_tester23, None, None, ["LABEL:[  ]"])
    tester.converter_test_caller("2-37-24", tracer_tester24, None, None, ["LABEL:DATA"])
    tester.converter_test_caller("2-37-25", tracer_tester25, None, None, ["LABEL:1"])
    tester.converter_test_caller("2-37-26", tracer_tester26, None, None, ["LABEL:None"])
    tester.converter_test_caller("2-37-27", tracer_tester27, None, None, [])
    tester.converter_test_caller("2-37-28", tracer_tester28, None, None, ["DATA"])
    tester.converter_test_caller("2-37-29", tracer_tester29, None, None, [])
    tester.converter_test_caller("2-37-30", tracer_tester30, None, None, ["1"])
    tester.converter_test_caller("2-37-31", tracer_tester31, None, None, ["None"])
    tester.converter_test_caller("2-37-32", tracer_tester32, None, None, ["[1, 2, 3]"])
    tester.converter_test_caller("2-37-33", tracer_tester33, None, None, [])
    tester.converter_test_caller("2-37-34", tracer_tester34, None, None, ["LABEL:"])
    tester.converter_test_caller("2-37-35", tracer_tester35, None, None, [":"])
    tester.converter_test_caller("2-37-36", tracer_tester36, None, None, ["1:"])
    tester.converter_test_caller("2-37-37", tracer_tester37, None, None, ["None:"])
    tester.converter_test_caller("2-37-38", tracer_tester38, None, None, ["[1, 2, 3]:"])
    tester.converter_test_caller("2-37-39", tracer_tester39, None, None, [])
    tester.converter_test_caller("2-37-40", tracer_tester40, None, None, ["DATA"])
    tester.converter_test_caller("2-37-41", tracer_tester41, None, None, [""])
    tester.converter_test_caller("2-37-42", tracer_tester42, None, None, ["1"])
    tester.converter_test_caller("2-37-43", tracer_tester43, None, None, ["None"])
    tester.converter_test_caller("2-37-44", tracer_tester44, None, None, ["[1, 2, 3]"])
    tester.converter_test_caller("2-37-45", tracer_tester45, None, None, [])
    tester.converter_test_caller("2-37-46", tracer_tester46, None, None, ["[1, 2, 3]"])
    tester.converter_test_caller("2-37-47", tracer_tester47, None, None, ["[]"])
    tester.converter_test_caller("2-37-48", tracer_tester48, None, None, ["DATA"])
    tester.converter_test_caller("2-37-49", tracer_tester49, None, None, ["1"])
    tester.converter_test_caller("2-37-50", tracer_tester50, None, None, ["None"])
    tester.converter_test_caller("2-37-51", tracer_tester51, None, None, [])
    tester.converter_test_caller("2-37-52", tracer_tester52, None, None, [" --(COMVNAME(OPTION) )--> "])
    tester.converter_test_caller("2-37-53", tracer_tester53, None, None, [" --((OPTION) )--> "])
    tester.converter_test_caller("2-37-54", tracer_tester54, None, None, [" --(1(OPTION) )--> "])
    tester.converter_test_caller("2-37-55", tracer_tester55, None, None, [" --(None(OPTION) )--> "])
    tester.converter_test_caller("2-37-56", tracer_tester56, None, None, [" --([1, 2, 3](OPTION) )--> "])
    tester.converter_test_caller("2-37-57", tracer_tester57, None, None, [" --(COMVNAME(OPTION) )--> "])
    tester.converter_test_caller("2-37-58", tracer_tester58, None, None, [" --(COMVNAME() )--> "])
    tester.converter_test_caller("2-37-59", tracer_tester59, None, None, [" --(COMVNAME(1) )--> "])
    tester.converter_test_caller("2-37-60", tracer_tester60, None, None, [" --(COMVNAME(None) )--> "])
    tester.converter_test_caller("2-37-61", tracer_tester61, None, None, [" --(COMVNAME([1, 2, 3]) )--> "])
    tester.converter_test_caller("2-37-62", tracer_tester62, None, None, [])
    """
    2-37-63/64はstderrを戻り値に取得できないので単体ではなく実使用側で確認
    """

    return "All Test Finished Normally."

import lib.Tracer as Tracer

def tracer_tester1(input, option):
    try:
        testerTracer = Tracer.Tracer( False )
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester2(input, option):
    try:
        testerTracer = Tracer.Tracer( 1 )
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester3(input, option):
    try:
        testerTracer = Tracer.Tracer("a")
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester4(input, option):
    try:
        testerTracer = Tracer.Tracer(None)
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester5(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester6(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester7(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester8(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push(1, "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester9(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push(None, "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester10(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push([1,2,3], "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester11(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester12(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", "")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester13(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", 1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester14(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester15(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester16(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.push("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester17(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("LABEL", [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester18(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("", [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester19(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData(1, [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester20(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData(None, [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester21(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData([1,2,3], [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester22(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("LABEL", [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester23(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("LABEL", [])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester24(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("LABEL", "DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester25(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("LABEL", 1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester26(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.pushListData("LABEL", None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester27(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.pushListData("LABEL", [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester28(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.add("DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester29(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.add("")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester30(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.add(1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester31(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.add(None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester32(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.add([1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester33(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.push()
        testerTracer.add("DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester34(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addLabel("LABEL")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester35(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addLabel("")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester36(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addLabel(1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester37(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addLabel(None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester38(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addLabel([1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester39(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.push()
        testerTracer.addLabel("LABEL")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester40(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addData("DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester41(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addData("")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester42(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addData(1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester43(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addData(None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester44(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addData([1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester45(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.push()
        testerTracer.addData("DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester46(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addListData([1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester47(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addListData([])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester48(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addListData("DATA")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester49(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addListData(1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester50(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addListData(None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester51(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.push()
        testerTracer.addListData([1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester52(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester53(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("", "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester54(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname(1, "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester55(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname(None, "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester56(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname([1,2,3], "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester57(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester58(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", "")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester59(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", 1)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester60(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", None)
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester61(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", [1,2,3])
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester62(input, option):
    try:
        testerTracer = Tracer.Tracer(False)
        testerTracer.push()
        testerTracer.addConvname("COMVNAME", "OPTION")
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester63(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", "DATA")
        testerTracer.dump()
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

def tracer_tester64(input, option):
    try:
        testerTracer = Tracer.Tracer(True)
        testerTracer.push("LABEL", "DATA")
        testerTracer.outputFlag = False
        testerTracer.dump()
    except Exception as e:
        testerTracer.push("exception", str(e))
    finally:
        return testerTracer.records

