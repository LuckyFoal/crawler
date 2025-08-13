// 微信泡泡玛特小程序自动操作脚本
// 功能：打开小程序 → 进入首页 → 点击"我的"
// 需要 Hamibot 2.0.0 及以上版本

// 配置参数
const config = {
    wechatName: "微信",          // 微信APP名称
    ppmAppletName: "泡泡玛特",    // 小程序名称
    waitTime: 1000,             // 各步骤等待时间(毫秒)
    maxRetry: 3                 // 最大重试次数
};

// 主函数
function main() {
    // 请求必要权限
    console.show();
    console.setSize(600, 800);
    auto();
//   	click('取消')
//     requestScreenCapture(false);
    toast("开始执行脚本");
  
    


    // 启动微信
    if (!openWeChat()) {
        console.error("微信启动失败，脚本终止");
        return;
    }

    if (!openPPMTApplet()) {
        console.error("泡泡玛特小程序打开失败，脚本终止");
        return;
    }

    // 点击商品
    if (!clickProduct()) {
        console.error("商品点击失败，脚本终止");
        return;
    }


    console.log("脚本执行完成");
    toast("操作完成");
}

// 打开微信
function openWeChat() {
    console.log("尝试打开微信...");

    // 先尝试通过包名启动
    if (launch("com.tencent.mm")) {
        console.log("通过包名启动微信成功");
        sleep(config.waitTime);
        return true;
    }

    // 包名启动失败则尝试通过APP名称启动
    console.log("通过包名启动失败，尝试通过APP名称启动");
//     home();
//     sleep(500);

    return false;
}

// 打开泡泡玛特小程序
function openPPMTApplet() {
    console.log("尝试打开泡泡玛特小程序...");
    // 获取屏幕尺寸
    // let width = device.width;
    // let height = device.height;

    // // 从屏幕中央向下滑动
    // swipe(width / 3, height * 0.3, width / 2, height * 0.8, 500);
    // sleep(5000)
    click('泡泡玛特');

    return true;
}

// 点击商品
function clickProduct() {
    console.log("尝试点击商品...");
    sleep(3000);
    // 获取屏幕尺寸
    let width = device.width;
    let height = device.height;

    press(width * 0.8, height * 0.95, 1);

}

// 启动脚本
main();
