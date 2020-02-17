import re, requests
from flask import current_app


def grab_tests():
    counter_of_questions = 0
    per = 0
    global_list = []
    links = []

    pattern_questions = r"<p class=\"questionContent\">[^<]+?</p><ul class=\"choiceList\">.+?</ul>"
    pattern_question = r"<p class=\"questionContent\">.+?</p>"
    pattern_answers = r"<ul class=\"choiceList\">.+?</ul>"
    pattern_answer = r"<li class=\".+?</li>"
    pattern_title = r"<title>(.+?)</title>"
    pattern_links = r'(?<=<a href=")[^"]*'
    pattern_valid_extensions = r'^.*\.(htm|html|php)$'

    if (current_app.config['TESTS_LINKS_PAGE_URL']):
        response = requests.get(current_app.config['TESTS_LINKS_PAGE_URL'])
        response.encoding = response.apparent_encoding
        links = re.findall(pattern_links, response.text)
    else:
        with open(current_app.config['LINKS_PATH'], "r") as file:
            links = file.read()
            links = links.split().replace(" ", "")

    for link in links:
        if not re.match(pattern_valid_extensions, link):
            continue
        link = current_app.config['TESTS_LINKS_PAGE_URL'] + link
        questions = []
        lst = []
        per += 1
        response = requests.get(link)
        response.encoding = response.apparent_encoding
        page_html = str(response.text).replace("\n\n", "").replace("\r\n", "").replace("&nbsp;", "").replace("<br>",
                                                                                                             "").replace(
            "&laquo;", "\"").replace("&raquo;", "\"").replace("&ndash;", " - ")
        list_of_questions = re.findall(pattern_questions, page_html)

        for question in list_of_questions:
            name_of_question = re.findall(pattern_question, question)
            name_of_question = name_of_question[0].replace("<p class=\"questionContent\">", "").replace("</p>", "")
            questions.append(name_of_question)
            answers = re.findall(pattern_answers, question)
            answers = answers[0].replace("<ul class=\"choiceList\">", "").replace("</ul>", "")
            list_of_answers = re.findall(pattern_answer, answers)
            for i in range(int(len(list_of_answers))):
                list_of_answers[i] = list_of_answers[i].replace("<li class=\"", "").replace("ncorrect choice\">",
                                                                                            "").replace(
                    "orrect choice\">", "").replace("</li>", "")
                if list_of_answers[i][0] == "i":
                    app = list_of_answers[i][1:]
                    list_of_answers[i] = []
                    list_of_answers[i].append(app)
                    list_of_answers[i].append(0)
                else:
                    app = list_of_answers[i][1:]
                    list_of_answers[i] = []
                    list_of_answers[i].append(app)
                    list_of_answers[i].append(1)
            dict_of_answers = dict(list_of_answers)
            lst.append(dict_of_answers)
        len_answers = int(len(lst))
        len_questions = int(len(questions))

        if not len_answers == len_questions:
            print("Произошла ошибка: количество вопросов не совпадает с количеством ответов!")
            print("Тесты с названием ")
            continue

        dictionary = dict.fromkeys(questions)

        for i in range(int(len(questions))):
            name_of_q = questions[i]
            dictionary[name_of_q] = lst[i]

        name_of_page = re.findall(pattern_title, page_html)

        vr_dict_for_title = {}

        vr_dict_for_title.setdefault("name", name_of_page[0])
        vr_dict_for_title.setdefault("url", link)
        vr_dict_for_title.setdefault("questions", dictionary)

        global_list.append(vr_dict_for_title)

        print("==================================")
        print("Загружено тестов " + str(per) + " из " + str(len(links)))
        print("Название тестов: " + str(name_of_page[0]))
        print("Количество вопросов: " + str(len_questions))
        print("==================================")

        counter_of_questions += len_questions

    print("\n\n\nВсего загружено вопросов: " + str(counter_of_questions))

    return global_list
