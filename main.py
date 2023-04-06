from flask import Flask, render_template
import school_api

if __name__ == "__main__" :
    
    school_info = {
        "office_of_education": "서울특별시교육청",
        "school": "가락고등학교"
    }

    school_api.get_info(**school_info)

    print(school_api.meal_service())

    # print(time_table())

    # input으로 값을 받으면 다음과 같은 형식으로 출력
    # 202005


#    나중에 작성



#     print(params["param"]["CODE"])

#     app = Flask("JobScrapper")

#     @app.route("/")
#     def main():
#         return render_template("home.html", name="J.Seo")

#     app.run("127.0.0.1")
