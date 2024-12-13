https://github.com/sanyochek58/ConverterInTOML


Задание:


Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки. Выходной текст на
языке toml попадает в файл, путь к которому задан ключом командной строки.


Многострочные комментарии:
#|
Это многострочный
комментарий
|#


Словари:
{
имя : значение;
имя : значение;
имя : значение;
...
}


Имена:
[a-z][a-z0-9_]*


Значения:
37
• Числа.
• Строки.
• Словари.


Строки:
@"Это строка"


Объявление константы на этапе трансляции:
имя := значение


Вычисление константного выражения на этапе трансляции (постфиксная
форма), пример:
?(имя 1 +)

Результатом вычисления константного выражения является значение.


Для константных вычислений определены операции и функции:
1. Сложение.
2. Вычитание.
3. Умножение.
4. Деление.
5. chr().
6. pow().


   
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.


Структура проекта:


input.txt - файл со скриптом конфигурационного языка


main.py - файл с главным скриптом перевода конфигурационного языка в язык TOML


test.py - файл с тестами 


output.toml - выходной файл конвертации в язык TOML



Тестирование:

<img width="330" alt="Снимок экрана 2024-12-13 в 13 38 50" src="https://github.com/user-attachments/assets/f87fbe6a-8ccf-405f-861e-c8221d952c93" />


<img width="707" alt="Снимок экрана 2024-12-13 в 13 39 29" src="https://github.com/user-attachments/assets/91abb3e1-577a-475e-bb91-250795afb9bb" />


<img width="1005" alt="Снимок экрана 2024-12-13 в 13 39 58" src="https://github.com/user-attachments/assets/4d856b6d-44fa-4dd9-aa86-8bdc156c6225" />


Пример конфигурационного языка


<img width="471" alt="Снимок экрана 2024-12-13 в 13 40 39" src="https://github.com/user-attachments/assets/0b4867b6-c6f9-4b61-87af-1d3d4d62a4ff" />


<img width="227" alt="Снимок экрана 2024-12-13 в 13 41 05" src="https://github.com/user-attachments/assets/504d7089-e41d-45b2-a4a5-50db29ba3bfe" />


<img width="694" alt="Снимок экрана 2024-12-13 в 13 41 46" src="https://github.com/user-attachments/assets/f7609e38-58f3-47b0-ad68-368cba23dce7" />





Выходной файл




<img width="575" alt="Снимок экрана 2024-12-12 в 22 20 14" src="https://github.com/user-attachments/assets/72e527e7-ab5d-4463-8835-80f08ea43b83" />

Выполнение тестов







