module.exports = function(RED) {
    // ノード論理名の定義
    const myNodeName = "get-format-number";

    // メッセージ入力時のコールバック
    function on_msg_input( node, msg, input_props ) {
        node.trace("Start Method: get-format-number.on_msg_input");

        node.log("1 node-message received.");
        node.trace("Received node-message properties:" + (msg.properties?msg.properties:null));

        // GAUDI標準フォーマットのRecordHeader（先頭レコード）からからフォーマット番号を取得
        try {

            var propfromname = input_props["from"];
            var proptoname = input_props["to"];
            var proptotype = input_props["toType"];

            // msgプロパティの枠を設定
            if ("metaKey" == proptotype) {
                if ( false == ("properties" in msg) ) {
                    msg["properties"] =  {};
                };
                if ( false == ("propertyList" in msg.properties) ) {
                    msg.properties["propertyList"] = [];
                }
            }

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

            node.debug("output : " + proptotype + " - " + formatNo );

        } catch (ex) {
            // ログを出力
            var output_msg = "Error : Get format number failed. " + ex.message;
            node.error( output_msg );
            node.trace("Exit Method: get-format-number.on_msg_input");
            throw new Error(output_msg);
        }

        node.trace("End Method: get-format-number.on_msg_input");
        return msg;
    }

    // ノードの登録用関数
    function registerNode(config) {
        // ノードの構築
        RED.nodes.createNode(this,config);

        var node = this;
        // メッセージ受信時の処理
        node.on('input', function(msg) {
            node.trace("Start Method: get-format-number.on('input')");

            // メッセージ入力時のコールバックを実行
            msg = on_msg_input(node, msg, config);

            // メッセージを送信する
            node.send(msg);

            node.log("1 node-message sent.");
            node.trace("Output message : " + JSON.stringify(msg));

            node.trace("End Method: get-format-number.on('input')");
        });
    }
    // ノードを登録する
    RED.nodes.registerType(myNodeName, registerNode);

}
