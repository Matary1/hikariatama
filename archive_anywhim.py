import telebot
import requests
import json

bot = telebot.TeleBot('<token>')
admins = [659800858]
types = telebot.types

main_markup = types.InlineKeyboardMarkup(row_width=2)
main_markup.add(
    types.InlineKeyboardButton("⌚️ Время работы", callback_data="time"),
    types.InlineKeyboardButton("📍 Адрес", callback_data="address"),
    types.InlineKeyboardButton("🛎 Заказать", callback_data="order"),
    types.InlineKeyboardButton("❓ Вопрос", callback_data="question"),
    types.InlineKeyboardButton("💶 Прайс-лист", callback_data="prices"),
    types.InlineKeyboardButton(
        "↪️ Заказать обратный звонок", callback_data="call")


)

db = dict()


prices_db = {
    'Ателье': {
        'Пошив': {
            'Брюки': [
                'Брюки женские: 2000',
                'Капри: 1500',
                'Комбинезон: 2500',
                'Шорты: 1500'
            ],
            'Юбка': [
                '"Мини": 1000',
                '"Солнце": 1500',
                'Модельная: 1700',
                'Сарафан: 2000',
                'Подклад: 500'
            ],
            'Платье': [
                'Платье: 2000',
                'Вечернее: 3000',
                'Свадебное: 6000'
            ],
            'Пиджак \\ Жилет': [
                'Пиджак на подкладе: 3000',
                'Пиджак без подклада: 2500',
                'Жакет на подкладе: 2500',
                'Жакет без подклада: 2200',
                'Жилет на подкладе: 1500',
                'Жилет без подклада: 1000'
            ],
            'Куртка \\ плащ': [
                'Куртка короткая без внутренних карманов: 3000',
                'Куртка короткая с внутренними карманами: 3500',
                'Куртка длинная без внутренних карманов: 3300',
                'Куртка длинная с внутренними карманами: 3800',
                'Плащ: 4000',
                'Плащ утепленный: 5000'
            ]
        },
        'Ремонт': {
            'Джинсы \\ брюки': {
                'Укоротить низ': [
                    'Обычное укорачивание: 250',
                    'Утепленные джинсы: 250',
                    'Евро подгиб: 300',
                    'Замена молнии на изделии: 350',
                    'Замена мешковины кармана: 350',
                    'Установка пуговиц 1 шт.: 70',
                    'Работа с поясом: 250',
                    'Мелкий ремонт: 50'
                ],
                'Подгон джинсов по фигуре': [
                    'Средний шов: 250',
                    'Средний шов + работа с поясом: 350',
                    'Боковой ,шаговый шов: 200',
                    'Боковой, шаговый шов с отделочной строчкой: 300',
                    'Восстановление пояса: 100',
                    'Восстановление низа: 100',
                    'Восстановление шлевки (1 шт): 50'
                ],
                'Устранение порыва': [
                    'Карман (с его отпарыванием) 1 угол: 250',
                    'Шлёвка (1 шт.): 150',
                    'Шлевка с открытием шва (1 шт.): 200',
                    'Двусторонняя штуковка среднего шва с открытием одного шва : 450',
                    'Двусторонняя штуковка среднего шва с открытием двух швов: 500',
                    'Односторонняя штуковка среднего шва с открытием одного шва: 300',
                    'Односторонняя штуковка среднего шва с открытием двух швов: 400',
                    'Порыв до 4 см: 200',
                    'Порыв от 4 см: 300',
                    'Декоративная штуковка с заплаткой: 250',
                    'Штукирование порыва под пуговицей : 50'
                ],
                'Брюки классические': [
                    'С тесьмой: 300',
                    'Без тесьмы : 200',
                    'С разрезами: 300',
                    'С молниями: 350',
                    'Замена молнии на изделии (без фурнитуры): 300',
                    'Работа с поясом: 200',
                    'Установка пуговиц (без фурнитуры) за 1 шт: 50',
                    'Установка крючка (без фурнитуры) за 1 шт: 200',
                    'Устранение порыва за 1 шт.: 100',
                    'Замена мешковины кармана за 1 шт.: 350'
                ],
                'Подгон брюк по фигуре': [
                    'Средний шов: 200',
                    'Средний шов + работа с поясом: 300',
                    'Боковой, шаговый шов (швы вразутюжку): 250',
                    'Боковой, шаговый шов (швы взаутюжку): 200',
                    'Боковой, шаговый шов с отделочной строчкой: 300',
                    'Восстановление пояса: 100',
                    'Восстановление низа (тесьмой): 200',
                    'Восстановление низа (без тесьмы): 100',
                    'Восстановление шлевки за 1 шт: 50'
                ]
            },
            'Юбка': {
                'Укоротить низ': [
                    'Прямая: 200',
                    'Прямая + подклад: 300',
                    'Со шлицей или разрезом: 250',
                    'Со шлицей +подклад: 350',
                    'Трикотажный шов: 300',
                    'Клёш: 300',
                    'Клёш + подклад: 350',
                    'роликовый: 300',
                    'Восстановление потайной строчки низа: 150',
                    'Проклейка низа (клейкой лентой): 150',
                    'Замена молнии (без фурнитуры): 300',
                    'Установка пуговиц (без фурнитуры) за 1 шт.: 30',
                    'Установка крючка (без фурнитуры): 100',
                    'Восстановление шва: 100',
                    'Ремонт шлицы, разреза: 150',
                    'Замена подклада: 600',
                    'Работа с поясом: 300'
                ],
                'Подгон по фигуре': [
                    'По боковым: 200',
                    'По боковым, работа с поясом : 150',
                    'По боковым, работа с низом: 100',
                    'По боковым с подкладом: 300',
                    'Изготовление выточки 1 шт.: 100',
                    'Изготовление выточки 1шт.+ подклад: 150',
                    'Закрепление шлёвки 1 шт.: 50',
                    'Мелкий ремонт: 100',
                    'Замена резинки (без фурнитуры): 200'
                ]
            },
            'Платье': {
                'Укоротить низ': [
                    'Прямой: 200',
                    'Прямой + подкладка: 300',
                    'Со шлицей или разрезом: 250',
                    'Со шлицей + подклад: 350',
                    'Трикотажный шов: 300',
                    'Клёш: 300',
                    'Клеш + подклад: 350',
                    'Роликовый: 300',
                    'Восстановление потайной строчки низа: 150'
                ],
                'Укоротить низ рукавов': [
                    'Текстиль: 250',
                    'Трикотажный шов: 250',
                    'С манжетом или разрезом: 300',
                    'Фигурный край: 300',
                    'Изменение линии горловины: 350',
                    'Изменение формы воротника: 350',
                    'Замена молнии (без фурнитуры): 800',
                    'Изменение фасона рукава: 500'
                ]
            },
            'Пиджак \\ жакет \\ жилет': {
                'Ремонт': [
                    'Укоротить низ: 550',
                    'Шлица,фигурные борта: 100',
                    'Укоротить рукава: 350',
                    'Укоротить рукава со шлицей и пуговицами: 550',
                    'Изменение формы лацкана и воротника: 600'
                ],
                'Подгон по фигуре': [
                    'Боковые швы: 250',
                    'Боковые швы с подкладом: 400',
                    'Рельефы: 250',
                    'Рельефы с подкладом: 400',
                    'Перенос линии проймы без подклада: 700',
                    'Перенос линии проймы с подкладом: 800',
                    'Установка пуговиц (без фурнитуры) за 1 шт.	50',
                    'Замена мешковины кармана за 1 шт: 250',
                    'Сделать петлю: 100',
                    'Замена подклада (без материала): 1300',
                    'Мелкий ремонт: 100',
                    'Восстановление отделочной строчки: 100',
                    'Замена молнии (без фурнитуры): 500'
                ]
            },
            'Куртка \\ пальто (на пуху)': {
                'Укоротить низ': [
                    'Закрытый: 1200',
                    'Со шлицей или усложняющим элементом: 1500'
                ],
                'Укоротить низ рукавов': [
                    'Убавление/прибавление по длине: 600',
                    'С манжетом,шлицей или патами: 700',
                    'С трикотажным манжетом: 700',
                    'Ушить рукав за пару: 700',
                    'Устранение порыва за 1 шт: 250',
                    'Восстановление отделочной строчки: 250',
                    'Ремонт кармана за 1 шт: 300',
                    'Восстановление внутреннего шва: 200'
                ],
                'Подгон по боковым швам': [
                    'короткое: 700',
                    'среднее: 1000',
                    'длинное: 1300',
                    'По пройме: 1300'
                ],
                'Подгон по рельефам': [
                    'короткое: 700',
                    'среднее: 1000',
                    'Длинное (с отделочной строчкой +20% от стоимости): 1300',
                    'Изготовление воротника: 1500',
                    'Ремонт воротника: 500'
                ],
                'Замена подкладочной ткани': [
                    'короткий: 1400',
                    'средний: 1600',
                    'длинный: 1900',
                    'Мешковина кармана за 1 шт: 300'
                ],
                'Замена молнии': [
                    'Короткая до 50 см: 600',
                    'Средняя от 50 до 60 см: 700',
                    'Длинная от 65 см: 800',
                    'Кант, подгонка рисунка или строчки, усложняющие элементы: 100',
                    'Установка кнопки 1 шт.(без фурнитуры): 70',
                    'Установка пуговиц 1 шт.(без фурнитуры): 70',
                    'Установка беггунка 1 шт. (без фурнитуры): 100',
                    'Установка аппликации 1 шт.(без фурнитуры): 200',
                    'Изготовление «петля-вешалка» 1 шт.: 200'
                ]
            },
            'Куртка, пальто (на синтепоне)': {
                'Укоротить низ': [
                    'Закрытый: 1000',
                    'Со шлицей или разрезом: 1200',
                    'Со отлетной подкладкой: 1200'
                ],
                'Укоротить низ рукавов': [
                    'Убавление/прибавление по длине: 500',
                    'С манжетом,шлицей или патами: 600',
                    'С трикотажным манжетом: 600',
                    'Ушить рукав за пару: 600',
                    'Устранение порыва за 1 шт: 200',
                    'Восстановление отделочной строчки: 250',
                    'Ремонт кармана за 1 шт: 250',
                    'Восстановление внутреннего шва: 200'
                ],
                'Подгон по боковым швам': [
                    'короткое: 700',
                    'среднее: 1000',
                    'длинное: 1300',
                    'По пройме: 1300'
                ],
                'Подгон по рельефам': [
                    'короткое: 600',
                    'среднее: 800',
                    'Длинное (с отделочной строчкой +20% от стоимости): 1000',
                    'Изготовление воротника: 1300',
                    'Ремонт воротника: 500',
                    'Изготовление капюшона: 1500'
                ],
                'Замена подкладочной ткани': [
                    'короткий: 1300',
                    'короткий со шлицей: 1500',
                    'средний: 1700',
                    'Шлица или разрез 1 шт.: 250',
                    'Мешковина кармана за 1 шт: 250'
                ],
                'Замена молнии': [
                    'Короткая до 50 см: 500',
                    'Средняя от 50 до 60 см: 600',
                    'Длинная от 65 см: 700',
                    'Кант, подгонка рисунка или строчки, усложняющие элементы: 100',
                    'Установка кнопки 1 шт.(без фурнитуры): 70',
                    'Установка пуговиц 1 шт.(без фурнитуры): 70',
                    'Установка беггунка 1 шт. (без фурнитуры): 100',
                    'Установка аппликации 1 шт.(без фурнитуры): 200',
                    'Изготовление «петля-вешалка» 1 шт.: 200'
                ]

            },
            'Куртка на тонком подкладе, плащ': {
                'Укоротить низ': [
                    'Закрытый: 1000',
                    'Со шлицей или разрезом: 1200',
                    'Со отлетной подкладкой: 1200'
                ],
                'Укоротить низ рукавов': [
                    'Убавление/прибавление по длине: 500',
                    'С манжетом,шлицей или патами: 600',
                    'С трикотажным манжетом: 600',
                    'Ушить рукава : 500',
                    'Устранение порыва за 1 шт: 150',
                    'Восстановление отделочной строчки: 250',
                    'Ремонт кармана за 1 шт: 250',
                    'Восстановление внутреннего шва: 200'
                ],
                'Подгон по боковым швам': [
                    'короткое: 500',
                    'среднее: 700',
                    'длинное: 900',
                    'По пройме: 900'
                ],
                'Подгон по рельефам': [
                    'короткое: 500',
                    'среднее: 700',
                    'Длинное (с отделочной строчкой +20% от стоимости): 900',
                    'Изготовление воротника: 1200',
                    'Ремонт воротника: 500',
                    'Изготовление капюшона: 1400'
                ],
                'Замена подкладочной ткани': [
                    'короткий: 1300',
                    'средний: 1500',
                    'длинный: 1700',
                    'Резинки-кулиски: 3500',
                    'Шлица или разрез 1 шт.: 250',
                    'Мешковина кармана за 1 шт: 250'
                ],
                'Замена молнии': [
                    'Короткая до 50 см: 500',
                    'Средняя от 50 до 60 см: 600',
                    'Длинная от 65 см: 700',
                    'Кант, подгонка рисунка или строчки, усложняющие элементы: 100',
                    'Установка кнопки 1 шт.(без фурнитуры): 70',
                    'Установка пуговиц 1 шт.(без фурнитуры): 70',
                    'Установка бегунка 1 шт. (без фурнитуры): 100',
                    'Установка аппликации 1 шт.(без фурнитуры): 150',
                    'Изготовление «петли-вешалка» 1 шт.: 200',
                    'Изготовить пояс: 300',
                    'Изготовление шлёвки 1 шт.: 50'
                ]
            },
            'Комбинезон лыжный': {
                'Укоротить низ': [
                    'Убавление/прибавление по длине: 400',
                    'С молнией: 500',
                    'Дополнительный подклад: 200'
                ],
                'Замена молнии': [
                    'брюки: 400',
                    'комбинезон: 450',
                    'Восстановление шва 1 шт.: 100',
                    'Установка аппликации 1 шт. : 200',
                    'Установка пуговиц 1 шт.: 50'
                ],
                'Подгон по боковым швам': [
                    'Без отделочной строки: 400',
                    'С отделочной строчкой: 500',
                    'По среднему шву: 400',
                    'Работа с поясом: 350'
                ]
            },
            'Брюки спортивные': {
                'Укоротить низ': [
                    'Укоротить низ изделия: 250',
                    'С подкладом: 350',
                    'С молнией: 350',
                    'Молния +подклад:  450',
                    'С переносом молнии: 700',
                    'С манжетом: 300',
                    'Манжет + резинка: 350'
                ],
                'Замена резинки на поясе': [
                    'Резинка ширина 1 см (без фурнитуры): 250',
                    'Резинка шириной 3 см (без фурнитуры): 350',
                    'Работа с поясом: 250',
                    'Замена мешковины кармана 1 шт.: 200',
                    'Замена молнии на изделии (без фурнитуры): 350'
                ],
                'Подгон по фигуре': [
                    'По боковым швам: 250',
                    'По боковым швам + подклад: 350',
                    'По среднему шву: 300',
                    'По среднему шву+подклад: 350',
                    'Установка люверса 1 шт.(без фурнитуры): 50',
                    'Мелкий ремонт: 100',
                    'Установка бегунка (без фурнитуры): 150'
                ]
            }
        }
    },
    'Химчистка': {
        'Дубленки': [
            'Дубленка-куртк: 2200',
            'Дубленка средней длины: 2480',
            'Дубленка длинная: 2750'
        ],
        'Замша и крек': [
            'Жакет, пиджак, куртка: 1380',
            'Плащ: 1550',
            'Брюки, рубашка, сарафан: 840',
            'Шорты,  трикотажный жилет с замшевыми вставками: 600',
            'Перчатки, головные уборы: 600',
            'Жилет, юбка из замши, шорты, трикотажный жилет с замшевыми вставками: 650'
        ],
        'Кожа': [
            'Пальто, полупальто: 1450',
            'Пальто, полупальто (на утепленном подкладе): 1530',
            'Плащ (на натуральном меху): 2200',
            'Куртка короткая (на подкладе): 1610',
            'Куртка средняя (на подкладе): 1740',
            'Куртка короткая (на натуральном меху): 2100',
            'Куртка средняя (на натуральном меху): 2400',
            'Куртка из кожи (на утепленном подкладе): 1450',
            'Пуховик кожаный: 1450',
            'Жакет, пиджак, короткий/длинный: 1390',
            'Жилет короткий: 850',
            'Жилет длинный: 950',
            'Брюки, рубашка, сарафан из кожи: 900',
            'Юбка, короткая: 1050',
            'Юбка, длинная: 1100',
            'Шорты, жилет, юбка, трикотажный жилет с кожаными вставками: 600',
            'Перчатки, кепка, шапка: 450'
        ],
        'Жилеты (Пушнина \\ Овчина)': [
            'Жилет короткий: 9580',
            'Жилет средней длины: 12700',
            'Жилет длинный: 15820'
        ],
        'Шуба (Пушнина \\ Овчина)': [
            'Полушубок (мутон): 4690',
            'Шуба (мутон): 430',
            'Жилет (мутон): 4530',
            'Полушубок автоледи: 5920',
            'Полушубок стрижка (щипка) автоледи: 6820',
            'Шуба средней длины: 6525',
            'Шуба стрижка (щипка) средней длин: 7475',
            'Шуба длинная: 6950',
            'Шуба стрижка (щипка) длинная: 7910',
            'Жилет пушнина: 5490',
            'Жилет пушнина стрижка (щипка): 6420'
        ],
        'Дубленка': [
            'Дубленка короткая: 6200',
            'Дубленка средней длины: 6700',
            'Дубленка длинная: 7170'
        ],
        'Химчистка в перхлорэтилене': [
            'Шуба (мутон): 1430',
            'Полушубок (мутон): 1100',
            'Шуба (норка, песец, енот, лиса, кролик-шиншилла и т.п): 2530',
            'Шуба стрижка или щипка (норка, бобер, кролик-шиншилла, лиса, песец, енот и т.д): 3490',
            'Полушубок (норка, песец, енот, лиса, кролик и т.п. ) средней длины (по колено): 2310',
            'Полушубок стрижка или щипка (норка, песец, енот, лиса, кролик-шиншилла и т.п) средней длины (по колено): 3260',
            'Полушубок стрижка или щипка (норка, бобер, кролик и т.д) автоледи: 2820',
            'Полушубок (норка, песец, енот, лиса, кролик и т.п. ) автоледи: 1920',
            'Куртка тканевая на натуральном меху (короткая/средняя): 880 / 990',
            'Жилет (мутон): 940',
            'Жилет (кролик, каракуль, норка, песец, енот, лиса и т.д): 1490',
            'Жилет стрижка или щипка (норка, песец, енот, лиса, кролик-шиншилла и т.д): 2420',
            'Шапка меховая, воротник + манжеты искусст./натур. мех: 200 / 450',
            'Подстежка из искусственного меха: 390',
            'Подстежка из натурального меха: 740',
            'Коврики из искусственного меха: 280',
            'Коврики из натурального меха: 520'
        ],
        'Изделия из искусственного меха': [
            'Жилет из искусственного меха: 700',
            'Полушубок из искусственного меха: 880',
            'Шуба, дубленка из искусственного меха: 1050'
        ],
        'Костюмы, платья, куртки, пальто': [
            'Пиджак, жакет: 480',
            'Брюки: 350',
            'Джинсы: 320',
            'Брюки тренировочные: 200',
            'Костюм (двойка): 800',
            'Китель (пиджак): 520',
            'Рубашка, блузка: 280',
            'Топ, майка, футболка: 200',
            'Юбка простого покроя: 290',
            'Юбка сложная (складки, плиссе): 380',
            'Платье, сарафан простого покроя: 450',
            'Платье сложного покроя (воланы, плиссе, складки): 580',
            'Вечернее платье: 1100',
            'Свитер, джемпер, пуловер: 310',
            'Костюм спортивный: 450',
            'Жилет, шорты: 210',
            'Комбинезон летний: 440',
            'Комбинезон демисезонный (утепленный): 580',
            'Берет, кепка, шапка (тканевые): 210',
            'Платок, шарф (до 1 кв.м/более 1 кв.м): 210',
            'Галстук: 180',
            'Куртка-ветровка, джинсовая куртка: 500',
            'Куртка-парка: 750',
            'Куртка на искусственном меху короткая/средняя: 720 / 760',
            'Полупальто демисезонное, плащ, пальто летнее: 670',
            'Пальто / Полупальто зимнее: 900 / 780',
            'Пальто демисезонное, плащ на утепленной подкладке: 780',
            'Жилет на синтепоне / пуховой: 380 / 580',
            'Подстежка тканевая: 260',
            'Меховой воротник, манжеты искусст / натурал: 180 / 380'
        ],
        'Пуховики': [
            'Куртка на синтепоне; куртка, жакет драповый: 690',
            'Пальто на синтепоне: 770',
            'Пуховик короткий/средний: 810 / 870',
            'Пуховик длинный: 960',
            'Пуховик двусторонний: 1050',
            'Пальто/полупальто зимнее (на пуху): 1030 / 920',
            'Горнолыжный костюм: 1200'
        ],
        'Чехлы': [
            'Чехлы автомобильные (тканевые) передние / задние (за каждое): 350 / 610',
            'Чехлы автомобильные из искусств. меха передние / задние (за каждое): 450 / 720',
            'Чехлы автомобильные из натур. меха передние / задние (за каждое): 590 / 1030',
            'Чехлы на подушки (гобелен): 200',
            'Чехлы (тканевые) кресло / диван: 450 / 970',
            'Чехлы на синтепоне кресло / диван: 750 / 1330'
        ],
        'Шторы, одеяла, скатерти, покрывала': [
            'Тюли прямые/ двойные (1м2): 100 / 130',
            'Шторы прямые (1м2): 130',
            'Шторы фасонные (1м2)/Двойные: 140 / 160',
            'Скатерть, 1м2: 190',
            'Покрывало п/спальное: 500',
            'Покрывало двуспальное/ евро: 560 / 610',
            'Одеяло п/спальное на синтепоне: 550',
            'Одеяло двуспальное/евро на синтепоне: 630',
            'Одеяло п/спальное пуховое, шерстяное, плед: 630',
            'Одеяло двуспальное/евро пуховое, шерстяное, плед: 700'
        ],
        'Пуховики до 36 размера': [
            'Пуховик: 400',
            'Комбинезон демисезонный (утепленный): 300',
            'Горнолыжный костюм (сплошной): 600',
            'Куртка на синтепоне: 350'
        ]
    }
}


def show_me_de_wae(string):
    iters = string[7:].split("_")
    db = prices_db
    wae = ""
    for iteration in iters:
        wae += list(db.items())[int(iteration)][0] + " -> "
        db = db[list(db.items())[int(iteration)][0]]
    return wae


def order_handle_first(message):
    if not str(message.chat.id) in db:
        bot.send_message(
            message.chat.id, "Извините. Произошел технический сбой, который привел к прерыванию заказа. Пожалуйста, попробуйте снова!", reply_markup=main_markup)
        return
    if not 'answers' in db[str(message.chat.id)]:
        bot.send_message(
            message.chat.id, "Извините. Произошел технический сбой, который привел к прерыванию заказа. Пожалуйста, попробуйте снова!", reply_markup=main_markup)
        return
    db[str(message.chat.id)]['answers'].append(message.text)
    msg = bot.send_message(
        message.chat.id, "*Замечательно!* Теперь мне нужен номер телефона для связи.", parse_mode="Markdown")
    bot.register_next_step_handler(msg, order_handle_second)


def order_step_atelie_final(message):
    db[str(message.from_user.id)]['answers'].append(message.text)
    params = ""
    for answ in db[str(message.from_user.id)]['answers']:
        params += "    _" + answ + "_\n"
    for admin in admins:
        bot.send_message(admin, "*Заказ:* \n" + params, parse_mode="Markdown")
    bot.send_message(chat_id=message.chat.id, text="*Ваша заявка принята! Скоро с вами свяжется наш менеджер!*",
                     parse_mode="Markdown", reply_markup=main_markup)


def order_handle_second(message):
    if not str(message.chat.id) in db:
        bot.send_message(
            message.chat.id, "Извините. Произошел технический сбой, который привел к прерыванию заказа. Пожалуйста, попробуйте снова!", reply_markup=main_markup)
        return
    if not 'answers' in db[str(message.chat.id)]:
        bot.send_message(
            message.chat.id, "Извините. Произошел технический сбой, который привел к прерыванию заказа. Пожалуйста, попробуйте снова!", reply_markup=main_markup)
        return
    db[str(message.chat.id)]['answers'].append(message.text)
    mark_2 = types.InlineKeyboardMarkup(row_width=2)
    mark_2.add(types.InlineKeyboardButton("✂️ Ателье", callback_data="order_step_3_Ателье"),
               types.InlineKeyboardButton("🧽 Химчистка", callback_data="order_step_3_Химчистка"))
    bot.send_message(message.chat.id, "*Прелестно!* Какой тип заказа вас интересует?",
                     reply_markup=mark_2, parse_mode="Markdown")


def get_table(sheet="price"):
    try:
        return json.loads(requests.get("https://sheets.googleapis.com/v4/spreadsheets/<sheet-id>/values/'" + sheet + "'!A1:Z500?key=<service-key>").text)['values']
    except:
        print(json.loads(requests.get("https://sheets.googleapis.com/v4/spreadsheets/<sheet-id>/values/'" +
                                      sheet + "'!A1:Z500?key=<service-key>").text))
        return []


@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_message(message.chat.id, "*Привет! 👋* Я - бот-помощник ателье \"Любой Каприз\". Я могу помочь тебе найти необходимую информацию, или же принять заказ\\вопрос. Что тебе нужно?",
                     reply_markup=main_markup, parse_mode="Markdown", reply_to_message_id=message.message_id)


def error(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Извините. Произошел технический сбой, который привел к прерыванию заказа. Пожалуйста, попробуйте снова!", reply_markup=main_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global db
    if call.data == "time":
        msg = "🕖 *Ателье \"Любой Каприз\" работает по следующему распорядку:*\n\n"
        time_arr = get_table("work_time")
        for row in time_arr:
            msg += "    *" + row[0] + "*: _" + row[1] + "_\n"
        if call.message.chat.id < 0:
            try:
                bot.send_message(call.from_user.id, msg,
                                 parse_mode="Markdown", reply_markup=main_markup)
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, я отправил информацию вам в личные сообщения", parse_mode="Markdown")
            except:
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, запросите это в личных сообщениях с ботом", parse_mode="Markdown")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=msg, parse_mode="Markdown", reply_markup=main_markup)
    elif call.data == "address":
        msg = "*Мы находимся по следующим адресам:*\n_   📍 г. Казань, ул. Азата Аббасова, д. 10\n   📍 г. Казань, ул. Татарстан, д. 9_"
        if call.message.chat.id < 0:
            try:
                bot.send_location(chat_id=call.from_user.id,
                                  latitude=55.779377, longitude=49.112673)
                bot.send_location(chat_id=call.from_user.id,
                                  latitude=55.7925002, longitude=49.2451939)
                bot.send_message(call.from_user.id, msg,
                                 parse_mode="Markdown", reply_markup=main_markup)
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, я отправил информацию вам в личные сообщения", parse_mode="Markdown")
            except:
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, запросите это в личных сообщениях с ботом", parse_mode="Markdown")
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_location(chat_id=call.from_user.id,
                              latitude=55.779377, longitude=49.112673)
            bot.send_location(chat_id=call.from_user.id,
                              latitude=55.7925002, longitude=49.2451939)
            bot.send_message(call.from_user.id, msg,
                             parse_mode="Markdown", reply_markup=main_markup)
    elif call.data == "order":
        if call.message.chat.id < 0:
            bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                             "*, чтобы совершить заказ, напишите в личные сообщения боту.")
        else:
            db[str(call.from_user.id)] = dict()
            db[str(call.from_user.id)]['answers'] = []
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="*Давайте начнем!* Для начала, отправьте мне свое ФИО.", parse_mode="Markdown")
            bot.register_next_step_handler(msg, order_handle_first)

    elif call.data.startswith("order_step_3_"):
        if not str(call.from_user.id) in db:
            error(call)
            return
        if not 'answers' in db[str(call.from_user.id)]:
            error(call)
            return

        s = call.data[13:]
        db[str(call.from_user.id)]['answers'].append(s)
        if s == "Ателье":
            mark_3 = types.InlineKeyboardMarkup(row_width=2)
            mark_3.add(types.InlineKeyboardButton("🛠 Ремонт", callback_data="order_step_atelie_1_Ремонт"),
                       types.InlineKeyboardButton("➿ Пошив", callback_data="order_step_atelie_1_Пошив"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="*Продолжим.* Выберите, что вам требуется:", reply_markup=mark_3, parse_mode="Markdown")
        else:
            mark_3 = types.InlineKeyboardMarkup(row_width=2)
            prices = get_table("prices")
            for price in prices[1:]:
                if price[0].startswith('Химчистка'):
                    mark_3.add(
                        types.InlineKeyboardButton(
                            price[0][11:], callback_data="order_step_chem_1_" + price[0][11:])
                    )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="*Продолжим.* Что вам нужно почистить?", reply_markup=mark_3, parse_mode="Markdown")

    elif call.data.startswith("order_step_atelie_1_"):
        if not str(call.from_user.id) in db:
            error(call)
            return
        if not 'answers' in db[str(call.from_user.id)]:
            error(call)
            return

        s = call.data[20:]
        db[str(call.from_user.id)]['answers'].append(s)
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="*Почти все.* Опишите вашу проблему одним сообщением.", parse_mode="Markdown")
        bot.register_next_step_handler(msg, order_step_atelie_final)
    elif call.data.startswith("order_step_chem_1_"):
        if not str(call.from_user.id) in db:
            error(call)
            return
        if not 'answers' in db[str(call.from_user.id)]:
            error(call)
            return

        s = call.data[18:]
        db[str(call.from_user.id)]['answers'].append(s)
        params = ""
        for answ in db[str(call.from_user.id)]['answers']:
            params += "    _" + answ + "_\n"
        for admin in admins:
            bot.send_message(admin, "*Заказ:* \n" +
                             params, parse_mode="Markdown")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="*Ваша заявка принята! Скоро с вами свяжется наш менеджер!*", parse_mode="Markdown", reply_markup=main_markup)
    elif call.data == "question":
        msg = "*Задайте ваш вопрос прямо здесь. Я передам его администраторам!*"
        if call.message.chat.id < 0:
            try:
                kkk = bot.send_message(
                    call.from_user.id, msg, parse_mode="Markdown")
                bot.register_next_step_handler(kkk, handle_question)
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, я отправил информацию вам в личные сообщения", parse_mode="Markdown")
            except:
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, запросите это в личных сообщениях с ботом", parse_mode="Markdown")
        else:
            kkk = bot.edit_message_text(
                chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode="Markdown")
            bot.register_next_step_handler(kkk, handle_question)
    elif call.data == "prices":
        # prices = get_table("prices")
        res = "💶 *Прайс-лист*\n_Выберите категорию:_"
        # for row in prices:
        # 	if row[0] == "Позиция":
        # 		continue
        # 	res += "   💠_ " + row[0] + "_ : *" + str(row[1]) + " RUB*\n"
        mark_1 = types.InlineKeyboardMarkup(row_width=2)
        i = 0
        for key, value in list(prices_db.items()):
            mark_1.add(types.InlineKeyboardButton(
                key, callback_data="cprice_" + str(i)))
            i += 1
        mark_1.add(types.InlineKeyboardButton(
            "🏠 Главное меню", callback_data="home"))
        if call.message.chat.id < 0:
            try:
                bot.send_message(call.from_user.id, res,
                                 parse_mode="Markdown", reply_markup=mark_1)
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, я отправил информацию вам в личные сообщения", parse_mode="Markdown")
            except:
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, запросите это в личных сообщениях с ботом", parse_mode="Markdown")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=res, parse_mode="Markdown", reply_markup=mark_1)

    elif call.data.startswith("cprice_"):
        iterations = call.data.split("_")[1:]
        now_db = prices_db
        for iteration in iterations:
            # print(1)
            try:
                now_db = now_db[list(now_db.items())[int(iteration)][0]]
            except:
                print(iterations)
        mark_1 = types.InlineKeyboardMarkup(row_width=2)
        res = "💶 *Прайс-лист*\n" + \
            show_me_de_wae(call.data) + " \\_\n_Выберите категорию_"
        try:
            i = 0
            for key, value in list(now_db.items()):
                # print(call.data + "_" + key)
                mark_1.add(types.InlineKeyboardButton(
                    key, callback_data=call.data + "_" + str(i)))
                i += 1
        except AttributeError:
            res = "💶 *Прайс-лист*\n" + show_me_de_wae(call.data)
            for row in now_db:
                res += "\n   `" + row + " RUB`"

        mark_1.add(types.InlineKeyboardButton(
            "🏠 Главное меню", callback_data="home"))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=res, parse_mode="Markdown", reply_markup=mark_1)

        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=res, parse_mode="Markdown", reply_markup=main_markup)
    elif call.data == "call":
        msg = "*Отправьте мне ваш номер телефона, и я попрошу администраторов перезвонить вам.*"
        if call.message.chat.id < 0:
            try:
                kkk = bot.send_message(
                    call.from_user.id, msg, parse_mode="Markdown")
                bot.register_next_step_handler(kkk, handle_call)
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, я отправил информацию вам в личные сообщения", parse_mode="Markdown")
            except:
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, запросите это в личных сообщениях с ботом", parse_mode="Markdown")
        else:
            kkk = bot.edit_message_text(
                chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode="Markdown")
            bot.register_next_step_handler(kkk, handle_call)

    elif call.data == "home":
        msg = "Главная"
        if call.message.chat.id < 0:
            try:
                bot.send_message(call.from_user.id, msg,
                                 parse_mode="Markdown", reply_markup=main_markup)
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, я отправил информацию вам в личные сообщения", parse_mode="Markdown")
            except:
                bot.send_message(call.message.chat.id, "*" + call.from_user.first_name +
                                 "*, запросите это в личных сообщениях с ботом", parse_mode="Markdown")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=msg, parse_mode="Markdown", reply_markup=main_markup)


def handle_call(message):
    for admin in admins:
        bot.send_message(admin, "*" + message.from_user.first_name +
                         "*, запросил обратную связь по номеру:", parse_mode="Markdown")
        bot.forward_message(admin, from_chat_id=message.chat.id,
                            message_id=message.message_id)

    bot.send_message(message.chat.id, "*Я направил запрос администраторам 😌*",
                     parse_mode="Markdown", reply_markup=main_markup, reply_to_message_id=message.message_id)


def handle_question(message):
    for admin in admins:
        bot.forward_message(
            chat_id=admin, from_chat_id=message.chat.id, message_id=message.message_id)

    bot.send_message(message.chat.id, "*Ваш вопрос принят! Скоро с вами свяжутся.*",
                     parse_mode="Markdown", reply_markup=main_markup, reply_to_message_id=message.message_id)


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    first_name = message.new_chat_member.first_name if isinstance(
        message.new_chat_member.first_name, str) else "Annonymous"
    last_name = message.new_chat_member.last_name if isinstance(
        message.new_chat_member.last_name, str) else ""
    username = message.new_chat_member.username if isinstance(
        message.new_chat_member.username, str) else "username"
    chat_markup = types.InlineKeyboardMarkup(row_width=2)
    chat_markup.add(types.InlineKeyboardButton(
        "Ателье \"Любой Каприз\"", url="https://t.me/AnyWhim_Bot"))
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        print("sorry")
        # bot.send_message(message.chat.id, "Для того, чтобы полноценно приветствовать новых участников, а также модерировать чат, мне нужны права администратора с возможностью:\n   Ограничивать права пользователей\n   Удалять сообщения")
    s = bot.send_message(message.chat.id, "Привет, <b>{0}</b>!\nРады видеть тебя в нашем чате!".format(
        message.new_chat_member.first_name), parse_mode="HTML", reply_markup=chat_markup, disable_web_page_preview=True)
    # s.reply_to_message, 120)


bot.polling(none_stop=True, timeout=123)
