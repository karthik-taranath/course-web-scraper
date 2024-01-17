from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://app.testudo.umd.edu/soc/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

departmentDiv = soup.find_all("div", class_="course-prefix")

data = []
for department in departmentDiv[52:53]:
    a = department.a
    departmentUrl = url + a.get('href')
    print(f"url: {departmentUrl}")
    departmentResponse = requests.get(departmentUrl)
    print(f"response: {departmentResponse}")
    departmentSoup = BeautifulSoup(departmentResponse.text, "html.parser")

    departmentName = departmentSoup.find("span", class_="course-prefix-name").text.strip()
    print(departmentName)

    courseDivs = departmentSoup.find_all("div", class_="course")

    for courseDiv in courseDivs:
        dictionary = {
          "department": departmentName,
          "department_id": departmentName,
          "Code": courseDiv['id'],
          "Name": courseDiv.find("span", class_="course-title").text,
          "Credits": courseDiv.find("span", class_="course-min-credits").text
        }

        print(courseDiv['id'])
        data.append(dictionary)

df = pd.DataFrame(data)
df.to_csv('courses2.csv', index=False)
