module.exports = function(RED) {
    // 配列判定
    function isArray(iObj) {
        var toString = Object.prototype.toString;
        const arrayType = toString.call([]);

        var retIsArray = arrayType == toString.call(iObj);
        return retIsArray;
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
    const myNodeName = "data-cleansing";

    // 使用プロパティ名 
    const prop_name = "name";
    const prop_data = "data";
    const prop_dataType = "dataType";
    const prop_fmtInfo = "fmtinfo";
    const prop_addins = "addins";
    const prop_dirty = "dirty";
    const prop_trace = "trace";
    // 使用サブプロパティ名 
    const prop_funcName = "funcName";
    const prop_funcDescription = "funcDescription";
    const prop_pythonCode = "pythonCode";
        
    // ノード停止時のコールバック
    function on_node_close( node, removed, done ) {
        try {
            // ユーザ定義addin用テンポラリフォルダ削除
            // ノード毎に生成するので、ノードのIDを使用している
            // 次に使用されない可能性を考慮し、リスタート等でも一旦削除する。
            removeTempFolder( node.id );
        } catch (ex) {
            var err = "Error : Removing templary folder failed. (" + ex.message + ")";
            debuglog("error", err);
            throw new Error(err);
        }

        // 処理完了時のコールバック呼び出し
        if ( done != null ) {
            done();
        }
        return;
    }

    // メッセージ入力時のコールバック
    function on_msg_input( node, msg, input_props ) {

        try {

            var userAddinFolder = "";
            var rebuildFlag = false;
            var traceFlag = false;
            
            // トレースフラグの取得
            if (input_props[prop_trace]) {
                // トレースフラグをセット
                traceFlag = true;
            }

            // プロパティ更新フラグONまたはテンポラリフォルダが無い場合
            if (input_props[prop_dirty] || false == existsTempFolder(node.id)) {
                // 再構築（既存フォルダの一旦削除・アドインコードの出力）が必要
                rebuildFlag = true;
            }

            // ユーザ定義アドインコード用テンポラリフォルダ作成
            // ノード毎に生成するので、ノードのIDを使用する
            userAddinFolder = createTempFolder( node.id, rebuildFlag );

            if ( rebuildFlag == true ) {
                // ユーザ定義アドインコードの書き込み
                createUserAddinFiles(userAddinFolder, input_props[prop_addins]["data"]);
                debuglog("trace", "Rebuilded addin folder. : " + userAddinFolder);

                input_props[prop_dirty] = false;
            }

            // Pythonの実行
            var sysaddinFolder = path.join(__dirname, systemAddinSubFolder);
            var addinFolders = sysaddinFolder + ";" + userAddinFolder;
            var dataType = input_props[prop_dataType];
            var data = input_props[prop_data];
            var fmtInfo = ""
            if ( input_props[prop_fmtInfo] in msg && msg[input_props[prop_fmtInfo]] != null) {
                fmtInfo = msg[input_props[prop_fmtInfo]];
                if ( fmtInfo != "" ) {
                    fmtInfo = JSON.stringify(fmtInfo);
                }
            }

            executePython( node, dataType, data, msg, fmtInfo, [addinFolders, traceFlag.toString()] );

        } catch (ex) {
            var err = "Error : Data cleansing failed. (" + ex.message + ")";
            debuglog("error", err);
            throw new Error(err);
        }   

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
            debuglog("trace", "Addin folder deleted. : " + targetFolder);
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
                debuglog("error", err);
                throw new Error(err);
            }
            
        }
    }

    // Python実行
    function executePython(node, dataType, data, msg, fmtInfo, args) {
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
            msg["properties"] =  {propertyList:[], count:function(){return this.propertyList.length;} };
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
                    targetDataList.push(record.RecordData);
                }
                break;
            case "msg":
                if (!isArray(msg.payload)) {
                    throw new Error("Payload must be array.");
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
            if (code != 0) {
                node.log(JSON.stringify(err));
                node.error(err, msg);
                let errout_msg = {
                    _msgid : msg._msgid,
                    payload : JSON.stringify(err)
                }
                node.send([null, errout_msg]);
                debuglog("info", "sent error message : " + JSON.stringify(errout_msg));
            } else {
                // エラー側の出力メッセージ生成
                let errout_msg = {
                    _msgid : msg._msgid,
                    payload : logs
                }
                // 正常出力メッセージ
                for (var idx = 0; idx < output.length; idx++ ) {
                    try {
                        var outdata = output[idx];
                        var outjson = JSON.parse(outdata);
                        if ( "data" in outjson ) {
                            // データ部の取り出しと保存
                            var outrecord = outjson["data"];
                            // データの置き換え（配列を空にして出力要素を順に追加）
                            targetDataList[idx].length = 0;
                            outrecord.forEach( col => targetDataList[idx].push(col) );
                        }

                        // プロパティの取り出しと保存
                        if ( "properties" in outjson ) {
                            var outprops = outjson["properties"];
                            for (var oProp of outprops.propertyList) {
                                // 同じKeyのプロパティを検索
                                var filted_props = msg.properties.propertyList.filter( prop => prop.key == oProp.key );
                                // 
                                if ( 0 < filted_props.length ) {
                                    // 一致プロパティがある場合、更新
                                    filted_props[0].value = oProp.value;
                                } else {
                                    // 不一致なので追加
                                    msg.properties.propertyList.push(oProp);
                                }
                            }
                        }
                    } catch (e) {
                        err = "Output error : data = " + output[idx] + " index=" + idx;
                        errout_msg.payload.push(err);
                        debuglog("error", err);
                    }
                }
                
                // erroutに情報がなければnullにする
                if (0 === errout_msg.payload.length) {
                    errout_msg = null;
                }

                // 出力メッセージを送信
                node.send([msg, errout_msg]);    
                debuglog("info", "sent message : " + JSON.stringify(msg));
                debuglog("info", "sent error message : " + JSON.stringify(errout_msg));
            }

        });
    }

    // ノードの登録用関数
    function registerNode(config) {
        // ノードの構築
        RED.nodes.createNode(this,config);

        var node = this;
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
