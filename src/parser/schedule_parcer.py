import datetime
from bs4 import BeautifulSoup
import requests
import re

class Schedule:
    def __init__(self,day_pairs: dict[str, list[str]], url: str, text: list[str]) -> None:
        self.pattern = r"^(Пн|Вт|Ср|Чт|Пт|Сб|Нд)"
        self.url = url
        self.text = text 
        self.day_pairs = day_pairs

    def get_schedule(self):
        response = requests.get(self.url)  # Виправлено тут, додано self.url
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        schedule_elements = soup.find_all('div', class_='stud_schedule')

        for schedule_element in schedule_elements:
            day = schedule_element.find_previous('span', class_='view-grouping-header').text
            lesson_element = schedule_element.find('div', class_='group_content')

            lesson_number_element = lesson_element.find_previous('h3')
            lesson_number = lesson_number_element.text if lesson_number_element else "Номер пари не знайдено"

            lesson_info = lesson_element.text.strip()

            status_text = self.get_lesson_status(lesson_element)  

            self.text.append((f'{day}: Пара {lesson_number} {status_text} - {lesson_info}'))

        print(self.text)  
        self.print_pairs()          

    def get_lesson_status(self, lesson_element):  
        if lesson_element.find('div', id='group_chys'):
            return '(чисельник)'
        elif lesson_element.find('div', id='group_znam'):
            return '(знаменник)'
        elif lesson_element.find('div', id="sub_1_znam"):
            return '(перша група знаменник)'
        elif lesson_element.find('div', id="sub_2_znam"):
            return '(друга група знаменник)'
        elif lesson_element.find('div', id="sub_1_chys"):
            return '(перша група чисельник)'
        elif lesson_element.find('div', id="sub_2_chys"):
            return '(друга гарпа чисельник)'
        else:
            return ''
    def check_match(self):
        for lesson in self.text:
            match = re.search(self.pattern, lesson)
            if match:
                day = match.group(1)
                if day in self.day_pairs:
                    self.day_pairs[day].append(f'{lesson}\n')
        return self.day_pairs
        
    def print_pairs(self):
        replacements = {
    "Пн: ": " ",
    "Вт: ": "",
    "Ср: ": " ",
    "Чт: ": " ",
    "Пт: ": " ",
    "Сб: ": " ",
    "Нд: ": " ",
}
        self.check_match()
        for day, lessons in self.day_pairs.items():
            if lessons:
                print(day)
                for lesson in lessons:
                    for old, new in replacements.items():
                        lesson = re.sub(rf'\b{old}\b', new, lesson)
                    print(lesson)