""" 'Интерфейс' (если быть точнее - жалкая ООП реплика на Python :) )
Сделана в основном, чтоб обозначить методы которыми должен обладать сторедж для хранения заявок.
Строгих требований к хранилищу нет. Данные хранение которых необходимо обеспечить и являются 
обязательными - это: 

 - id:[str,int]                 - order_id с биржи
 - state:[str]                  - order_state - с биржи: filled, open, reject и т.п.
 - instrument:str               - указывающий на инструмент ордера
 - group_id:[str]               - ID круппы ордера, вписывается в order.label на бирже
 - active:[int]                 - указывает на то, актуальный ли ордер или нет для бота 1 - да, 0 - нет
 - active_comment:[str]         - комментарий, в котором отмечается причина смены статуса active
 - real_create:[str:datetime]   - реальная дата создания объекта
 - operation:[str]              - направление операции bay или sell

Остальные параметры по желанию.
Порядок полей неважен.
Соотвественно обхекты, возвращаемые методами должны содержать указанный набор данных

Такой набор данных обеспечит синхронизацию с биржей после остановки.

Такой подход может обеспечить хранение данных где угодно.
"""

class IBotStore:

    def get(self, id = None, param = {}, order_by = {}):
        pass

    def insert(self, order, other_param, return_is_active = True, modify_active = True):
        pass

    def update(self, id, order, other_param, return_is_active = True, modify_active = True):
        pass