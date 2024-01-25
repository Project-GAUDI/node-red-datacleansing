import ast
import datetime
import glob
import json
import os
import runpy
import sys
import types

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
        print( f'Input data read error ({properyName}): ' + json.dumps(inputLine[properyName],ensure_ascii=True), file=sys.stderr )
        print( e, file=sys.stderr )

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
    """
    # 出力データ領域の作成
    outputSize = 0
    for outInfo in outputInfos['OutputData']:
        ithOutputIndex = outInfo['OutputIndex']
        if isinstance((ithOutputIndex),int) and (outputSize < ithOutputIndex):
            outputSize = ithOutputIndex

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

    return outputRecord


#
# 初期処理
#

# 入力引数の取り出し
try:
    addinFolders = sys.argv[1]
    traceFlag = False
    if sys.argv[2].lower() == "true":
        traceFlag = True

except Exception as e:
    print( "Error in input parameters. arg length = " + str(len(sys.argv)) + " ,args = " + sys.argv, file=sys.stderr )
    print( e, file=sys.stderr )
    sys.exit(1)

# 参照ライブラリの追加
try:
    libpath = os.path.dirname(__file__)
    sys.path.append(libpath)
    import lib.Tracer as Tracer
    traceData = Tracer.Tracer(traceFlag)
except Exception as e:
    print( "Error in importing libraries.", file=sys.stderr )
    print( e, file=sys.stderr )
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
    print( "Error in loading addins. ", file=sys.stderr )
    print( e, file=sys.stderr )
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
        print( "Illegal output information format.", file=sys.stderr )
        raise Exception('')

except Exception as e:

    print( "Error in output information parameter. ", file=sys.stderr )
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
    print( "Properties read error. ", file=sys.stderr )
    print( e, file=sys.stderr )    

#
# レコード毎の処理の実施
#
for line in sys.stdin:

    recordDic = json.loads(line)

    # １レコードの変換処理
    output = {}
    try:
        # 入力データ取り出し
        inputData = GetInputData(recordDic, 'data')
        if inputData is None :
            continue

        if (traceFlag):
            traceData.pushListData("input", inputData)

        # 変換処理実行
        outputRecord = main(inputData, properties)
        if (traceFlag):
            traceData.pushListData("output", outputRecord)

        # 出力の設定
        output['data'] = outputRecord

    except Exception as e:
        errMsg = "Convert error : " + json.dumps(inputData,ensure_ascii=True)
        print( errMsg, file=sys.stderr )
        print( e, file=sys.stderr )

        # 出力の設定
        output['data'] = [errMsg]

    finally:
        # 変換結果を出力
        print(json.dumps(output,ensure_ascii=True))


# プロパティの出力
try:
    output = {}
    output['properties'] = Dict2Props(properties)
    print(json.dumps(output,ensure_ascii=True))
    if (traceFlag):
        traceData.push("output properties", json.dumps(output['properties'],ensure_ascii=True))
except Exception as e:
    print( "Error in output properties : ", file=sys.stderr )
    print( e, file=sys.stderr )

# トレースデータの出力
try:
    if (traceFlag):
        print( "=== Trace data START ===", file=sys.stderr )
        traceData.dump()
        print( "=== Trace data END ===", file=sys.stderr )
except Exception as e:
    print( "Error in output trace data : ", file=sys.stderr )
    print( e, file=sys.stderr )
