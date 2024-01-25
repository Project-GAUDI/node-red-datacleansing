import datetime
import glob
import json
import runpy
import sys
import types
from decimal import Decimal
from lib import converter_tester

## テンプレート
# def func(inputs, options):
#     """
#     関数の説明
#
#     Args:
#         input (str): 引数の説明
#         optios (str): 引数の説明
#
#     Returns:
#         戻り値の型: 戻り値の説明
#
#     """


def change_normal(inputs, options=None):
    """
    上位・下位バイトに分割し、それぞれ２桁の数値文字列にして文字連結する。

    Args:
        input (int/list[int]): 10進数の値, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 0埋め4桁で表される数値文字列

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

    for input in targetList:
        idxValue = input
        if isinstance(input, str):
            idxValue = int(input)

        if idxValue > 0:
            byte = format(idxValue, '016b')
        else:
            byte = format(idxValue, '016b')[-16:]
        UP = int(byte[1:8], 2)
        DOWN = int(byte[9:16], 2)
        convertedList.append(str(UP).zfill(2) + str(DOWN).zfill(2))

    # 入力が配列でなければ戻り値を非配列化
    retVal = convertedList
    if isNotList:
        retVal = convertedList[0]

    return retVal


def change_normal_swap(inputs, options=None):
    """
    上位・下位バイトに分割し、それぞれ２桁の数値文字列にして上位・下位入れ替え後、文字連結する。

    Args:
        input (int/list[int]): 10進数の値, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 0埋め4桁で表される数値文字列

    """

    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

    for input in targetList:
        idxValue = input
        if isinstance(input, str):
            idxValue = int(input)

        if idxValue > 0:
            byte = format(idxValue, '016b')
        else:
            byte = format(idxValue, '016b')[-16:]
        UP = int(byte[1:8], 2)
        DOWN = int(byte[9:16], 2)
        convertedList.append(str(DOWN).zfill(2) + str(UP).zfill(2))

    # 入力が配列でなければ戻り値を非配列化
    retVal = convertedList
    if isNotList:
        retVal = convertedList[0]

    return retVal


def UnionDate(inputs, option):
    """
    日時データ結合

    Args:
        inputs (list[int]): 3つの数値
        option (any): 未使用

    Returns:
        str: inputsの値を元に変換された、"yyyy/mm/dd hh:mm:ss"の形式の文字列

    """
    retDate = ""
    dt_now = datetime.datetime.now()
    r = [inputs[0], inputs[1], inputs[2]]
    r[0] = change_normal(int(r[0]))
    r[1] = change_normal(int(r[1]))
    r[2] = change_normal(int(r[2]))
    retDate = str(dt_now.year)[:2] + r[0][:2] + "/" + r[0][-2:] + "/" + r[1][:2] + " " + r[1][-2:] + ":" + r[2][:2] + ":" + r[2][-2:]

    return retDate


def UnionDateSwap(inputs, options):
    """
    日時データ結合swap付き

    Args:
        inputs (list[int]): 3つの数値
        option (any): 未使用

    Returns:
        str: inputsの値を元に変換された、"yyyy/mm/dd hh:mm:ss"の形式の文字列

    """

    retDate = ""
    dt_now = datetime.datetime.now()
    r = [inputs[0], inputs[1], inputs[2]]
    r[0] = change_normal_swap(int(r[0]))
    r[1] = change_normal_swap(int(r[1]))
    r[2] = change_normal_swap(int(r[2]))
    retDate = str(dt_now.year)[:2] + r[0][:2] + "/" + r[0][-2:] + "/" + r[1][:2] + " " + r[1][-2:] + ":" + r[2][:2] + ":" + r[2][-2:]

    return retDate


def UnionDateF12(inputs, option):
    """
    日時データ結合12桁数値のみ

    Args:
        inputs (list[int]): 3つの数値
        option (any): 未使用

    Returns:
        list[str]: inputsの値を元に変換された、"yymmddhhmmss"の形式の文字列

    """

    retDate = ""
    dt_now = datetime.datetime.now()
    r = [inputs[0], inputs[1], inputs[2]]
    r[0] = change_normal(int(r[0]))
    r[1] = change_normal(int(r[1]))
    r[2] = change_normal(int(r[2]))
    retDate = r[0][:2] + r[0][-2:] + r[1][:2] + r[1][-2:] + r[2][:2] + r[2][-2:]

    return retDate


def UnionDateF12Swap(inputs, option):
    """
    # 日時データ結合12桁数値のみswap付き

    Args:
        inputs (list[int]): 3つの数値
        option (any): 未使用

    Returns:
        str: inputsの値を元に変換された、"yymmddhhmmss"の形式の文字列

    """

    retDate = ""
    dt_now = datetime.datetime.now()
    r = [inputs[0], inputs[1], inputs[2]]
    r[0] = change_normal_swap(int(r[0]))
    r[1] = change_normal_swap(int(r[1]))
    r[2] = change_normal_swap(int(r[2]))
    retDate = r[0][:2] + r[0][-2:] + r[1][:2] + r[1][-2:] + r[2][:2] + r[2][-2:]

    return retDate


def DateFormat(input, option):
    """
    日付データをフォーマット

    Args:
        input (str): 日付形式文字列
        option (str): python式フォーマット書式(デフォルト: %y%m%d%H%M%S)

    Returns:
        str : 指定書式に変換した日付文字列

    """

    retDate = ""
    format = '%y%m%d%H%M%S'
    if option is not None:
        format = option

    date_time = datetime.datetime.strptime(input, '%Y/%m/%d %H:%M:%S.%f')
    retDate = datetime.datetime.strftime(date_time, format)

    return retDate


def Date2DateF12(input, option):
    """
    日付から時刻キー生成

    Args:
        input (str): 日付形式の文字列
        option (any): 未使用

    Returns:
        str: inputを'%y%m%d%H%M%S'で変換した文字列

    """

    retDateF12 = ""
    myoption = '%y%m%d%H%M%S'

    retDateF12 = DateFormat(input, myoption)

    return retDateF12


def Operation(input, option):
    """
    積算

    Args:
        input (Decimal): 入力値
        option (Decimal): 倍数

    Returns:
        Decimal(文字列): input x optionの乗算結果

    """

    # 数値をDecimalに変換すると計算誤差が発生することがあるため、一度文字列化している
    retValue = Decimal(str(input)) * Decimal(str(option))

    return str(retValue)


def SetValue(input, option):
    """
    数値設定

    Args:
        inputs (any): 未使用
        option (any): セットする値

    Returns:
        any: optionの値

    """

    retValue = option

    return retValue


def RevertFlag(input, option):
    """
    フラグ反転

    Args:
        input (int): 0 or 1の値
        option (any): 未使用

    Returns:
        int: inputが0であれば1, その他の場合0

    """

    retValue = 0
    if 0 == int(input):
        retValue = 1

    return retValue


def dec_to_hex(input, option):
    """
    10進データを16進データに変換。(2byte)

    Args:
        input (int/list[int]): 10進数の値, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 16進数の値('0x'は省く)

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = input
    isNotList = not isinstance(input, list)
    if isNotList:
        targetList = [input]

    convertedValue = ""
    for input in targetList:
        # 文字列考慮
        convertedValue = int(input)

        if convertedValue > 0:
            convertedValue = format(convertedValue, 'x').zfill(4)[-4:]
        else:
            convertedValue = format(int("f" * 4, 16) + convertedValue + 1, 'x').zfill(4)[-4:]
        convertedList.append(convertedValue)

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue


def two_word_to_hour(inputs, option):
    """
    上位・下位Word(2byte)データを16進文字化後、連結してint(4byte)化、msecからhour単位に変換。
    (昇圧コンID計算相当)

    Args:
        inputs (list[int,int]): 10進数数値(2byte) x 2
        option (any): 未使用

    Returns:
        str: 変換結果

    """

    retValue = ""
    if False == isinstance(inputs, list):
        raise Exception("Input must be List")

    inputsHEX = dec_to_hex(inputs, None)
    retValue = int(str(inputsHEX[0]) + str(inputsHEX[1]), 16) / 1000 / 60 / 60

    return retValue


def join(inputs, option):
    """
    文字のリストを連結し、１文字列にする。

    Args:
        inputs (list[str,...]): 文字列の配列
        options (str): 結合セパレータ, 連結する文字列間に挿入する文字。省略時は、挿入しない。

    Returns:
        str: 結合後の文字列

    """

    retValue = ""
    sep = ""
    if option is not None:
        sep = option[0]

    if False == isinstance(inputs, list):
        raise Exception("Input must be List")

    for idx in range(len(inputs)):
        idxValue = inputs[idx]
        if idxValue is None:
            raise Exception("Can not input None")

        elif False == isinstance(idxValue, str):
            # 文字列でないとjoinできないのでstr化
            inputs[idx] = str(idxValue)

    retValue = sep.join(inputs)

    return retValue


def substring(input, options):
    """
    文字列から一部を抽出する。

    Args:
        input (str): 対象文字列。
        options (list[int,int]): [抽出開始位置, 抽出文字数]
            抽出開始位置: 切り出し開始位置。（1～）
                         負値の場合、文字列末端からの文字数となる。
                         省略時は、1。
            抽出文字数: 切り出し文字数。（1～）
                       負値の場合、元文字列長と合算した値を抽出文字数とする。
                       省略時は、末尾まで切り出し。

    Returns:
        str: inputsから切り出した文字

    """

    retValue = ""

    if input is None:
        raise Exception("Can not set input None")

    targetValue = str(input)

    myOptions = options
    if False == (isinstance(options, list)):
        myOptions = [options]


    start = 1
    if (1 <= len(myOptions)):
        if myOptions[0] is not None:
            start = myOptions[0]

        if False == isinstance(start, int):
            start = int(start)

    end = len(targetValue) + 1
    if (2 <= len(myOptions)) and (myOptions[1] is not None):
        textLength = myOptions[1]

        if False == isinstance(textLength, int):
            textLength = int(textLength)

        end = start + textLength

    retValue = targetValue[start - 1 : end - 1]

    return retValue


def split(input, options):
    """
    文字列を指定セパレータで分解し、指定位置のデータを抽出する。

    Args:
        input (str): 対象文字列。
        optios (list[str,int]): [セパレータ, 抽出位置]
            セパレータ: 文字の分解に使用する文字。省略不可。
            抽出位置: 分解した文字列の配列から抜き出す位置。（1～）

    Returns:
        str: inputsから分割された文字列の一部

    """

    retValue = ""
    targetValue = input

    if targetValue is None:
        raise Exception("Can not set input None")

    if False == isinstance(targetValue, str):
        targetValue = str(input)

    myOptions = options
    if False == (isinstance(options, list)):
        myOptions = [options]

    # 必須なのでサイズチェックなし
    if myOptions[0] is None:
        raise Exception("Can not set option None")

    sep = myOptions[0]
    if False == isinstance(sep, str):
        sep = str(myOptions[0])

    index = 1
    if (2 <= len(myOptions)):
        if myOptions[1] is not None:
            index = myOptions[1]

        if False == isinstance(index, int):
            index = int(myOptions[1])

        if index <= 0:
            raise Exception("Set option [1] to a number greater than 0")

    splitedList = targetValue.split(sep)
    retValue = splitedList[index - 1]

    return retValue


def trim(inputs, option):
    """
    スペースを除去。

    Args:
        inputs (str/list[str]): 任意の文字列, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 空白が削除された結果

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

    convertedValue = ""
    for input in targetList:
        convertedValue = input.replace(' ', '')
        convertedList.append(convertedValue)

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue


def bit_to_dec(inputs, option):
    """
    2進データを10進データに変換。（1byte分)

    Args:
        input (str/list[str]): 2進数の値, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 10進数の値

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

    convertedValue = ""
    for input in targetList:
        idxValue = input.zfill(8)[-8:]
        HEAD = idxValue[0]
        VALUE = idxValue[1:]

        if HEAD == "0":
            convertedValue = int(VALUE, 2)
        else:
            convertedValue = int(VALUE, 2) - 128
        convertedList.append(convertedValue)

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue


def standard_converter_tester(input, option):
    tester = converter_tester.converter_tester()

    tester.converter_test_caller("2-1-1-1", UnionDate, [None,1295,8752], None, None)
    tester.converter_test_caller("2-1-1-2", UnionDate, [5384,None,8752], None, None)
    tester.converter_test_caller("2-1-1-3", UnionDate, [5384,1295,None], None, None)
    tester.converter_test_caller("2-1-1-4", UnionDate, ["ABC",1295,8752], None, None)
    tester.converter_test_caller("2-1-1-5", UnionDate, [5384,"ABC",8752], None, None)
    tester.converter_test_caller("2-1-1-6", UnionDate, [5384,1295,"ABC"], None, None)
    tester.converter_test_caller("2-1-1-7", UnionDate, [5384,1295,8752], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-1-1-8", UnionDate, ["5384","1295","8752"], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-1-1-9", UnionDate, [5384,1295], None, None)

    tester.converter_test_caller("2-1-2-1", UnionDateSwap, [None,3845,12322], None, None)
    tester.converter_test_caller("2-1-2-2", UnionDateSwap, [2069,None,12322], None, None)
    tester.converter_test_caller("2-1-2-3", UnionDateSwap, [2069,3845,None], None, None)
    tester.converter_test_caller("2-1-2-4", UnionDateSwap, ["ABC",3845,12322], None, None)
    tester.converter_test_caller("2-1-2-5", UnionDateSwap, [2069,"ABC",12322], None, None)
    tester.converter_test_caller("2-1-2-6", UnionDateSwap, [2069,3845,"ABC"], None, None)
    tester.converter_test_caller("2-1-2-7", UnionDateSwap, [2069,3845,12322], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-1-2-8", UnionDateSwap, ["2069","3845","12322"], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-1-2-9", UnionDateSwap, [2069,3845], None, None)

    tester.converter_test_caller("2-1-3-1", UnionDateF12, [None,1295,8752], None, None)
    tester.converter_test_caller("2-1-3-2", UnionDateF12, [5384,None,8752], None, None)
    tester.converter_test_caller("2-1-3-3", UnionDateF12, [5384,1295,None], None, None)
    tester.converter_test_caller("2-1-3-4", UnionDateF12, ["ABC",1295,8752], None, None)
    tester.converter_test_caller("2-1-3-5", UnionDateF12, [5384,"ABC",8752], None, None)
    tester.converter_test_caller("2-1-3-6", UnionDateF12, [5384,1295,"ABC"], None, None)
    tester.converter_test_caller("2-1-3-7", UnionDateF12, [5384,1295,8752], None, "210805153448")
    tester.converter_test_caller("2-1-3-8", UnionDateF12, ["5384","1295","8752"], None, "210805153448")
    tester.converter_test_caller("2-1-3-9", UnionDateF12, [5384,1295], None, None)

    tester.converter_test_caller("2-1-4-1", UnionDateF12Swap, [None,3845,12322], None, None)
    tester.converter_test_caller("2-1-4-2", UnionDateF12Swap, [2069,None,12322], None, None)
    tester.converter_test_caller("2-1-4-3", UnionDateF12Swap, [2069,3845,None], None, None)
    tester.converter_test_caller("2-1-4-4", UnionDateF12Swap, ["ABC",3845,12322], None, None)
    tester.converter_test_caller("2-1-4-5", UnionDateF12Swap, [2069,"ABC",12322], None, None)
    tester.converter_test_caller("2-1-4-6", UnionDateF12Swap, [2069,3845,"ABC"], None, None)
    tester.converter_test_caller("2-1-4-7", UnionDateF12Swap, [2069,3845,12322], None, "210805153448")
    tester.converter_test_caller("2-1-4-8", UnionDateF12Swap, ["2069","3845","12322"], None, "210805153448")
    tester.converter_test_caller("2-1-4-9", UnionDateF12Swap, [2069,3845], None, None)

    tester.converter_test_caller("2-1-5-1", DateFormat, None, None, None)
    tester.converter_test_caller("2-1-5-2", DateFormat, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("2-1-5-3", DateFormat, "2021/08/05 15:34:48", None, None)
    tester.converter_test_caller("2-1-5-4", DateFormat, "2021/08/05T15:34:48.123Z", None, None)
    tester.converter_test_caller("2-1-5-5", DateFormat, "ABC", None, None)
    tester.converter_test_caller("2-1-5-6", DateFormat, "2021/08/05 15:34:48.123", "ABC", "ABC")
    tester.converter_test_caller("2-1-5-7", DateFormat, "2021/08/05 15:34:48.123", "%Y%m%d%H%M%S%f", "20210805153448123000")
    tester.converter_test_caller("2-1-5-8", DateFormat, "2021/08/05 15:34:48.123", "%Y-%m-%d %H#%M#%S#%f", "2021-08-05 15#34#48#123000")
    tester.converter_test_caller("2-1-5-9", DateFormat, "2021/08/05 15:34:48.123", None, "210805153448")

    tester.converter_test_caller("2-1-6-1", Date2DateF12, None, None, None)
    tester.converter_test_caller("2-1-6-2", Date2DateF12, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("2-1-6-3", Date2DateF12, "2021/08/05 15:34:48", None, None)
    tester.converter_test_caller("2-1-6-4", Date2DateF12, "2021/08/05T15:34:48.123Z", None, None)
    tester.converter_test_caller("2-1-6-5", Date2DateF12, "ABC", None, None)

    tester.converter_test_caller("2-1-7-1", Operation, None, 0.1, None)
    tester.converter_test_caller("2-1-7-2", Operation, 123, None, None)
    tester.converter_test_caller("2-1-7-3", Operation, "ABC", 0.1, None)
    tester.converter_test_caller("2-1-7-4", Operation, 123, "ABC", None)
    tester.converter_test_caller("2-1-7-5", Operation, 123, 0.1, "12.3")
    tester.converter_test_caller("2-1-7-6", Operation, "123", "0.1", "12.3")

    tester.converter_test_caller("2-1-8-1", SetValue, None, 0.1, 0.1)
    tester.converter_test_caller("2-1-8-2", SetValue, 123, None, None)
    tester.converter_test_caller("2-1-8-3", SetValue, "ABC", 0.1, 0.1)
    tester.converter_test_caller("2-1-8-4", SetValue, 123, "ABC", "ABC")

    tester.converter_test_caller("2-1-9-1", RevertFlag, None, None, None)
    tester.converter_test_caller("2-1-9-2", RevertFlag, "ABC", None, None)
    tester.converter_test_caller("2-1-9-3", RevertFlag, True, None, 0)
    tester.converter_test_caller("2-1-9-4", RevertFlag, False, None, 1)
    tester.converter_test_caller("2-1-9-5", RevertFlag, 123, None, 0)
    tester.converter_test_caller("2-1-9-6", RevertFlag, 1, None, 0)
    tester.converter_test_caller("2-1-9-7", RevertFlag, 0, None, 1)
    tester.converter_test_caller("2-1-9-8", RevertFlag, "0", None, 1)

    tester.converter_test_caller("2-1-10-1", dec_to_hex, None, None, None)
    tester.converter_test_caller("2-1-10-2", dec_to_hex, "AB", None, None)
    tester.converter_test_caller("2-1-10-3", dec_to_hex, 32767, None, "7fff")
    tester.converter_test_caller("2-1-10-4", dec_to_hex, "-32768", None, "8000")
    tester.converter_test_caller("2-1-10-5", dec_to_hex, 65535, None, "ffff")
    tester.converter_test_caller("2-1-10-6", dec_to_hex, [None,-32768], None, None)
    tester.converter_test_caller("2-1-10-7", dec_to_hex, [-32768,None], None, None)
    tester.converter_test_caller("2-1-10-8", dec_to_hex, [-1,-12345,12345,32767,-32768], None, ['ffff', 'cfc7', '3039', '7fff', '8000'])

    tester.converter_test_caller("2-1-11-1", two_word_to_hour, [None,12345], None, None)
    tester.converter_test_caller("2-1-11-2", two_word_to_hour, [54,None], None, None)
    tester.converter_test_caller("2-1-11-3", two_word_to_hour, ["ABC",12345], None, None)
    tester.converter_test_caller("2-1-11-4", two_word_to_hour, [54,"ABC"], None, None)
    tester.converter_test_caller("2-1-11-5", two_word_to_hour, [54,12345], None, 0.9864691666666666)
    tester.converter_test_caller("2-1-11-6", two_word_to_hour, ["54","12345"], None, 0.9864691666666666)
    tester.converter_test_caller("2-1-11-7", two_word_to_hour, [108,24690], None, 1.9729383333333332)
    tester.converter_test_caller("2-1-11-8", two_word_to_hour, 540, None, None)

    tester.converter_test_caller("2-1-12-1", join, [None,"DEF"], None, None)
    tester.converter_test_caller("2-1-12-2", join, ["ABC",None], None, None)
    tester.converter_test_caller("2-1-12-3", join, ["ABC","DEF"], None, "ABCDEF")
    tester.converter_test_caller("2-1-12-4", join, [123,456], "-", "123-456")
    tester.converter_test_caller("2-1-12-5", join, "ABC", "#", None)
    tester.converter_test_caller("2-1-12-6", join, [12,34,56], ":", "12:34:56")

    tester.converter_test_caller("2-1-13-1", substring, None, None, None)
    tester.converter_test_caller("2-1-13-2", substring, "1234567890", None, "1234567890")
    tester.converter_test_caller("2-1-13-3", substring, "1234567890", 2, "234567890")
    tester.converter_test_caller("2-1-13-4", substring, "1234567890", None, "1234567890")
    tester.converter_test_caller("2-1-13-5", substring, "1234567890", "ABC", None)
    tester.converter_test_caller("2-1-13-6", substring, "1234567890", [2,None], "234567890")
    tester.converter_test_caller("2-1-13-7", substring, "1234567890", [2,"ABC"], None)
    tester.converter_test_caller("2-1-13-8", substring, "1234567890", ["2","3"], "234")
    tester.converter_test_caller("2-1-13-9", substring, 1234567890, [2,3], "234")
    tester.converter_test_caller("2-1-13-10", substring, "1234567890", [0,3], "")
    tester.converter_test_caller("2-1-13-11", substring, "1234567890", [11,3], "")
    tester.converter_test_caller("2-1-13-12", substring, "1234567890", [9,3], "90")
    tester.converter_test_caller("2-1-13-13", substring, "1234567890", [1,0], "")
    tester.converter_test_caller("2-1-13-14", substring, "1234567890", [1,11], "1234567890")

    tester.converter_test_caller("2-1-14-1", split, None, [",",1], None)
    tester.converter_test_caller("2-1-14-2", split, "ABC,DEF,GHI", [None,1], None)
    tester.converter_test_caller("2-1-14-3", split, "ABC,DEF,GHI", [",",None], "ABC")
    tester.converter_test_caller("2-1-14-4", split, "ABC,DEF,GHI", [",","ABC"], None)
    tester.converter_test_caller("2-1-14-5", split, "ABC,DEF,GHI", [",",0], None)
    tester.converter_test_caller("2-1-14-6", split, "ABC,DEF,GHI", [",",1], "ABC")
    tester.converter_test_caller("2-1-14-7", split, "ABC,DEF,GHI", [",",2], "DEF")
    tester.converter_test_caller("2-1-14-8", split, "ABC,DEF,GHI", [",",3], "GHI")
    tester.converter_test_caller("2-1-14-9", split, "ABC,DEF,GHI", [",",4], None)
    tester.converter_test_caller("2-1-14-10", split, "ABC,DEF,GHI", ["#",1], "ABC,DEF,GHI")
    tester.converter_test_caller("2-1-14-11", split, "ABCD,DEF,FGHI", ["DEF",2], ",FGHI")
    tester.converter_test_caller("2-1-14-12", split, "ABC,DEF,GHI", ",", "ABC")
    tester.converter_test_caller("2-1-14-13", split, "ABC,DEF,GHI", None, None)
    tester.converter_test_caller("2-1-14-14", split, 123453673, [3,2], "45")

    tester.converter_test_caller("2-1-15-1", trim, [None," 1 2 3 4 5 "], None, None)
    tester.converter_test_caller("2-1-15-2", trim, [" A B C D ",None], None, None)
    tester.converter_test_caller("2-1-15-3", trim, 123, None, None)
    tester.converter_test_caller("2-1-15-4", trim, " ABCD", None, "ABCD")
    tester.converter_test_caller("2-1-15-5", trim, "AB CD", None, "ABCD")
    tester.converter_test_caller("2-1-15-6", trim, "ABCD ", None, "ABCD")
    tester.converter_test_caller("2-1-15-7", trim, ["  A  B  C  D  ","  1  2  3  4  5  "], None, ["ABCD","12345"])

    tester.converter_test_caller("2-1-16-1", bit_to_dec, None, None, None)
    tester.converter_test_caller("2-1-16-2", bit_to_dec, "ABC", None, None)
    tester.converter_test_caller("2-1-16-3", bit_to_dec, "12345678", None, None)
    tester.converter_test_caller("2-1-16-4", bit_to_dec, "10000000", None, -128)
    tester.converter_test_caller("2-1-16-5", bit_to_dec, "11111111", None, -1)
    tester.converter_test_caller("2-1-16-6", bit_to_dec, "01111111", None, 127)
    tester.converter_test_caller("2-1-16-7", bit_to_dec, "1111", None, 15)
    tester.converter_test_caller("2-1-16-8", bit_to_dec, 100, None, None)

    tester.converter_test_caller("2-1-17-1", change_normal, [None,1295,8752], None, None)
    tester.converter_test_caller("2-1-17-2", change_normal, [5384,None,8752], None, None)
    tester.converter_test_caller("2-1-17-3", change_normal, [5384,1295,None], None, None)
    tester.converter_test_caller("2-1-17-4", change_normal, ["ABC",1295,8752], None, None)
    tester.converter_test_caller("2-1-17-5", change_normal, [5384,"ABC",8752], None, None)
    tester.converter_test_caller("2-1-17-6", change_normal, [5384,1295,"ABC"], None, None)
    tester.converter_test_caller("2-1-17-7", change_normal, [5384,1295,8752], None, ["2108", "0515", "3448"])
    tester.converter_test_caller("2-1-17-8", change_normal, ["5384","1295","8752"], None, ["2108", "0515", "3448"])
    tester.converter_test_caller("2-1-17-9", change_normal, 5384, None, "2108")

    tester.converter_test_caller("2-1-18-1", change_normal_swap, [None,3845,12322], None, None)
    tester.converter_test_caller("2-1-18-2", change_normal_swap, [2069,None,12322], None, None)
    tester.converter_test_caller("2-1-18-3", change_normal_swap, [2069,3845,None], None, None)
    tester.converter_test_caller("2-1-18-4", change_normal_swap, ["ABC",3845,12322], None, None)
    tester.converter_test_caller("2-1-18-5", change_normal_swap, [2069,"ABC",12322], None, None)
    tester.converter_test_caller("2-1-18-6", change_normal_swap, [2069,3845,"ABC"], None, None)
    tester.converter_test_caller("2-1-18-7", change_normal_swap, [2069,3845,12322], None, ["2108", "0515", "3448"])
    tester.converter_test_caller("2-1-18-8", change_normal_swap, ["2069","3845","12322"], None, ["2108", "0515", "3448"])
    tester.converter_test_caller("2-1-18-9", change_normal_swap, 2069, None, "2108")

    return 0
