from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from ..models import Course
from webdriver_manager.chrome import ChromeDriverManager


def crwaling(rq_year, rq_semester):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get("https://wis.hufs.ac.kr/src08/jsp/lecture/LECTURE2020L.jsp")

    semester_trans = {'1' : '1', '2' : '3', '여름' : '2', '겨울' : '4'}
    
    year = driver.find_element_by_name('ag_ledg_year')
    year_obj = Select(year)
    year_obj.select_by_value('20' + rq_year)
    
    semester = driver.find_element_by_name('ag_ledg_sessn')
    semester_obj = Select(semester)
    semester_obj.select_by_value(semester_trans[rq_semester])


    dept_list = []
    dept_eles = driver.find_element_by_name('ag_crs_strct_cd')
    for i in dept_eles.find_elements_by_tag_name('option'):
        dept_list.append(i.text.strip()[6:].split('(')[0].strip())

    dept_eles = Select(dept_eles)

    for k in range(len(dept_list)):
        dept_eles.select_by_index(k)

        dept_eles = driver.find_element_by_name('ag_crs_strct_cd')
        dept_eles = Select(dept_eles)

        html = bs(driver.page_source, 'html.parser')

        tbody = html.findAll('tbody')
        trs = tbody[-1].findAll('tr')[1:]

        for i in trs:
            tds = i.findAll('td')
            year = int(tds[2].get_text().strip())
            subject = tds[4].get_text().strip().splitlines()
            subject = " ".join(subject)
            try:
                syllabus = tds[5].find('a')['href'].split('\'')
                ag_1 = syllabus[1]
                ag_2 = syllabus[3]
                ag_3 = syllabus[5]
                ag_4 = syllabus[7]
                syllabus = "https://wis.hufs.ac.kr/src08/jsp/lecture/syllabus.jsp?mode=print&ledg_year=" \
                            +str(ag_1)+"&ledg_sessn="+str(ag_2)+"&org_sect="+str(ag_3)+"&lssn_cd="+str(ag_4)
            except:
                syllabus = 'None'

            prof = tds[11].get_text().strip().split('(')[0].strip()
            if len(prof) == 0:
                continue
            credit = int(tds[12].get_text().strip())
            try:
                Course(year=year, name=subject, syllabus=syllabus, prof=prof, credit=credit, dept=dept_list[k]).save()
            except Exception as err:
                print(err)
                print(subject, prof)

    driver.close()


