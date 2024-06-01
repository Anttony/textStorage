import os
import secrets

from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = secrets.token_hex()
app.config['StoreDirectory'] = 'resources'  # каталог по умолчанию
app.config['FileName'] = 'exchange.md'  # файл по умолчанию


@app.route("/", methods=['GET', "POST"])
def index():
    """Обрабатывает корневую страницу сайта.
    - GET возвращает форму с содержимым файла, указанного в конфигурации
    - POST сохраняет текст из формы в файл, указанный в конфигурации
    """
    filename = app.config.get('FileName')
    file_content = get_file_context(filename=filename)

    return render_template('index.html', filename=filename, fileContent=file_content)


@app.route("/form", methods=['POST'])
def form():
    """Обработка нажатия на кнопку отправить"""
    if request.method == "POST":
        filename = request.form.get("filename")
        text = request.form.get("text")
        flash("filename={0}, text={1}".format(filename, text))
        # TODO: проверить, что имя файла не изменилось. Иначе выкидывать исключением
        filename = app.config.get('FileName')
        save_text_to_file(filename, text)
    return redirect("/")


def get_file_context(filename: str) -> str:
    """Получаем содержимое файла"""
    with open(app.config.get('StoreDirectory') + filename, 'r', encoding='utf-8') as f:
        text = f.read()

    return text


def save_text_to_file(filename, text):
    """Сохраняем файл"""
    path = os.path.abspath(app.config.get('StoreDirectory') + filename)
    with open(path, 'wt', encoding="utf-8", newline='\n') as f:
        f.write(text)

    return vars


def app_init():
    """
    Инициализация приложения.
    Проверяется наличие каталога, в котором будут храниться файлы. Если каталога нет, он создается.
    Проверяется наличие файла по умолчанию. Если файла нет, то он создается.
    """
    # TODO: сделать инициализацию приложения
    pass


if __name__ == '__main__':
    app_init()
    app.run(debug=True)
