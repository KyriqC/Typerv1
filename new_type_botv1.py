import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === SETTINGS ===
URL = "https://www.typing.com/student/typing-test/1-minute"
TYPING_TIME_SECONDS = 75  # How long to type before stopping


def get_user_settings():
    wpm = float(input("Enter desired words per minute (WPM): "))
    accuracy = float(input("Enter desired accuracy (0.0 to 1.0): "))
    chars_per_minute = wpm * 5
    delay = 60 / chars_per_minute
    return delay, accuracy


def launch_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep window open
    service = Service("./chromedriver.exe")  # Make sure chromedriver is in your project folder
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)
    return driver


def wait_for_user():
    print("\n▶️ Press Enter AFTER:")
    print("• You click 'Start Test'")
    print("• The text is visible")
    print("• Your cursor is blinking in the typing box")
    input("Press Enter to start typing...\n")


def get_typing_elements(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".letter--basic.screenBasic-letter"))
        )
        return driver.find_elements(By.CSS_SELECTOR, ".letter--basic.screenBasic-letter")
    except Exception as e:
        raise RuntimeError(f"Failed to load typing test content: {e}")


def smart_typing(driver, letters, delay, accuracy):
    active = driver.switch_to.active_element
    start_time = time.time()

    for i, letter_elem in enumerate(letters):
        if time.time() - start_time > TYPING_TIME_SECONDS:
            break

        correct_char = letter_elem.text

        # Randomly choose to type wrong char based on accuracy
        if random.random() > accuracy:
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            active.send_keys(wrong_char)
            time.sleep(delay)

            # If error visually detected, fix it
            try:
                if "is-wrong" in letter_elem.get_attribute("class"):
                    active.send_keys(Keys.BACKSPACE)
                    time.sleep(0.05)
                    active.send_keys(correct_char)
            except Exception:
                pass
        else:
            active.send_keys(correct_char)

        time.sleep(delay)


def main():
    try:
        delay, accuracy = get_user_settings()
        driver = launch_browser()
        print("Opening Typing.com...")

        wait_for_user()
        letters = get_typing_elements(driver)

        print("⌨️ Typing started...")
        smart_typing(driver, letters, delay, accuracy)

        input("🔚 Type 'quit' and press Enter to close the browser...\n")
        driver.quit()

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
