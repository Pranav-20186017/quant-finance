# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # import time
# # from selenium.webdriver.common.by import By
# # # Correct path to your ChromeDriver
# # chrome_driver_path = r'C:\\chrome\\chromedriver.exe'

# # # Set up Selenium WebDriver
# # service = Service(chrome_driver_path)
# # driver = webdriver.Chrome(service=service)

# # # URL to open
# # url = 'https://finance.yahoo.com/quote/BAC/holders?p=BAC'  # Replace with the URL you want to visit

# # # Open the URL
# # driver.get(url)

# # # Wait for 10 seconds to ensure the page is fully loaded
# # time.sleep(10)

# # # Find the element by XPath
# # xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/div[4]/table'
# # element =  driver.find_element(By.XPATH, xpath)

# # # Do something with the element, e.g., print its text
# # print(element.text)

# # # Close the browser
# # driver.quit()
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import time
# import pandas as pd

# # Set up Selenium WebDriver
# chrome_driver_path = r'C:\\chrome\\chromedriver.exe'
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service)

# # Open the URL
# url = 'https://finance.yahoo.com/quote/BAC/holders?p=BAC'
# driver.get(url)

# # Wait for 10 seconds to ensure the page is fully loaded
# time.sleep(10)

# # Find the element by XPath
# xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/div[4]/table'
# element = driver.find_element(By.XPATH, xpath)

# # Extract text from the element
# text = element.text

# # Close the browser
# driver.quit()

# # Process the text into a DataFrame
# lines = text.split('\n')
# headers = lines[0].split('\t')
# data = [line.split('\t') for line in lines[1:]]

# df = pd.DataFrame(data, columns=headers)

# # Print the DataFrame
# print(df)
# df.to_excel('mfhld.xlsx')




# # Open the URL
# url = 'https://finance.yahoo.com/quote/BAC/holders?p=BAC'
# driver.get(url)

# # Wait for 10 seconds to ensure the page is fully loaded
# time.sleep(10)

# # Find the element by XPath
# xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/div[3]/table'
# element = driver.find_element(By.XPATH, xpath)

# # Extract text from the element
# text = element.text

# # Close the browser
# driver.quit()

# # Process the text into a DataFrame
# lines = text.split('\n')
# headers = lines[0].split('\t')
# data = [line.split('\t') for line in lines[1:]]

# df = pd.DataFrame(data, columns=headers)

# # Print the DataFrame
# print(df)
# df.to_excel('inst.xlsx')



# # Open the URL
# url = 'https://finance.yahoo.com/quote/BAC/holders?p=BAC'
# driver.get(url)

# # Wait for 10 seconds to ensure the page is fully loaded
# time.sleep(10)

# # Find the element by XPath
# xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/div[2]/div/table'
# element = driver.find_element(By.XPATH, xpath)

# # Extract text from the element
# text = element.text

# # Close the browser
# driver.quit()

# # Process the text into a DataFrame
# lines = text.split('\n')
# headers = lines[0].split('\t')
# data = [line.split('\t') for line in lines[1:]]

# df = pd.DataFrame(data, columns=headers)

# # Print the DataFrame
# print(df)
# df.to_excel('top.xlsx')




from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Set up Selenium WebDriver
chrome_driver_path = r'C:\\chrome\\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the URL
url = 'https://finance.yahoo.com/quote/BAC/insider-transactions?p=BAC'
driver.get(url)

# Wait for 10 seconds to ensure the page is fully loaded
time.sleep(10)

# Find the element by XPath
xpath = '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/div[2]/table'
element = driver.find_element(By.XPATH, xpath)

# Extract text from the element
text = element.text

# Close the browser
driver.quit()

# Process the text into a DataFrame
lines = text.split('\n')
headers = lines[0].split('\t')
data = [line.split('\t') for line in lines[1:]]

df = pd.DataFrame(data, columns=headers)

# Print the DataFrame
print(df)
df.to_excel('insider-holding.xlsx')

