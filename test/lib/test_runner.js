var helper = require("node-red-node-test-helper");

class TestRunner {

    constructor() {
        // テスト前処理
        this._preTester = null;
        // テスト後処理
        this._postTester = null;
        // テスト関数リスト
        this._funcList = [];
    }

    set preTester(preMethod){
        this._preTester = preMethod;
    }
    set postTester(postMethod){
        this._postTester = postMethod;
    }

    // テスト関数追加
    test_entry(title, okng, testfunc, errmsg){
        this._funcList.push(
            {"title": title, "type": okng, "testFunc": testfunc, "errormsg":errmsg}
        );
    }

    // テスト反映
    describe(targetName) {    
        // テストの登録
        describe(targetName, ()=>{this.test_runner(this);});
    }

    test_runner(myInstance) {

        // テスト前処理呼び出し
        beforeEach(() => {
            if (myInstance._preTester) {
                myInstance._preTester();
            }
            helper.unload();
        });

        
        // テスト後処理呼び出し
        afterEach(() => {
            if (myInstance._postTester) {
                myInstance._postTester();
            }
            helper.unload();
        });

        myInstance._funcList.forEach((test) => {
            it(test.title, async () => {
                var error = null;
                try {
                    // テスト実行
                    await test.testFunc();
                    if (test.type === "OK") {
                        // テスト成功
                        error = null;
                    } else {
                        // テスト失敗（期待例外未発生）
                        error = new Error(`"${test.errormsg}" error required. \n<StackTrace>\n${err.stack}`);
                    }
                } catch (err) {
                    if (test.type === "NG") {
                        if (0 <= err.message.indexOf(test.errormsg)) {
                            if ( test.errormsg === "" ) {
                                // テスト失敗（例外発生(想定例外未設定)）
                                error = new Error(`"${err}" error occured. (Require error not set.) \n<StackTrace>\n${err.stack}`);
                            } else {
                                // テスト成功（期待例外発生）
                                error = null;
                            }
                        } else {
                            // テスト失敗（想定外例外発生）
                            error = new Error(`"${err}" error occured. But "${test.errormsg}" error required. \n<StackTrace>\n${err.stack}`);
                        }
                    } else {
                        // テスト失敗（例外発生）
                        error = new Error(`"${err}" error occured. \n<StackTrace>\n${err.stack}`);
                    }
                }
                if (error) {
                    throw error;
                }

                return;
            });
        });
    }
};

module.exports = TestRunner;
