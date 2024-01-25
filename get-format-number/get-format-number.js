module.exports = function(RED) {
    // ノード論理名の定義
    const myNodeName = "get-format-number";

    // メッセージ入力時のコールバック
    function on_msg_input( msg, input_props ) {

        // GAUDI標準フォーマットのRecordHeader（先頭レコード）からからフォーマット番号を取得
        try {
            debuglog( "trace", "inupts : " + JSON.stringify(input_props) );

            // msgプロパティを設定
            if ( false == ("properties" in msg) ) {
                msg["properties"] =  {propertyList:[], count:function(){return this.propertyList.length;} };
            };
            if ( false == ("propertyList" in msg.properties) ) {
                msg.properties["propertyList"] = [];
            }

            var propfromname = input_props["from"];
            var proptoname = input_props["to"];
            var proptotype = input_props["toType"];

            // 入力元・出力先が空欄の場合エラー (読み込み時は参照エラー、書き出し時は空欄で書き出せてしまう)
            if ("" == propfromname) {
                throw new Error("入力" + " field is empty.");
            }

            if ("" == proptoname) {
                throw new Error("出力" + " field is empty.");
            }

            var recordHeader = msg[propfromname].RecordList[0].RecordHeader[0];
            var splitedList = [];

            try {
                splitedList = recordHeader.split("_");
            }
            catch (ex) {
                throw new Error("RecordHeader not found.");
            }

            var formatNo = "";
            if (splitedList.length < 2) {
                throw new Error("RecordHeader need format no after '_'");
            }
            else {
                formatNo = splitedList[1];
            }


            switch (proptotype) {
                case "msg":
                    msg[proptoname] = formatNo;
                    break;
                case "metaKey":
                    // 同じKeyのプロパティを検索
                    var filted_props = msg.properties.propertyList.filter( prop => prop.key == proptoname );

                    if ( 0 < filted_props.length ) {
                        // 一致プロパティがある場合、更新
                        filted_props[0].value = formatNo;
                    } else {
                        // 不一致なので追加
                        msg.properties.propertyList.push({"key":proptoname,"value":formatNo});
                    }
                    break;
            }

            debuglog( "trace", "output : " + proptotype + " - " + formatNo );

        } catch (ex) {
            // ログを出力
            var output_msg = "Error : Get format number failed. " + ex.message;
            debuglog( "error", output_msg );
            throw new Error(output_msg);
        }

        return msg;
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
