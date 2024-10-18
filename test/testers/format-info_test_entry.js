// テストヘルパ取り込み
var helper = require("node-red-node-test-helper");

// テスト対象lib取り込み
var formatInfoLib = require("../../format-info/format-info.js");

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




const id_default = "fmtinfo01";
const type_default = "format-info";
const name_default = "Format Info";
const fmtinfos_default = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[]}\"}]";
const fmtinfos_default2 = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert_null\\\",\\\"Enabled\\\":false,\\\"Options\\\":null}]}]}\"}]";

const name_empty = "";
const fmtinfos_emptystring = "";
const fmtinfos_emptyarray = "[]";
const fmtinfos_nofno = "[{\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[]}\"}]";
const fmtinfos_nofmt = "[{\"fno\":\"000\"}]";
const fmtinfos_noformat = "[{\"fno\":\"000\",\"fmt\":\"{\\\"OutputData\\\":[]}\"}]";
const fmtinfos_nooutputdata = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\"}\"}]";
const fmtinfos_badoutputdata = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":\\\"bad-outputdata\\\"}\"}]";
const fmtinfos_emptyoutputdata = fmtinfos_default;
const fmtinfos_noconverter = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1]}]}\"}]";
const fmtinfos_badconverter = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":\\\"\\\"}]}\"}]";
const fmtinfos_emptyconverter = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[]}]}\"}]";
const fmtinfos_noenabled = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert_null\\\",\\\"Options\\\":null}]}]}\"}]";
const fmtinfos_noenabledtrue = fmtinfos_default2;
const fmtinfos_onlyenabledtrue = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert_null\\\",\\\"Enabled\\\":true,\\\"Options\\\":null}]}]}\"}]";
const fmtinfos_mixedenabled = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert1\\\",\\\"Enabled\\\":true,\\\"Options\\\":null},{\\\"Converter\\\":\\\"convert2\\\",\\\"Enabled\\\":false,\\\"Options\\\":null},{\\\"Converter\\\":\\\"convert3\\\",\\\"Enabled\\\":true,\\\"Options\\\":null},{\\\"Converter\\\":\\\"convert4\\\",\\\"Enabled\\\":false,\\\"Options\\\":null}]}]}\"}]";
const fmtinfos_badenabled = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert_null\\\",\\\"Enabled\\\":\\\"true\\\",\\\"Options\\\":null}]}]}\"}]";
const fmtinfos_3infos = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert0\\\",\\\"Enabled\\\":true,\\\"Options\\\":null}]}]}\"},{\"fno\":\"001\",\"fmt\":\"{\\\"format\\\":\\\"001\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert1\\\",\\\"Enabled\\\":true,\\\"Options\\\":null}]}]}\"},{\"fno\":\"002\",\"fmt\":\"{\\\"format\\\":\\\"002\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert2\\\",\\\"Enabled\\\":true,\\\"Options\\\":null}]}]}\"}]";

// const fmtinfos_default2 = "[{\"fno\":\"000\",\"fmt\":\"{\\\"format\\\":\\\"000\\\",\\\"OutputData\\\":[{\\\"OutputIndex\\\":1,\\\"InputIndex\\\":[1],\\\"Converters\\\":[{\\\"Converter\\\":\\\"convert_null\\\",\\\"Enabled\\\":false,\\\"Options\\\":null}]}]}\"}]";

const node_template = [{"id":id_default,"type":type_default,"name":name_default,"fmtinfos":fmtinfos_default}];
const node_template2 = [{"id":id_default,"type":type_default,"name":name_default,"fmtinfos":fmtinfos_default2}];


testRunner.test_entry( "01 正常読み込み", "OK", load_01_OK, ""); 
async function load_01_OK() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_default;

    var flow = structuredClone(target_template);
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    finfo01.should.have.property('name', name_default);
}

testRunner.test_entry( "02 AAA未設定(NGテストサンプル)", "NG", load_02_NG_no_AAA, "to have property AAA");
async function load_02_NG_no_AAA() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_default;

    var flow = structuredClone(target_template);
    delete flow[0].name;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    // 未設定でエラー。
    // NGテストのサンプル。
    finfo01.should.have.property('AAA', name_empty);
}

testRunner.test_entry( "03 name空", "OK", load_03_OK_empty_name, "");
async function load_03_OK_empty_name() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_default;

    var flow = structuredClone(target_template);
    flow[0].name = name_empty;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    finfo01.should.have.property('name', name_empty);
}

testRunner.test_entry( "04 fmtinfos未設定", "OK", load_04_OK_no_fmtinfos, "");
async function load_04_OK_no_fmtinfos() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_default;

    var flow = structuredClone(target_template);
    delete flow[0].fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    finfo01.should.have.property('fmtinfos', fmtinfos_emptystring);
}

testRunner.test_entry( "05 fmtinfos空文字列", "OK", load_05_OK_emptystring_fmtinfos, "");
async function load_05_OK_emptystring_fmtinfos() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_emptystring;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    finfo01.should.have.property('fmtinfos', fmtinfos_emptystring);
}

testRunner.test_entry( "06 fmtinfos空配列", "OK", load_06_OK_emptyarray_fmtinfos, "");
async function load_06_OK_emptyarray_fmtinfos() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_emptyarray;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    finfo01.should.have.property('fmtinfos', fmtinfos_emptyarray);
}

testRunner.test_entry( "07 fmtinfos fno未設定", "OK", load_07_OK_no_fno, "");
async function load_07_OK_no_fno() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_nofno;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    ('fno' in JSON.parse(finfo01.fmtinfos)).should.be.false();
}

testRunner.test_entry( "08 fmtinfos fmt未設定", "OK", load_08_OK_no_fmt, "");
async function load_08_OK_no_fmt() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_nofmt;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    ('fmt' in JSON.parse(finfo01.fmtinfos)).should.be.false();
}

testRunner.test_entry( "09 fmtinfos fmt-format未設定", "OK", load_09_OK_no_fmt_format, "");
async function load_09_OK_no_fmt_format() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_noformat;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    // エラーにならずfmtinfosが取り出しできる事のみ確認。
    finfo01.should.have.property('fmtinfos', fmtinfos_noformat);
}

testRunner.test_entry( "10 fmtinfos fmt-OutputData未設定", "OK", load_10_OK_no_fmt_outputdata, "");
async function load_10_OK_no_fmt_outputdata() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_nooutputdata;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    // エラーにならずfmtinfosが取り出しできる事のみ確認。
    finfo01.should.have.property('fmtinfos', fmtinfos_nooutputdata);
}

testRunner.test_entry( "01 getFormatInfo fmtinfos未設定->null", "OK", getFormatInfo_01_OK_no_fmtinfos, "");
async function getFormatInfo_01_OK_no_fmtinfos() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_default;

    var flow = structuredClone(target_template);
    delete flow[0].fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    
    var fmtinfo = finfo01.getFormatInfo('000');

    should(fmtinfo).be.exactly(null);        // nullチェック
}

testRunner.test_entry( "02 getFormatInfo fmtinfos空文字列->null", "OK", getFormatInfo_02_OK_emptystring_fmtinfos, "");
async function getFormatInfo_02_OK_emptystring_fmtinfos() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_emptystring;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
    
    var fmtinfo = finfo01.getFormatInfo('000');

    should(fmtinfo).be.exactly(null);        // nullチェック
}

testRunner.test_entry( "03 getFormatInfo fmtinfos空配列->null", "OK", getFormatInfo_03_OK_emptyarray_fmtinfos, "");
async function getFormatInfo_03_OK_emptyarray_fmtinfos() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_emptyarray;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');

    should(fmtinfo).be.exactly(null);        // nullチェック
}

testRunner.test_entry( "04 getFormatInfo fmtinfos fno未設定->null", "OK", getFormatInfo_04_OK_no_fno, "");
async function getFormatInfo_04_OK_no_fno() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_nofno;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');

    should(fmtinfo).be.exactly(null);        // nullチェック
}
    
testRunner.test_entry( "05 getFormatInfo fmtinfos fmt未設定->null", "OK", getFormatInfo_05_OK_no_fmt, "");
async function getFormatInfo_05_OK_no_fmt() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_nofmt;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');

    should(fmtinfo).be.exactly(null);        // nullチェック
}
    
testRunner.test_entry( "06 getFormatInfo fmtinfos fmt-format未設定->正常", "OK", getFormatInfo_06_OK_no_fmt_format, "");
async function getFormatInfo_06_OK_no_fmt_format() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_noformat;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('format' in fmtinfoObj).should.be.false();
}
    
testRunner.test_entry( "07 getFormatInfo fmtinfos fmt-OutputData未設定->正常(更新無し)", "OK", getFormatInfo_07_OK_no_fmt_outputdata, "");
async function getFormatInfo_07_OK_no_fmt_outputdata() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_nooutputdata;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.false();

    (fmtinfo).should.be.exactly( JSON.parse(fmtinfos_nooutputdata)[0].fmt );
}
    
testRunner.test_entry( "08 getFormatInfo fmtinfos fmt-OutputData配列以外->null", "OK", getFormatInfo_08_OK_bad_fmt_outputdata, "");
async function getFormatInfo_08_OK_bad_fmt_outputdata() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_badoutputdata;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');

    should(fmtinfo).be.exactly(null);        // nullチェック
}

testRunner.test_entry( "09 getFormatInfo fmtinfos fmt-OutputData空配列->null", "OK", getFormatInfo_09_OK_empty_fmt_outputdata, "");
async function getFormatInfo_09_OK_empty_fmt_outputdata() {
    var target_template = node_template;
    var target_fmtinfos = fmtinfos_emptyoutputdata;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();

    (fmtinfo).should.be.exactly( JSON.parse(fmtinfos_emptyoutputdata)[0].fmt );
}

testRunner.test_entry( "10 getFormatInfo fmtinfos fmt-OutputData-conveters未設定->null", "OK", getFormatInfo_10_OK_no_fmt_outputdata_converters, "");
async function getFormatInfo_10_OK_no_fmt_outputdata_converters() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_noconverter;

    var flow = structuredClone(node_template2);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('OutputIndex' in fmtinfoObj.OutputData[0]).should.be.true();
    ('InputIndex' in fmtinfoObj.OutputData[0]).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.false();

    (fmtinfo).should.be.exactly( JSON.parse(fmtinfos_noconverter)[0].fmt );
}

testRunner.test_entry( "11 getFormatInfo fmtinfos fmt-OutputData-conveters配列以外->null", "OK", getFormatInfo_11_OK_bad_fmt_outputdata_converters, "");
async function getFormatInfo_11_OK_bad_fmt_outputdata_converters() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_badconverter;

    var flow = structuredClone(node_template2);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.exactly(null);        // nullチェック

}

testRunner.test_entry( "12 getFormatInfo fmtinfos fmt-OutputData-conveters空配列->正常(更新無し)", "OK", getFormatInfo_12_OK_empty_fmt_outputdata_converters, "");
async function getFormatInfo_12_OK_empty_fmt_outputdata_converters() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_emptyconverter;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('OutputIndex' in fmtinfoObj.OutputData[0]).should.be.true();
    ('InputIndex' in fmtinfoObj.OutputData[0]).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.true();
    fmtinfoObj.OutputData[0].Converters.should.be.Array();

    // フォーマット情報に更新の無い事をチェック
    (fmtinfo).should.be.exactly( JSON.parse(target_fmtinfos)[0].fmt );
}

testRunner.test_entry( "13 getFormatInfo fmtinfos fmt-OutputData-conveters Enabled未設定->正常(converters空)", "OK", getFormatInfo_13_OK_no_fmt_outputdata_converters_enabled, "");
async function getFormatInfo_13_OK_no_fmt_outputdata_converters_enabled() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_noenabled;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.true();
    fmtinfoObj.OutputData[0].Converters.should.be.Array();

    // 更新前後の件数チェック
    (JSON.parse(JSON.parse(target_fmtinfos)[0].fmt).OutputData[0].Converters.length).should.be.exactly( 1 );
    (fmtinfoObj.OutputData[0].Converters.length).should.be.exactly(0);

    // フォーマット情報に更新がある事をチェック
    (fmtinfo).should.not.be.exactly( JSON.parse(target_fmtinfos)[0].fmt );
}

testRunner.test_entry( "14 getFormatInfo fmtinfos fmt-OutputData-conveters Enabled=trueなし->正常(converters空)", "OK", getFormatInfo_14_OK_no_fmt_outputdata_converters_enabled_true, "");
async function getFormatInfo_14_OK_no_fmt_outputdata_converters_enabled_true() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_noenabledtrue;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.true();
    fmtinfoObj.OutputData[0].Converters.should.be.Array();

    // 更新前後の件数チェック
    (JSON.parse(JSON.parse(target_fmtinfos)[0].fmt).OutputData[0].Converters.length).should.be.exactly( 1 );
    (fmtinfoObj.OutputData[0].Converters.length).should.be.exactly(0);

    // フォーマット情報に更新がある事をチェック
    (fmtinfo).should.not.be.exactly( JSON.parse(target_fmtinfos)[0].fmt );
}

testRunner.test_entry( "15 getFormatInfo fmtinfos fmt-OutputData-conveters Enabled=trueのみ->正常(更新無し)", "OK", getFormatInfo_15_OK_only_fmt_outputdata_converters_enabled_true, "");
async function getFormatInfo_15_OK_only_fmt_outputdata_converters_enabled_true() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_onlyenabledtrue;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.true();
    fmtinfoObj.OutputData[0].Converters.should.be.Array();

    (JSON.parse(JSON.parse(target_fmtinfos)[0].fmt).OutputData[0].Converters.length).should.be.exactly( 1 );
    (fmtinfoObj.OutputData[0].Converters.length).should.be.exactly(1);

    // フォーマット情報に更新の無い事をチェック
    (fmtinfo).should.be.exactly( JSON.parse(target_fmtinfos)[0].fmt );
}

testRunner.test_entry( "16 getFormatInfo fmtinfos fmt-OutputData-conveters Enabled=true/false混在->正常(converters true分のみ)", "OK", getFormatInfo_16_OK_mixed_fmt_outputdata_converters_enabled_truefalse, "");
async function getFormatInfo_16_OK_mixed_fmt_outputdata_converters_enabled_truefalse() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_mixedenabled;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.true();
    fmtinfoObj.OutputData[0].Converters.should.be.Array();

    (JSON.parse(JSON.parse(target_fmtinfos)[0].fmt).OutputData[0].Converters.length).should.be.exactly( 4 );
    (fmtinfoObj.OutputData[0].Converters.length).should.be.exactly(2);

    // フォーマット情報に更新がある事をチェック
    (fmtinfo).should.not.be.exactly( JSON.parse(target_fmtinfos)[0].fmt );
}

testRunner.test_entry( "17 getFormatInfo fmtinfos fmt-OutputData-conveters Enabled=true/false以外->null", "OK", getFormatInfo_17_OK_bad_fmt_outputdata_converters_enabled, "");
async function getFormatInfo_17_OK_bad_fmt_outputdata_converters_enabled() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_badenabled; //"Enabled":"true"(文字列) なので、判定失敗する。

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    ('OutputData' in fmtinfoObj).should.be.true();
    ('Converters' in fmtinfoObj.OutputData[0]).should.be.true();
    fmtinfoObj.OutputData[0].Converters.should.be.Array();

    // 更新前後の件数チェック
    (JSON.parse(JSON.parse(target_fmtinfos)[0].fmt).OutputData[0].Converters.length).should.be.exactly( 1 );
    (fmtinfoObj.OutputData[0].Converters.length).should.be.exactly(0);

    // フォーマット情報に更新がある事をチェック
    (fmtinfo).should.not.be.exactly( JSON.parse(target_fmtinfos)[0].fmt );
}

testRunner.test_entry( "18 getFormatInfo 1番目(先頭)で一致", "OK", getFormatInfo_18_OK_match_1st_formatinfo, "");
async function getFormatInfo_18_OK_match_1st_formatinfo() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_3infos;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('000');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    fmtinfoObj.format.should.be.exactly("000");
    fmtinfoObj.OutputData[0].Converters[0].Converter.should.be.exactly("convert0");
}

testRunner.test_entry( "19 getFormatInfo 2番目(中間)で一致", "OK", getFormatInfo_19_OK_match_2nd_formatinfo, "");
async function getFormatInfo_19_OK_match_2nd_formatinfo() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_3infos;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('001');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    fmtinfoObj.format.should.be.exactly("001");
    fmtinfoObj.OutputData[0].Converters[0].Converter.should.be.exactly("convert1");
}

testRunner.test_entry( "20 getFormatInfo 3番目(末尾)で一致", "OK", getFormatInfo_20_OK_match_3rd_formatinfo, "");
async function getFormatInfo_20_OK_match_3rd_formatinfo() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_3infos;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('002');
    should(fmtinfo).be.ok();

    var fmtinfoObj = JSON.parse(fmtinfo); 
    fmtinfoObj.format.should.be.exactly("002");
    fmtinfoObj.OutputData[0].Converters[0].Converter.should.be.exactly("convert2");
}

testRunner.test_entry( "21 getFormatInfo 一致なし->null", "OK", getFormatInfo_21_OK_nomatch_formatinfo, "");
async function getFormatInfo_21_OK_nomatch_formatinfo() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_3infos;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var fmtinfo = finfo01.getFormatInfo('003');
    should(fmtinfo).be.exactly(null);

}

testRunner.test_entry( "22 getFormatInfo 再取得", "OK", getFormatInfo_22_OK_SameFormatID, "");
async function getFormatInfo_22_OK_SameFormatID() {
    var target_template = node_template2;
    var target_fmtinfos = fmtinfos_3infos;

    var flow = structuredClone(target_template);
    flow[0].fmtinfos = target_fmtinfos;
    await helper.load(formatInfoLib, flow);
    var finfo01 = helper.getNode("fmtinfo01");
        
    var start1 = performance.now();
    var fmtinfo = finfo01.getFormatInfo('001');
    var end1 = performance.now();
    should(fmtinfo).be.ok();

    var start2 = performance.now();
    var fmtinfo2 = finfo01.getFormatInfo('001');
    var end2 = performance.now();
    should(fmtinfo).be.exactly(fmtinfo2);

    should((end1 - start1) > (end2 - start2)).be.true();
}


// テスト反映（最後に実施）
testRunner.describe('format-info Node');
