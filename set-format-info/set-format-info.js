
module.exports = function(RED) {
    // ノード論理名の定義
    const myNodeName = "set-format-info";

    // 配列判定
    function isArray(iObj) {
        var toString = Object.prototype.toString;
        const arrayType = toString.call([]);

        var retIsArray = arrayType == toString.call(iObj);
        return retIsArray;
    }


    // メッセージ入力時のコールバック
    function on_msg_input( msg, input_props ) {

        // フォーマット番号が一致するフォーマット情報を抽出し、メンバにセットする
        try {
            debuglog( "trace", "inupts : " + JSON.stringify(input_props) );

            // msgプロパティを設定
            if ( false == ("properties" in msg) ) {
                msg["properties"] =  {propertyList:[], count:function(){return this.propertyList.length;} };
            };
            if ( false == ("propertyList" in msg.properties) ) {
                msg.properties["propertyList"] = [];
            }

            var fnopropname = input_props["fno"];
            var fnoproptype = input_props["fnoType"];
            var fmtpropname = input_props["fmt"];
            var formatinfos = input_props["fmtinfos"];

            // 入力元・出力先が空欄の場合エラー (読み込み時は参照エラー、書き出し時は空欄で書き出せてしまう)
            if ("" == fnopropname) {
                throw new Error("入力(フォーマット番号)" + " field is empty.");
            }

            if ("" == fmtpropname) {
                throw new Error("出力(フォーマット情報)" + " field is empty.");
            }

            // フォーマット番号が一致するフォーマット情報を抽出する
            var fno = "";
            switch (fnoproptype) {
                case "msg":
                    if (fnopropname in msg) {
                        fno = msg[fnopropname];
                    }
                    else {
                        throw new Error(fnopropname + " property not found.");
                    }
                    break;
                case "metaKey":
                    // 同じKeyのプロパティを検索
                    var filted_props = msg.properties.propertyList.filter( prop => prop.key == fnopropname );

                    if ( 0 < filted_props.length ) {
                        // 一致プロパティがある場合、取得
                        fno = filted_props[0].value;
                    } else {
                        // 見つからないのでエラー
                        throw new Error(fnopropname + " meta key not found.");
                    }
                    break;
            }

            var filted_fmtinfos = formatinfos.data.filter( info => info.fno == fno );

            var targetInfo = "";
            if ( 0 < filted_fmtinfos.length ) {
                // 一致プロパティがある場合

                // オブジェクト化が未実施の場合、オブジェクト化する。
                if ( ("obj" in filted_fmtinfos[0]) != true ) {
                    filted_fmtinfos[0]["obj"] = getFormatInfo(filted_fmtinfos[0].fmt);

                    if (null === filted_fmtinfos[0]["obj"]) {
                        // フォーマット不正
                        throw new Error("Illegal format.");
                    }
                }

                targetInfo = filted_fmtinfos[0]["obj"];
                debuglog( "debug", "get formatinfo from no: " + fno );
            } else {
                targetInfo = {}
                throw new Error("no formatinfo from no: " + fno);
            }
            // 出力用プロパティにセット
            msg[fmtpropname] = targetInfo;

            debuglog( "trace", "output : " + JSON.stringify(fmtpropname) );

        } catch (ex) {
            // ログを出力
            var output_msg = "Error : Set format info. failed. " + ex.message;
            debuglog( "error", output_msg );
            throw new Error(output_msg);
        }

        return msg;
    }

    // フォーマット情報の取り出しと軽量化
    function getFormatInfo(fmtJSON) {
        debuglog( "trace", "getFormatInfo called." );
        var retInfo = null;

        try {
            var fmtInfo = JSON.parse(fmtJSON);
            // fmtInfo.OutputDataが配列でない場合
            if (!isArray(fmtInfo.OutputData)) {
                throw new Error("OutputData is not found or not array.");
            }

            for ( var outInfo of fmtInfo.OutputData ) {
                // outInfo.Convertersが配列でない場合
                if (!isArray(outInfo.Converters)) {
                    throw new Error("Converters is not found or not array.");
                }

                // Convertersの"Enabled":falseのデータは不要なので除去する。(trueのみのリストにする)
                var tmpList = [];
                for ( var cnvInfo of outInfo.Converters ) {
                    if (cnvInfo.Enabled == true) {
                        tmpList.push(cnvInfo);
                    }
                }
                outInfo.Converters = tmpList;
            }
            retInfo = fmtInfo;
        }
        catch (ex) {
            retInfo = null;
        }

        return retInfo;
    }

    // ノードの登録用関数
    function registerNode(config) {
        // ノードの構築
        RED.nodes.createNode(this,config);

        var node = this;
        // メッセージ受信時の処理
        node.on('input', function(msg) {

            // メッセージ入力時のコールバックを実行
            msg = on_msg_input(msg, config);

            // メッセージを送信する
            node.send(msg);
        });
    }
    // ノードを登録する
    RED.nodes.registerType(myNodeName, registerNode);

    // ログ出力
    // GAUDI_NODERED_CUSTUMNODE_LOG_TARGET 環境変数に
    // ノード名（myNodeName）が含まれている場合、ログ出力する。
    // 複数ノードを設定する場合は、";"区切りなどで記述。
    // GAUDI_NODERED_CUSTUMNODE_LOG_LEVEL 環境変数に指定されたログレベルに従う。
    // "trace" > "debug" > "info"(default) > "warn" > "error"
    // 複数ノードを設定する場合は、";"区切りなどで記述。
    function debuglog(level, logmsg){
        const LOG_TARGET_ENVNAME = "GAUDI_NODERED_CUSTUMNODE_LOG_TARGET";
        const LOG_LEVEL_ENVNAME = "GAUDI_NODERED_CUSTUMNODE_LOG_LEVEL";
        const level_values = {"trace":5, "debug":4, "info":3, "warn":2, "error":1};
        try {
            // 環境変数取得
            var target_env = process.env[LOG_TARGET_ENVNAME];
            if (target_env == undefined) {
                target_env = "";
            }
            var loglevel_env = process.env[LOG_LEVEL_ENVNAME];
            if (loglevel_env == undefined) {
                loglevel_env = "info";
            }
            loglevel_env = loglevel_env.toLowerCase();

            // ログレベルの数値化
            var level_str2int = function(str) {
                var retValue = 3;       // default:info
                if ( str in level_values ) {
                    retValue = level_values[str];
                }
                return retValue;
            };
            var loglevel_int = level_str2int(loglevel_env);
            var outlevel_int = level_str2int(level.toLowerCase());

            if ( outlevel_int <= loglevel_int ) {
                if ( 0 <= target_env.indexOf(myNodeName) ) {
                    var output_msg = "# " + myNodeName + " - " + level + " : " + new Date() + " : " + logmsg;
                    console.log( output_msg );
                }
            }
        } catch (e) {
            ;
        }
    }
}
