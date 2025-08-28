from playwright.sync_api import sync_playwright

def run_playwright_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://google.com.br")
        print(page.title())
        browser.close()

if __name__ == "__main__":
    run_playwright_test()
