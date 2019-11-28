#### TEST
#### Задача
##### Напишите код приложения для Django (Python 3), в котором у пользователей есть помимо основных полей 2 дополнительных: 
- [X] ИНН (может повторяться у разных пользователей, пользователей в системе может быть очень много) 
- [X] и счет (в рублях, с точностью до копеек).
 
##### [X] Также есть форма состоящая из полей (допускается использование REST API):

- Выпадающий список со всеми пользователями в системе, со счета которого нужно перевести деньги
- Поле для ввода ИНН пользователей, на счета  которых будут переведены деньги
- Поле для указания какую сумму нужно перевести с одного счета на другие
- [X] Необходимо проверять есть ли достаточная сумма у пользователя, со счета которого списываются средства, 
и есть ли пользователи с указанным ИНН в БД. При валидности введенных данных необходимо указанную сумму списать
 со счета указанного пользователя и перевести на счета пользователей с указанным ИНН в равных частях 
 (если переводится 60 рублей 10ти пользователям, то каждому попадет 6 рублей на счет).
- [X] Обязательно наличие unit-тестов.


#### Решение

- Скачать проект. 
- Поднять окружение
    ```bash
    $   virtualenv venv
    $   source ./venv/bin/activate 
    ```
- запустить 
    ```bash
    $   sh setup.sh
    ```
- интерфейс к переводам есть. Он находится по пути http://127.0.0.1:8000/users/<uuid>/transfer_money
    для каждого пользователя. 
    Также есть описание формата вызова при переходе с пустыми параметрами. 

#### Заметки
По поводу русских комментариев:
    Я считаю, что их лучше делать на родном языке. 
    В современных IDE есть автоматический перевод коменнтариев в коде.
    
#### TODO
- Дополнить тесты интеграционные
- Написать тесты производительности
- Завершить методы транзакций
