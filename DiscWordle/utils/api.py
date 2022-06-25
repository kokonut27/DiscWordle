from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import json

def api():
  driver = webdriver.Firefox(executable_path="./geckodriver") 
  url = 'https://www.nytimes.com/games/wordle/index.html'
  driver.get(url)
  scriptArray="""return localStorage.getItem('nyt-wordle-state')"""
  result = driver.execute_script(scriptArray)
  data = json.loads(result)
  answer = data["solution"]
  driver.close();
  return answer