from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def fetch_breach_data(email):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://intelx.io/")  # Open IntelligenceX homepage
        time.sleep(2)

        # Locate search bar and enter email
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(email)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # Allow results to load

        # Extract breach data
        results = driver.find_elements(By.CLASS_NAME, "searchresult")

        breaches = []
        for result in results:
            try:
                title = result.find_element(By.TAG_NAME, "a").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                breaches.append({"title": title, "link": link})
            except:
                continue

        return {"email": email, "breaches": breaches}
    
    finally:
        driver.quit()

@app.route("/breach-check", methods=["GET"])
def breach_check():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400
    
    data = fetch_breach_data(email)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
