import time
import subprocess
import random

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
        time.sleep(1)

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


        get_goods(page)

    except Exception as e:
        print(f"发生错误: {e}")


def get_goods(page):
    page.goto("https://www.jd.com")

    # 定义需要依次点击的元素选择器列表，以及是否打开新页面
    click_sequence = [
        ('img.user_avatar_img', True),  # 点击用户头像，会打开新页面
        ('dd#_MYJD_product a:has-text("商品收藏")', False),  # 点击菜单项，在当前页面导航
    ]

    current_page = page

    for i, (selector, opens_new_page) in enumerate(click_sequence):
        try:
            print(f"执行第 {i + 1} 步: 点击 {selector}")
            # 等待元素出现
            current_page.wait_for_selector(selector)

            if opens_new_page:
                # 监听新页面并点击元素
                with current_page.context.expect_page() as new_page_info:
                    current_page.locator(selector).click()
                    new_page = new_page_info.value
                    new_page.wait_for_load_state("networkidle")
                    # 更新当前页面为新页面
                    current_page = new_page
            else:
                # 在当前页面点击并等待加载完成
                current_page.locator(selector).click()
                current_page.wait_for_load_state("networkidle")

        except Exception as e:
            print(f"第 {i + 1} 步执行出错: {e}")
            # 继续执行下一步而不是中断

    # 直接处理商品列表页面
    process_goods_list(current_page)


def process_goods_list(page):
    """
    专门处理商品列表页面
    """
    try:
        # 等待商品列表加载
        page.wait_for_selector('.mf-goods-list')

        # 获取所有商品项
        goods_items = page.locator('.mf-goods-item')
        goods_count = goods_items.count()

        print(f"找到 {goods_count} 个商品，开始依次处理...")

        # 依次处理每个商品
        for i in range(goods_count):
            try:
                print(f"\n处理第 {i + 1} 个商品:")

                # 获取当前商品项
                goods_item = page.locator('.mf-goods-item').nth(i)

                # 获取商品信息
                goods_id = goods_item.get_attribute('id') or '未知ID'
                title_elem = goods_item.locator('.p-name a')
                title = title_elem.get_attribute('title') if title_elem.count() > 0 else '未知标题'

                print(f"商品ID: {goods_id}")
                print(f"商品标题: {title}")

                # 点击商品（打开新页面）
                if goods_item.locator('.p-img a').count() > 0:
                    with page.context.expect_page() as product_page_info:
                        goods_item.locator('.p-img a').click()
                        product_page = product_page_info.value

                        print(f"已打开商品详情页: {product_page.url}")

                        buy_item(product_page)

                        # 简单处理商品页面
                        product_title = product_page.title()
                        print(f"商品页面标题: {product_title}")

                        # 关闭商品详情页
                        product_page.close()
                        print("已关闭商品详情页")

            except Exception as e:
                print(f"处理第 {i + 1} 个商品时出错: {e}")
                continue

    except Exception as e:
        print(f"处理商品列表时出错: {e}")

def buy_item(product_page):
    # 点击"立即购买"按钮
    try:
        # 等待"立即购买"按钮出现
        product_page.wait_for_selector('#InitTradeUrl')

        # 点击"立即购买"
        product_page.locator('#InitTradeUrl').click()
        print("已点击'立即购买'按钮")

        # 等待可能的跳转页面加载
        product_page.wait_for_load_state("networkidle")

        # 可以在这里添加处理订单页面的逻辑
        print(f"当前页面URL: {product_page.url}")
    except Exception as buy_error:
        print(f"点击'立即购买'时出错: {buy_error}")


if __name__ == "__main__":
    # 使用上下文管理器确保资源正确释放
    with sync_playwright() as playwright:
        run(playwright)
