import datetime
import glob
import json
import re
import runpy
import sys
import types
from decimal import Decimal
from lib import converter_tester
from zoneinfo import ZoneInfo

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
        option (list[str,str]): [ 変換書式(省略可能), 入力データフォーマット(省略可能) ]
            [0]: 変換書式。Pythonの書式形式で指定。省略可能。デフォルト＝"%y%m%d%H%M%S"
            [1]: 入力データフォーマット（Pythonフォーマット形式）。省略可能。デフォルト＝"%Y/%m/%d %H:%M:%S.%f"

    Returns:
        str : 指定書式に変換した日付文字列

    """

    retDate = ""
    format = '%y%m%d%H%M%S'
    in_format = '%Y/%m/%d %H:%M:%S.%f'
    if option is not None:
        if False == isinstance(option, list):
            format = option
        else:
            opt_length = len(option)
            if 1 <= opt_length:
                format = option[0]
            if 2 <= opt_length:
                in_format = option[1]

    date_time = datetime.datetime.strptime(input, in_format)
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


def NativeTimeToISOTime(input, options):
    """
    タイムゾーン情報を持たない非ISO形式日時文字列を
    オプションで指定したタイムゾーンの時刻値と書式に変換する。

    Args:
        input (str): 非ISO形式日時文字列（タイムゾーン情報なし）
        options (list[str,str,str,str]): [入力データタイムゾーン, 入力データフォーマット, 出力データタイムゾーン(省略可能), 出力データフォーマット(省略可能)]
            [0]: 入力データタイムゾーン　例）"Asia/Tokyo"
            [1]: 入力データフォーマット（Pythonフォーマット形式。例："%Y-%m-%d %H:%M:%S.%f"）
            [2]: 出力データタイムゾーン（デフォルト＝"UTC"）
            [3]: 出力データフォーマット（Pythonフォーマット形式。デフォルト＝"%Y-%m-%dT%H:%M:%S.%f%z"）

    Returns:
        str : 指定書式に変換した日付文字列
              %z出力による時差表記部分は、基本的に"+0000"の形式となる。（"+00:00"の形式ではない)
              出力データタイムゾーンにUTCを指定した場合、時差表記は、"+0000"ではなく、"Z"となる。

    """

    retDate = ""
    out_timezone = 'UTC'
    out_format = '%Y-%m-%dT%H:%M:%S.%f%z'

    if False == isinstance(options, list):
        raise Exception("Options must be List.")

    opt_length = len(options)
    if opt_length < 2:
        raise Exception("Options[0],[1] must be set.")

    in_timezone = options[0]
    in_format = options[1]
    if 3 <= opt_length:
        out_timezone = options[2]
    if 4 <= opt_length:
        out_format = options[3]

    # 指定の入力書式で日付データを取り込み
    date_time = datetime.datetime.strptime(input, in_format)
    # 日付データに指定のゾーン情報属性を付ける
    date_time_in_tz = date_time.replace(tzinfo=ZoneInfo(key=in_timezone))
    # 日付データを指定の出力タイムゾーンデータに変換する
    date_time_out_tz = date_time_in_tz.astimezone(ZoneInfo(key=out_timezone))
    # 指定の出力書式で日付データを文字列化
    retDate = datetime.datetime.strftime(date_time_out_tz, out_format)

    # 末尾の"+0000"を"Z"に置換
    retDate = re.sub('\+0000$', 'Z', retDate)


    return retDate


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


def Division(input, option):
    """
    除算

    Args:
        input (Decimal): 入力値
        option (Decimal): 除数

    Returns:
        Decimal(文字列): input / optionの除算結果

    """

    # 数値をDecimalに変換すると計算誤差が発生することがあるため、一度文字列化している
    retValue = Decimal(str(input)) / Decimal(str(option))

    return str(retValue)


def Max(inputs, option):
    """
    最大値取得

    Args:
        inputs (list[Decimal]): 入力値リスト
        option (any): 未使用

    Returns:
        Decimal(文字列): inputs中の最大値

    """

    return str(max(inputs))


def Min(inputs, option):
    """
    最小値取得

    Args:
        inputs (list[Decimal]): 入力値リスト
        option (any): 未使用

    Returns:
        Decimal(文字列): inputs中の最小値

    """

    return str(min(inputs))


def Swap(inputs, option):
    """
    16進データの上位・下位をSwapする。(2byte)
    桁数不足（４桁未満）の場合は、0埋めの上処理する。

    Args:
        inputs (str/list[str]): 16進数('0x'は省く)の文字列, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 16進数の値('0x'は省く)

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

    convertedValue = ""
    for input in targetList:
        convertedValue = input.zfill(4)[-4:]

        convertedValue=convertedValue[-2:]+convertedValue[:2]

        convertedList.append(convertedValue)

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue
    

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
    Joinのエイリアス
    """
    return Join(inputs, option)

def Join(inputs, option):
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
    SubStringのエイリアス
    """
    return SubString(input, options)

def SubString(input, options):
    """
    文字列から一部を抽出する。

    Args:
        input (str): 対象文字列。
        options (list[int,int]): [抽出開始位置(省略可能), 抽出文字数]
            抽出開始位置: 切り出し開始位置。（1オリジン）
                         負値の場合、文字列末端からの文字数として扱う。
                         省略時は、1。
            抽出文字数: 切り出し文字数。（1オリジン）
                       総文字数を超える場合、末尾までを出力する。
                       負値の場合、文字列長からの差値として扱い抽出文字数を計算する。
                       省略時は、末尾まで切り出す。

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

    textLength = len(targetValue)
    subTextLength = textLength
    if (2 <= len(myOptions)) and (myOptions[1] is not None):
        subTextLength = myOptions[1]

        if False == isinstance(subTextLength, int):
            subTextLength = int(subTextLength)

    if 0 < start:
        startidx = start - 1
    else:
        startidx = textLength + start

    if 0 <= subTextLength:
        endidx = startidx + subTextLength
    else:
        endidx = startidx + (textLength + subTextLength)

    retValue = targetValue[startidx : endidx]

    return retValue


def split(input, options):
    """
    Splitのエイリアス
    """
    return Split(input, options)

def Split(input, options):
    """
    文字列を指定セパレータで分解し、指定位置のデータを抽出する。

    Args:
        input (str): 対象文字列。
        optios (list[str,int]): [セパレータ, 抽出位置(省略可能)]
            セパレータ: 文字の分解に使用する文字。省略不可。
            抽出位置: 分解した文字列の配列から抜き出す位置。（1オリジン）
            　　　　　デフォルト=1。

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
    Trimのエイリアス
    """
    return Trim(inputs, option)

def Trim(inputs, option):
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


def dec_to_hex(inputs, option):
    """
    DecToHexのエイリアス
    """
    return DecToHex(inputs, option)

def DecToHex(inputs, option):
    """
    10進データを16進データに変換。(2byte)

    Args:
        inputs (int/list[int]): 10進数の値, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 16進数の値('0x'は省く)

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

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

def HexToDec(inputs, option):
    """
    16進データを10進データに変換。（2byte分)

    Args:
        inputs (str/list[str]): 16進数の値('0x'は省く), またはその配列
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
        idxValue = input.zfill(4)[-4:]

        convertedValue = int(idxValue, 16)
        if 32767 < convertedValue:
            convertedValue = convertedValue - 65536

        convertedList.append(convertedValue)

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue

def bit_to_dec(inputs, option):
    """
    BitToDecのエイリアス
    """
    return BitToDec(inputs, option)

def BitToDec(inputs, option):
    """
    2進データを10進データに変換。（1byte分)

    Args:
        inputs (str/list[str]): 2進数の値('0b'は省く), またはその配列
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

def DecToBit(inputs, option):
    """
    10進データを2進データに変換。（2byte分)

    Args:
        input (str/list[str]): 10進数の値, またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 2進数の値('0b'は省く)

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(inputs, list)
    if isNotList:
        targetList = [inputs]

    convertedValue = ""
    for input in targetList:
        # 文字列考慮
        convertedValue = int(input)

        if 0 <= convertedValue:
            convertedValue = convertedValue
        else:
            # 負値の場合補数をとる
            convertedValue = 65536 + convertedValue

        convertedValue = format(convertedValue, '016b')
        convertedList.append(convertedValue)

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue

def HexToBit(inputs, option):
    """
    16進データを2進データに変換。（2byte分)

    Args:
        input (str/list[str]): 16進数の値('0x'は省く), またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 2進数の値('0b'は省く)

    """
    return DecToBit(HexToDec(inputs, option), option)

def BitToHex(inputs, option):
    """
    2進データを16進データに変換。（1byte分)

    Args:
        input (str/list[str]): 2進数の値('0b'は省く), またはその配列
        option (any): 未使用

    Returns:
        str, list[str]: 16進数の値('0x'は省く)

    """
    convertedList = []

    # 配列でなければ配列化
    targetList = DecToHex(BitToDec(inputs, option), option)
    isNotList = not isinstance(targetList, list)
    if isNotList:
        targetList = [targetList]

    # 結果が２byte分なので、下位１byte分を切り出す
    convertedList = [ convertedValue[-2:] for convertedValue in targetList ]

    # 入力が配列でなければ戻り値を非配列化
    retValue = convertedList
    if isNotList:
        retValue = convertedList[0]

    return retValue


def Format(inputs, option):
    """
    文字列リストを書式指定で配置

    Args:
        inputs (list[str, str, ...]): 入力データ配列
        option (str): python式フォーマット書式
                        変換書式参考： https://docs.python.org/ja/3.8/library/string.html#format-string-syntax
    Returns:
        str : 指定書式に変換した文字列

    """

    retData = ""
    formatStr = option
    if not isinstance(formatStr, str):
        raise Exception("Option must be set as string.")

    # 配列でなければ配列化
    targetList = inputs
    isNotList = not isinstance(targetList, list)
    if isNotList:
        targetList = [targetList]

    retData = formatStr.format(*targetList)
  
    return retData








def standard_converter_tester(input, option):
    """
    標準変換関数のテスト関数

    Args:
        input (any): 未使用
        option (any): 未使用

    Returns:
        str : 成功時："All Test Finished Normally."
        　　　失敗時は、失敗テストからの例外を発生。
    """
    tester = converter_tester.converter_tester()

    tester.converter_test_caller("2-1-1", change_normal, 00, None, "0000")
    tester.converter_test_caller("2-1-2", change_normal, "!!", None, None)
    tester.converter_test_caller("2-1-3", change_normal, "aa", None, None)
    tester.converter_test_caller("2-1-4", change_normal, "ｱｱ", None, None)
    tester.converter_test_caller("2-1-5", change_normal, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-1-6", change_normal, "1000", None, "03104")
    tester.converter_test_caller("2-1-7", change_normal, "100 200", None, None)
    tester.converter_test_caller("2-1-8", change_normal, None, None, None)
    tester.converter_test_caller("2-1-9", change_normal, 2069, None, "0821")
    tester.converter_test_caller("2-1-10", change_normal, [2069,3845,12322], None, ["0821", "1505", "4834"])
    tester.converter_test_caller("2-1-11", change_normal, sys.maxsize, None, "127127")
    tester.converter_test_caller("2-1-12", change_normal, (sys.maxsize+1), None, "0000")
    tester.converter_test_caller("2-1-13", change_normal, [(sys.maxsize-1), sys.maxsize], None, ["127127", "127127"])
    tester.converter_test_caller("2-1-14", change_normal, [sys.maxsize, (sys.maxsize+1)], None, ["127127", "0000"])
    tester.converter_test_caller("2-1-15", change_normal, 2069, 00, "0821")
    tester.converter_test_caller("2-1-16", change_normal, 2069, "!!", "0821")
    tester.converter_test_caller("2-1-17", change_normal, 2069, [1, "aa"], "0821")
    tester.converter_test_caller("2-1-18", change_normal, 2069, None, "0821")

    tester.converter_test_caller("2-2-1", change_normal_swap, 00, None, "0000")
    tester.converter_test_caller("2-2-2", change_normal_swap, "!!", None, None)
    tester.converter_test_caller("2-2-3", change_normal_swap, "aa", None, None)
    tester.converter_test_caller("2-2-4", change_normal_swap, "ｱｱ", None, None)
    tester.converter_test_caller("2-2-5", change_normal_swap, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-2-6", change_normal_swap, "1000", None, "10403")
    tester.converter_test_caller("2-2-7", change_normal_swap, "100 200", None, None)
    tester.converter_test_caller("2-2-8", change_normal_swap, None, None, None)
    tester.converter_test_caller("2-2-9", change_normal_swap, [5384, 1295, 8752], None, ['0821', '1505', '4834'])
    tester.converter_test_caller("2-2-10", change_normal_swap, sys.maxsize, None, "127127")
    tester.converter_test_caller("2-2-11", change_normal_swap, (sys.maxsize+1), None, "0000")
    tester.converter_test_caller("2-2-12", change_normal_swap, [sys.maxsize-1, sys.maxsize], None, ["127127", "127127"])
    tester.converter_test_caller("2-2-13", change_normal_swap, [sys.maxsize, sys.maxsize+1], None, ["127127", "0000"])
    tester.converter_test_caller("2-2-14", change_normal_swap, 5384, 00, "0821")
    tester.converter_test_caller("2-2-15", change_normal_swap, 5384, "!!", "0821")
    tester.converter_test_caller("2-2-16", change_normal_swap, 5384, [1, "aa"], "0821")
    tester.converter_test_caller("2-2-17", change_normal_swap, 5384, None, "0821")

    tester.converter_test_caller("2-3-1", UnionDate, [1000, 2000, 3000], None, "2003/04/07 80:11:56")
    tester.converter_test_caller("2-3-2", UnionDate, ["!!//", "??--", ">><<"], None, None)
    tester.converter_test_caller("2-3-3", UnionDate, ["aaaa", "bbbb", "cccc"], None, None)
    tester.converter_test_caller("2-3-4", UnionDate, ["ｱｱｱｱ", "ｲｲｲｲ", "ｳｳｳｳ"], None, None)
    tester.converter_test_caller("2-3-5", UnionDate, ["００！！", "ｂｂああ", "KKEE"], None, None)
    tester.converter_test_caller("2-3-6", UnionDate, ["5384", "1295", "8752"], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-3-7", UnionDate, [5384, 1295], None, None)
    tester.converter_test_caller("2-3-8", UnionDate, None, None, None)
    tester.converter_test_caller("2-3-9", UnionDate, [5384, 1295, 8752], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-3-10", UnionDate, [sys.maxsize-2, sys.maxsize-1, sys.maxsize], None, "2012/27/12 27:12:27")
    tester.converter_test_caller("2-3-11", UnionDate, [sys.maxsize-1, sys.maxsize, sys.maxsize+1], None, "2012/27/12 27:00:00")
    tester.converter_test_caller("2-3-12", UnionDate, ["5384", "1295", "8752"], 00, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-3-13", UnionDate, ["5384", "1295", "8752"], "!!", "2021/08/05 15:34:48")
    tester.converter_test_caller("2-3-14", UnionDate, ["5384", "1295", "8752"], [1, "aa"], "2021/08/05 15:34:48")
    tester.converter_test_caller("2-3-15", UnionDate, ["5384", "1295", "8752"], None, "2021/08/05 15:34:48")

    tester.converter_test_caller("2-4-1", UnionDateSwap, 00, None, None)
    tester.converter_test_caller("2-4-2", UnionDateSwap, "!!", None, None)
    tester.converter_test_caller("2-4-3", UnionDateSwap, "aa", None, None)
    tester.converter_test_caller("2-4-4", UnionDateSwap, "ｱｱ", None, None)
    tester.converter_test_caller("2-4-5", UnionDateSwap, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-4-6", UnionDateSwap, "1000", None, "2001/00/00 00:00:00")
    tester.converter_test_caller("2-4-7", UnionDateSwap, "100 200", None, "2001/00/00 00:00:00")
    tester.converter_test_caller("2-4-8", UnionDateSwap, None, None, None)
    tester.converter_test_caller("2-4-9", UnionDateSwap, [1000, 2000, 3000], None, "2010/03/80 07:56:11")
    tester.converter_test_caller("2-4-10", UnionDateSwap, ["!!//", "??--", ">><<"], None, None)
    tester.converter_test_caller("2-4-11", UnionDateSwap, ["aaaa", "bbbb", "cccc"], None, None)
    tester.converter_test_caller("2-4-12", UnionDateSwap, ["ｱｱｱｱ", "ｲｲｲｲ", "ｳｳｳｳ"], None, None)
    tester.converter_test_caller("2-4-13", UnionDateSwap, ["００！！", "ｂｂああ", "KKEE"], None, None)
    tester.converter_test_caller("2-4-14", UnionDateSwap, ["2069", "3845", "12322"], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-4-15", UnionDateSwap, [2069, 3845], None, None)
    tester.converter_test_caller("2-4-16", UnionDateSwap, [None, None, None], None, None)
    tester.converter_test_caller("2-4-17", UnionDateSwap, [2069, 3845, 12322], None, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-4-18", UnionDateSwap, [sys.maxsize-2, sys.maxsize-1, sys.maxsize], None, "2012/27/12 27:12:27")
    tester.converter_test_caller("2-4-19", UnionDateSwap, [sys.maxsize-1, sys.maxsize, sys.maxsize+1], None, "2012/27/12 27:00:00")
    tester.converter_test_caller("2-4-20", UnionDateSwap, ["2069", "3845", "12322"], 00, "2021/08/05 15:34:48")
    tester.converter_test_caller("2-4-21", UnionDateSwap, ["2069", "3845", "12322"], "!!", "2021/08/05 15:34:48")
    tester.converter_test_caller("2-4-22", UnionDateSwap, ["2069", "3845", "12322"], [1, "aa"], "2021/08/05 15:34:48")
    tester.converter_test_caller("2-4-23", UnionDateSwap, ["2069", "3845", "12322"], None, "2021/08/05 15:34:48")
    
    tester.converter_test_caller("2-5-1", UnionDateF12, 00, None, None)
    tester.converter_test_caller("2-5-2", UnionDateF12, "!!", None, None)
    tester.converter_test_caller("2-5-3", UnionDateF12, "aa", None, None)
    tester.converter_test_caller("2-5-4", UnionDateF12, "ｱｱ", None, None)
    tester.converter_test_caller("2-5-5", UnionDateF12, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-5-6", UnionDateF12, "1000", None, "000100000000")
    tester.converter_test_caller("2-5-7", UnionDateF12, "100 200", None, "000100000000")
    tester.converter_test_caller("2-5-8", UnionDateF12, None, None, None)
    tester.converter_test_caller("2-5-9", UnionDateF12, [1000, 2000, 3000], None, "030407801156")
    tester.converter_test_caller("2-5-10", UnionDateF12, ["!!//", "??--", ">><<"], None, None)
    tester.converter_test_caller("2-5-11", UnionDateF12, ["aaaa", "bbbb", "cccc"], None, None)
    tester.converter_test_caller("2-5-12", UnionDateF12, ["ｱｱｱｱ", "ｲｲｲｲ", "ｳｳｳｳ"], None, None)
    tester.converter_test_caller("2-5-13", UnionDateF12, ["００！！", "ｂｂああ", "KKEE"], None, None)
    tester.converter_test_caller("2-5-14", UnionDateF12, ["5384", "1295", "8752"], None, "210805153448")
    tester.converter_test_caller("2-5-15", UnionDateF12, [5384, 1295], None, None)
    tester.converter_test_caller("2-5-16", UnionDateF12, [None, None, None], None, None)
    tester.converter_test_caller("2-5-17", UnionDateF12, [5384, 1295, 8752], None, "210805153448")
    tester.converter_test_caller("2-5-18", UnionDateF12, [sys.maxsize-2, sys.maxsize-1, sys.maxsize], None, "122712271227")
    tester.converter_test_caller("2-5-19", UnionDateF12, [sys.maxsize-1, sys.maxsize, sys.maxsize+1], None, "122712270000")
    tester.converter_test_caller("2-5-20", UnionDateF12, ["5384", "1295", "8752"], 00, "210805153448")
    tester.converter_test_caller("2-5-21", UnionDateF12, ["5384", "1295", "8752"], "!!", "210805153448")
    tester.converter_test_caller("2-5-22", UnionDateF12, ["5384", "1295", "8752"], [1, "aa"], "210805153448")
    tester.converter_test_caller("2-5-23", UnionDateF12, ["5384", "1295", "8752"], None, "210805153448")

    tester.converter_test_caller("2-6-1", UnionDateF12Swap, [1000, 2000, 3000], None, "100380075611")
    tester.converter_test_caller("2-6-2", UnionDateF12Swap, ["!!//", "??--", ">><<"], None, None)
    tester.converter_test_caller("2-6-3", UnionDateF12Swap, ["aaaa", "bbbb", "cccc"], None, None)
    tester.converter_test_caller("2-6-4", UnionDateF12Swap, ["ｱｱｱｱ", "ｲｲｲｲ", "ｳｳｳｳ"], None, None)
    tester.converter_test_caller("2-6-5", UnionDateF12Swap, ["００！！", "ｂｂああ", "KKEE"], None, None)
    tester.converter_test_caller("2-6-6", UnionDateF12Swap, ["2069", "3845", "12322"], None, "210805153448")
    tester.converter_test_caller("2-6-7", UnionDateF12Swap, [2069, 3845], None, None)
    tester.converter_test_caller("2-6-8", UnionDateF12Swap, [None, None, None], None, None)
    tester.converter_test_caller("2-6-9", UnionDateF12Swap, [2069, 3845, 12322], None, "210805153448")
    tester.converter_test_caller("2-6-10", UnionDateF12Swap, [sys.maxsize-2, sys.maxsize-1, sys.maxsize], None, "122712271227")
    tester.converter_test_caller("2-6-11", UnionDateF12Swap, [sys.maxsize-1, sys.maxsize, sys.maxsize+1], None, "122712270000")
    tester.converter_test_caller("2-6-12", UnionDateF12Swap, ["2069", "3845", "12322"], 00, "210805153448")
    tester.converter_test_caller("2-6-13", UnionDateF12Swap, ["2069", "3845", "12322"], "!!", "210805153448")
    tester.converter_test_caller("2-6-14", UnionDateF12Swap, ["2069", "3845", "12322"], [1, "aa"], "210805153448")
    tester.converter_test_caller("2-6-15", UnionDateF12Swap, ["2069", "3845", "12322"], None, "210805153448")

    tester.converter_test_caller("2-7-1", DateFormat, 00, None, None)
    tester.converter_test_caller("2-7-2", DateFormat, "!!", None, None)
    tester.converter_test_caller("2-7-3", DateFormat, "aa", None, None)
    tester.converter_test_caller("2-7-4", DateFormat, "ｱｱ", None, None)
    tester.converter_test_caller("2-7-5", DateFormat, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-7-6", DateFormat, "1000", None, None)
    tester.converter_test_caller("2-7-7", DateFormat, "100 200", None, None)
    tester.converter_test_caller("2-7-8", DateFormat, None, None, None)
    tester.converter_test_caller("2-7-9", DateFormat, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("2-7-10", DateFormat, "08/05 15:34:48.123", None, None)
    tester.converter_test_caller("2-7-11", DateFormat, "2021//05 15:34:48.123", None, None)
    tester.converter_test_caller("2-7-12", DateFormat, "2021/08/ 15:34:48.123", None, None)
    tester.converter_test_caller("2-7-13", DateFormat, "2021/08/05 :34:48.123", None, None)
    tester.converter_test_caller("2-7-14", DateFormat, "2021/08/05 15::48.123", None, None)
    tester.converter_test_caller("2-7-15", DateFormat, "2021/08/05 15:34:.123", None, None)
    tester.converter_test_caller("2-7-16", DateFormat, "2021/08/05 15:34:48.123", "00", "00")
    tester.converter_test_caller("2-7-17", DateFormat, "2021/08/05 15:34:48.123", "!!", "!!")
    tester.converter_test_caller("2-7-18", DateFormat, "2021/08/05 15:34:48.123", "aa", "aa")
    tester.converter_test_caller("2-7-19", DateFormat, "2021/08/05 15:34:48.123", "ｱｱ", "ｱｱ")
    tester.converter_test_caller("2-7-20", DateFormat, "2021/08/05 15:34:48.123", "００！！ｂｂああ", "００！！ｂｂああ")
    tester.converter_test_caller("2-7-21", DateFormat, "2021/08/05 15:34:48.123", "aa aa", "aa aa")
    tester.converter_test_caller("2-7-22", DateFormat, "2021/08/05 15:34:48.123", ["%y%m%d%H%M%S", "%Y/%m/%d %H:%M:%S.%f"], "210805153448")
    tester.converter_test_caller("2-7-23", DateFormat, "2021/08/05 15:34:48.123", [ "%Y/%m/%d %I:%M(%p)", "%Y/%m/%d %H:%M:%S.%f"], "2021/08/05 03:34(PM)")
    tester.converter_test_caller("2-7-24", DateFormat, "2021/08/05 15:34:48.123", [ "%Y年%m月%d日（%a）", "%Y/%m/%d %H:%M:%S.%f"], "2021年08月05日（Thu）")

    tester.converter_test_caller("2-8-1", Date2DateF12, 00, None, None)
    tester.converter_test_caller("2-8-2", Date2DateF12, "!!", None, None)
    tester.converter_test_caller("2-8-3", Date2DateF12, "aa", None, None)
    tester.converter_test_caller("2-8-4", Date2DateF12, "ｱｱ", None, None)
    tester.converter_test_caller("2-8-5", Date2DateF12, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-8-6", Date2DateF12, "1000", None, None)
    tester.converter_test_caller("2-8-7", Date2DateF12, "100 200", None, None)
    tester.converter_test_caller("2-8-8", Date2DateF12, None, None, None)
    tester.converter_test_caller("2-8-9", Date2DateF12, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("2-8-10", Date2DateF12, "08/05 15:34:48.123", None, None)
    tester.converter_test_caller("2-8-11", Date2DateF12, "2021//05 15:34:48.123", None, None)
    tester.converter_test_caller("2-8-12", Date2DateF12, "2021/08/ 15:34:48.123", None, None)
    tester.converter_test_caller("2-8-13", Date2DateF12, "2021/08/05 :34:48.123", None, None)
    tester.converter_test_caller("2-8-14", Date2DateF12, "2021/08/05 15::48.123", None, None)
    tester.converter_test_caller("2-8-15", Date2DateF12, "2021/08/05 15:34:.123", None, None)
    tester.converter_test_caller("2-8-16", Date2DateF12, "2021/08/05 15:34:48.", None, None)
    tester.converter_test_caller("2-8-17", Date2DateF12, "2021/08/05 15:34:48.123", 00, "210805153448")
    tester.converter_test_caller("2-8-18", Date2DateF12, "2021/08/05 15:34:48.123", "!!", "210805153448")
    tester.converter_test_caller("2-8-19", Date2DateF12, "2021/08/05 15:34:48.123", [1, "aa"], "210805153448")
    tester.converter_test_caller("2-8-20", Date2DateF12, "2021/08/05 15:34:48.123", None, "210805153448")

    tester.converter_test_caller("2-9-1", NativeTimeToISOTime, 00, ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-2", NativeTimeToISOTime, "!!", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-3", NativeTimeToISOTime, "aa", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-4", NativeTimeToISOTime, "ｱｱ", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-5", NativeTimeToISOTime, "００！！ｂｂああ", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-6", NativeTimeToISOTime, "aa aa", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-7", NativeTimeToISOTime, None, ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-8", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T13:56:07.890000+0900")
    tester.converter_test_caller("2-9-9", NativeTimeToISOTime, "01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-10", NativeTimeToISOTime, "2023--23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-11", NativeTimeToISOTime, "2023-01- 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-12", NativeTimeToISOTime, "2023-01-23 :56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-13", NativeTimeToISOTime, "2023-01-23 04::07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-14", NativeTimeToISOTime, "2023-01-23 04:56:.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-15", NativeTimeToISOTime, "2023-01-23 04:56:07.", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-16", NativeTimeToISOTime, "2023-01-23 04:56:07.890", 00, None)
    tester.converter_test_caller("2-9-17", NativeTimeToISOTime, "2023-01-23 04:56:07.890", "!!", None)
    tester.converter_test_caller("2-9-18", NativeTimeToISOTime, "2023-01-23 04:56:07.890", "aa", None)
    tester.converter_test_caller("2-9-19", NativeTimeToISOTime, "2023-01-23 04:56:07.890", "ｱｱ", None)
    tester.converter_test_caller("2-9-20", NativeTimeToISOTime, "2023-01-23 04:56:07.890", "００！！ｂｂああ", None)
    tester.converter_test_caller("2-9-21", NativeTimeToISOTime, "2023-01-23 04:56:07.890", "aa aa", None)
    tester.converter_test_caller("2-9-22", NativeTimeToISOTime, "2023-01-23 04:56:07.890", [], None)
    tester.converter_test_caller("2-9-23", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC"], None)
    tester.converter_test_caller("2-9-24", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T13:56:07.890000+0900")
    tester.converter_test_caller("2-9-25", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f", "UTC", "%Y/%m/%dT%H:%M:%S.%f%z"], "2023/01/22T19:56:07.890000Z")
    tester.converter_test_caller("2-9-26", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "UTC", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T04:56:07.890000Z")
    tester.converter_test_caller("2-9-27", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T04:56:07.890000+0900")
    tester.converter_test_caller("2-9-28", NativeTimeToISOTime, "2023-01-23 04:56:07.890", [None, "%Y-%m-%d %H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-29", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["日本", "%Y-%m-%d %H:%M:%S.%f%z"], None)
    tester.converter_test_caller("2-9-30", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", None], None)
    tester.converter_test_caller("2-9-31", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "年:月:日 時/分/秒"], None)
    tester.converter_test_caller("2-9-32", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f%z", None], None)
    tester.converter_test_caller("2-9-33", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f%z", "世界"], None)
    tester.converter_test_caller("2-9-34", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f%z", "Asia/Tokyo", None], None)
    tester.converter_test_caller("2-9-35", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f%z", "世界"], None)

    tester.converter_test_caller("2-10-1", Operation, 100, 2, "200")
    tester.converter_test_caller("2-10-2", Operation, "!!", 2, None)
    tester.converter_test_caller("2-10-3", Operation, "aa", 2, None)
    tester.converter_test_caller("2-10-4", Operation, "ｱｱ", 2, None)
    tester.converter_test_caller("2-10-5", Operation, "００！！ｂｂああ", 2, None)
    tester.converter_test_caller("2-10-6", Operation, "aa aa", 2, None)
    tester.converter_test_caller("2-10-7", Operation, None, 2, None)
    tester.converter_test_caller("2-10-8", Operation, 100, 1, "100")
    tester.converter_test_caller("2-10-9", Operation, sys.maxsize, 2, "18446744073709551614")
    tester.converter_test_caller("2-10-10", Operation, sys.maxsize+1, 2, "18446744073709551616")
    tester.converter_test_caller("2-10-11", Operation, 10, 2, "20")
    tester.converter_test_caller("2-10-12", Operation, 100, "!!", None)
    tester.converter_test_caller("2-10-13", Operation, 100, "aa", None)
    tester.converter_test_caller("2-10-14", Operation, 100, "ｱｱ", None)
    tester.converter_test_caller("2-10-15", Operation, 100, "００！！ｂｂああ", None)
    tester.converter_test_caller("2-10-16", Operation, 100, "aa aa", None)
    tester.converter_test_caller("2-10-17", Operation, 100, None, None)
    tester.converter_test_caller("2-10-18", Operation, 100, 4, "400")
    tester.converter_test_caller("2-10-19", Operation, 2, sys.maxsize, "18446744073709551614")
    tester.converter_test_caller("2-10-20", Operation, 2, sys.maxsize+1, "18446744073709551616")

    tester.converter_test_caller("2-11-1", Division, 100, 2, "50")
    tester.converter_test_caller("2-11-2", Division, "!!", 2, None)
    tester.converter_test_caller("2-11-3", Division, "aa", 2, None)
    tester.converter_test_caller("2-11-4", Division, "ｱｱ", 2, None)
    tester.converter_test_caller("2-11-5", Division, "００！！ｂｂああ", 2, None)
    tester.converter_test_caller("2-11-6", Division, "aa aa", 2, None)
    tester.converter_test_caller("2-11-7", Division, None, 2, None)
    tester.converter_test_caller("2-11-8", Division, 2, 2, "1")
    tester.converter_test_caller("2-11-9", Division, sys.maxsize, 2, "4611686018427387903.5")
    tester.converter_test_caller("2-11-10", Division, sys.maxsize+1, 2, "4611686018427387904")
    tester.converter_test_caller("2-11-11", Division, 100, 00, None)
    tester.converter_test_caller("2-11-12", Division, 100, "!!", None)
    tester.converter_test_caller("2-11-13", Division, 100, "aa", None)
    tester.converter_test_caller("2-11-14", Division, 100, "ｱｱ", None)
    tester.converter_test_caller("2-11-15", Division, 100, "００！！ｂｂああ", None)
    tester.converter_test_caller("2-11-16", Division, 100, "aa aa", None)
    tester.converter_test_caller("2-11-17", Division, 100, None, None)
    tester.converter_test_caller("2-11-18", Division, 100, 4, "25")
    tester.converter_test_caller("2-11-19", Division, 100, sys.maxsize, "1.084202172485504434125002236E-17")
    tester.converter_test_caller("2-11-20", Division, 100, sys.maxsize+1, "1.084202172485504434007452801E-17")

    tester.converter_test_caller("2-12-1", Max, 100, None, None)
    tester.converter_test_caller("2-12-2", Max, "!!", None, "!")
    tester.converter_test_caller("2-12-3", Max, "aa", None, "a")
    tester.converter_test_caller("2-12-4", Max, "ｱｱ", None, "ｱ")
    tester.converter_test_caller("2-12-5", Max, "００！！ｂｂああ", None, "ｂ")
    tester.converter_test_caller("2-12-6", Max, "aa aa", None, "a")
    tester.converter_test_caller("2-12-7", Max, None, None, None)
    tester.converter_test_caller("2-12-8", Max, [10,20,30,40,50], None, "50")
    tester.converter_test_caller("2-12-9", Max, ["10","20","30","40","50"], None, "50")
    tester.converter_test_caller("2-12-10", Max, [10,20,30,40,"AAA"], None, None)
    tester.converter_test_caller("2-12-11", Max, [sys.maxsize-1, sys.maxsize], None, "9223372036854775807")
    tester.converter_test_caller("2-12-12", Max, [sys.maxsize, sys.maxsize+1], None, "9223372036854775808")
    tester.converter_test_caller("2-12-13", Max, [10,20,30,40,50], 00, "50")
    tester.converter_test_caller("2-12-14", Max, [10,20,30,40,50], "!!", "50")
    tester.converter_test_caller("2-12-15", Max, [10,20,30,40,50], [1, "aa"], "50")
    tester.converter_test_caller("2-12-16", Max, [10,20,30,40,50], None, "50")

    tester.converter_test_caller("2-13-1", Min, 100, None, None)
    tester.converter_test_caller("2-13-2", Min, "!!", None, "!")
    tester.converter_test_caller("2-13-3", Min, "aa", None, "a")
    tester.converter_test_caller("2-13-4", Min, "ｱｱ", None, "ｱ")
    tester.converter_test_caller("2-13-5", Min, "００！！ｂｂああ", None, "あ")
    tester.converter_test_caller("2-13-6", Min, "aa aa", None, " ")
    tester.converter_test_caller("2-13-7", Min, None, None, None)
    tester.converter_test_caller("2-13-8", Min, [10,20,30,40,50], None, "10")
    tester.converter_test_caller("2-13-9", Min, ["10","20","30","40","50"], None, "10")
    tester.converter_test_caller("2-13-10", Min, ["AAA",20,30,40,50], None, None)
    tester.converter_test_caller("2-13-11", Min, [sys.maxsize-1, sys.maxsize], None, "9223372036854775806")
    tester.converter_test_caller("2-13-12", Min, [sys.maxsize, sys.maxsize+1], None, "9223372036854775807")
    tester.converter_test_caller("2-13-13", Min, [10,20,30,40,50], 00, "10")
    tester.converter_test_caller("2-13-14", Min, [10,20,30,40,50], "!!", "10")
    tester.converter_test_caller("2-13-15", Min, [10,20,30,40,50], [1, "aa"], "10")
    tester.converter_test_caller("2-13-16", Min, [10,20,30,40,50], None, "10")

    tester.converter_test_caller("2-14-1", Swap, 00, None, None)
    tester.converter_test_caller("2-14-2", Swap, "!!", None, "!!00")
    tester.converter_test_caller("2-14-3", Swap, "aa", None, "aa00")
    tester.converter_test_caller("2-14-4", Swap, "ｱｱ", None, "ｱｱ00")
    tester.converter_test_caller("2-14-5", Swap, "００！！ｂｂああ", None, "ああｂｂ")
    tester.converter_test_caller("2-14-6", Swap, "1000", None, "0010")
    tester.converter_test_caller("2-14-7", Swap, "100 200", None, "00 2")
    tester.converter_test_caller("2-14-8", Swap, None, None, None)
    tester.converter_test_caller("2-14-9", Swap, ["AA", "BB"], None, ["AA00","BB00"])
    tester.converter_test_caller("2-14-10", Swap, ["170","187"], None, ["7001", "8701"])
    tester.converter_test_caller("2-14-11", Swap, ["123456", "ABCDEF"], None, ["5634", "EFCD"])
    tester.converter_test_caller("2-14-12", Swap, sys.maxsize, None, None)
    tester.converter_test_caller("2-14-13", Swap, sys.maxsize+1, None, None)
    tester.converter_test_caller("2-14-14", Swap, [sys.maxsize-1,sys.maxsize], None, None)
    tester.converter_test_caller("2-14-15", Swap, [sys.maxsize,sys.maxsize+1], None, None)
    tester.converter_test_caller("2-14-16", Swap, "1000", 00, "0010")
    tester.converter_test_caller("2-14-17", Swap, "1000", "!!", "0010")
    tester.converter_test_caller("2-14-18", Swap, "1000", [1,"aa"], "0010")
    tester.converter_test_caller("2-14-19", Swap, "1000", None, "0010")

    tester.converter_test_caller("2-15-1", SetValue, 00, 100, 100)
    tester.converter_test_caller("2-15-2", SetValue, "!!", 100, 100)
    tester.converter_test_caller("2-15-3", SetValue, [1, "aa"], 100, 100)
    tester.converter_test_caller("2-15-4", SetValue, None, 100, 100)
    tester.converter_test_caller("2-15-5", SetValue, 100, 00, 00)
    tester.converter_test_caller("2-15-6", SetValue, 100, "!!" , "!!")
    tester.converter_test_caller("2-15-7", SetValue, 100, "aa" , "aa")
    tester.converter_test_caller("2-15-8", SetValue, 100, "ｱｱ" , "ｱｱ")
    tester.converter_test_caller("2-15-9", SetValue, 100, "００！！ｂｂああ" , "００！！ｂｂああ")
    tester.converter_test_caller("2-15-10", SetValue, 100, "aa aa" , "aa aa")
    tester.converter_test_caller("2-15-11", SetValue, 100, None , None)
    tester.converter_test_caller("2-15-12", SetValue, 100, 2 , 2)
    tester.converter_test_caller("2-15-13", SetValue, 100, sys.maxsize , sys.maxsize)
    tester.converter_test_caller("2-15-14", SetValue, 100, sys.maxsize+1 , sys.maxsize+1)

    tester.converter_test_caller("2-16-1", RevertFlag, 00, None, 1)
    tester.converter_test_caller("2-16-2", RevertFlag, "!!", None, None)
    tester.converter_test_caller("2-16-3", RevertFlag, "aa", None, None)
    tester.converter_test_caller("2-16-4", RevertFlag, "ｱｱ", None, None)
    tester.converter_test_caller("2-16-5", RevertFlag, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-16-6", RevertFlag, "aa aa", None, None)
    tester.converter_test_caller("2-16-7", RevertFlag, None, None, None)
    tester.converter_test_caller("2-16-8", RevertFlag, 100, None, 0)
    tester.converter_test_caller("2-16-9", RevertFlag, sys.maxsize, None, 0)
    tester.converter_test_caller("2-16-10", RevertFlag, sys.maxsize+1, None, 0)
    tester.converter_test_caller("2-16-11", RevertFlag, 100, 00, 0)
    tester.converter_test_caller("2-16-12", RevertFlag, 100, "!!", 0)
    tester.converter_test_caller("2-16-13", RevertFlag, 100, [1, "aa"], 0)
    tester.converter_test_caller("2-16-14", RevertFlag, 100, None, 0)

    tester.converter_test_caller("2-17-1", two_word_to_hour, 00, None, None)
    tester.converter_test_caller("2-17-2", two_word_to_hour, "!!", None, None)
    tester.converter_test_caller("2-17-3", two_word_to_hour, "aa", None, None)
    tester.converter_test_caller("2-17-4", two_word_to_hour, "ｱｱ", None, None)
    tester.converter_test_caller("2-17-5", two_word_to_hour, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-17-6", two_word_to_hour, "1000", None, None)
    tester.converter_test_caller("2-17-7", two_word_to_hour, "100 200", None, None)
    tester.converter_test_caller("2-17-8", two_word_to_hour, None, None, None)
    tester.converter_test_caller("2-17-9", two_word_to_hour, [54,12345], None, 0.9864691666666666)
    tester.converter_test_caller("2-17-10", two_word_to_hour, ["54","12345"], None, 0.9864691666666666)
    tester.converter_test_caller("2-17-11", two_word_to_hour, [123456, 123456], None, 1054.4175111111113)
    tester.converter_test_caller("2-17-12", two_word_to_hour, [sys.maxsize-1, sys.maxsize], None, 1193.0282663888888)
    tester.converter_test_caller("2-17-13", two_word_to_hour, [sys.maxsize, sys.maxsize+1], None, 1193.0282666666667)
    tester.converter_test_caller("2-17-14", two_word_to_hour, [54,12345], 00, 0.9864691666666666)
    tester.converter_test_caller("2-17-15", two_word_to_hour, [54,12345], "!!", 0.9864691666666666)
    tester.converter_test_caller("2-17-16", two_word_to_hour, [54,12345], [1, "aa"], 0.9864691666666666)
    tester.converter_test_caller("2-17-17", two_word_to_hour, [54,12345], None, 0.9864691666666666)

    tester.converter_test_caller("2-18-1", join, 00, ",", None)
    tester.converter_test_caller("2-18-2", join, "!!", ",", None)
    tester.converter_test_caller("2-18-3", join, "aa", ",", None)
    tester.converter_test_caller("2-18-4", join, "ｱｱ", ",", None)
    tester.converter_test_caller("2-18-5", join, "００！！ｂｂああ", ",", None)
    tester.converter_test_caller("2-18-6", join, "1000", ",", None)
    tester.converter_test_caller("2-18-7", join, "100 200", ",", None)
    tester.converter_test_caller("2-18-8", join, None, ",", None)
    tester.converter_test_caller("2-18-9", join, [54,12345], ",", "54,12345")
    tester.converter_test_caller("2-18-10", join, ["54","12345"], ",", "54,12345")
    tester.converter_test_caller("2-18-11", join, ["12345",None], ",", None)
    tester.converter_test_caller("2-18-12", join, [sys.maxsize-1, sys.maxsize], ",", "9223372036854775806,9223372036854775807")
    tester.converter_test_caller("2-18-13", join, [sys.maxsize, sys.maxsize+1], ",", "9223372036854775807,9223372036854775808")
    tester.converter_test_caller("2-18-14", join, [54,12345], 00, None)
    tester.converter_test_caller("2-18-15", join, [54,12345], "!!", "54!12345")
    tester.converter_test_caller("2-18-16", join, [54,12345], "aa", "54a12345")
    tester.converter_test_caller("2-18-17", join, [54,12345], "ｱｱ", "54ｱ12345")
    tester.converter_test_caller("2-18-18", join, [54,12345], "００！！ｂｂああ", "54０12345")
    tester.converter_test_caller("2-18-19", join, [54,12345], "aa aa", "54a12345")
    tester.converter_test_caller("2-18-20", join, [54,12345], "aa 00", "54a12345")
    tester.converter_test_caller("2-18-21", join, [54,12345], "!! 00", "54!12345")
    tester.converter_test_caller("2-18-22", join, [54,12345], "ｱｱ 00", "54ｱ12345")
    tester.converter_test_caller("2-18-23", join, [54,12345], None, "5412345")

    tester.converter_test_caller("2-19-1", Join, 00, ",", None)
    tester.converter_test_caller("2-19-2", Join, "!!", ",", None)
    tester.converter_test_caller("2-19-3", Join, "aa", ",", None)
    tester.converter_test_caller("2-19-4", Join, "ｱｱ", ",", None)
    tester.converter_test_caller("2-19-5", Join, "００！！ｂｂああ", ",", None)
    tester.converter_test_caller("2-19-6", Join, "1000", ",", None)
    tester.converter_test_caller("2-19-7", Join, "100 200", ",", None)
    tester.converter_test_caller("2-19-8", Join, None, ",", None)
    tester.converter_test_caller("2-19-9", Join, [54,12345], ",", "54,12345")
    tester.converter_test_caller("2-19-10", Join, ["54","12345"], ",", "54,12345")
    tester.converter_test_caller("2-19-11", Join, ["123456",None], ",", None)
    tester.converter_test_caller("2-19-12", Join, [sys.maxsize-1, sys.maxsize], ",", "9223372036854775806,9223372036854775807")
    tester.converter_test_caller("2-19-13", Join, [sys.maxsize, sys.maxsize+1], ",", "9223372036854775807,9223372036854775808")
    tester.converter_test_caller("2-19-14", Join, [54,12345], 00, None)
    tester.converter_test_caller("2-19-15", Join, [54,12345], "!!", "54!12345")
    tester.converter_test_caller("2-19-16", Join, [54,12345], "aa", "54a12345")
    tester.converter_test_caller("2-19-17", Join, [54,12345], "ｱｱ", "54ｱ12345")
    tester.converter_test_caller("2-19-18", Join, [54,12345], "００！！ｂｂああ", "54０12345")
    tester.converter_test_caller("2-19-19", Join, [54,12345], "aa aa", "54a12345")
    tester.converter_test_caller("2-19-20", Join, [54,12345], "aa 00", "54a12345")
    tester.converter_test_caller("2-19-21", Join, [54,12345], "!! 00", "54!12345")
    tester.converter_test_caller("2-19-22", Join, [54,12345], "ｱｱ 00", "54ｱ12345")
    tester.converter_test_caller("2-19-23", Join, [54,12345], None, "5412345")

    tester.converter_test_caller("2-20-1", substring, 00, [2,3], "")
    tester.converter_test_caller("2-20-2", substring, "!!", [2,3], "!")
    tester.converter_test_caller("2-20-3", substring, "aa", [2,3], "a")
    tester.converter_test_caller("2-20-4", substring, "ｱｱ", [2,3], "ｱ")
    tester.converter_test_caller("2-20-5", substring, "００！！ｂｂああ", [2,3], "０！！")
    tester.converter_test_caller("2-20-6", substring, "1000", [2,3], "000")
    tester.converter_test_caller("2-20-7", substring, "100 200", [2,3], "00 ")
    tester.converter_test_caller("2-20-8", substring, None, [2,3], None)
    tester.converter_test_caller("2-20-9", substring, "ABCDEFGHI", [2,3], "BCD")
    tester.converter_test_caller("2-20-10", substring, "123456", 00, "")
    tester.converter_test_caller("2-20-11", substring, "123456", "!!", None)
    tester.converter_test_caller("2-20-12", substring, "123456", "aa", None)
    tester.converter_test_caller("2-20-13", substring, "123456", "ｱｱ", None)
    tester.converter_test_caller("2-20-14", substring, "123456", "００！！ｂｂああ", None)
    tester.converter_test_caller("2-20-15", substring, "123456", "aa aa", None)
    tester.converter_test_caller("2-20-16", substring, "123456", None, "123456")
    tester.converter_test_caller("2-20-17", substring, "123456", [1], "123456")
    tester.converter_test_caller("2-20-18", substring, "123456", [-1], "6")
    tester.converter_test_caller("2-20-19", substring, "123456", [1,2], "12")
    tester.converter_test_caller("2-20-20", substring, "123456", ["1","2"], "12")
    tester.converter_test_caller("2-20-21", substring, "123456", [1,0], "")
    tester.converter_test_caller("2-20-22", substring, "123456", [-1,0], "")
    tester.converter_test_caller("2-20-23", substring, "123456", [-1,-2], "6")
    tester.converter_test_caller("2-20-24", substring, "123456", ["-1","-2"], "6")
    tester.converter_test_caller("2-20-25", substring, "123456", [",",2], None)
    tester.converter_test_caller("2-20-26", substring, "123456", [1,","], None)
    tester.converter_test_caller("2-20-27", substring, "123456", sys.maxsize, "")
    tester.converter_test_caller("2-20-28", substring, "123456", sys.maxsize+1, "")
    tester.converter_test_caller("2-20-29", substring, "123456", [sys.maxsize-1, sys.maxsize], "")
    tester.converter_test_caller("2-20-30", substring, "123456", [sys.maxsize, sys.maxsize+1], "")
    tester.converter_test_caller("2-20-31", substring, "123456", -sys.maxsize, "")
    tester.converter_test_caller("2-20-32", substring, "123456", -sys.maxsize-1, "")
    tester.converter_test_caller("2-20-33", substring, "123456", [-sys.maxsize+1, -sys.maxsize], "")
    tester.converter_test_caller("2-20-34", substring, "123456", [-sys.maxsize, -sys.maxsize-1], "")

    tester.converter_test_caller("2-21-1", SubString, 00, [2,3], "")
    tester.converter_test_caller("2-21-2", SubString, "!!", [2,3], "!")
    tester.converter_test_caller("2-21-3", SubString, "aa", [2,3], "a")
    tester.converter_test_caller("2-21-4", SubString, "ｱｱ", [2,3], "ｱ")
    tester.converter_test_caller("2-21-5", SubString, "００！！ｂｂああ", [2,3], "０！！")
    tester.converter_test_caller("2-21-6", SubString, "1000", [2,3], "000")
    tester.converter_test_caller("2-21-7", SubString, "100 200", [2,3], "00 ")
    tester.converter_test_caller("2-21-8", SubString, None, [2,3], None)
    tester.converter_test_caller("2-21-9", SubString, "ABCDEFGHI", [2,3], "BCD")
    tester.converter_test_caller("2-21-10", SubString, "123456", 00, "")
    tester.converter_test_caller("2-21-11", SubString, "123456", "!!", None)
    tester.converter_test_caller("2-21-12", SubString, "123456", "aa", None)
    tester.converter_test_caller("2-21-13", SubString, "123456", "ｱｱ", None)
    tester.converter_test_caller("2-21-14", SubString, "123456", "００！！ｂｂああ", None)
    tester.converter_test_caller("2-21-15", SubString, "123456", "aa aa", None)
    tester.converter_test_caller("2-21-16", SubString, "123456", None, "123456")
    tester.converter_test_caller("2-21-17", SubString, "123456", [1], "123456")
    tester.converter_test_caller("2-21-18", SubString, "123456", [-1], "6")
    tester.converter_test_caller("2-21-19", SubString, "123456", [1,2], "12")
    tester.converter_test_caller("2-21-20", SubString, "123456", ["1","2"], "12")
    tester.converter_test_caller("2-21-21", SubString, "123456", [1,0], "")
    tester.converter_test_caller("2-21-22", SubString, "123456", [-1,0], "")
    tester.converter_test_caller("2-21-23", SubString, "123456", [-1,-2], "6")
    tester.converter_test_caller("2-21-24", SubString, "123456", ["-1","-2"], "6")
    tester.converter_test_caller("2-21-25", SubString, "123456", [",",2], None)
    tester.converter_test_caller("2-21-26", SubString, "123456", [1,","], None)
    tester.converter_test_caller("2-21-27", SubString, "123456", sys.maxsize, "")
    tester.converter_test_caller("2-21-28", SubString, "123456", sys.maxsize+1, "")
    tester.converter_test_caller("2-21-29", SubString, "123456", [sys.maxsize-1, sys.maxsize], "")
    tester.converter_test_caller("2-21-30", SubString, "123456", [sys.maxsize, sys.maxsize+1], "")
    tester.converter_test_caller("2-21-31", SubString, "123456", -sys.maxsize, "")
    tester.converter_test_caller("2-21-32", SubString, "123456", -sys.maxsize-1, "")
    tester.converter_test_caller("2-21-33", SubString, "123456", [-sys.maxsize+1, -sys.maxsize], "")
    tester.converter_test_caller("2-21-34", SubString, "123456", [-sys.maxsize, -sys.maxsize-1], "")

    tester.converter_test_caller("2-22-1", split, "012", ["1"], "0")
    tester.converter_test_caller("2-22-2", split, "!/@;", ["@"], "!/")
    tester.converter_test_caller("2-22-3", split, "abcde", ["d"], "abc")
    tester.converter_test_caller("2-22-4", split, "ｱｲｳｴｵ", ["ｵ"], "ｱｲｳｴ")
    tester.converter_test_caller("2-22-5", split, "０１！＠Aｂああ", ["A"], "０１！＠")
    tester.converter_test_caller("2-22-6", split, "a1b2c", ["b"], "a1")
    tester.converter_test_caller("2-22-7", split, "100 200", [" "], "100")
    tester.converter_test_caller("2-22-8", split, None, [","], None)
    tester.converter_test_caller("2-22-9", split, "ABC,DEF,GHI", [","], "ABC")
    tester.converter_test_caller("2-22-10", split, "ABC1DEF1GHI", ["1"], "ABC")
    tester.converter_test_caller("2-22-11", split, 5678901234, 12, "567890")
    tester.converter_test_caller("2-22-12", split, "[[]]!!//^^", "!!", "[[]]")
    tester.converter_test_caller("2-22-13", split, "a12345aa67890a", "aa", "a12345")
    tester.converter_test_caller("2-22-14", split, "ｱｶｻﾀﾅｱｱﾊﾏﾔﾗﾜ", "ｱｱ", "ｱｶｻﾀﾅ")
    tester.converter_test_caller("2-22-15", split, "あｚｊ３・９０１！＠Aｂああ９－０ｓ・ぃ", "０１！＠Aｂああ", "あｚｊ３・９")
    tester.converter_test_caller("2-22-16", split, "a12345aaaa67aa aa890a", "aa aa", "a12345aaaa67")
    tester.converter_test_caller("2-22-17", split, "12345None67890", None, None)
    tester.converter_test_caller("2-22-18", split, "12345,67890", [",", 2], "67890")
    tester.converter_test_caller("2-22-19", split, "12345,67890", [",", "3"], None)
    tester.converter_test_caller("2-22-20", split, "12345,67890", [",", -1], None)
    tester.converter_test_caller("2-22-21", split, "12345,67890,54321", [",", sys.maxsize], None)
    tester.converter_test_caller("2-22-22", split, "12345,67890,54321", [",", sys.maxsize+1], None)
    
    tester.converter_test_caller("2-23-1", Split, "012", ["1"], "0")
    tester.converter_test_caller("2-23-2", Split, "!/@;", ["@"], "!/")
    tester.converter_test_caller("2-23-3", Split, "abcde", "d", "abc")
    tester.converter_test_caller("2-23-4", Split, "ｱｲｳｴｵ", "ｵ", "ｱｲｳｴ")
    tester.converter_test_caller("2-23-5", Split, "０１！＠Aｂああ", ["A"], "０１！＠")
    tester.converter_test_caller("2-23-6", Split, "a1b2c", ["b"], "a1")
    tester.converter_test_caller("2-23-7", Split, "100 200", [" "], "100")
    tester.converter_test_caller("2-23-8", Split, None, [","], None)
    tester.converter_test_caller("2-23-9", Split, "ABC,DEF,GHI", [","], "ABC")
    tester.converter_test_caller("2-23-10", Split, "ABC1DEF1GHI", ["1"], "ABC")
    tester.converter_test_caller("2-23-11", Split, 5678901234, 12, "567890")
    tester.converter_test_caller("2-23-12", Split, "[[]]!!//^^", "!!", "[[]]")
    tester.converter_test_caller("2-23-13", Split, "a12345aa67890a", "aa", "a12345")
    tester.converter_test_caller("2-23-14", Split, "ｱｶｻﾀﾅｱｱﾊﾏﾔﾗﾜ", "ｱｱ", "ｱｶｻﾀﾅ")
    tester.converter_test_caller("2-23-15", Split, "あｚｊ３・９０１！＠Aｂああ９－０ｓ・ぃ", "０１！＠Aｂああ", "あｚｊ３・９")
    tester.converter_test_caller("2-23-16", Split, "a12345aaaa67aa aa890a", "aa aa", "a12345aaaa67")
    tester.converter_test_caller("2-23-17", Split, "12345None67890", None, None)
    tester.converter_test_caller("2-23-18", Split, "12345,67890", [",", 2], "67890")
    tester.converter_test_caller("2-23-19", Split, "12345,67890", [",", "3"], None)
    tester.converter_test_caller("2-23-20", Split, "12345,67890", [",", -1], None)
    tester.converter_test_caller("2-23-21", Split, "12345,67890,54321", [",", sys.maxsize], None)
    tester.converter_test_caller("2-23-22", Split, "12345,67890,54321", [",", sys.maxsize+1], None)
    
    tester.converter_test_caller("2-24-1", trim, 00, None, None)
    tester.converter_test_caller("2-24-2", trim, "!!", None, "!!")
    tester.converter_test_caller("2-24-3", trim, "aa", None, "aa")
    tester.converter_test_caller("2-24-4", trim, "ｱｱ", None, "ｱｱ")
    tester.converter_test_caller("2-24-5", trim, "００！！ｂｂああ", None, "００！！ｂｂああ")
    tester.converter_test_caller("2-24-6", trim, "1000", None, "1000")
    tester.converter_test_caller("2-24-7", trim, "100 200 300", None, "100200300")
    tester.converter_test_caller("2-24-8", trim, "100　200　300", None, "100　200　300")
    tester.converter_test_caller("2-24-9", trim, None, None, None)
    tester.converter_test_caller("2-24-10", trim, "ABC DEF", None, "ABCDEF")
    tester.converter_test_caller("2-24-11", trim, ["ABCDEF GHI", "123 456"], None, ["ABCDEFGHI", "123456"])
    tester.converter_test_caller("2-24-12", trim, ["ABCDEF GHI", None], None, None)
    tester.converter_test_caller("2-24-13", trim, "aaa bb", 00, "aaabb")
    tester.converter_test_caller("2-24-14", trim, "aaa bb", "!!", "aaabb")
    tester.converter_test_caller("2-24-15", trim, "aaa bb", [1,"aa"], "aaabb")
    tester.converter_test_caller("2-24-16", trim, "aaa bb", None, "aaabb")

    tester.converter_test_caller("2-25-1", Trim, 00, None, None)
    tester.converter_test_caller("2-25-2", Trim, "!!", None, "!!")
    tester.converter_test_caller("2-25-3", Trim, "aa", None, "aa")
    tester.converter_test_caller("2-25-4", Trim, "ｱｱ", None, "ｱｱ")
    tester.converter_test_caller("2-25-5", Trim, "００！！ｂｂああ", None, "００！！ｂｂああ")
    tester.converter_test_caller("2-25-6", Trim, "1000", None, "1000")
    tester.converter_test_caller("2-25-7", Trim, "100 200 300", None, "100200300")
    tester.converter_test_caller("2-25-8", Trim, "100　200　300", None, "100　200　300")
    tester.converter_test_caller("2-25-9", Trim, None, None, None)
    tester.converter_test_caller("2-25-10", Trim, "ABC DEF", None, "ABCDEF")
    tester.converter_test_caller("2-25-11", Trim, ["ABCDEF GHI", "123 456"], None, ["ABCDEFGHI", "123456"])
    tester.converter_test_caller("2-25-12", Trim, ["ABCDEF GHI", None], None, None)
    tester.converter_test_caller("2-25-13", Trim, "aaa bb", 00, "aaabb")
    tester.converter_test_caller("2-25-14", Trim, "aaa bb", "!!", "aaabb")
    tester.converter_test_caller("2-25-15", Trim, "aaa bb", [1,"aa"], "aaabb")
    tester.converter_test_caller("2-25-16", Trim, "aaa bb", None, "aaabb")

    tester.converter_test_caller("2-26-1", dec_to_hex, 00, None, "0000")
    tester.converter_test_caller("2-26-2", dec_to_hex, "!!", None, None)
    tester.converter_test_caller("2-26-3", dec_to_hex, "aa", None, None)
    tester.converter_test_caller("2-26-4", dec_to_hex, "ｱｱ", None, None)
    tester.converter_test_caller("2-26-5", dec_to_hex, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-26-6", dec_to_hex, "1000", None, "03e8")
    tester.converter_test_caller("2-26-7", dec_to_hex, "100 200", None, None)
    tester.converter_test_caller("2-26-8", dec_to_hex, None, None, None)
    tester.converter_test_caller("2-26-9", dec_to_hex, 2069, None, "0815")
    tester.converter_test_caller("2-26-10", dec_to_hex, -100, None,"ff9c")
    tester.converter_test_caller("2-26-11", dec_to_hex, [2069, 3845, 12322], None, ["0815","0f05","3022"])
    tester.converter_test_caller("2-26-12", dec_to_hex, ["2069", "3845", "12322"], None, ["0815","0f05","3022"])
    tester.converter_test_caller("2-26-13", dec_to_hex, [-100, -200, -300], None, ["ff9c", "ff38", "fed4"])
    tester.converter_test_caller("2-26-14", dec_to_hex, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-26-15", dec_to_hex, [2069, 3845, None], None, None)
    tester.converter_test_caller("2-26-16", dec_to_hex, sys.maxsize, None, "ffff")
    tester.converter_test_caller("2-26-17", dec_to_hex, sys.maxsize+1, None, "0000")
    tester.converter_test_caller("2-26-18", dec_to_hex, sys.maxsize-1, None, "fffe")
    tester.converter_test_caller("2-26-19", dec_to_hex, [sys.maxsize, sys.maxsize+1], None, ["ffff","0000"])
    tester.converter_test_caller("2-26-20", dec_to_hex, -sys.maxsize, None, "ffff")
    tester.converter_test_caller("2-26-21", dec_to_hex, -sys.maxsize-1, None, "0000")
    tester.converter_test_caller("2-26-22", dec_to_hex, [-sys.maxsize+1, -sys.maxsize], None, ["fffe","ffff"])
    tester.converter_test_caller("2-26-23", dec_to_hex, [-sys.maxsize, -sys.maxsize-1], None, ["ffff","0000"])
    tester.converter_test_caller("2-26-24", dec_to_hex, "00", 00, "0000")
    tester.converter_test_caller("2-26-25", dec_to_hex, "00", "!!", "0000")
    tester.converter_test_caller("2-26-26", dec_to_hex, "00", [1,"aa"], "0000")
    tester.converter_test_caller("2-26-27", dec_to_hex, "00", None, "0000")

    tester.converter_test_caller("2-27-1", DecToHex, 00, None, "0000")
    tester.converter_test_caller("2-27-2", DecToHex, "!!", None, None)
    tester.converter_test_caller("2-27-3", DecToHex, "aa", None, None)
    tester.converter_test_caller("2-27-4", DecToHex, "ｱｱ", None, None)
    tester.converter_test_caller("2-27-5", DecToHex, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-27-6", DecToHex, "1000", None, "03e8")
    tester.converter_test_caller("2-27-7", DecToHex, "100 200", None, None)
    tester.converter_test_caller("2-27-8", DecToHex, None, None, None)
    tester.converter_test_caller("2-27-9", DecToHex, 2069, None, "0815")
    tester.converter_test_caller("2-27-10", DecToHex, -100, None, "ff9c")
    tester.converter_test_caller("2-27-11", DecToHex, [2069, 3845, 12322], None, ["0815","0f05","3022"])
    tester.converter_test_caller("2-27-12", DecToHex, ["2069", "3845", "12322"], None, ["0815","0f05","3022"])
    tester.converter_test_caller("2-27-13", DecToHex, [-100, -200, -300], None, ["ff9c", "ff38", "fed4"])
    tester.converter_test_caller("2-27-14", DecToHex, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-27-15", DecToHex, [2069, 3845, None], None, None)
    tester.converter_test_caller("2-27-16", DecToHex, sys.maxsize, None, "ffff")
    tester.converter_test_caller("2-27-17", DecToHex, sys.maxsize+1, None, "0000")
    tester.converter_test_caller("2-27-18", DecToHex, sys.maxsize-1, None, "fffe")
    tester.converter_test_caller("2-27-19", DecToHex, [sys.maxsize, sys.maxsize+1], None, ["ffff","0000"])
    tester.converter_test_caller("2-27-20", DecToHex, -sys.maxsize, None, "ffff")
    tester.converter_test_caller("2-27-21", DecToHex, -sys.maxsize-1, None, "0000")
    tester.converter_test_caller("2-27-22", DecToHex, [-sys.maxsize+1, -sys.maxsize], None, ["fffe","ffff"])
    tester.converter_test_caller("2-27-23", DecToHex, [-sys.maxsize, -sys.maxsize-1], None, ["ffff","0000"])
    tester.converter_test_caller("2-27-24", DecToHex, "00", 00, "0000")
    tester.converter_test_caller("2-27-25", DecToHex, "00", "!!", "0000")
    tester.converter_test_caller("2-27-26", DecToHex, "00", [1, "aa"], "0000")
    tester.converter_test_caller("2-27-27", DecToHex, "00", None, "0000")
    
    tester.converter_test_caller("2-28-1", HexToDec, 00, None, None)
    tester.converter_test_caller("2-28-2", HexToDec, "!!", None, None)
    tester.converter_test_caller("2-28-3", HexToDec, "aa", None, 170)
    tester.converter_test_caller("2-28-4", HexToDec, "ｱｱ", None, None)
    tester.converter_test_caller("2-28-5", HexToDec, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-28-6", HexToDec, "1000", None, 4096)
    tester.converter_test_caller("2-28-7", HexToDec, "100 200", None, 512)
    tester.converter_test_caller("2-28-8", HexToDec, None, None, None)
    tester.converter_test_caller("2-28-9", HexToDec, "2069", None, 8297)
    tester.converter_test_caller("2-28-10", HexToDec, "32768", None, 10088)
    tester.converter_test_caller("2-28-11", HexToDec, ["2069", "3845", "12322"], None, [8297, 14405, 8994])
    tester.converter_test_caller("2-28-12", HexToDec, ["2069", "3845", "32768"], None, [8297, 14405, 10088])    
    tester.converter_test_caller("2-28-13", HexToDec, f"{sys.maxsize}", None, 22535)
    tester.converter_test_caller("2-28-14", HexToDec, f"{sys.maxsize+1}", None, 22536)
    tester.converter_test_caller("2-28-15", HexToDec, [f"{sys.maxsize-1}", f"{sys.maxsize}"], None, [22534, 22535])
    tester.converter_test_caller("2-28-16", HexToDec, [f"{sys.maxsize}", f"{sys.maxsize+1}"], None, [22535, 22536])
    tester.converter_test_caller("2-28-17", HexToDec, "00", 00, 0)
    tester.converter_test_caller("2-28-18", HexToDec, "00", "!!", 0)
    tester.converter_test_caller("2-28-19", HexToDec, "00", [1, "aa"], 0) 
    tester.converter_test_caller("2-28-20", HexToDec, "00", None, 0)

    tester.converter_test_caller("2-29-1", bit_to_dec, 00, None, None)
    tester.converter_test_caller("2-29-2", bit_to_dec, "!!", None, None)
    tester.converter_test_caller("2-29-3", bit_to_dec, "aa", None, None)
    tester.converter_test_caller("2-29-4", bit_to_dec, "ｱｱ", None, None)
    tester.converter_test_caller("2-29-5", bit_to_dec, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-29-6", bit_to_dec, "1000", None, 8)
    tester.converter_test_caller("2-29-7", bit_to_dec, "100 200", None, None)
    tester.converter_test_caller("2-29-8", bit_to_dec, None, None, None)
    tester.converter_test_caller("2-29-9", bit_to_dec, "01111111", None, 127)
    tester.converter_test_caller("2-29-10", bit_to_dec, "11111111", None, -1)
    #tester.converter_test_caller("2-29-11", bit_to_dec, [00001111, 00011111, 00111111], None, None)
    tester.converter_test_caller("2-29-12", bit_to_dec, ["00001111", "00011111", "00111111"], None, [15, 31, 63])
    tester.converter_test_caller("2-29-13", bit_to_dec, [10001111, 10011111, 10111111], None, None)
    tester.converter_test_caller("2-29-14", bit_to_dec, ["10001111", "10011111", "10111111"], None, [-113, -97, -65])
    tester.converter_test_caller("2-29-15", bit_to_dec, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-29-16", bit_to_dec, ["00001111","00011111", None], None, None)
    tester.converter_test_caller("2-29-17", bit_to_dec, f"{sys.maxsize}", None, None)
    tester.converter_test_caller("2-29-18", bit_to_dec, f"{sys.maxsize+1}", None, None)
    tester.converter_test_caller("2-29-19", bit_to_dec, [f"{sys.maxsize-1}", f"{sys.maxsize}"], None, None)
    tester.converter_test_caller("2-29-20", bit_to_dec, [f"{sys.maxsize}", f"{sys.maxsize+1}"], None, None)
    tester.converter_test_caller("2-29-21", bit_to_dec, f"{-sys.maxsize}", None, None)
    tester.converter_test_caller("2-29-22", bit_to_dec, f"{-sys.maxsize-1}", None, None)
    tester.converter_test_caller("2-29-23", bit_to_dec, [f"{-sys.maxsize+1}", f"{-sys.maxsize}"], None, None)
    tester.converter_test_caller("2-29-24", bit_to_dec, [f"{-sys.maxsize}", f"{-sys.maxsize-1}"], None, None)
    tester.converter_test_caller("2-29-25", bit_to_dec, "00", 00, 0)
    tester.converter_test_caller("2-29-26", bit_to_dec, "00", "!!", 0)
    tester.converter_test_caller("2-29-27", bit_to_dec, "00", [1, "aa"], 0)
    tester.converter_test_caller("2-29-28", bit_to_dec, "00", None, 0)

    tester.converter_test_caller("2-30-1", BitToDec, 00, None, None)
    tester.converter_test_caller("2-30-2", BitToDec, "!!", None, None)
    tester.converter_test_caller("2-30-3", BitToDec, "aa", None, None)
    tester.converter_test_caller("2-30-4", BitToDec, "ｱｱ", None, None)
    tester.converter_test_caller("2-30-5", BitToDec, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-30-6", BitToDec, "1000", None, 8)
    tester.converter_test_caller("2-30-7", BitToDec, "100 200", None, None)
    tester.converter_test_caller("2-30-8", BitToDec, None, None, None)
    tester.converter_test_caller("2-30-9", BitToDec, "01111111", None, 127)
    tester.converter_test_caller("2-30-10", BitToDec, "11111111", None, -1)
    #tester.converter_test_caller("2-30-11", BitToDec, [00001111, 00011111, 00111111], None, None)
    tester.converter_test_caller("2-30-12", BitToDec, ["00001111", "00011111", "00111111"], None, [15, 31, 63])
    tester.converter_test_caller("2-30-13", BitToDec, [10001111, 10011111, 10111111], None, None)
    tester.converter_test_caller("2-30-14", BitToDec, ["10001111", "10011111", "10111111"], None, [-113, -97, -65])
    tester.converter_test_caller("2-30-15", BitToDec, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-30-16", BitToDec, ["00001111","00011111", None], None, None)
    tester.converter_test_caller("2-30-17", BitToDec, f"{sys.maxsize}", None, None)
    tester.converter_test_caller("2-30-18", BitToDec, f"{sys.maxsize+1}", None, None)
    tester.converter_test_caller("2-30-19", BitToDec, [f"{sys.maxsize-1}", f"{sys.maxsize}"], None, None)
    tester.converter_test_caller("2-30-20", BitToDec, [f"{sys.maxsize}", f"{sys.maxsize+1}"], None, None)
    tester.converter_test_caller("2-30-21", BitToDec, f"{-sys.maxsize}", None, None)
    tester.converter_test_caller("2-30-22", BitToDec, f"{-sys.maxsize-1}", None, None)
    tester.converter_test_caller("2-30-23", BitToDec, [f"{-sys.maxsize+1}", f"{-sys.maxsize}"], None, None)
    tester.converter_test_caller("2-30-24", BitToDec, [f"{-sys.maxsize}", f"{-sys.maxsize-1}"], None, None)
    tester.converter_test_caller("2-30-25", BitToDec, "00", 00, 0)
    tester.converter_test_caller("2-30-26", BitToDec, "00", "!!", 0)
    tester.converter_test_caller("2-30-27", BitToDec, "00", [1, "aa"], 0)
    tester.converter_test_caller("2-30-28", BitToDec, "00", None, 0)
    
    tester.converter_test_caller("2-31-1", DecToBit, 00, None, "0000000000000000")
    tester.converter_test_caller("2-31-2", DecToBit, "!!", None, None)
    tester.converter_test_caller("2-31-3", DecToBit, "aa", None, None)
    tester.converter_test_caller("2-31-4", DecToBit, "ｱｱ", None, None)
    tester.converter_test_caller("2-31-5", DecToBit, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-31-6", DecToBit, "1000", None, "0000001111101000")
    tester.converter_test_caller("2-31-7", DecToBit, "100 200", None, None)
    tester.converter_test_caller("2-31-8", DecToBit, None, None, None)
    tester.converter_test_caller("2-31-9", DecToBit, 2069, None, "0000100000010101")
    tester.converter_test_caller("2-31-10", DecToBit, -100, None, "1111111110011100")
    tester.converter_test_caller("2-31-11", DecToBit, [2069, 3845, 12322], None, ["0000100000010101", "0000111100000101", "0011000000100010"])
    tester.converter_test_caller("2-31-12", DecToBit, ["2069", "3845", "12322"], None, ["0000100000010101", "0000111100000101", "0011000000100010"])
    tester.converter_test_caller("2-31-13", DecToBit, [-100, -200, -300], None, ['1111111110011100', '1111111100111000', '1111111011010100'])
    tester.converter_test_caller("2-31-14", DecToBit, ["-100", "-200", "-300"], None, ['1111111110011100', '1111111100111000', '1111111011010100'])
    tester.converter_test_caller("2-31-15", DecToBit, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-31-16", DecToBit, [2069, 3845, None], None, None)
    tester.converter_test_caller("2-31-17", DecToBit, sys.maxsize, None, "111111111111111111111111111111111111111111111111111111111111111")
    tester.converter_test_caller("2-31-18", DecToBit, sys.maxsize+1, None, "1000000000000000000000000000000000000000000000000000000000000000")
    tester.converter_test_caller("2-31-19", DecToBit, [sys.maxsize-1, sys.maxsize], None, ['111111111111111111111111111111111111111111111111111111111111110', '111111111111111111111111111111111111111111111111111111111111111'])
    tester.converter_test_caller("2-31-20", DecToBit, [sys.maxsize, sys.maxsize+1], None, ['111111111111111111111111111111111111111111111111111111111111111', "1000000000000000000000000000000000000000000000000000000000000000"])
    tester.converter_test_caller("2-31-21", DecToBit, -sys.maxsize, None, "-111111111111111111111111111111111111111111111101111111111111111")
    tester.converter_test_caller("2-31-22", DecToBit, -sys.maxsize-1, None, "-111111111111111111111111111111111111111111111110000000000000000")
    tester.converter_test_caller("2-31-23", DecToBit, [-sys.maxsize+1, -sys.maxsize], None, ['-111111111111111111111111111111111111111111111101111111111111110', '-111111111111111111111111111111111111111111111101111111111111111'])
    tester.converter_test_caller("2-31-24", DecToBit, [-sys.maxsize, -sys.maxsize-1], None, ["-111111111111111111111111111111111111111111111101111111111111111", "-111111111111111111111111111111111111111111111110000000000000000"])
    tester.converter_test_caller("2-31-25", DecToBit, "00", 00, "0000000000000000")
    tester.converter_test_caller("2-31-26", DecToBit, "00", "!!", "0000000000000000")
    tester.converter_test_caller("2-31-27", DecToBit, "00", [1, "aa"], "0000000000000000")
    tester.converter_test_caller("2-31-28", DecToBit, "00", None, "0000000000000000")

    tester.converter_test_caller("2-32-1", HexToBit, 00, None, None)
    tester.converter_test_caller("2-32-2", HexToBit, "!!", None, None)
    tester.converter_test_caller("2-32-3", HexToBit, "aa", None, "0000000010101010")
    tester.converter_test_caller("2-32-4", HexToBit, "ｱｱ", None, None)
    tester.converter_test_caller("2-32-5", HexToBit, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-32-6", HexToBit, "100", None, "0000000100000000")
    tester.converter_test_caller("2-32-7", HexToBit, "100 200", None, "0000001000000000")
    tester.converter_test_caller("2-32-8", HexToBit, None, None, None)
    tester.converter_test_caller("2-32-9", HexToBit, "2069", None, "0010000001101001")
    tester.converter_test_caller("2-32-10", HexToBit, "-100", None, "1111111100000000")
    #tester.converter_test_caller("2-32-11", HexToBit, [0815,0F05,3022], None, None)
    tester.converter_test_caller("2-32-12", HexToBit, ["0815", "0F05","3022"], None, ['0000100000010101', '0000111100000101', '0011000000100010'])
    #tester.converter_test_caller("2-32-13", HexToBit, [FFFFFF9C, FFFFFF38, FFFFFED4], None, None)
    tester.converter_test_caller("2-32-14", HexToBit, ["FFFFFF9C", "FFFFFF38", "FFFFFED4"], None, ['1111111110011100', '1111111100111000', '1111111011010100'])
    tester.converter_test_caller("2-32-15", HexToBit, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-32-16", HexToBit, ["0815", "0F05", None], None, None)
    tester.converter_test_caller("2-32-17", HexToBit, f"{sys.maxsize}", None, "0101100000000111")
    tester.converter_test_caller("2-32-18", HexToBit, f"{sys.maxsize+1}", None, "0101100000001000")
    tester.converter_test_caller("2-32-19", HexToBit, [f"{sys.maxsize-1}", f"{sys.maxsize}"], None, ['0101100000000110', '0101100000000111'])
    tester.converter_test_caller("2-32-20", HexToBit, [f"{sys.maxsize}", f"{sys.maxsize+1}"], None, ["0101100000000111", "0101100000001000"])
    tester.converter_test_caller("2-32-21", HexToBit, f"{-sys.maxsize}", None, "0101100000000111")
    tester.converter_test_caller("2-32-22", HexToBit, f"{-sys.maxsize-1}", None, "0101100000001000")
    tester.converter_test_caller("2-32-23", HexToBit, [f"{-sys.maxsize+1}", f"{-sys.maxsize}"], None, ['0101100000000110', '0101100000000111'])
    tester.converter_test_caller("2-32-24", HexToBit, [f"{-sys.maxsize}", f"{-sys.maxsize-1}"], None, ["0101100000000111", "0101100000001000"])
    tester.converter_test_caller("2-32-25", HexToBit, "00", 00, "0000000000000000")
    tester.converter_test_caller("2-32-26", HexToBit, "00", "!!", "0000000000000000")
    tester.converter_test_caller("2-32-27", HexToBit, "00", [1, "aa"], "0000000000000000")
    tester.converter_test_caller("2-32-28", HexToBit, "00", None, "0000000000000000")

    tester.converter_test_caller("2-33-1", HexToBit, 00, None, None)
    tester.converter_test_caller("2-33-2", HexToBit, "!!", None, None)
    tester.converter_test_caller("2-33-3", HexToBit, "aa", None, "0000000010101010")
    tester.converter_test_caller("2-33-4", HexToBit, "ｱｱ", None, None)
    tester.converter_test_caller("2-33-5", HexToBit, "００！！ｂｂああ", None, None)
    tester.converter_test_caller("2-33-6", HexToBit, "1000", None, "0001000000000000")
    tester.converter_test_caller("2-33-7", HexToBit, "100 200", None, "0000001000000000")
    tester.converter_test_caller("2-33-8", HexToBit, None, None, None)
    tester.converter_test_caller("2-33-9", HexToBit, "01111111", None, "0001000100010001")
    tester.converter_test_caller("2-33-10", HexToBit, "11111111", None, "0001000100010001")
    #tester.converter_test_caller("2-33-11", HexToBit, [00001111,00011111,00111111], None, None)
    tester.converter_test_caller("2-33-12", HexToBit, ["00001111", "00011111", "00111111"], None, ['0001000100010001', '0001000100010001', '0001000100010001'])
    tester.converter_test_caller("2-33-13", HexToBit, [10001111,10011111,10111111], None, None)
    tester.converter_test_caller("2-33-14", HexToBit, ["10001111","10011111","10111111"], None, ['0001000100010001', '0001000100010001', '0001000100010001'])
    tester.converter_test_caller("2-33-15", HexToBit, ["AA", "DD", "GG"], None, None)
    tester.converter_test_caller("2-33-16", HexToBit, ["00001111","00011111", None], None, None)
    tester.converter_test_caller("2-33-17", HexToBit, f"{sys.maxsize}", None, "0101100000000111")
    tester.converter_test_caller("2-33-18", HexToBit, f"{sys.maxsize+1}", None, "0101100000001000")
    tester.converter_test_caller("2-33-19", HexToBit, [f"{sys.maxsize-1}", f"{sys.maxsize}"], None, ['0101100000000110', '0101100000000111'])
    tester.converter_test_caller("2-33-20", HexToBit, [f"{sys.maxsize}", f"{sys.maxsize+1}"], None, ["0101100000000111", "0101100000001000"])
    tester.converter_test_caller("2-33-21", HexToBit, f"{-sys.maxsize}", None, "0101100000000111")
    tester.converter_test_caller("2-33-22", HexToBit, f"{-sys.maxsize-1}", None, "0101100000001000")
    tester.converter_test_caller("2-33-23", HexToBit, [f"{-sys.maxsize+1}", f"{-sys.maxsize}"], None, ['0101100000000110', '0101100000000111'])
    tester.converter_test_caller("2-33-24", HexToBit, [f"{-sys.maxsize}", f"{-sys.maxsize-1}"], None, ['0101100000000111', '0101100000001000'])
    tester.converter_test_caller("2-33-25", HexToBit, "00", 00, "0000000000000000")
    tester.converter_test_caller("2-33-26", HexToBit, "00", "!!", "0000000000000000")
    tester.converter_test_caller("2-33-27", HexToBit, "00", [1, "aa"], "0000000000000000")
    tester.converter_test_caller("2-33-28", HexToBit, "00", None, "0000000000000000")

    tester.converter_test_caller("2-34-1", Format, 00, "{}", "0")
    tester.converter_test_caller("2-34-2", Format, "!!", "{}", "!!")
    tester.converter_test_caller("2-34-3", Format, "aa", "{}", "aa")
    tester.converter_test_caller("2-34-4", Format, "ｱｱ", "{}", "ｱｱ")
    tester.converter_test_caller("2-34-5", Format, "００！！ｂｂああ", "{}", "００！！ｂｂああ")
    tester.converter_test_caller("2-34-6", Format, "1000", "{}", "1000")
    tester.converter_test_caller("2-34-7", Format, "100 200", "{}", "100 200")
    tester.converter_test_caller("2-34-8", Format, None, "{}", "None")
    tester.converter_test_caller("2-34-9", Format, [1000, 2000, 3000], "{:04X}", "03E8")
    tester.converter_test_caller("2-34-10", Format, ["!!//", "??--", ">><<"],  "{}-{}", "!!//-??--")
    tester.converter_test_caller("2-34-11", Format, ["aaaa", "bbbb", "cccc"],  "{}-{}", "aaaa-bbbb")
    tester.converter_test_caller("2-34-12", Format, ["ｱｱｱｱ", "ｲｲｲｲ", "ｳｳｳｳ"],  "{}-{}", "ｱｱｱｱ-ｲｲｲｲ")
    tester.converter_test_caller("2-34-13", Format, ["００！！", "ｂｂああ", "KKEE"],  "{}-{}", "００！！-ｂｂああ")
    tester.converter_test_caller("2-34-14", Format, ["5384", "1295", "8752"],  "{}-{}", "5384-1295")
    tester.converter_test_caller("2-34-15", Format, [None, None, None],  "{}-{}", "None-None")
    tester.converter_test_caller("2-34-16", Format, [5384, 1295, 8752],  "{}-{}", "5384-1295")
    tester.converter_test_caller("2-34-17", Format, [1000, 2000, 3000], 00, None)
    tester.converter_test_caller("2-34-18", Format, [1000, 2000, 3000], "!!", "!!")
    tester.converter_test_caller("2-34-19", Format, [1000, 2000, 3000], "aa", "aa")
    tester.converter_test_caller("2-34-20", Format, [1000, 2000, 3000], "ｱｱ", "ｱｱ")
    tester.converter_test_caller("2-34-21", Format, [1000, 2000, 3000], "００！！ｂｂああ", "００！！ｂｂああ")
    tester.converter_test_caller("2-34-22", Format, [1000, 2000, 3000], "aa aa", "aa aa")
    tester.converter_test_caller("2-34-23", Format, [1000, 2000, 3000], None, None)
    tester.converter_test_caller("2-34-24", Format, [1000, 2000, 3000], "{}-{}", "1000-2000")
    tester.converter_test_caller("2-34-25", Format, [1000, 2000, 3000], "{:02X}", "3E8")
    tester.converter_test_caller("2-34-26", Format, [1000, 2000, 3000], "{:>10}", "      1000")
    tester.converter_test_caller("2-34-27", Format, [1000, 2000, 3000], "{-5}", None)
    tester.converter_test_caller("2-34-28", Format, [1000, 2000, 3000], "{/}", None)

    tester.converter_test_caller("old", standard_converter_tester_old, None, None, "All Test Finished Normally.")

    return "All Test Finished Normally."


def standard_converter_tester_old(input, option):
    """
    標準変換関数のテスト関数

    Args:
        input (any): 未使用
        option (any): 未使用

    Returns:
        str : 成功時："All Test Finished Normally."
        　　　失敗時は、失敗テストからの例外を発生。
    """
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

    tester.converter_test_caller("DateFormat-1 入力未設定", DateFormat, None, None, None)
    tester.converter_test_caller("DateFormat-2 オプション未設定", DateFormat, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("DateFormat-3 入力書式デフォルト不一致（msecなし）", DateFormat, "2021/08/05 15:34:48", None, None)
    tester.converter_test_caller("DateFormat-4 入力書式デフォルト不一致（ISO形式）", DateFormat, "2021/08/05T15:34:48.123Z", None, None)
    tester.converter_test_caller("DateFormat-5 非日付データ", DateFormat, "ABC", None, None)
    tester.converter_test_caller("DateFormat-6 出力書式に日付フォーマットなし", DateFormat, "2021/08/05 15:34:48.123", "ABC", "ABC")
    tester.converter_test_caller("DateFormat-7 出力書式連結型", DateFormat, "2021/08/05 15:34:48.123", "%Y%m%d%H%M%S%f", "20210805153448123000")
    tester.converter_test_caller("DateFormat-8 特殊な出力書式", DateFormat, "2021/08/05 15:34:48.123", "%Y-%m-%d %H#%M#%S#%f", "2021-08-05 15#34#48#123000")
    tester.converter_test_caller("DateFormat-9 デフォルト出力書式", DateFormat, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("DateFormat-10 オプション空配列", DateFormat, "2021/08/05 15:34:48.123", [], "210805153448")
    tester.converter_test_caller("DateFormat-11 オプション配列数=1", DateFormat, "2021/08/05 15:34:48.123", ["%Y%m%d%H%M%S%f"], "20210805153448123000")
    tester.converter_test_caller("DateFormat-12 入力書式空", DateFormat, "2021/08/05 15:34:48.123", ["%Y%m%d%H%M%S%f", ""], None)
    tester.converter_test_caller("DateFormat-13 入力書式不一致（msecなし）", DateFormat, "2021/08/05 15:34:48.123", ["%Y%m%d%H%M%S%f", "%Y/%m/%d %H:%M:%S"], None)
    tester.converter_test_caller("DateFormat-14 入力書式不一致（ISO形式）", DateFormat, "2021/08/05 15:34:48.123", ["%Y%m%d%H%M%S%f", "%Y/%m/%dT%H:%M:%SZ"], None)
    tester.converter_test_caller("DateFormat-15 入力書式指定（msecなし）", DateFormat, "2021/08/05 15:34:48", ["%Y%m%d%H%M%S%f", "%Y/%m/%d %H:%M:%S"], "20210805153448000000")
    tester.converter_test_caller("DateFormat-16 入力書式指定（ISO形式）", DateFormat, "2021/08/05T15:34:48.123Z", ["%Y%m%d%H%M%S%f", "%Y/%m/%dT%H:%M:%S.%fZ"], "20210805153448123000")

    tester.converter_test_caller("Date2DateF12-1", Date2DateF12, None, None, None)
    tester.converter_test_caller("Date2DateF12-2", Date2DateF12, "2021/08/05 15:34:48.123", None, "210805153448")
    tester.converter_test_caller("Date2DateF12-3", Date2DateF12, "2021/08/05 15:34:48", None, None)
    tester.converter_test_caller("Date2DateF12-4", Date2DateF12, "2021/08/05T15:34:48.123Z", None, None)
    tester.converter_test_caller("Date2DateF12-5", Date2DateF12, "ABC", None, None)

    tester.converter_test_caller("NativeTimeToISOTime-1 入力未設定", NativeTimeToISOTime, None, ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f"], None)
    tester.converter_test_caller("NativeTimeToISOTime-2 オプション未設定", NativeTimeToISOTime, "2023-01-23 04:56:07.890", None, None)
    tester.converter_test_caller("NativeTimeToISOTime-3 入力が非文字列", NativeTimeToISOTime, 0, ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f"], None)
    tester.converter_test_caller("NativeTimeToISOTime-4 オプション非配列", NativeTimeToISOTime, "2023-01-23 04:56:07.890", "Asia/Tokyo,%Y-%m-%d %H:%M:%S.%f%z", None)
    tester.converter_test_caller("NativeTimeToISOTime-5 オプション配列が空", NativeTimeToISOTime, "2023-01-23 04:56:07.890", [], None)
    tester.converter_test_caller("NativeTimeToISOTime-6 オプション数不足(1)", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo"], None)
    tester.converter_test_caller("NativeTimeToISOTime-7 オプション１：空文字", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["", "%Y-%m-%d %H:%M:%S.%f%z"], None)
    tester.converter_test_caller("NativeTimeToISOTime-8 オプション１：非TimeZone文字", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["東京", "%Y-%m-%d %H:%M:%S.%f%z"], None)
    tester.converter_test_caller("NativeTimeToISOTime-9 オプション２：非書式文字列", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["東京", "年-月-日 時:分:秒"], None)
    tester.converter_test_caller("NativeTimeToISOTime-10 オプション２：書式不一致(: -> /)", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y/%m/%d %H:%M:%S.%f"], None)
    tester.converter_test_caller("NativeTimeToISOTime-11 オプション２：書式不一致(%fなし)", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y/%m/%d %H:%M:%S"], None)
    tester.converter_test_caller("NativeTimeToISOTime-12 UTC -> JST", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T13:56:07.890000+0900")
    tester.converter_test_caller("NativeTimeToISOTime-13 JST -> UTC(オプション数2)", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f"], "2023-01-22T19:56:07.890000Z")
    tester.converter_test_caller("NativeTimeToISOTime-14 JST -> UTC(オプション数3)", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f", "UTC"], "2023-01-22T19:56:07.890000Z")
    tester.converter_test_caller("NativeTimeToISOTime-15 JST -> UTC(オプション数4)", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f", "UTC", "%Y/%m/%dT%H:%M:%S.%f%z"], "2023/01/22T19:56:07.890000Z")
    tester.converter_test_caller("NativeTimeToISOTime-16 UTC -> UTC", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["UTC", "%Y-%m-%d %H:%M:%S.%f", "UTC", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T04:56:07.890000Z")
    tester.converter_test_caller("NativeTimeToISOTime-17 JST -> JST", NativeTimeToISOTime, "2023-01-23 04:56:07.890", ["Asia/Tokyo", "%Y-%m-%d %H:%M:%S.%f", "Asia/Tokyo", "%Y-%m-%dT%H:%M:%S.%f%z"], "2023-01-23T04:56:07.890000+0900")

    tester.converter_test_caller("Operation-1 入力未設定", Operation, None, 0.1, None)
    tester.converter_test_caller("Operation-2 オプション未設定", Operation, 123, None, None)
    tester.converter_test_caller("Operation-3 入力が文字列", Operation, "ABC", 0.1, None)
    tester.converter_test_caller("Operation-4 オプションが文字列", Operation, 123, "ABC", None)
    tester.converter_test_caller("Operation-5 全て数値", Operation, 123, 0.1, "12.3")
    tester.converter_test_caller("Operation-6 全て数値の文字列", Operation, "123", "0.1", "12.3")

    tester.converter_test_caller("Division-1 入力未設定", Division, None, 0.1, None)
    tester.converter_test_caller("Division-2 オプション未設定", Division, 123, None, None)
    tester.converter_test_caller("Division-3 入力が文字列", Division, "ABC", 0.1, None)
    tester.converter_test_caller("Division-4 オプションが文字列", Division, 123, "ABC", None)
    tester.converter_test_caller("Division-5 全て数値", Division, 1.23, 0.1, "12.3")
    tester.converter_test_caller("Division-6 全て数値の文字列", Division, "1.23", "0.1", "12.3")

    tester.converter_test_caller("Max-1 入力未設定", Max, None, None, None)
    tester.converter_test_caller("Max-2 入力が非配列", Max, 123, None, None)
    tester.converter_test_caller("Max-3 入力が文字列", Max, "ABC", None, "C")
    tester.converter_test_caller("Max-4 入力が整数リスト", Max, [1,2,3,4,5], None, "5")
    tester.converter_test_caller("Max-5 入力が実数リスト", Max, [1.4142,2.236,3.141592], None, "3.141592")
    tester.converter_test_caller("Max-6 入力が整数・実数混在リスト", Max, [1,2.236,3.141592,2,3], None, "3.141592")
    tester.converter_test_caller("Max-7 入力が整数・実数混在文字列リスト", Max, ["1","2.236","3.141592","2","3"], None, "3.141592")
    tester.converter_test_caller("Max-8 入力が文字列リスト", Max, ["ABC","DEF","ABC","EFG","BCD"], None, "EFG")
    tester.converter_test_caller("Max-9 入力が整数・文字列混在", Max, ["ABC","DEF","ABC",123,"BCD"], None, None)

    tester.converter_test_caller("Min-1 入力未設定", Min, None, None, None)
    tester.converter_test_caller("Min-2 入力が非配列", Min, 123, None, None)
    tester.converter_test_caller("Min-3 入力が文字列", Min, "ABC", None, "A")
    tester.converter_test_caller("Min-4 入力が整数リスト", Min, [1,2,3,4,5], None, "1")
    tester.converter_test_caller("Min-5 入力が実数リスト", Min, [1.4142,2.236,3.141592], None, "1.4142")
    tester.converter_test_caller("Min-6 入力が整数・実数混在リスト", Min, [2.236,1.4142,3.141592,2,3], None, "1.4142")
    tester.converter_test_caller("Min-7 入力が整数・実数混在文字列リスト", Min, ["2.236","3.141592","2","3"], None, "2")
    tester.converter_test_caller("Min-8 入力が文字列リスト", Min, ["ABC","DEF","ABC","EFG","BCD"], None, "ABC")
    tester.converter_test_caller("Min-9 入力が整数・文字列混在", Min, ["ABC","DEF","ABC",123,"BCD"], None, None)

    tester.converter_test_caller("Swap-1 未設定", Swap, None, None, None)
    tester.converter_test_caller("Swap-2 16進以外(実数)", Swap, "12.345", None, "45.3")
    tester.converter_test_caller("Swap-2 16進以外(実数＋下４桁は１６進)", Swap, "12.3456", None, "5634")
    tester.converter_test_caller("Swap-3 16進以外(数値)＋非文字列", Swap, 1025, None, None)
    tester.converter_test_caller("Swap-7 FFFFF（桁数オーバー：５桁）", Swap, "ABCDEF", None, "EFCD")
    tester.converter_test_caller("Swap-8 123(桁数不足：３桁)", Swap, "123", None, "2301")
    tester.converter_test_caller("Swap-9 5(桁数不足：１桁)", Swap, "5", None, "0500")
    tester.converter_test_caller("Swap-10 配列不正値あり１", Swap, [None,"abcd"], None, None)
    tester.converter_test_caller("Swap-11 配列不正値あり２", Swap, ["cdef",None], None, None)
    tester.converter_test_caller("Swap-12 配列正常値のみ", Swap, ['ffff', 'cfc7', '3039', '7fff', '8000'], None, ['ffff', 'c7cf', '3930', 'ff7f', '0080'])
    
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

    tester.converter_test_caller("2-1-11-1", two_word_to_hour, [None,12345], None, None)
    tester.converter_test_caller("2-1-11-2", two_word_to_hour, [54,None], None, None)
    tester.converter_test_caller("2-1-11-3", two_word_to_hour, ["ABC",12345], None, None)
    tester.converter_test_caller("2-1-11-4", two_word_to_hour, [54,"ABC"], None, None)
    tester.converter_test_caller("2-1-11-5", two_word_to_hour, [54,12345], None, 0.9864691666666666)
    tester.converter_test_caller("2-1-11-6", two_word_to_hour, ["54","12345"], None, 0.9864691666666666)
    tester.converter_test_caller("2-1-11-7", two_word_to_hour, [108,24690], None, 1.9729383333333332)
    tester.converter_test_caller("2-1-11-8", two_word_to_hour, 540, None, None)

    tester.converter_test_caller("join-1 nullと文字列", join, [None,"DEF"], None, None)
    tester.converter_test_caller("join-2 文字列とnull", join, ["ABC",None], None, None)
    tester.converter_test_caller("join-3 文字列ｘ文字列", join, ["ABC","DEF"], None, "ABCDEF")
    tester.converter_test_caller("join-4 '-'結合子", join, [123,456], "-", "123-456")
    tester.converter_test_caller("join-5 入力非配列", join, "ABC", "#", None)
    tester.converter_test_caller("join-6 ':'結合子", join, [12,34,56], ":", "12:34:56")

    tester.converter_test_caller("Join-1 nullと文字列", Join, [None,"DEF"], None, None)
    tester.converter_test_caller("Join-2 文字列とnull", Join, ["ABC",None], None, None)
    tester.converter_test_caller("Join-3 文字列ｘ文字列", Join, ["ABC","DEF"], None, "ABCDEF")
    tester.converter_test_caller("Join-4 '-'結合子", Join, [123,456], "-", "123-456")
    tester.converter_test_caller("Join-5 入力非配列", Join, "ABC", "#", None)
    tester.converter_test_caller("Join-6 ':'結合子", Join, [12,34,56], ":", "12:34:56")

    tester.converter_test_caller("substring-1 入力未指定", substring, None, None, None)
    tester.converter_test_caller("substring-2 オプション未指定", substring, "1234567890", None, "1234567890")
    tester.converter_test_caller("substring-3 オプション１のみ指定", substring, "1234567890", 2, "234567890")
    tester.converter_test_caller("substring-4 オプション１が空文字", substring, "1234567890", "", None)
    tester.converter_test_caller("substring-5 オプション１が文字列", substring, "1234567890", "ABC", None)
    tester.converter_test_caller("substring-6 オプション２がnull", substring, "1234567890", [2,None], "234567890")
    tester.converter_test_caller("substring-7 オプション２が文字列", substring, "1234567890", [2,"ABC"], None)
    tester.converter_test_caller("substring-8 オプション２が数値文字列", substring, "1234567890", ["2","3"], "234")
    tester.converter_test_caller("substring-9 オプション１，２指定", substring, 1234567890, [2,3], "234")
    tester.converter_test_caller("substring-10 オプション１下限インデックス外", substring, "1234567890", [0,3], "")
    tester.converter_test_caller("substring-11 オプション１上限インデックス外", substring, "1234567890", [11,3], "")
    tester.converter_test_caller("substring-12 オプション２末尾超過", substring, "1234567890", [9,3], "90")
    tester.converter_test_caller("substring-13 オプション２＝０", substring, "1234567890", [1,0], "")
    tester.converter_test_caller("substring-14 全範囲指定", substring, "1234567890", [1,10], "1234567890")
    tester.converter_test_caller("substring-15 全範囲指定+1", substring, "1234567890", [1,11], "1234567890")
    tester.converter_test_caller("substring-16 開始位置マイナス", substring, "1234567890", [-1,2], "0")
    tester.converter_test_caller("substring-17 文字数マイナス", substring, "1234567890", [1,-8], "12")
    tester.converter_test_caller("substring-18 開始位置・文字数マイナス", substring, "1234567890", [-3,-8], "89")
    tester.converter_test_caller("substring-19 マイナス開始位置境界", substring, "1234567890", [-10,2], "12")
    tester.converter_test_caller("substring-20 マイナス文字数境界", substring, "1234567890", [1,-9], "1")
    tester.converter_test_caller("substring-21 マイナス開始位置オーバー", substring, "1234567890", [-11,2], "")
    tester.converter_test_caller("substring-22 マイナス文字数オーバー", substring, "1234567890", [1,-10], "")

    tester.converter_test_caller("SubString-1 入力未指定", SubString, None, None, None)
    tester.converter_test_caller("SubString-2 オプション未指定", SubString, "1234567890", None, "1234567890")
    tester.converter_test_caller("SubString-3 オプション１のみ指定", SubString, "1234567890", 2, "234567890")
    tester.converter_test_caller("SubString-4 オプション１が空文字", SubString, "1234567890", "", None)
    tester.converter_test_caller("SubString-5 オプション１が文字列", SubString, "1234567890", "ABC", None)
    tester.converter_test_caller("SubString-6 オプション２がnull", SubString, "1234567890", [2,None], "234567890")
    tester.converter_test_caller("SubString-7 オプション２が文字列", SubString, "1234567890", [2,"ABC"], None)
    tester.converter_test_caller("SubString-8 オプション２が数値文字列", SubString, "1234567890", ["2","3"], "234")
    tester.converter_test_caller("SubString-9 オプション１，２指定", SubString, 1234567890, [2,3], "234")
    tester.converter_test_caller("SubString-10 オプション１下限インデックス外", SubString, "1234567890", [0,3], "")
    tester.converter_test_caller("SubString-11 オプション１上限インデックス外", SubString, "1234567890", [11,3], "")
    tester.converter_test_caller("SubString-12 オプション２末尾超過", SubString, "1234567890", [9,3], "90")
    tester.converter_test_caller("SubString-13 オプション２＝０", SubString, "1234567890", [1,0], "")
    tester.converter_test_caller("SubString-14 全範囲指定", SubString, "1234567890", [1,10], "1234567890")
    tester.converter_test_caller("SubString-15 全範囲指定+1", SubString, "1234567890", [1,11], "1234567890")
    tester.converter_test_caller("SubString-16 開始位置マイナス", SubString, "1234567890", [-1,2], "0")
    tester.converter_test_caller("SubString-17 文字数マイナス", SubString, "1234567890", [1,-8], "12")
    tester.converter_test_caller("SubString-18 開始位置・文字数マイナス", SubString, "1234567890", [-3,-8], "89")
    tester.converter_test_caller("SubString-19 マイナス開始位置境界", SubString, "1234567890", [-10,2], "12")
    tester.converter_test_caller("SubString-20 マイナス文字数境界", SubString, "1234567890", [1,-9], "1")
    tester.converter_test_caller("SubString-21 マイナス開始位置オーバー", SubString, "1234567890", [-11,2], "")
    tester.converter_test_caller("SubString-22 マイナス文字数オーバー", SubString, "1234567890", [1,-10], "")

    tester.converter_test_caller("split-1 入力未指定", split, None, [",",1], None)
    tester.converter_test_caller("split-2 セパレータ未指定", split, "ABC,DEF,GHI", [None,1], None)
    tester.converter_test_caller("split-3 抽出位置null", split, "ABC,DEF,GHI", [",",None], "ABC")
    tester.converter_test_caller("split-4 抽出位置文字列", split, "ABC,DEF,GHI", [",","ABC"], None)
    tester.converter_test_caller("split-5 抽出位置0(下限オーバー)", split, "ABC,DEF,GHI", [",",0], None)
    tester.converter_test_caller("split-6 抽出位置1", split, "ABC,DEF,GHI", [",",1], "ABC")
    tester.converter_test_caller("split-7 抽出位置2", split, "ABC,DEF,GHI", [",",2], "DEF")
    tester.converter_test_caller("split-8 抽出位置3", split, "ABC,DEF,GHI", [",",3], "GHI")
    tester.converter_test_caller("split-9 抽出位置4(上限オーバー)", split, "ABC,DEF,GHI", [",",4], None)
    tester.converter_test_caller("split-10 セパレータ不一致", split, "ABC,DEF,GHI", ["#",1], "ABC,DEF,GHI")
    tester.converter_test_caller("split-11 セパレータ文字列", split, "ABCD,DEF,FGHI", ["DEF",2], ",FGHI")
    tester.converter_test_caller("split-12 オプション１のみ指定(非配列)", split, "ABC,DEF,GHI", ",", "ABC")
    tester.converter_test_caller("split-13 オプション未指定", split, "ABC,DEF,GHI", None, None)
    tester.converter_test_caller("split-14 入力が数値", split, 123453673, [3,2], "45")

    tester.converter_test_caller("Split-1 入力未指定", Split, None, [",",1], None)
    tester.converter_test_caller("Split-2 セパレータ未指定", Split, "ABC,DEF,GHI", [None,1], None)
    tester.converter_test_caller("Split-3 抽出位置null", Split, "ABC,DEF,GHI", [",",None], "ABC")
    tester.converter_test_caller("Split-4 抽出位置文字列", Split, "ABC,DEF,GHI", [",","ABC"], None)
    tester.converter_test_caller("Split-5 抽出位置0(下限オーバー)", Split, "ABC,DEF,GHI", [",",0], None)
    tester.converter_test_caller("Split-6 抽出位置1", Split, "ABC,DEF,GHI", [",",1], "ABC")
    tester.converter_test_caller("Split-7 抽出位置2", Split, "ABC,DEF,GHI", [",",2], "DEF")
    tester.converter_test_caller("Split-8 抽出位置3", Split, "ABC,DEF,GHI", [",",3], "GHI")
    tester.converter_test_caller("Split-9 抽出位置4(上限オーバー)", Split, "ABC,DEF,GHI", [",",4], None)
    tester.converter_test_caller("Split-10 セパレータ不一致", Split, "ABC,DEF,GHI", ["#",1], "ABC,DEF,GHI")
    tester.converter_test_caller("Split-11 セパレータ文字列", Split, "ABCD,DEF,FGHI", ["DEF",2], ",FGHI")
    tester.converter_test_caller("Split-12 オプション１のみ指定(非配列)", Split, "ABC,DEF,GHI", ",", "ABC")
    tester.converter_test_caller("Split-13 オプション未指定", Split, "ABC,DEF,GHI", None, None)
    tester.converter_test_caller("Split-14 入力が数値", Split, 123453673, [3,2], "45")

    tester.converter_test_caller("trim-1 入力配列にnullあり１", trim, [None," 1 2 3 4 5 "], None, None)
    tester.converter_test_caller("trim-2 入力配列にnullあり２", trim, [" A B C D ",None], None, None)
    tester.converter_test_caller("trim-3 入力が数値", trim, 123, None, None)
    tester.converter_test_caller("trim-4 先頭空白", trim, " ABCD", None, "ABCD")
    tester.converter_test_caller("trim-5 中間空白", trim, "AB CD", None, "ABCD")
    tester.converter_test_caller("trim-6 末尾空白", trim, "ABCD ", None, "ABCD")
    tester.converter_test_caller("trim-7 入力配列", trim, ["  A  B  C  D  ","  1  2  3  4  5  "], None, ["ABCD","12345"])

    tester.converter_test_caller("Trim-1 入力配列にnullあり１", Trim, [None," 1 2 3 4 5 "], None, None)
    tester.converter_test_caller("Trim-2 入力配列にnullあり２", Trim, [" A B C D ",None], None, None)
    tester.converter_test_caller("Trim-3 入力が数値", Trim, 123, None, None)
    tester.converter_test_caller("Trim-4 先頭空白", Trim, " ABCD", None, "ABCD")
    tester.converter_test_caller("Trim-5 中間空白", Trim, "AB CD", None, "ABCD")
    tester.converter_test_caller("Trim-6 末尾空白", Trim, "ABCD ", None, "ABCD")
    tester.converter_test_caller("Trim-7 入力配列", Trim, ["  A  B  C  D  ","  1  2  3  4  5  "], None, ["ABCD","12345"])

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

    tester.converter_test_caller("dec_to_hex-1 未設定", dec_to_hex, None, None, None)
    tester.converter_test_caller("dec_to_hex-2 10進以外", dec_to_hex, "AB", None, None)
    tester.converter_test_caller("dec_to_hex-3 正値上限(32767)＋非文字列", dec_to_hex, 32767, None, "7fff")
    tester.converter_test_caller("dec_to_hex-4 負値下限(-32768)", dec_to_hex, "-32768", None, "8000")
    tester.converter_test_caller("dec_to_hex-5 符号なし上限(65535)", dec_to_hex, 65535, None, "ffff")
    tester.converter_test_caller("dec_to_hex-6 配列不正値あり１", dec_to_hex, [None,-32768], None, None)
    tester.converter_test_caller("dec_to_hex-7 配列不正値あり２", dec_to_hex, [-32768,None], None, None)
    tester.converter_test_caller("dec_to_hex-8 配列正常値のみ", dec_to_hex, [-1,-12345,12345,32767,-32768], None, ['ffff', 'cfc7', '3039', '7fff', '8000'])

    tester.converter_test_caller("DecToHex-1 未設定", DecToHex, None, None, None)
    tester.converter_test_caller("DecToHex-2 10進以外", DecToHex, "AB", None, None)
    tester.converter_test_caller("DecToHex-3 正値上限(32767)＋非文字列", DecToHex, 32767, None, "7fff")
    tester.converter_test_caller("DecToHex-4 負値下限(-32768)", DecToHex, "-32768", None, "8000")
    tester.converter_test_caller("DecToHex-5 符号なし上限(65535)", DecToHex, 65535, None, "ffff")
    tester.converter_test_caller("DecToHex-6 配列不正値あり１", DecToHex, [None,-32768], None, None)
    tester.converter_test_caller("DecToHex-7 配列不正値あり２", DecToHex, [-32768,None], None, None)
    tester.converter_test_caller("DecToHex-8 配列正常値のみ", DecToHex, [-1,-12345,12345,32767,-32768], None, ['ffff', 'cfc7', '3039', '7fff', '8000'])

    tester.converter_test_caller("HexToDec-1 未設定", HexToDec, None, None, None)
    tester.converter_test_caller("HexToDec-2 16進以外(実数)", HexToDec, "12.345", None, None)
    tester.converter_test_caller("HexToDec-3 16進以外(数値)＋非文字列", HexToDec, 1025, None, None)
    tester.converter_test_caller("HexToDec-4 正値上限(7FFF)", HexToDec, "7FFF", None, 32767)
    tester.converter_test_caller("HexToDec-5 負値下限(8000)", HexToDec, "8000", None, -32768)
    tester.converter_test_caller("HexToDec-6 FFFF", HexToDec, "FFFF", None, -1)
    tester.converter_test_caller("HexToDec-7 FFFFF（桁数オーバー：５桁）", HexToDec, "FFFFF", None, -1)
    tester.converter_test_caller("HexToDec-8 123(桁数不足：３桁)", HexToDec, "123", None, 291)
    tester.converter_test_caller("HexToDec-9 5(桁数不足：１桁)", HexToDec, "5", None, 5)
    tester.converter_test_caller("HexToDec-10 配列不正値あり１", HexToDec, [None,"abcd"], None, None)
    tester.converter_test_caller("HexToDec-11 配列不正値あり２", HexToDec, ["cdef",None], None, None)
    tester.converter_test_caller("HexToDec-12 配列正常値のみ", HexToDec, ['ffff', 'cfc7', '3039', '7fff', '8000'], None, [-1,-12345,12345,32767,-32768])
    
    tester.converter_test_caller("bit_to_dec-1 未指定", bit_to_dec, None, None, None)
    tester.converter_test_caller("bit_to_dec-2 数値外", bit_to_dec, "ABC", None, None)
    tester.converter_test_caller("bit_to_dec-3 2進以外", bit_to_dec, "12345678", None, None)
    tester.converter_test_caller("bit_to_dec-4 10000000(負値下限)", bit_to_dec, "10000000", None, -128)
    tester.converter_test_caller("bit_to_dec-5 11111111(-1)", bit_to_dec, "11111111", None, -1)
    tester.converter_test_caller("bit_to_dec-6 01111111(127)", bit_to_dec, "01111111", None, 127)
    tester.converter_test_caller("bit_to_dec-7 1111(15)", bit_to_dec, "1111", None, 15)
    tester.converter_test_caller("bit_to_dec-8 100(非文字列：数値)", bit_to_dec, 100, None, None)
    tester.converter_test_caller("bit_to_dec-9 111111111(桁数オーバー：９桁)", bit_to_dec, "111111111", None, -1)

    tester.converter_test_caller("BitToDec-1 未指定", BitToDec, None, None, None)
    tester.converter_test_caller("BitToDec-2 数値外", BitToDec, "ABC", None, None)
    tester.converter_test_caller("BitToDec-3 2進以外", BitToDec, "12345678", None, None)
    tester.converter_test_caller("BitToDec-4 10000000(負値下限)", BitToDec, "10000000", None, -128)
    tester.converter_test_caller("BitToDec-5 11111111(-1)", BitToDec, "11111111", None, -1)
    tester.converter_test_caller("BitToDec-6 01111111(127)", BitToDec, "01111111", None, 127)
    tester.converter_test_caller("BitToDec-7 1111(15)", BitToDec, "1111", None, 15)
    tester.converter_test_caller("BitToDec-8 100(非文字列：数値)", BitToDec, 100, None, None)
    tester.converter_test_caller("BitToDec-9 111111111(桁数オーバー：９桁)", BitToDec, "111111111", None, -1)
    tester.converter_test_caller("BitToDec-10 配列不正値あり１", BitToDec, [None,"0101"], None, None)
    tester.converter_test_caller("BitToDec-11 配列不正値あり２", BitToDec, ["1010",None], None, None)
    tester.converter_test_caller("BitToDec-12 配列正常値のみ", BitToDec, ["11111111", "11001111", "00111001", "01111111", "10000000"], None, [-1,-49,57,127,-128])


    tester.converter_test_caller("DecToBit-1 未指定", DecToBit, None, None, None)
    tester.converter_test_caller("DecToBit-2 数値外", DecToBit, "ABC", None, None)
    tester.converter_test_caller("DecToBit-3 10進以外(実数)", DecToBit, "12.345", None, None)
    tester.converter_test_caller("DecToBit-4 -32768(負値下限)", DecToBit, "-32768", None, "1000000000000000")
    tester.converter_test_caller("DecToBit-5 -1", DecToBit, "-1", None, "1111111111111111")
    tester.converter_test_caller("DecToBit-6 32767(正値上限)", DecToBit, "32767", None, "0111111111111111")
    tester.converter_test_caller("DecToBit-7 65(正常値)", DecToBit, "65", None, "0000000001000001")
    tester.converter_test_caller("DecToBit-8 65(非文字列：数値)", DecToBit, 65, None, "0000000001000001")
    tester.converter_test_caller("DecToBit-9 32768(正値上限オーバー)", DecToBit, "32768", None, "1000000000000000")
    tester.converter_test_caller("DecToBit-10 65535(符号なし上限)", DecToBit, "65535", None, "1111111111111111")
    tester.converter_test_caller("DecToBit-11 65536(符号なし上限オーバー)", DecToBit, "65536", None, "10000000000000000")

    tester.converter_test_caller("HexToBit-1 未設定", HexToBit, None, None, None)
    tester.converter_test_caller("HexToBit-2 16進以外(実数)", HexToBit, "12.345", None, None)
    tester.converter_test_caller("HexToBit-3 16進以外(数値)＋非文字列", HexToBit, 1025, None, None)
    tester.converter_test_caller("HexToBit-4 正値上限(7FFF)", HexToBit, "7FFF", None, "0111111111111111")
    tester.converter_test_caller("HexToBit-5 負値下限(8000)", HexToBit, "8000", None, "1000000000000000")
    tester.converter_test_caller("HexToBit-6 FFFF", HexToBit, "FFFF", None, "1111111111111111")
    tester.converter_test_caller("HexToBit-7 FFFFF（桁数オーバー：５桁）", HexToBit, "FFFFF", None, "1111111111111111")
    tester.converter_test_caller("HexToBit-8 123(桁数不足：３桁)", HexToBit, "123", None, "0000000100100011")
    tester.converter_test_caller("HexToBit-9 5(桁数不足：１桁)", HexToBit, "5", None, "0000000000000101")
    tester.converter_test_caller("HexToBit-10 配列不正値あり１", HexToBit, [None,"abcd"], None, None)
    tester.converter_test_caller("HexToBit-11 配列不正値あり２", HexToBit, ["cdef",None], None, None)
    tester.converter_test_caller("HexToBit-12 配列正常値のみ", HexToBit, ['ffff', 'cfc7', '3039', '7fff', '8000'], None, ["1111111111111111","1100111111000111","0011000000111001","0111111111111111","1000000000000000"])

    tester.converter_test_caller("BitToHex-1 未指定", BitToHex, None, None, None)
    tester.converter_test_caller("BitToHex-2 数値外", BitToHex, "ABC", None, None)
    tester.converter_test_caller("BitToHex-3 2進以外", BitToHex, "12345678", None, None)
    tester.converter_test_caller("BitToHex-4 10000000(負値下限)", BitToHex, "10000000", None, "80")
    tester.converter_test_caller("BitToHex-5 11111111(FF)", BitToHex, "11111111", None, "ff")
    tester.converter_test_caller("BitToHex-6 01111111(7F)", BitToHex, "01111111", None, "7f")
    tester.converter_test_caller("BitToHex-7 1111(0F)", BitToHex, "1111", None, "0f")
    tester.converter_test_caller("BitToHex-8 100(非文字列：数値)", BitToHex, 100, None, None)
    tester.converter_test_caller("BitToHex-9 111111111(桁数オーバー：９桁)", BitToHex, "111111111", None, "ff")
    tester.converter_test_caller("BitToHex-10 配列不正値あり１", BitToHex, [None,"0101"], None, None)
    tester.converter_test_caller("BitToHex-11 配列不正値あり２", BitToHex, ["1010",None], None, None)
    tester.converter_test_caller("BitToHex-12 配列正常値のみ", BitToHex, ["11111111", "11001111", "00111001", "01111111", "10000000"], None, ["ff","cf",'39','7f','80'])

    tester.converter_test_caller("Format-1 入力未指定", Format, None, "{}", "None")
    tester.converter_test_caller("Format-2 入力非配列", Format, "1", "{}", "1")
    tester.converter_test_caller("Format-3 オプション未指定", Format, ["1"], None, None)
    tester.converter_test_caller("Format-4 入力データ不足", Format, ["1"], "{}-{}", None)
    tester.converter_test_caller("Format-5 入力データ超過", Format, ["1","2","3"], "{}-{}", "1-2")
    tester.converter_test_caller("Format-6 書式不一致(文字→数値書式)", Format, ["AB"], "{:02d}", None)
    tester.converter_test_caller("Format-7 書式不一致(数文字→数値書式)", Format, ["10"], "{:03d}", None)
    tester.converter_test_caller("Format-8 書式不一致(整数→実数書式)", Format, [10], "{:6.2f}", " 10.00")
    tester.converter_test_caller("Format-9 書式不一致(実数→整数書式 切り捨て)", Format, [12.345], "{:03d}", None)
    tester.converter_test_caller("Format-10 書式不一致(実数→整数書式 切り上げ)", Format, [34.567], "{:03d}", None)
    tester.converter_test_caller("Format-11 書式一致+配列", Format, ["AB",10,12.345], "{:4s}/{:03d}/{:6.2f}", "AB  /010/ 12.35")

    return "All Test Finished Normally."