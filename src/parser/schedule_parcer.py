from bs4 import BeautifulSoup
import requests

urls = [ 'https://student2023.lpnu.ua/students_schedule?studygroup_abbrname=%D0%BA%D0%B1-105&semestr=1&semestrduration=1',
]

def get_schedule(url):
    response = requests.get(url)
    html = response.text

    # Створення об'єкта BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Знаходимо всі елементи з розкладом
    schedule_elements = soup.find_all('div', class_='stud_schedule')

    # Ітеруємося через елементи розкладу та отримуємо інформацію
    for schedule_element in schedule_elements:
        day = schedule_element.find_previous('span', class_='view-grouping-header').text
        lesson_element = schedule_element.find('div', class_='group_content')

        # Отримуємо номер пари
        lesson_number_element = lesson_element.find_previous('h3')
        lesson_number = lesson_number_element.text if lesson_number_element else "Номер пари не знайдено"

        # Отримуємо інформацію про пару
        lesson_info = lesson_element.text.strip()

        # Отримуємо статус тижня з функції get_week_status
        status_text = get_lesson_status(schedule_element)

        # Виводимо інформацію
        print(f'{day}: Пара {lesson_number} {status_text} - {lesson_info}')

def get_lesson_status(lesson_element): 
    if lesson_element.find('div', id='group_chys'):
        return '(чисельник)'
     
    elif lesson_element.find('div', id='group_znam'):
        return '(знаменник)'
    elif lesson_element.find('div',id="sub_1_znam"):
        return '(перша група знаменник)'
    elif lesson_element.find('div',id="sub_2_znam"):
                return '(друга група знаменник)'
    elif lesson_element.find('div',id="sub_1_chys"):
                 return '(перша група чисельник)'
    elif lesson_element.find('div',id="sub_2_chys"):
                  return '(друга гарпа чисельник)'        
    else:
        return ''


if __name__ == '__main__':
    url = 'https://student2023.lpnu.ua/students_schedule?studygroup_abbrname=%D0%BA%D0%B1-105&semestr=1&semestrduration=1' 
    get_schedule(url)