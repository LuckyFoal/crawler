import time
import subprocess
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    # Chrome 浏览器路径
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # 启动参数
    debugging_port = "--remote-debugging-port=9222"
    user_data_dir = r"--user-data-dir=D:\code\python\spcript\pythonProject\userData"  # 指定用户数据目录

    # 构建命令
    command = f'"{chrome_path}" {debugging_port} "{user_data_dir}" '

    try:
        # 启动 Chrome 浏览器
        subprocess.Popen(command, shell=True)
        print("Chrome 浏览器启动中...")

        # 等待浏览器完全启动
        time.sleep(10)

        # 连接到浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("成功连接到浏览器")

        # 获取或创建上下文
        if browser.contexts:
            context = browser.contexts[0]
        else:
            context = browser.new_context()

        # 获取或创建页面
        if context.pages:
            page = context.pages[0]
        else:
            page = context.new_page()

        # 访问京东网站
        page.goto("https://www.bilibili.com/")



        # 保持运行以便观察
        time.sleep(3)



    except Exception as e:
        print(f"发生错误: {e}")

def get_goods(page):
    page.goto("https://www.jd.com")
    page.locator('input#key').fill('mac pro')



if __name__ == "__main__":
    # 使用上下文管理器确保资源正确释放
    with sync_playwright() as playwright:
        run(playwright)
