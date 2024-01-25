import json
import sys

class Tracer:
    """
    変換内容トレース用クラス
    """
    records = []
    enabled = False          # False:出力しない、True:出力する

    def __init__(self, outputFlag):
        self.records = []
        self.outputFlag = outputFlag
    
    def push(self, label = "", data = ""):
        if (not self.outputFlag):
            return

        """ トレース出力用レコードを追加 """
        self.records.append( "" )
        if ( label != "" ) :
            self.addLabel( label )
        if ( data != "" ) :
            self.add( data )

    def pushListData(self, label, inputData):
        if (not self.outputFlag):
            return

        """ トレース出力用レコードとしてリストデータを追加 """
        self.push(label, "[ ")
        separater = ""
        for dat in inputData:
            self.add(separater)
            self.add(str(dat))
            separater=", "
        
        self.add(" ]")

    def add(self, data):
        if (not self.outputFlag):
            return

        """ 最新トレース出力用レコードにデータを追加 """
        if isinstance(data, list):
            self.addListData(data)
        else:
            self.addData(data)

    def addLabel(self, label):
        if (not self.outputFlag):
            return

        """ 最新トレース出力用レコードにデータを追加 """
        self.addData(label + ":")

    def addData(self, data):
        if (not self.outputFlag):
            return

        """ 最新トレース出力用レコードにデータを追加 """
        self.records[-1] += str(data)

    def addListData(self, data):
        if (not self.outputFlag):
            return

        """ 最新トレース出力用レコードにデータを追加 """
        self.addData("[")
        separater = ""
        for dat in data:
            self.addData(separater)
            self.addData(str(dat))
            separater=", "
        
        self.addData("]")

    def addConvname(self, converterName, option = "" ):
        if (not self.outputFlag):
            return

        """ 最新トレース出力用レコードにデータを追加 """
        self.records[-1] += " --(" + converterName + "(" + str(option) + ") )--> "

    def dump(self):
        if (not self.outputFlag):
            return

        for dat in self.records:
            print( dat, file=sys.stderr )
