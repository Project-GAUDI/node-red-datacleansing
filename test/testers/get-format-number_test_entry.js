// テストヘルパ取り込み
var helper = require("node-red-node-test-helper");

// テスト対象lib取り込み
var getFormatNumberLib = require("../../get-format-number/get-format-number.js");

// テスト実行Lib取り込み
const TestRunner = require("../lib/test_runner.js");


// テスト実行クラス取得
var testRunner = new TestRunner();


// テスト前処理登録
testRunner.preTester = myPreTester;
function myPreTester() {
    // 前処理を記述
    return;
}

// テスト後処理登録
testRunner.preTester = myPostTester;
function myPostTester() {
    // 後処理を記述
    helper.unload();
    return;
}

const id_default = "getfmtno01";
const type_default = "get-format-number";
const name_default = "GetFormatNumber";
const to_default = "format";
const toType_default = "metaKey";

const default_payload = "{\"RecordList\":[{\"RecordHeader\":[\"999_001_ABC\",\"1\"],\"RecordData\":[\"1\",\"2\"]}]}";

const sample = [
    {
        "id": id_default,
        "type": type_default,
        "name": name_default,
        "from": "payload",
        "to": "format",
        "toType": toType_default,
        "wires": [
            [
                "helper01"
            ]
        ]
    },
    {
        "id": "helper01",
        "type": "helper"
    }
]




// const node_template = [{"id":id_default,"type":type_default,"name":name_default,"fmtinfos":fmtinfos_default}];
// const node_template2 = [{"id":id_default,"type":type_default,"name":name_default,"fmtinfos":fmtinfos_default2}];

function getResult(msg, propertyType, propertyName) {
    var result = null;
    switch (propertyType) {
        case "msg":
            result = msg[propertyName];
            break;
        case "metaKey":
            // 同じKeyのプロパティを検索
            var filted_props = msg.properties.propertyList.filter( prop => prop.key == propertyName );

            if ( 0 < filted_props.length ) {
                // 一致プロパティがある場合
                result = filted_props[0].value;
            }
            break;
    }

    return result;
}




// ＃＃＃＃＃　このテストの組み込みは、一旦行わない事とする　＃＃＃＃＃
//　課題１：グローバル設定ノードを含む構成(node_sample)だと、フローのロードに失敗する→getNodeでnullが返り、その後の処理でエラー
//　課題２：test_runnerが非同期実行に対応できていない。on("input")のコールバック型の処理を待機させる事ができず、素通りしてしまう

// testRunner.test_entry( "01 正常読み込み", "OK", load_01_OK, ""); 
async function load_01_OK() {
    // var target_template = node_template;
    var target_template = sample;
    var test_toType = toType_default;

    var flow = structuredClone(target_template);
    await helper.load(getFormatNumberLib, flow);
    var getfmtno01 = helper.getNode("getfmtno01");
    var helper01 = helper.getNode("helper01");

    helper01.on("input", async function(msg){
        msg.should.have.property("payload", "All Test Finished Normally.")
        getResult(msg, test_toType, to_default).should.be.exactly("001");
        (false).should.be.true();
    });

    (false).should.be.true();
}

// testRunner.test_entry( "02 name空", "OK", load_03_OK_empty_name, "");


// テスト反映（最後に実施）
testRunner.describe('get-format-number Node');
