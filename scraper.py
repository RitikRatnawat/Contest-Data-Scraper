import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


CODECHEF_CONTEST_PAGE_URL = "https://www.codechef.com/contests"
LEETCODE_CONTEST_PAGE_URL = "https://leetcode.com/contest"
CODEFORCES_CONTEST_PAGE_URL = "https://codeforces.com/contests"


def get_driver():
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("./WebDriver/chromedriver", options=driver_options)
    return driver


def get_CodeChef_Data(driver):
    driver.get(CODECHEF_CONTEST_PAGE_URL)
    table = driver.find_element_by_id("future-contests-data")
    rows = table.find_elements_by_tag_name("tr")
    
    contest_data = []
    for row in rows:
        columns = row.find_elements_by_tag_name("td")
        code = columns[0].text
        name = columns[1].text
        url = columns[1].find_element_by_tag_name("a").get_attribute("href")
        duration = columns[3].text
        start = pd.to_datetime(columns[4].get_attribute("data-start-time"))
        date = start.strftime("%d %B,%Y")
        day = start.strftime("%A")
        time = start.strftime("%I:%M %p")
        
        contest_data.append({
            "Contest Code" : code,
            "Contest Name" : name,
            "Contest URL" : url,
            "Date" : date,
            "Day" : day,
            "Time" : time,
            "Duration" : duration
        })
        
    return contest_data


def get_LeetCode_Data(driver):
    driver.get(LEETCODE_CONTEST_PAGE_URL)
    wrapper = driver.find_element_by_class_name("swiper-wrapper")
    contest_divs = wrapper.find_elements_by_class_name("swiper-slide")
    
    contest_data = []
    for div in contest_divs:
        name = div.find_element_by_tag_name("span").text
        time = div.find_element_by_class_name("text-label-2").text
        url = div.find_element_by_tag_name('a').get_attribute("href")
        
        contest_data.append({
            "Contest Name" : name,
            "Timeline" : "Upcoming " + time,
            "Contest URL" : url
        })
        
    return contest_data
        
    
def get_Codeforces_data(driver):
    driver.get(CODEFORCES_CONTEST_PAGE_URL)
    table = driver.find_element_by_class_name("datatable")
    rows = table.find_elements_by_tag_name("tr")
    rows = rows[1:]
    
    contest_data = []
    for row in rows:
        columns = row.find_elements_by_tag_name("td")
        name = columns[0].text
        start = pd.to_datetime(columns[2].find_element_by_tag_name('a').text[:-7])
        date = start.strftime("%d %B,%Y")
        time = start.strftime("%I:%M %p")
        duration = str(int(columns[3].text[:-3])) + " hours"
        
        try:
            url = columns[5].find_element_by_tag_name('a').get_attribute("href")
        except:
            url = columns[5].text
            
        contest_data.append({
            "Contest Name" : name,
            "Contest URL" : url,
            "Date" : date,
            "Time" : time,
            "Duration" : duration,
        })
        
    return contest_data
    
    
def run_contest_scraper():
    print("Creating Web Driver")
    driver = get_driver()
    
    print("Fetching Codechef Contest Data")
    codechef_data = get_CodeChef_Data(driver)
    codechef_df = pd.DataFrame(codechef_data)
    
    print("Fetching Leetcode Contest Data")
    leetcode_data = get_LeetCode_Data(driver)
    leetcode_df = pd.DataFrame(leetcode_data)
    
    print("Fetching Codeforces Contest Data")
    codeforces_data = get_Codeforces_data(driver)
    codeforces_df = pd.DataFrame(codeforces_data)
    
    print("Saving the Data")
    with pd.ExcelWriter("Upcoming Contests.xlsx") as writer:
        codechef_df.to_excel(writer, sheet_name="CodeChef", index=False)
        leetcode_df.to_excel(writer, sheet_name="LeetCode", index=False)
        codeforces_df.to_excel(writer, sheet_name='Codeforces', index=False)
    
    
if __name__ == "__main__":
    run_contest_scraper()