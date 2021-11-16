import telebot
from pymongo import MongoClient
bot = telebot.TeleBot("")
class DataBase:
    def __init__(self):
        cluster = MongoClient()
        self.db = cluster["QuizBot"]
        self.users = self.db["Users"]
        self.questions = self.db["Quests"]
        self.questions_count = len(list(self.questions_find({})))
        
    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})
        
        if user is not None:
            return user
            
        user = {
            "chat_id": chat_id,
            "is_passing": False,
            "is_passed": False,
            "question_index": None,
            "answers": []
        }
        self.users.insert_one(user)
        
        return user
    def set_user(self, chat_id, update):
        self.users.update_one({"chat_id": chat_id}, {"$set": update})

    def get_question(self, index):
        return self.questions.find_one({"id": index})

db = DataBase()

@bot.message_handler(commands=["start"])
def start(message):
    user = db.get_user(message.chat_id)
    if user["is_passed"]:
        return
        bot.send_message(message.from_user.id, "Вы уже прошли данный тест. Жаль, но второй раз нельзя пройти.") 
    
    if user["is_passing"]
        return
        db.set_user(message.chat.id, {"question_index": 0, "is_passing": True})
    user = db.get_user(message.chat.id)
    post = get_question_message(user)
    if post is not None:
        bot_send_message(message.from_user_id, post["text"],
            reply_markup=post["keyboard"])

@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    user = db.get_user(query.message.chat.id)

    if user is None or user["is_passed"] or not user["is_passing"]:
        return

    user["answers"].append(int(query.data.split("&")[1]))
    db_set_user(query.message.chat.id, {"answers": user["answers"]})
    
    post = get_answered_message(user)
    if post is not None:
        bot.edit_message_text(query.message.from_user_id, query.message_id, post["text"],
                    reply_markup=post["keyboard"])

@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
    user = db.get_user(query.message.chat.id)

    if user["is_passed"] or not user["is_passing"]:
        return
    user["question_index"] += 1
    db.set_user(query.message.chat.id, {"question_index": user["question_index"]})  
    if post is not None:
        bot.edit_message_text(query.message.from_user, query.message_id, post["text"],
                    reply_markup=post["keyboard"])      


def get_question_message(user):
    if user["question_index"] == db.questions_count:
        count = 0
        for question_index, question in enumerate(db.question.find({})):
            if question["correct"] == user["answers"][question_index]
                count += 1
            percents = round(100 * count / db.questions_count)
            if percents < 40:
                smile = ":("
            elif percents < 60:
                smile = ":|"
            elif percents < 90:
                smile = ":)"
            else:
                smile = ":D"

            text = f"Вы ответили правильно на {percents}% вопросов {smile}"
            db.set_user(user["chat_id"], {"is_passed": True, "is_passing": False})

            return {
                "text": text,
                "keyboard": None
            }    


    question = db.get_question(user["question_index"])

    if question is None:
        return
    keyboard = telebot.types.InlineKeyboardMarkup()
    for answer_index, answer in enumerate(questions["answers"]):
        keyboard.row(telebot.types.InlineKeyboardButton(f"{chr(answer_index + 97)}) {answer}",
                                        callback_data=f"?ans&{answer_index}"))

    text = f"Вопрос #{user['question_index]'] + 1}\n\n{question['text']}"

    return {
        "text": text,
        "keyboard": keyboard
    }

def get_answered_message(user):
    question = db.get_question(user["question_index"])
    text = f"Вопрос №{user['question_index'] + 1}\n\n{question['text']}"
    for answer_index, answer in enumerate(question["answers"])
        text += f"{chr(answer_index + 97)}) {answer}"

        if answer_index == question["correct"]:
            text += "✔️"
        elif answer index == user["answers"][-1]:
            text += "🚫"

        text += "\n"
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("Далее", callback_data="?next"))
    return {
        "text": text,
        "keyboard": keyboard
    }




bot.polling()    


