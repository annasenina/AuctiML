# AuctiML
# Рекомендательный сервис по оценке открытых торгов по земельным участкам
Проект в рамках [ML System Design Autumn 23/24](https://ods.ai/tracks/ml-system-design-23/competitions/mlsys23-project)   
  
#### ML Design Doc
[ML Design Doc](systemdesign/design.md)

#### Проблематика
 Сайт https://torgi.gov.ru поззволяет участвовать в торгах всем желающим. Данная площадка активно используется инвесторами для приобретения ликвидных объектов.  
  
 Сейчас, для анализа торгов по объекту, пользователь должен вручную смотреть результаты прошлых торгов и руками анализировать, заявится ли кто-то на них, до какой цены доходили другие лоты.  
  
 Задача проекта научиться предсказывать результаты торгов по земельным участкам с сайта https://torgi.gov.ru/new/public/lots/reg  
   
 Итоговое решение должно обеспечить: 
  - предсказание результатов торгов:  состоялись, не состоялись - заявился один участник, не состоялись - не заявился никто.
  - предсказание финальной цены, за которую уйдет лот.   

#### Общее описание проекта
Система будет предсказывать результат торгов для новых лотов, которые только выставили на торги.    
Пользователь может использовать данные для принятия решения: участвовать или нет в торгах по этому лоту, а не анализировать каждый лот вручную.  
 

#### Общее описание решения
Предсказание результатов торгов по земельным участкам.


#### Архитектура решения
Решение состоит из:  
 - [Модель](model)   
 - [Backend (FastApi)](front)  
 - [Frontend (Telegram бот)](back)  
 

![arch](media/main_image1.png)

 
 
 
 
###### Установка 
 