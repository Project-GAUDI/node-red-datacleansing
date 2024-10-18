// テストヘルパ取り込み
var helper = require("node-red-node-test-helper");

// テスト対象lib取り込み
var dataCleansingLib = require("../../data-cleansing/data-cleansing.js");
var testlib = function(RED) {
    var formatInfoLib = require("../../format-info/format-info.js");
    var dataCleansingLib = require("../../data-cleansing/data-cleansing.js");
}

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



const node_sample =[
    {
        "id": "71f816ebf00b5fe6",
        "type": "function",
        "z": "10f96327bc417903",
        "name": "createMsg000 (standard_converter_tester)",
        "func": "const testValues = [null]\nconst format = \"000\"\n\nmsg.properties = { \"propertyList\": [{ \"key\": \"format\", \"value\": format }] };\nmsg.payload = {\"RecordList\":[]};\n\nfor (var value of testValues) {\n    msg.payload.RecordList.push(\n        { \"RecordHeader\": [], \"RecordData\": [value] }\n    );\n}\n\nreturn msg;\n",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 390,
        "y": 220,
        "wires": [
            [
                "data-cleansing2"
            ]
        ]
    },
    {
        "id": "data-cleansing2",
        "type": "data-cleansing2",
        "z": "10f96327bc417903",
        "name": "",
        "data": "payload",
        "dataType": "GaudiMsg",
        "fmtid": "format",
        "fmtidType": "metaKey",
        "fmtinfo": "39e8c09b901c2ac6",
        "addins": {
            "data": []
        },
        "dirty": false,
        "editors": [],
        "codecheck": 0,
        "cnverr": "1",
        "trace": false,
        "x": 710,
        "y": 220,
        "wires": [
            ["helper01"],
            ["helper02"]
        ]
    },
    {
        "id": "39e8c09b901c2ac6",
        "type": "format-info",
        "name": "Format Info000",
        "fmtinfos": "[{\"fno\":\"000\",\"fmt\":\"{\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"OutputName\\\":\\\"\\\",\\\"InputIndex\\\":[1],\\\"InputName\\\":[],\\\"Converters\\\":[{\\\"Converter\\\":\\\"standard_converter_tester\\\",\\\"Enabled\\\":true,\\\"Options\\\":[]}]}]}\"}]"
    },
    {
        "id": "helper01",
        "type": "helper"
    },
    {
        "id": "helper02",
        "type": "helper"
    }
];

const node_sample2 =[
    {
        "id": "data-cleansing2",
        "type": "data-cleansing2",
        "z": "10f96327bc417903",
        "name": "",
        "data": "payload",
        "dataType": "GaudiMsg",
        "fmtid": "format",
        "fmtidType": "metaKey",
        "fmtinfo": "",
        "addins": {
            "data": []
        },
        "dirty": false,
        "editors": [],
        "codecheck": 0,
        "cnverr": "1",
        "trace": false,
        "x": 710,
        "y": 220,
        "wires": [
            ["helper01"],
            ["helper02"]
        ]
    },
    {
        "id": "helper01",
        "type": "helper"
    },
    {
        "id": "helper02",
        "type": "helper"
    }
];



function craete_message() {
    const testValues = [""];
    const format = "000";
    
    msg = {};
    msg.properties = { "propertyList": [{ "key": "format", "value": format }] };
    msg.payload = {"RecordList":[]};
    for (var value of testValues) {
        msg.payload.RecordList.push(
            { "RecordHeader": [], "RecordData": [value] }    
        );
    }
    return msg;
}

const input_message = craete_message();

// ＃＃＃＃＃　このテストの組み込みは、一旦行わない事とする　＃＃＃＃＃
//　課題１：グローバル設定ノードを含む構成(node_sample)だと、フローのロードに失敗する→getNodeでnullが返り、その後の処理でエラー
//　課題２：test_runnerが非同期実行に対応できていない。on("input")のコールバック型の処理を待機させる事ができず、素通りしてしまう

// testRunner.test_entry( "01 standard_conerter_tester関数実行", "OK", standard_conerter_tester_01_OK, ""); 
async function standard_conerter_tester_01_OK() {
    var target_template = node_sample;

    var flow = structuredClone(target_template);
    await helper.load(dataCleansingLib, flow);

    var cleansing01 = helper.getNode("data-cleansing2");
    var helper01 = helper.getNode("helper01");
    var helper02 = helper.getNode("helper02");

    helper01.on("input", async function(msg){
        msg.should.have.property("payload", "All Test Finished Normally.")
        (false).should.be.true();
    });
    helper02.on("input", async function(msg){
        (false).should.be.true();
    });

    await cleansing01.receive({ payload: "UpperCase" });

    (false).should.be.true();
}




// テスト反映（最後に実施）
testRunner.describe('standard converters');
