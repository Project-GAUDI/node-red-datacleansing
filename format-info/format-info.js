
module.exports = function(RED) {
    "use strict";
    
    // ノード論理名の定義
    const myNodeName = "format-info";

    // 配列判定
    function isArray(iObj) {
        var toString = Object.prototype.toString;
        const arrayType = toString.call([]);

        var retIsArray = arrayType == toString.call(iObj);
        return retIsArray;
    }

    // ノードの登録用関数
    function registerNode(config) {
        // ノードの構築
        RED.nodes.createNode(this,config);

        const node = this;
        // フォーマット情報辞書
        node.formatInfoDict = {};
        node.name = config.name||"";
        node.fmtinfos = config.fmtinfos||"";

        // フォーマット情報の取り出しと軽量化
        node.getFormatInfo = function(fmtno) {
            node.trace("Start Method: format-info.getFormatInfo");
            var retInfo = null;
    
            if ( fmtno in node.formatInfoDict ) {

                retInfo = node.formatInfoDict[fmtno];
                node.trace("retInfo(in dict) : " + retInfo);
    
            } else {
    
                try {
                    // node.fmtinfos=[{"fno":"000","fmt":"..."},{"fno"}]
                    node.debug("fmtinfos : " + node.fmtinfos);
                    var fmtInfoList = JSON.parse(node.fmtinfos);
    
                    var filtedInfos = fmtInfoList.filter( info => info.fno == fmtno );
                    node.debug("filtedInfos : " + JSON.stringify(filtedInfos));

                    node.debug("filtedInfos.length : " + filtedInfos.length.toString());
                    var fmtInfo = null;
                    if ( 0 < filtedInfos.length ) {
                        // 一致がある場合、抽出。
                        fmtInfo = JSON.parse(filtedInfos[0].fmt);
                        node.debug("fmtInfo : " + JSON.stringify(fmtInfo));

                        if ( "OutputData" in fmtInfo ) {
                            // OutputData を持つ場合、軽量化

                            node.debug("isArray : " + isArray(fmtInfo.OutputData).toString());
                            // fmtInfo.OutputDataが配列でない場合
                            if (!isArray(fmtInfo.OutputData)) {
                                node.error("OutputData is not an Array.");
                                throw new Error("OutputData is not array.");
                            }
        
                            for ( var outInfo of fmtInfo.OutputData ) {
                                if ( "Converters" in outInfo ) {
                                    // outInfo.Convertersが配列でない場合
                                    if (!isArray(outInfo.Converters)) {
                                        node.error("Converters is not an Array.");
                                        throw new Error("Converters is not array.");
                                    }
            
                                    // Convertersの"Enabled":falseのデータは不要なので除去する。(trueのみのリストにする)
                                    var tmpList = [];
                                    for ( var cnvInfo of outInfo.Converters ) {
                                        if ( "Enabled" in cnvInfo ) {
                                            if (cnvInfo.Enabled === true) {
                                                tmpList.push(cnvInfo);
                                            }
                                        }
                                    }
                                    outInfo.Converters = tmpList;
                                }
                            }
                        }

                        retInfo = JSON.stringify(fmtInfo);
                        // 辞書に追加
                        node.formatInfoDict[fmtno] = retInfo;
                    }

                    node.trace("retInfo(not in dict) : " + retInfo);
    
                }
                catch (e){
                    node.error( "getFormatInfo failed : " + e);
                    retInfo = null;
                }
    
            }
            node.trace("retInfo : " + retInfo);
    
            node.trace("End Method: format-info.getFormatInfo");
            return retInfo;
        }

    }
    // ノードを登録する
    RED.nodes.registerType(myNodeName, registerNode);

}
