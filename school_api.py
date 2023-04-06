from requests import get
from bs4 import BeautifulSoup, CData
import re

# input을 통해 입력받은 값
# main.py에 작성
school_info = {
    "office_of_education": "서울특별시교육청",
    "school": "가락고등학교",
}

# 기본값
school_meal_data = {
    "KEY": "9da752136d5849b985288deb5036dba1",
    "Type": "xml",
    # 아래는 다 완성되면 지우자
    # 'ATPT_OFCDC_SC_CODE': 'B10', 
    # 'SD_SCHUL_CODE': '7010057',
    # main에서 입력받을 값
    "MLSV_YMD": 202205
}

school_time_data = {
    "KEY": "9da752136d5849b985288deb5036dba1",
    "Type": "xml",
    # 아래는 다 완성되면 지우자
    # 'ATPT_OFCDC_SC_CODE': 'B10', 
    # 'SD_SCHUL_CODE': '7010057',
    # main에서 입력받을 값
    "AY": 2023,
    "SEM": 1,
    "ALL_TI_YMD": 202303
}

# 함수를 통해 받을 값을 저장하는 변수
school_url = {
    "base_url": "http://open.neis.go.kr/hub/",
    "basic_url": "schoolInfo",
    "meal_sub_url": "mealServiceDietInfo",
    "time_sub_url": "hisTimetable"
}

# 급식 데이터
school_meal = {}

# CData -> get_info = soup.find(text=lambda text: isinstance(text, CData))
# lambda 사용 : https://www.tomordonez.com/python-lambda-beautifulsoup/

# 배열 분할
def list_chunk(_list, n):
    return [_list[i:i+n] for i in range(0, len(_list), n)]

# 정규표현식
def regular_expression(_list) :

    global new_list

    new_list=[]

    for i in _list :
        text = re.sub('[a-zA-Z0-9.()]','',i).strip()
        if (text!="") :
            new_list.append(text)

    return new_list

# main.py로 부터 값을 받음
def get_info(**kwargs) :
    school_info.update(kwargs)
    # school_data({"MLSV_YMD": (변수명)})
    # print("school_info :", school_info)

# 교육청 코드 + 학교 코드
def get_data(self) :
    global get_office_of_education_code, get_school_code

    URL = school_url["base_url"] + school_url["basic_url"]
    
    response = get(f"{URL}?KEY={school_meal_data['KEY']}&Type={school_meal_data['Type']}")
    # response = get(URL, school_meal_data)

    if response.status_code != 200 :
        print("Can't request website")
        print("This response code is ", response.status_code)
    else :
        print("Sucess!")
        soup = BeautifulSoup(response.text, "html.parser")

        get_office_of_education = soup.find(text=school_info["office_of_education"])
        get_office_of_education_code = get_office_of_education.find_previous(text=lambda text: isinstance(text, CData))
        school_meal_data.update({"ATPT_OFCDC_SC_CODE": get_office_of_education_code})
        school_time_data.update({"ATPT_OFCDC_SC_CODE": get_office_of_education_code})

        get_school = soup.find(text=school_info["school"])
        get_school_code = get_school.find_previous(text=lambda text: isinstance(text, CData))
        school_meal_data.update({"SD_SCHUL_CODE": get_school_code})
        school_time_data.update({"SD_SCHUL_CODE": get_school_code})
        
    return self

# 급식 식단 정보
@get_data
def meal_service() :
    global meal_data, meal_list, meal_list_2, date_data, date_list

    URL = school_url["base_url"] + school_url["meal_sub_url"]

    response = get(URL, school_meal_data)

    if response.status_code != 200 :
        print("Can't request website")
        print("This response code is ", response.status_code)
    else :
        print("Sucess!")
        soup = BeautifulSoup(response.text, "html.parser")

        get_school_meal_date = soup.find_all("mlsv_ymd")

        _cnt = len(get_school_meal_date)
        date_data = [i for i in range(_cnt)]
        for i, info in enumerate(get_school_meal_date) :
            date_data[i] = info.find(text=lambda text: isinstance(text, CData))

        date_list = list_chunk(date_data, 1)

        get_school_meal_info = soup.find_all("ddish_nm")
       
        meal_data = [i for i in range(_cnt)]

        for i, info in enumerate(get_school_meal_info) :
            meal_data[i] = info.find(text=lambda text: isinstance(text, CData))

        meal_list = list_chunk(meal_data, 1)

        for i in range(_cnt) :
            meal_str = meal_list[i][0]
            meal_list_2 = meal_str.split("<br/>")
            meal_list_2 = regular_expression(meal_list_2)
            school_meal.update({"".join(date_list[i]): meal_list_2})
        
        return school_meal
       
# 고등학생 시간표 (준비중)
# @get_data
# def time_table(*args, **kwargs) :
    
# URL = school_url["base_url"] + school_url["time_sub_url"]
# response = get(URL, school_time_data)
# soup = BeautifulSoup(response.text,"html.parser")

# _perio = (soup.find("perio")).find(text=lambda text: isinstance(text, CData))
# _class = (soup.find("itrt_cntnt")).find(text=lambda text: isinstance(text, CData))
# _date = (soup.find("all_ti_ymd")).find(text=lambda text: isinstance(text, CData))
# # _date = ".".join(_date)
# _date = list(_date)
# _date.insert(4, ".")
# _date.insert(7, ".")
# _date.insert(10, ".")
# _date = "".join(_date)
# print(f"{_date}")
# print(f"{_perio}교시")
# print(f"{_class}")
