import datetime
from bs4 import BeautifulSoup
import requests
import re

class Schedule:
    def __init__(self, day_pairs: dict[str, list[str]], url: str, text: list[str], search_ids: list[str]) -> None:
        self.pattern = r"^(Пн|Вт|Ср|Чт|Пт|Сб|Нд)"
        self.url = url
        self.text = text
        self.day_pairs = day_pairs
        self.search_ids = search_ids
    
    def get_schedule(self, url):
        response = requests.get(url)
        html = response.text

        self.text = []
        for day in self.day_pairs:
            self.day_pairs[day] = []

        soup = BeautifulSoup(html, 'html.parser')
        schedule_elements = soup.find_all('div', class_="views-row")
        for schedule_element in schedule_elements:
            day = schedule_element.find_previous('span', class_='view-grouping-header').text
            lessons_elements = schedule_element.find_all(lambda tag: tag.has_attr('id'))
            if lessons_elements:
                for lesson_element in lessons_elements:
                    lesson_content = lesson_element.find_all('div', class_='group_content')

                    lesson_number_element = lesson_element.find_previous('h3')
                    lesson_number = lesson_number_element.text if lesson_number_element else "Номер пари не знайдено"

                    lesson_info = lesson_content[0].text.strip()

                    status_text = self.get_lesson_status(lesson_element)

                    self.text.append(f'{day}: Пара {lesson_number} {status_text} - {lesson_info}')

        self.process_schedule()
        self.print_schedule()
        print(self.day_pairs)
        
    def get_lesson_status(self, lesson_element) -> str:
        lesson_id = lesson_element.get('id')
        if lesson_id == 'group_chys':
            return '(чисельник)'
        elif lesson_id == 'group_znam':
            return '(знаменник)'
        elif lesson_id == "sub_1_znam":
            return '(перша група знаменник)'
        elif lesson_id == "sub_2_znam":
            return '(друга група знаменник)'
        elif lesson_id == "sub_1_chys":
            return '(перша група чисельник)'
        elif lesson_id == "sub_2_chys":
            return '(друга група чисельник)'
        elif lesson_id == "sub_2_full":
            return '(друга група)'
        elif lesson_id == "sub_1_full":
            return '(перша група)'
        else:
            return ''

    def process_schedule(self):
        for lesson in self.text:
            match = re.search(self.pattern, lesson)
            if match:
                day = match.group(1)
                if day in self.day_pairs:
                    self.day_pairs[day].append(self.clean_lesson(lesson))



    def clean_lesson(self, lesson):
        replacements = {
            "Пн: ": " ",
            "Вт: ": " ",
            "Ср: ": " ",
            "Чт: ": " ",
            "Пт: ": " ",
            "Сб: ": " ",
            "Нд: ": " ",
        }
        for old, new in replacements.items():
            lesson = lesson.replace(old, new)
        return lesson

 
    def print_schedule(self):
        for day, lessons in self.day_pairs.items():
            if lessons:
                print(day)
                for lesson in lessons:
                   print(lesson)
                   return lesson
                
