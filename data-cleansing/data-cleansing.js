module.exports = function(RED) {
    // 配列判定
    function isArray(iObj) {
        var toString = Object.prototype.toString;
        const arrayType = toString.call([]);

        var retIsArray = arrayType == toString.call(iObj);
        return retIsArray;
    }

    // JSON判定
    function isJson(value) {
        try {
            JSON.parse(value)
        } catch (e) {
            return false
        }
        return true
    }

    // 使用ライブラリのロード
    const fs = require("fs");
    const path = require('path');
    const { PythonShell } = require("python-shell");

    // 内部処理用メインPythonスクリプト
    const datacleansing_mainpy = "data-cleansing-main.py";
    // テンポラリルートフォルダ
    const tempRootFolder = "/data/temp";
    // システムアドインサブフォルダ名
    const systemAddinSubFolder = "systemaddins";
    // ノード論理名の定義
    const myNodeName = "data-cleansing2";

    // 使用プロパティ名 
    const prop_name = "name";
    const prop_data = "data";
    const prop_dataType = "dataType";
    const prop_fmtId = "fmtid";
    const prop_fmtidType = "fmtidType";
    const prop_addins = "addins";
    const prop_dirty = "dirty";
    const prop_cnverr = "cnverr";
    const prop_trace = "trace";
    // 使用サブプロパティ名 
    const prop_funcName = "funcName";
    const prop_funcDescription = "funcDescription";
    const prop_pythonCode = "pythonCode";
        
    // ノード停止時のコールバック
    function on_node_close( node, removed, done ) {
        node.trace("Start Method: data-cleansing.on_node_close");

        try {
            // ユーザ定義addin用テンポラリフォルダ削除
            // ノード毎に生成するので、ノードのIDを使用している
            // 次に使用されない可能性を考慮し、リスタート等でも一旦削除する。
            removeTempFolder( node.id );
            node.log("removeTempFolder succeeded.");
        } catch (ex) {
            var err = "Error : Removing templary folder failed. (" + ex.message + ")";
            node.log(err);        // エラーをthrowしているので、infoレベルで出力
            node.trace("Exit Method: data-cleansing.on_node_close");
            throw new Error(err);
        }

        // 処理完了時のコールバック呼び出し
        if ( done != null ) {
            done();
        }
        node.trace("End Method: data-cleansing.on_node_close");
        return;
    }

    // メッセージ入力時のコールバック
    function on_msg_input( node, msg, input_props ) {
        node.trace("Start Method: data-cleansing.on_msg_input");

        node.log("1 node-message received.");
        node.trace("received node-message : " + JSON.stringify(msg));

        try {

            var userAddinFolder = "";
            var rebuildFlag = false;
            var cnvErr = "";
            var traceFlag = false;

            // エラー変換処理オプションの取得
            if (input_props[prop_cnverr]) {
                // エラー変換処理オプションの取得
                cnvErr = input_props[prop_cnverr];
            }
            node.debug("cnvErr : " + cnvErr);
            
            // トレースフラグの取得
            if (input_props[prop_trace]) {
                // トレースフラグをセット
                traceFlag = true;
            }
            node.debug("traceFlag : " + traceFlag.toString());

            // プロパティ更新フラグONまたはテンポラリフォルダが無い場合
            if (input_props[prop_dirty] || false == existsTempFolder(node.id)) {
                // 再構築（既存フォルダの一旦削除・アドインコードの出力）が必要
                rebuildFlag = true;
            }
            node.debug("rebuildFlag : " + rebuildFlag.toString());

            // ユーザ定義アドインコード用テンポラリフォルダ作成
            // ノード毎に生成するので、ノードのIDを使用する
            userAddinFolder = createTempFolder( node.id, rebuildFlag );

            if ( rebuildFlag == true ) {
                // ユーザ定義アドインコードの書き込み
                createUserAddinFiles(userAddinFolder, input_props[prop_addins]["data"]);
                node.debug("Rebuilt the add-in folder. : " + userAddinFolder);

                input_props[prop_dirty] = false;
            }

            // ノードプロパティの値を取得
            var sysaddinFolder = path.join(__dirname, systemAddinSubFolder);
            var addinFolders = sysaddinFolder + ";" + userAddinFolder;
            var dataType = input_props[prop_dataType];
            var data = input_props[prop_data];
            var fmtidproptype = input_props[prop_fmtidType];
            node.debug("fmtidproptype : " + fmtidproptype);
            var fmtidpropname = input_props[prop_fmtId];
            node.debug("fmtidpropname : " + fmtidpropname);

            // グローバル設定ノードからフォーマット情報を取得
            var fmtInfo = "";
            fmtInfo = getDataCleansingFormatInfo( node, fmtidproptype, fmtidpropname, msg );

            // Pythonの実行
            executePython( node, dataType, data, msg, fmtInfo, cnvErr, [addinFolders, traceFlag.toString(), dataType, cnvErr] );

        } catch (ex) {
            var err = "Error : Data cleansing failed. (" + ex.message + ")";
            node.log(err);        // エラーをthrowしているので、infoレベルで出力
            node.trace("Exit Method: data-cleansing.on_msg_input");
            throw new Error(err);
        }   

        node.trace("End Method: data-cleansing.on_msg_input");
        return;
    }

    // テンポラリフォルダ存在チェック
    function existsTempFolder( tempFolderName ){
        var retExists = false;
        var targetFolder = path.join(tempRootFolder, tempFolderName);
        try {
            retExists = fs.existsSync(targetFolder);
        } catch {
            // 何もしない
            ;
        }

        return retExists;
    }
    
    // テンポラリフォルダ作成
    function createTempFolder( tempFolderName, deleteIfExists = false ){
        var targetFolder = path.join(tempRootFolder, tempFolderName);
        // 同じ名称のフォルダがあれば一旦削除
        if ( deleteIfExists ) {
            // テンポラリフォルダ削除
            removeTempFolder(targetFolder);
        }
        if ( !fs.existsSync() ){
            // フォルダを作成
            fs.mkdirSync(targetFolder, { recursive: true });
        }

        return targetFolder;
    }

    // テンポラリフォルダ削除
    function removeTempFolder( tempFolderName ){
        var targetFolder = path.join(tempRootFolder, tempFolderName);
        try {
            fs.rmSync(targetFolder, { recursive: true, force: true });          // （v14.14.0以降）
            // fs.rmdirSync(targetFolder, { recursive: true });                    // Deprecated
        } catch {
            // 何もしない
            ;
        }

        return;
    }

    // ユーザ定義addin出力
    function createUserAddinFiles( tmpFolder, addinCodes ){
        for (var idx=0; idx < addinCodes.length; idx++ ) {

            var targetAddinFile = path.join(tmpFolder, addinCodes[idx][prop_funcName] + ".py");

            try{
                var pythonCode = "# " + addinCodes[idx][prop_funcDescription] + "\n";
                var pythonCode = pythonCode + addinCodes[idx][prop_pythonCode] + "\n";
                fs.writeFileSync(targetAddinFile, pythonCode);
            } catch (ex) {
                var err = "User addin file write error!(" + targetAddinFile + ") : " + ex.message;
                throw new Error(err);
            }
            
        }
    }

    // フォーマット情報取得
    function getDataCleansingFormatInfo(node, fmtidproptype, fmtidpropname, msg) {
        node.trace("Start Method: data-cleansing.getDataCleansingFormatInfo");

        var fmtId = "";
        switch (fmtidproptype) {
            case "msg":
                if (fmtidpropname in msg) {
                    fmtId = msg[fmtidpropname];
                }
                else {
                    var err = fmtidpropname + " property not found.";
                    node.log(err);        // エラーをthrowしているので、infoレベルで出力
                    node.trace("Exit Method: data-cleansing.getDataCleansingFormatInfo");
                    throw new Error(err);
                }
                break;
            case "metaKey":
                // 同じKeyのプロパティを検索
                var filted_props = msg.properties.propertyList.filter( prop => prop.key == fmtidpropname );

                if ( 0 < filted_props.length ) {
                    // 一致プロパティがある場合、取得
                    fmtId = filted_props[0].value;
                } else {
                    // 見つからないのでエラー
                    var err = fmtidpropname + " meta key not found.";
                    node.log(err);        // エラーをthrowしているので、infoレベルで出力
                    node.trace("Exit Method: data-cleansing.getDataCleansingFormatInfo");
                    throw new Error(err);
                }
                break;
        }
        node.debug("fmtId : " + fmtId);

        var fmtInfo = "";
        fmtInfo = node.node_fmtinfo.getFormatInfo(fmtId);
        if ( null == fmtInfo ) {
            var err = "format id (" + fmtId + ") not found.";
            node.log(err);        // エラーをthrowしているので、infoレベルで出力
            node.trace("Exit Method: data-cleansing.getDataCleansingFormatInfo");
            throw new Error(err);
        }
        node.debug("fmtInfo : " + fmtInfo);

        node.trace("End Method: data-cleansing.getDataCleansingFormatInfo");
        return fmtInfo;
    }

    // Python実行
    function executePython(node, dataType, data, msg, fmtInfo, cnvErr, args) {
        node.trace("Start Method: data-cleansing.executePython");

        const options = {
            pythonPath: "python3",
            pythonOptions: ["-u"],
            args: args
        };

        const mainpy_path = path.join(__dirname, datacleansing_mainpy);
        const shell = new PythonShell(mainpy_path, options);
        let output = [];
        let logs = [];

        // 標準出力の取り込み
        shell.on("message", function (message) {
            output.push(message);
        });

        // 標準エラー出力の取り込み
        shell.on("stderr", function (stderr) {
            logs.push(stderr);
        });

        // msgプロパティを設定
        if ( false == ("properties" in msg) ) {
            msg["properties"] =  {};
        };
        if ( false == ("propertyList" in msg.properties) ) {
            msg.properties["propertyList"] = [];
        }

        /// 標準入力として、フォーマット情報、プロパティと入力レコードを投入
        // フォーマット情報を投入
        var input = {formatInfo:fmtInfo};
        shell.send(JSON.stringify(input));

        // プロパティを投入
        var inprops = msg.properties;
        input = {properties:inprops};
        shell.send(JSON.stringify(input));

        // 入力レコードを投入
        var targetDataList = [];
        switch (dataType) {
            case "GaudiMsg":
                for ( var record of msg[data].RecordList ) {
                    targetDataList.push(record);
                }
                break;
            case "msg":
                if (!isArray(msg.payload)) {
                    var err = "Payload must be array.";
                    node.log(err);        // エラーをthrowしているので、infoレベルで出力
                    node.trace("Exit Method: data-cleansing.executePython");
                    throw new Error(err);
                }
                for ( var record of msg[data] ) {
                    targetDataList.push(record);
                }
                break;
        }
        for ( var record of targetDataList ) {
            input = {data:record};
            shell.send(JSON.stringify(input));
        }

        shell.end(function (err, code, signal) {
            node.trace("Start Method: data-cleansing.executePython-shell.end callback");

            node.debug("shell.end callback: code = " + code.toString());
            if (code != 0) {
                var errout_msg = msg;

                // エラー出力メッセージ更新
                UpdateMessage(node, logs, errout_msg, errout_msg, null);
                if ("error" in errout_msg){
                    var errmsg = "";
                    for (var item of errout_msg.error) {
                        errmsg = errmsg + item + "\n";
                    }
                    err.message = errmsg;
                }

                node.error(err);
                node.send([null, errout_msg]);
                node.log(   "0 node-message sent. " + 
                            "1 error(or trace) node-message sent. ")
                node.trace("sent error message : " + JSON.stringify(errout_msg));
            } else {
                // 通常側の出力メッセージ生成
                var output1_msg = msg;
                var output2_msg = JSON.parse(JSON.stringify(msg));

                // payload初期化
                var outputDataList = [];
                var errDataList = [];
                switch (dataType) {
                    case "GaudiMsg":
                        output1_msg.payload={RecordList: []};
                        outputDataList=output1_msg.payload.RecordList;

                        output2_msg.payload={RecordList: []};
                        errDataList=output2_msg.payload.RecordList;
                        break;
                    case "msg":
                        output1_msg.payload=[];
                        outputDataList=output1_msg.payload;

                        output2_msg.payload=[];
                        errDataList=output2_msg.payload;
                        break;
                }

                // converrorindex初期化
                output1_msg.converrorindex=[];
                output2_msg.converrorindex=[];

                // 正常出力メッセージ更新
                UpdateMessage(node, output, output1_msg, output2_msg, outputDataList);

                // エラー出力メッセージ更新
                UpdateMessage(node, logs, output2_msg, output2_msg, errDataList);

                // 変換エラーのレコードが存在するかつ、オプション「メッセージをエラー出力」選択時はnullにする
                if (0 !== errDataList.length && "3" == cnvErr ) {
                    output1_msg = null;
                }

                // 出力2に情報がなければnullにする
                if (0 === errDataList.length && !("trace" in output2_msg) && !("error" in output2_msg)) {
                    output2_msg = null;
                }

                // 出力メッセージを送信
                node.send([output1_msg, output2_msg]);
                node.log(   (Number(!!output1_msg)).toString() + " node-message sent. " + 
                            (Number(!!output2_msg)).toString() + " error(or trace) node-message sent. ")
                node.trace("sent node-message : " + JSON.stringify(output1_msg));
                node.trace("sent error node-message : " + JSON.stringify(output2_msg));
            }

            node.trace("End Method: data-cleansing.executePython-shell.end callback");
        });
        node.trace("End Method: data-cleansing.executePython");
    }

    // ノードの登録用関数
    function registerNode(config) {
        // ノードの構築
        RED.nodes.createNode(this,config);

        var node = this;

        node.fmtinfo = config.fmtinfo;
        node.node_fmtinfo = RED.nodes.getNode(config.fmtinfo)
        node.log("fmtinfo(on create) : " + node.fmtinfo);
        node.log("node_fmtinfo(on create) : " + JSON.stringify(node.node_fmtinfo));

        // メッセージ受信時の処理
        node.on('input', function(msg) {

            // メッセージ入力時のコールバックを実行
            on_msg_input(node, msg, config);

        });

        // ノード停止時の処理
        node.on('close', function(removed, done) {

            // メッセージ入力時のコールバックを実行
            on_node_close(node, removed, done);

        });
    }
    // ノードを登録する
    RED.nodes.registerType(myNodeName, registerNode);


    function UpdateMessage(node, msgary, normalmsg, errormsg, datalist){
        node.trace("Start Method: data-cleansing.UpdateMessage");

        for (var idx = 0; idx < msgary.length; idx++ ) {
            try {
                var outdata = msgary[idx];
                if (isJson(outdata)){
                    var outjson = JSON.parse(outdata);

                    // データ部の取り出し
                    if ( "data" in outjson && null != datalist ) {
                        outjson = outjson["data"];
                        if ( "Status" in outjson ) {
                            // 変換結果部の取り出し
                            var outstatus = outjson["Status"];
                            if (false == outstatus){
                                normalmsg.converrorindex.push(datalist.length);
                            }
                        }
                        if ( "Record" in outjson ) {
                            // レコード部の取り出し
                            var outrecord = outjson["Record"];
                            datalist.push(outrecord);
                        }
                    }

                    // プロパティの取り出しと保存
                    if ( "properties" in outjson ) {
                        var outprops = outjson["properties"];
                        for (var oProp of outprops.propertyList) {
                            // 同じKeyのプロパティを検索
                            var filted_props = normalmsg.properties.propertyList.filter( prop => prop.key == oProp.key );
                            // 
                            if ( 0 < filted_props.length ) {
                                // 一致プロパティがある場合、更新
                                filted_props[0].value = oProp.value;
                            } else {
                                // 不一致なので追加
                                normalmsg.properties.propertyList.push(oProp);
                            }
                        }
                    }

                    // トレース部の取り出し
                    if ( "trace" in outjson ) {
                        var outtrace = outjson["trace"];
                        if (!("trace" in normalmsg)){
                            normalmsg.trace=[];
                        }
                        normalmsg.trace.push(outtrace);
                    }

                    // エラー部の取り出し
                    if ( "error" in outjson ) {
                        var outerror = outjson["error"];
                        if (!("error" in normalmsg)){
                            normalmsg.error=[];
                        }
                        normalmsg.error.push(outerror);
                    }
                }
            } catch (e) {
                err = "Output error : data = " + msgary[idx] + " index=" + idx;
                if (!("error" in errormsg)){
                    errormsg.error=[];
                }
                errormsg.error.push(err);
                node.error(err);
            }

        }

        node.trace("End Method: data-cleansing.UpdateMessage");
    }
}
