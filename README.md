# AGItko
chat-bot on ruGPT-medium and AGIRussia corp

Бот обучен на корпусе диалогов из рускоязычных групп тематики AGI (Artificial general intelegense), можно говорить с ним на тему ИИ, сознания, мышления и смежные темы.

Процесс обучения расписан [в этом Colab](https://colab.research.google.com/drive/1P7cd70gSXjBqQtUJgG84n-NvgnN7nv2p?usp=sharing). 

так же прилагается файл [AGItko.py](https://github.com/Nehc/AGItko/blob/main/AGItko.py) для запуска бота с обученной моделью. Формат запуска:
    
    python AGItko.py 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    
не забудьте подставить свой токен бота.

Так же можно развернуть бота как docker-контейнер посредством следующих команд:
    
    git clone https://github.com/Nehc/AGItko.git
    cd AGItko
    docker build --tag="<your_name>/AGItko" .
    docker run --user 1000:100 -tid --gpus all --name AGItko --mount \
    type=bind,src=/home/<your_name>/BertMobile,target=/home/telebot \
    -e TG_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 <your_name>/AGItko

с поправкой на ваши локальные пути, имя пользователя и тп...

