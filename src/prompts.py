from typing import Dict

def get_math_examples(lang: str) -> str:
    math_examples = {
        'en': """Question: Carol and Jennifer are sisters from Los Angeles who love collecting signatures from celebrities. During their summer break from school, the sisters spend every afternoon collecting signatures. After five weeks, Carol and Jennifer compare their autograph books, counting up the number of signatures each sister has collected. Carol has 20 signatures in her book, and Jennifer has 44. The sisters have three more weeks of summer vacation, and they decide they want to reach 100 signatures between them by the end of the summer. How many signatures do the sisters need to collect to reach their goal?
Steps: 1. How many signatures have Carol and Jennifer collected?
2. How many signatures do the sisters need to collect?
Answer: How many signatures have Carol and Jennifer collected? ** Carol and Jennifer have already collected 20 + 44 signatures = <<20+44=64>>64 signatures.
How many signatures do the sisters need to collect? ** Since their goal is 100, they need to collect 100 - 64 signatures. 100 - 64 = <<100-64=36>>36 signatures
#### 36
Exact Answer: 36

==================================================

Question: A team of 4 painters worked on a mansion for 3/8ths of a day every day for 3 weeks. How many hours of work did each painter put in?
Steps: 1. How many hours is 3/8ths of a day?
2. How many days are in 3 weeks?
3. How many hours did each painter put in?
Answer: How many hours is 3/8ths of a day? ** There are 24 hours in a day so 3/8ths of a day is (3/8)*24 = <<3/8*24=9>>9 hours
How many days are in 3 weeks? ** One week has 7 days so 3 weeks have 7*3 = <<7*3=21>>21 days
How many hours did each painter put in? ** Each painter put in 9*21 = <<9*21=189>>189 hours of work
#### 189
Exact Answer: 189

==================================================

Question: It costs $194 per meter to repave a street. Monica's street is 150 meters long. How much more does it cost to repave Lewis' street, which is 490 meters long?
Steps: 1. What is the total cost to repave Monica's street?
2. What is the total cost to repave Lewis' street?
3. How much more does it cost to repave Lewis' street?
Answer: What is the total cost to repave Monica's street? ** Total cost to repave Monica's street is 194*150 = <<194*150=29100>>29,100 dollars.
What is the total cost to repave Lewis' street? ** Total cost to repave Lewis' street is 194*490 = <<194*490=95060>>95,060.
How much more does it cost to repave Lewis' street? ** It costs 95,060-29,100 = <<95060-29100=65960>>65,960 more dollars to repave Lewis' street.
#### 65,960
Exact Answer: 65,960

==================================================""",
        'kk': """Сұрақ: Кэрол мен Дженнифер - Лос-Анджелестен келген әпкелі-сіңлілер, олар атақты адамдардың қолтаңбаларын жинағанды жақсы көреді. Мектептегі жазғы демалыс кезінде әпкелі-сіңлілер әр түстен кейін қолтаңбалар жинайды. Бес аптадан кейін Кэрол мен Дженнифер өздерінің қолтаңба кітаптарын салыстырып, әр қарындастың жинаған қолтаңбаларын санайды. Кэролдың кітабында 20 қолтаңба, ал Дженниферде 44 қолтаңба бар. Әпкелі-сіңлілердің жазғы демалысына тағы үш апта қалды және олар жаздың соңына дейін жалпы саны 100 қолтаңбаға жеткісі келеді. Мақсатқа жету үшін әпкелі-сіңлілер қанша қолтаңба жинауы керек?
Қадамдар: 1. Кэрол мен Дженнифер қанша қолтаңба жинады?
2. Әпкелі-сіңлілер қанша қолтаңба жинауы керек?
Жауап: Кэрол мен Дженнифер қанша қолтаңба жинады? ** Кэрол мен Дженнифер 20 + 44 қолтаңба = <<20+44=64>>64 қолтаңба жинады.
Әпкелі-сіңлілер қанша қолтаңба жинауы керек? ** Мақсаттары 100 болғандықтан, олар 100 - 64 қолтаңба жинауы керек. 100 - 64 = <<100-64=36>>36 қолтаңба
#### 36
Нақты жауап: 36

==================================================

Сұрақ: 4 сырлаушыдан тұратын топ 3 апта бойы күн сайын күннің 3/8 бөлігін сарайды сырлауға жұмсады. Әр сырлаушы қанша сағат жұмыс істеді?
Қадамдар: 1. Күннің 3/8 бөлігі қанша сағат?
2. 3 аптада қанша күн бар?
3. Әр сырлаушы қанша сағат жұмыс істеді?
Жауап: Күннің 3/8 бөлігі қанша сағат? ** Бір күнде 24 сағат бар, сондықтан күннің 3/8 бөлігі (3/8)*24 = <<3/8*24=9>>9 сағат
3 аптада қанша күн бар? ** Бір аптада 7 күн бар, сондықтан 3 аптада 7*3 = <<7*3=21>>21 күн бар
Әр сырлаушы қанша сағат жұмыс істеді? ** Әр сырлаушы 9*21 = <<9*21=189>>189 сағат жұмыс істеді
#### 189
Нақты жауап: 189

==================================================

Сұрақ: Көшені қайта жөндеу құны бір метрге 194 доллар тұрады. Моника тұратын көше 150 метр. Льюис тұратын көшені қайта жөндеу қанша долларға қымбат, оның көшесі 490 метр?
Қадамдар: 1. Моника тұратын көшені қайта жөндеудің жалпы құны қанша?
2. Льюис тұратын көшені қайта жөндеудің жалпы құны қанша?
3. Льюис тұратын көшені қайта жөндеу қанша долларға қымбат?
Жауап: Моника тұратын көшені қайта жөндеудің жалпы құны қанша? ** Моника тұратын көшені қайта жөндеудің жалпы құны 194*150 = <<194*150=29100>>29,100 доллар.
Льюис тұратын көшені қайта жөндеудің жалпы құны қанша? ** Льюис тұратын көшені қайта жөндеудің жалпы құны 194*490 = <<194*490=95060>>95,060 доллар.
Льюис тұратын көшені қайта жөндеу қанша долларға қымбат? ** Льюис тұратын көшені қайта жөндеу 95,060-29,100 = <<95060-29100=65960>>65,960 долларға қымбат.
#### 65,960
Нақты жауап: 65,960

==================================================""",
        'ru': """Вопрос: Кэрол и Дженнифер - сестры из Лос-Анджелеса, которые любят собирать подписи знаменитостей. Во время летних каникул сестры каждый день после обеда собирают подписи. Через пять недель Кэрол и Дженнифер сравнивают свои книги автографов, подсчитывая количество подписей, собранных каждой сестрой. У Кэрол в книге 20 подписей, а у Дженнифер 44. У сестер осталось еще три недели летних каникул, и они решили, что хотят достичь 100 подписей между ними к концу лета. Сколько подписей нужно собрать сестрам, чтобы достичь своей цели?
Шаги: 1. Сколько подписей собрали Кэрол и Дженнифер?
2. Сколько подписей нужно собрать сестрам?
Ответ: Сколько подписей собрали Кэрол и Дженнифер? ** Кэрол и Дженнифер уже собрали 20 + 44 подписи = <<20+44=64>>64 подписи.
Сколько подписей нужно собрать сестрам? ** Поскольку их цель - 100, им нужно собрать 100 - 64 подписи. 100 - 64 = <<100-64=36>>36 подписей
#### 36
Точный ответ: 36

==================================================

Вопрос: Команда из 4 маляров работала над особняком по 3/8 дня каждый день в течение 3 недель. Сколько часов работы выполнил каждый маляр?
Шаги: 1. Сколько часов составляет 3/8 дня?
2. Сколько дней в 3 неделях?
3. Сколько часов проработал каждый маляр?
Ответ: Сколько часов составляет 3/8 дня? ** В дне 24 часа, поэтому 3/8 дня это (3/8)*24 = <<3/8*24=9>>9 часов
Сколько дней в 3 неделях? ** В одной неделе 7 дней, поэтому в 3 неделях 7*3 = <<7*3=21>>21 день
Сколько часов проработал каждый маляр? ** Каждый маляр проработал 9*21 = <<9*21=189>>189 часов
#### 189
Точный ответ: 189

==================================================

Вопрос: Перекладка улицы стоит 194 доллара за метр. Улица Моники длиной 150 метров. На сколько дороже перекладка улицы Льюиса, которая имеет длину 490 метров?
Шаги: 1. Какова общая стоимость перекладки улицы Моники?
2. Какова общая стоимость перекладки улицы Льюиса?
3. На сколько дороже перекладка улицы Льюиса?
Ответ: Какова общая стоимость перекладки улицы Моники? ** Общая стоимость перекладки улицы Моники составляет 194*150 = <<194*150=29100>>29,100 долларов.
Какова общая стоимость перекладки улицы Льюиса? ** Общая стоимость перекладки улицы Льюиса составляет 194*490 = <<194*490=95060>>95,060 долларов.
На сколько дороже перекладка улицы Льюиса? ** Перекладка улицы Льюиса дороже на 95,060-29,100 = <<95060-29100=65960>>65,960 долларов.
#### 65,960
Точный ответ: 65,960

=================================================="""}
    return math_examples[lang]



def create_humaneval_prompt_old(row: Dict) -> str:
    return f"""You are my intelligent coding assistant.
You have this Python function:

{row['prompt']}

Finish this function.
Give me the code without any explanation and extra symbols."""

def create_mcq_prompt(row: Dict, benchmark: str, lang: str) -> str:
    """Create zero-shot MCQ prompt for ARC and MMLU"""
    prompts = {
        'en': f"""The following question is presented for you to answer:
Question: {row['question']}
Choose the correct answer from the options listed below:
A: {row['A']}
B: {row['B']}
C: {row['C']}
D: {row['D']}
Return your answer as a single word, in the following format: X, where X is the letter indicating the correct option. Do not explain your answer.
Answer: """,
        'kk': f"""Келесі сұраққа жауап беруіңіз керек:
Сұрақ: {row['question']}
Төменде берілген нұсқалардан дұрыс жауапты таңдаңыз:
A: {row['A']}
B: {row['B']}
C: {row['C']}
D: {row['D']}
Жауабыңызды бір сөзбен беріңіз, келесі форматта: X, мұндағы X дұрыс нұсқаны көрсететін әріп. Жауабыңызды түсіндірмеңіз.
Жауап: """,
        'ru': f"""Вам предлагается ответить на следующий вопрос:
Вопрос: {row['question']}
Выберите правильный ответ из представленных ниже вариантов:
A: {row['A']}
B: {row['B']}
C: {row['C']}
D: {row['D']}
Дайте ответ одним словом в следующем формате: X, где X - буква, указывающая на правильный вариант. Не объясняйте свой ответ.
Ответ: """
    }
    return prompts[lang]

def create_winogrande_prompt(row: Dict, lang: str) -> str:
    prompts = {
        'en': f"""You are given a sentence with one missing word, indicated by an underscore. Read the sentence and choose the appropriate option from the two provided to fill in the blank.
Sentence: {row['sentence']}
Option 1: {row['option1']}
Option 2: {row['option2']}
Return your answer as a single word, in the following format: X, where X is the number (1 or 2) corresponding to the correct option. Do not include any explanation.
Answer: """,
        'kk': f"""Сізге бір сөз жетіспейтін сөйлем берілген, ол астын сызумен көрсетілген. Сөйлемді оқып, берілген екі нұсқадан бос орынға сәйкес келетін нұсқаны таңдаңыз.
Сөйлем: {row['sentence']}
1-нұсқа: {row['option1']}
2-нұсқа: {row['option2']}
Жауабыңызды X форматында бір сөзбен беріңіз, мұндағы X дұрыс нұсқаға сәйкес келетін сан (1 немесе 2). Түсіндірме қоспаңыз.
Жауап: """,
        'ru': f"""Вам дано предложение с одним пропущенным словом, обозначенным подчеркиванием. Прочитайте предложение и выберите подходящий вариант из двух предложенных для заполнения пропуска.
Предложение: {row['sentence']}
Вариант 1: {row['option1']}
Вариант 2: {row['option2']}
Дайте ответ одним словом в следующем формате: X, где X - это число (1 или 2), соответствующее правильному варианту. Не включайте объяснение.
Ответ: """
    }
    return prompts[lang]

def create_hellaswag_prompt(row: Dict, lang: str) -> str:
    prompts = {
        'en': f"""Please complete the sentence given below:
'{row['ctx']}'...
Choose the correct ending from the options listed below:
1: '{row['option1']}'
2: '{row['option2']}'
3: '{row['option3']}'
4: '{row['option4']}'
Return your answer as a single word, in the following format: X, where X is the number indicating the correct option. Do not explain your answer.
Answer: """,
        'kk': f"""Төмендегі берілген сөйлемді аяқтаңыз:
'{row['ctx']}'...
Төменде берілген нұсқалардан дұрыс аяқталуын таңдаңыз:
1: '{row['option1']}'
2: '{row['option2']}'
3: '{row['option3']}'
4: '{row['option4']}'
Жауабыңызды X форматында бір сөзбен беріңіз, мұндағы X дұрыс нұсқаны көрсететін сан. Жауабыңызды түсіндірмеңіз.
Жауап: """,
        'ru': f"""Пожалуйста, закончите предложение, данное ниже:
'{row['ctx']}'...
Выберите правильное окончание из перечисленных вариантов:
1: '{row['option1']}'
2: '{row['option2']}'
3: '{row['option3']}'
4: '{row['option4']}'
Дайте ответ одним словом в следующем формате: X, где X - это число, указывающее на правильный вариант. Не объясняйте свой ответ.
Ответ: """
    }
    return prompts[lang]

def create_drop_prompt(row: Dict, lang: str) -> str:
    prompts = {
        'en': f"""You are intelligent assistant in answering to questions from the given passage.
You will be given a passage and question. Read the passage first and look for the answer for the question.
Give the exact answer only without an explanation.
Give the answer in the given language of the passage and question.
If it is in english, your answer should be in english.
If it is in kazakh, your answer should be in kazakh.
If it is in russian, your answer should be in russian.

Read the following passage and answer the question:
Passage: {row['passage']}
Question: {row['question']}
Return your answer only. Do not include any explanation, just the final answer.
Answer: """,
        'kk': f"""You are intelligent assistant in answering to questions from the given passage.
You will be given a passage and question. Read the passage first and look for the answer for the question.
Give the exact answer only without an explanation.
Give the answer in the given language of the passage and question.
If it is in english, your answer should be in english.
If it is in kazakh, your answer should be in kazakh.
If it is in russian, your answer should be in russian.

Төмендегі мәтінді оқып, сұраққа жауап бер:
Мәтін: {row['passage']}
Сұрақ: {row['question']}
Тек жауапты бер. Ешқандай түсініктеме қосудың қажеті жоқ.
Жауабы: """,
        'ru': f"""You are intelligent assistant in answering to questions from the given passage.
You will be given a passage and question. Read the passage first and look for the answer for the question.
Give the exact answer only without an explanation.
Give the answer in the given language of the passage and question.
If it is in english, your answer should be in english.
If it is in kazakh, your answer should be in kazakh.
If it is in russian, your answer should be in russian.

Прочитайте следующий отрывок и ответьте на вопрос:
Отрывок: {row['passage']}
Вопрос: {row['question']}
Дайте только ответ без объяснений.
Ответ: """
    }
    return prompts[lang]

def create_math_prompt(row: Dict, lang: str) -> str:
    prompts = {
        'en': f"""You are intelligent assistant in solving mathematical questions.
You are given steps which are intermediate questions to calculate the final answer. Solve this questions first, and then calculate the final answer.
Give the exact answer only without an explanation.
Do not show me the intermediate calculations, give only the final answer.
Do not generate anything else, only the final answer is needed that comes after.
I need only the the number that comes after exact answer.

Here are some example problems and their solutions:

{get_math_examples('en')}

Question: {row['question']}
Steps: 
{row['hints']}
Return your answer as a single number.
Answer: """,
        'kk': f"""You are intelligent assistant in solving mathematical questions.
You are given steps which are intermediate questions to calculate the final answer. Solve this questions first, and then calculate the final answer.
Give the exact answer only without an explanation.
Do not show me the intermediate calculations, give only the final answer.
Do not generate anything else, only the final answer is needed.
I need only the the number that comes after нақты жауап.

Here are some example problems and their solutions:

{get_math_examples('kk')}

Сұрақ: {row['question']}
Қадамдар:
{row['hints']}
Жауабыңызды бір сан ретінде беріңіз.
Жауап: """,
        'ru': f"""You are intelligent assistant in solving mathematical questions.
You are given steps which are intermediate questions to calculate the final answer. Solve this questions first, and then calculate the final answer.
Give the exact answer only without an explanation.
Do not show me the intermediate calculations, give only the final answer.
Do not generate anything else, only the final answer is needed.
I need only the the number that comes after точный ответ.

Here are some example problems and their solutions:

{get_math_examples('ru')}

Вопрос: {row['question']}
Шаги:
{row['hints']}
Дайте ответ в виде одного числа.
Ответ: """
    }
    return prompts[lang]


