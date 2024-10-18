import ast
import datetime
import glob
import json
import os
import runpy
import sys
import types

# 出力内容の名称
OUTPUT_NAME_DATA = "data"
OUTPUT_NAME_ERROR = "error"
OUTPUT_NAME_PROPERTIES = "properties"
OUTPUT_NAME_TRACE = "trace"

#
def OutputStdout(section, value):
    output = {}
    output[section] = value
    print(json.dumps(output,ensure_ascii=True), file=sys.stdout)

#
def OutputStderr(section, value):
    output = {}
    output[section] = value
    print(json.dumps(output,ensure_ascii=True), file=sys.stderr)

#
def LoadAddin(addinFile):
    """
    Addin用pythonコードを読み込む

    Args:
        addinFile : 読み込み対象pythonファイル名

    Returns:
        Addin関数辞書（Key: 関数名、Value: 関数ポインタ）
    """
    retAddinDict = {}

    try:
        addin = runpy.run_path(addinFile)

        for key,value in addin.items():
            if isinstance(value, types.FunctionType):
                retAddinDict[key] = value
    except Exception as e:
        raise Exception('Add in (' + addinFile + ') load error!', e)

    return retAddinDict

#
def LoadAddins(addinFolder):
    """
    Addin用フォルダからpythonコードを読み込む

    Args:
        addinFolder : Addin検索対象フォルダ

    Returns:
        Addin関数辞書（Key: 関数名、Value: 関数ポインタ）
    """
    retAddinDict = {}
    try:
        sys.path.append(addinFolder)
        pyFiles = glob.glob(addinFolder + '/*.py')
        for pyfile in pyFiles:
            addinDict = LoadAddin(pyfile)
            retAddinDict.update(addinDict)
    except Exception as e:
        raise Exception(e)

    return retAddinDict

#
def GetConvertFunc(dictFuncs, funcName):
    """
    変換関数辞書から指定変換関数を取り出す

    Args:
        dictFuncs : 変換関数辞書（Key: 関数名、Value: 関数ポインタ）
        funcName : 変換関数名

    Returns:
        関数ポインタ(default:None)
    """
    retFunc = None
    try:
        retFunc = dictFuncs[funcName]
    except Exception as e:
        retFunc = None

    return retFunc

#
def GetInputData(inputLine, properyName):
    retInputData = None
    try:
        if properyName in inputLine:
            # 入力フォーマット情報
            if (traceFlag):
                traceData.push(f'input {properyName}.', json.dumps(inputLine[properyName],ensure_ascii=True))

            retInputData = inputLine[properyName]

    except Exception as e:
        OutputStderr(OUTPUT_NAME_ERROR, f'Input data read error ({properyName}): ' + json.dumps(inputLine[properyName],ensure_ascii=True))
        OutputStderr(OUTPUT_NAME_ERROR, str(e))

    return retInputData

#
def Props2Dict(properties):
    """
    プロパティオブジェクトを辞書化

    Args:
        properties : プロパティオブジェクト

    Returns:
        プロパティ辞書
    """
    retPropDict = {}
    for prop in properties['propertyList']:
        retPropDict[prop['key']] = prop['value']

    return retPropDict

#
def Dict2Props(propDict):
    """
    辞書形式プロパティをプロパティオブジェクト化

    Args:
        propDict : プロパティ辞書

    Returns:
        プロパティオブジェクト
    """
    propList = []
    for key, value in propDict.items():
        propList.append( {'key':key, 'value':value} )

    retProps = {'propertyList': propList }

    return retProps

#
def ChangeType(data):
    """
    データ形式を変換
        ・配列サイズ１データは、単独データに変換
        ・配列サイズ0データは、Noneに変換
        ・その他は無変換
    Args:
        data : 変換対象データ

    Returns:
        変換後データ
    """
    if isinstance(data, list) and len(data)==1:
        # 配列サイズ１データは、単独データに変換
        retdata = data[0]
    elif isinstance(data, list) and len(data)==0:
        # 配列サイズ0データは、Noneに変換
        retdata = None
    else:
        retdata = data

    return retdata

#
def CheckOutputInfo(iOutputInfo):
    retIsCorrectFormat = True

    if not isinstance(iOutputInfo, dict):
        retIsCorrectFormat = False

    elif not 'OutputData' in iOutputInfo:
        retIsCorrectFormat = False

    elif not isinstance(iOutputInfo['OutputData'], list):
        retIsCorrectFormat = False

    return retIsCorrectFormat

#
# メイン関数
#
def main(inputRecord, properties):
    """
    メイン関数

    Args:
        inputRecord : 入力レコード
        properties : プロパティ辞書

    Returns:
        変換後レコード
        変換ステータス(True:成功, False:失敗)
    """
    # 出力データ領域の作成
    outputSize = 0
    for outInfo in outputInfos['OutputData']:
        ithOutputIndex = outInfo['OutputIndex']
        if isinstance((ithOutputIndex),int) and (outputSize < ithOutputIndex):
            outputSize = ithOutputIndex

    convStatus = True
    outputRecord = []
    if 0 < outputSize:
        outputRecord = [None] * outputSize

    try:
        for outInfo in outputInfos['OutputData']:
            indices = []
            data = []
            for idx in outInfo['InputIndex']:
                indices.append(idx)
                data.append(inputRecord[int(idx)-1])

            if (traceFlag):
                traceData.push()
                traceData.addLabel( "index" )
                traceData.add( indices )
                traceData.addConvname("InputIndexToData")
                traceData.addLabel( "data" )
                traceData.add( data )


            for conv in outInfo['Converters']:
                if conv['Enabled'] != True:
                    continue

                convFunc = GetConvertFunc(dictConvFuncs, conv['Converter'])
                if convFunc == None:
                    raise Exception('function (' + conv['Converter'] + ') not found.')

                try:
                    data = ChangeType(data)
                    options = ChangeType(conv['Options'])

                    if (traceFlag):
                        traceData.addConvname(conv['Converter'], conv['Options'])

                    data = convFunc(data, options)
                    traceData.add( data )
                except Exception as e:
                    convStatus = False
                    functionName = "Unset"
                    if 'Converter' in conv:
                        functionName = conv['Converter']

                    options = "Unset"
                    if 'Options' in conv:
                        options = conv['Options']

                    data = {"Error":"Converror", "Function":functionName, "Input":data, "Options":options, "Type":str(type(e)), "Detail":str(e)}
                    if (traceFlag):
                        traceData.addLabel("Failed")
                        traceData.add(json.dumps(data, ensure_ascii=True))
                    break

            # 出力データを整形
            setdata = ChangeType(data)

            outidx = outInfo['OutputIndex']
            if outidx == "Property":
                outname = outInfo['OutputName']
                if "" == outname:
                    raise Exception('Error : Empty outputname')

                # プロパティを更新
                properties[outname] = setdata
                if (traceFlag):
                    traceData.addConvname("DataToProperty")
                    traceData.add(outname + "=" + str(setdata))

            elif outidx == "PropertyAddOnly":
                outname = outInfo['OutputName']
                if "" == outname:
                    raise Exception('Error : Empty outputname')

                # プロパティが存在しない場合のみ追加
                if outname not in properties:
                    properties[outname] = setdata
                    if (traceFlag):
                        traceData.addConvname("DataToProperty")
                        traceData.add(outname + "=" + str(setdata))

            elif isinstance(outidx, int):
                if 1 <= outidx and outidx <= len(outputRecord):
                    outidx -= 1
                    # 出力レコードにセット
                    outputRecord[outidx] = setdata
                    if (traceFlag):
                        traceData.addConvname("DataToOutputIndex")
                        traceData.addLabel("[" + str(outidx) + "]")
                        traceData.add(setdata)
                else:
                    raise Exception('Out of index : OutputIndex', outidx)
            else:
                raise Exception('Type error : OutputIndex', outidx)

    except Exception as e:
        raise Exception('Convert error :', e)

    return outputRecord, convStatus


#
# 初期処理
#

# 入力引数の取り出し
try:
    addinFolders = sys.argv[1]
    traceFlag = False
    if sys.argv[2].lower() == "true":
        traceFlag = True
    dataType = sys.argv[3]
    convErr = sys.argv[4]

except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in input parameters. arg length = " + str(len(sys.argv)) + " ,args = " + sys.argv)
    OutputStderr(OUTPUT_NAME_ERROR, str(e))
    sys.exit(1)

# 参照ライブラリの追加
try:
    libpath = os.path.dirname(__file__)
    sys.path.append(libpath)
    import lib.Tracer as Tracer
    traceData = Tracer.Tracer(traceFlag)
except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in importing libraries.")
    OutputStderr(OUTPUT_NAME_ERROR, str(e))
    sys.exit(1)


# Addinの取込
try:
    dictConvFuncs = {}
    addinFolderList = addinFolders.split(';')
    for addinFol in addinFolderList:
        if addinFol == "":
            continue

        # アドインフォルダからアドイン関数辞書取り出し
        dictAddin = LoadAddins(addinFol)
        # 変換関数辞書に統合
        dictConvFuncs.update(dictAddin)
except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in loading addins. ")
    OutputStderr(OUTPUT_NAME_ERROR, str(e))
    # 処理可能な範囲で処理継続する為、終了しない
    # sys.exit()

#
# フォーマット情報取り出し
#
outputInfos={}
try:
    line = sys.stdin.readline()
    recordDic = json.loads(line)

    inputData = GetInputData(recordDic, 'formatInfo')
    if not inputData is None :
        outputInfos = json.loads(inputData)
    else:
        raise Exception('')

    if not (CheckOutputInfo(outputInfos)):
        OutputStderr(OUTPUT_NAME_ERROR, "Illegal output information format.")
        raise Exception('')

except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in output information parameter. ")
    exit(1)

#
# プロパティ取り出し
#
properties={}
try:
    line = sys.stdin.readline()
    recordDic = json.loads(line)

    inputData = GetInputData(recordDic, 'properties')
    if not inputData is None :
        properties = Props2Dict(inputData)

except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Properties read error. ")
    OutputStderr(OUTPUT_NAME_ERROR, str(e))

#
# レコード毎の処理の実施
#
convStatusAll = True
output1 = []
output2 = []
outputnormal = output1
outputerror = output1
if "2" == convErr:
    outputerror = output2

for line in sys.stdin:

    recordDic = json.loads(line)

    # １レコードの変換処理
    output = ""
    convStatusRcd = False
    try:
        # 入力データ取り出し
        inputData = GetInputData(recordDic, 'data')
        if inputData is None :
            continue

        if "GaudiMsg" == dataType:
            # ヘッダ部の取り出し
            recordHeader = inputData['RecordHeader']
            if (traceFlag):
                traceData.pushListData("input RecordHeader", recordHeader)

            # データ部の取り出し
            recordData = inputData['RecordData']
            if (traceFlag):
                traceData.pushListData("input RecordData", recordData)
        elif "msg" == dataType:
            # データ部の取り出し
            recordData = inputData
            if (traceFlag):
                traceData.pushListData("input recordData", recordData)
        else:
            raise Exception('Type error : dataType', dataType)

        # 変換処理実行
        outputRecord, convStatusRcd = main(recordData, properties)
        if (traceFlag):
            traceData.pushListData("output", outputRecord)
        if True == convStatusAll and False == convStatusRcd:
            convStatusAll = False

        # 出力の設定
        if "GaudiMsg" == dataType:
            output = {"Status":convStatusRcd, "Record":{"RecordHeader":recordHeader, "RecordData":outputRecord}}
        elif "msg" == dataType:
            output = {"Status":convStatusRcd, "Record":outputRecord}
        else:
            raise Exception('Type error : dataType', dataType)

        # 出力用配列に設定
        if False == convStatusRcd:
            outputerror.append(output)
        else:
            outputnormal.append(output)
        
    except Exception as e:
        convStatusRcd = False
        convStatusAll = False

        # エラーメッセージ出力
        errMsg = "Convert error : " + json.dumps(recordData,ensure_ascii=True)
        OutputStderr(OUTPUT_NAME_ERROR, errMsg)
        OutputStderr(OUTPUT_NAME_ERROR, str(e))

        # 出力の設定
        output = {"Status":convStatusRcd, "Record":"Convert error : " + json.dumps(recordData,ensure_ascii=True)}

        # 出力用配列に設定
        outputerror.append(output)


# 変換結果の出力
try:
    if "3" == convErr and False == convStatusAll:
        output2 = output1
        output1 = []

    for item in output1:
        OutputStdout(OUTPUT_NAME_DATA, item)

    for item in output2:
        OutputStderr(OUTPUT_NAME_DATA, item)

except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in output convert data : ")
    OutputStderr(OUTPUT_NAME_ERROR, str(e))

# プロパティの出力
try:
    props = Dict2Props(properties)
    OutputStdout(OUTPUT_NAME_PROPERTIES, props)
    OutputStderr(OUTPUT_NAME_PROPERTIES, props)
    
    if (traceFlag):
        traceData.push("output properties", json.dumps(props,ensure_ascii=True))
except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in output properties : ")
    OutputStderr(OUTPUT_NAME_ERROR, str(e))

# トレースデータの出力
try:
    if (traceFlag):
        OutputStderr(OUTPUT_NAME_TRACE, "=== Trace data START ===")
        traceData.dump()
        for item in traceData.records: 
            OutputStderr(OUTPUT_NAME_TRACE, item)
        
        OutputStderr(OUTPUT_NAME_TRACE, "=== Trace data END ===")
except Exception as e:
    OutputStderr(OUTPUT_NAME_ERROR, "Error in output trace data : ")
    OutputStderr(OUTPUT_NAME_ERROR, str(e))
