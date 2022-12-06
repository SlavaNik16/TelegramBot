from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher,FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import sqlite3
from config_reader import config
import random

bot = Bot(token=config.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
connect = sqlite3.connect('users2.db',check_same_thread=False)
cursor = connect.cursor()
class Users(StatesGroup):
      Name = State()
      SurName = State()
      Phone = State()
      Kurs = State()
      NameInstitutions = State()
      InstitutionsTeachers = State()
      Date_Practic_Start = State()
      Date_Practic_End = State()
      NamePractic = State()
      Resumehh = State()
      Git = State()
      Login = State()
      Password = State()
      Password2 = State()
      InputLogin =State()
      InputPasswdord = State()

def get_Permissiion(message):
    cursor.execute(f'SELECT Permission FROM AccountingUser WHERE Id == {message.from_user.id}')
    data = cursor.fetchone()
    if data is not None and data[0] == 'True':
        return True
    return False

async def Delete_MES(message,val1, val2):
    try:
        for i in range(val1, val1 + val2):
            await bot.delete_message(message.chat.id,message.message_id - i)
    except:
        print()

async def Validate_Data(message, data):
    global run
    try:
        timeStr = data.split('.')
        time = [int(timeStr[i]) for i in range(3)]
        daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        run = True
        if time[1] > 12 or time[1] < 1:
            await bot.send_message(message.chat.id,'Несуществующий день/месяц !')
            run = False
        elif time[0] > daysInMonth[time[1]-1] or time[0] < 1:
            await bot.send_message(message.chat.id,'Несуществующий день/месяц !')
            run = False
        return run
    except:
        await bot.send_message(message.chat.id,'Неверный формат!')

async def Update(message, text, var1, var2):
    cursor.execute(f"UPDATE AccountingUser SET {var1} = '{var2}' WHERE Id == {message.from_user.id}")
    connect.commit()
    await message.answer(text)

#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands =['Menu'])
async def Menu(message: types.Message):
    if get_Permissiion(message):
        global markupMenu
        markupMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        Rename = types.KeyboardButton('/Rename')
        Practic = types.KeyboardButton('/Practic')
        AllCommands = types.KeyboardButton('/AllCommands')
        Developer = types.KeyboardButton('/Developer')
        Info = types.KeyboardButton('/Info')
        Exit = types.KeyboardButton('/Exit')
        markupMenu.add(Rename, Practic)
        markupMenu.add(AllCommands, Developer)
        markupMenu.add(Info, Exit)
        await message.answer(
                         'Меню - Здесь есть возможность:\n\r* /Rename - поменять свое ФИО, если вы зарегистрировались '
                         'в телеграмме вымышленным ФИО;'
                         '\n\r* /Practic - перейти на практику;\n\r* /AllCommands - посмотреть всевозможные команды;'
                         '\n\r* /Developer - узнать кто разработал бота;'
                         '\n\r* /Info - посмотреть всю информацию о вас;\n\r* /Exit - выход из профиля.',
                         reply_markup=markupMenu
                         )
    else:
        await message.answer('Войдите в профиль!')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Rename'],state=None)
async def Rename(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Введите новое имя:')
        await Users.Name.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.Name)
async def InputName(message: types.Message, state:FSMContext):
    global Name
    Name = message.text
    await message.answer('Введите Фамилию:')
    await Users.SurName.set()

@dp.message_handler(state = Users.SurName)
async def InputSurName(message:types.Message, state:FSMContext):
    SurName = message.text
    cursor.execute(f"UPDATE AccountingUser SET Name = '{Name}', SurName = '{SurName}' WHERE Id == {message.from_user.id}")
    connect.commit()
    await message.answer('Смена имени прошла успешно!')
    await state.finish()

#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Practic'])
async def Practic(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Вы готовы к практике, тогда переходите по ссылке!:')
        markup = types.InlineKeyboardMarkup()
        Send = types.InlineKeyboardButton('Перейти', url='https://t.me/+0Y9hJclUaNI4NzAy')
        markup.add(Send)
        await message.answer('Нажимая на ссылку, вы готовы перейти в практику!!!', reply_markup=markup)
    else:
        await message.answer('Войдите в профиль!')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['AllCommands'])
async def AllCommands(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Все команды!')
        await message.answer(
                 'Команды на изменение информации пользователя:\n\r/Phone - изменяет номер телефона;'
                 '\n\r/Kurs - изменяет курс;\n\r/NameInstitutions - изменяет название учреждения;'
                 '\n\r/InstitutionsTeachers - изменяет куратора от учреждения;'
                 '\n\r/Date_Practic - меняет начало и конец даты практики;\n\r/NamePractic - меняет название практики;'
                 '\n\r/Resumehh - добавляет ссылку на ваше резюме hh.ru;\n\r/Git - добавляет ссылку на GitHub и т.п.')
    else:
        await message.answer('Войдите в профиль!')

#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Developer'])
async def Developer(message: types.Message):
    await message.answer('Бота создал студент 3 курса группы ИП-20-3 Николаев Вячеслав')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Info'])
async def Info(message: types.Message):
    if get_Permissiion(message):
        cursor.execute(f'SELECT Name, SurName, Phone, Kurs, NameInstitutions, InstitutionsTeachers, Date_Start_Practic,'
                       f' Date_End_Practic, NamePractic, Resumehh, Git, Id FROM AccountingUser '
                       f'WHERE Id == {message.from_user.id}')
        data = cursor.fetchone()
        await message.answer(
                         f'Вся известная информация:\n\rId: {data[11]}\n\rИмя: {data[0]}\n\rФамилия: {data[1]}\n\r'
                         f'Телефон: {data[2]}\n\rКурс: {data[3]}\n\rНазвание учреждения: {data[4]}\n\r'
                         f'Куратор от учреждения: {data[5]}\n\rНачало/Конец практики: {data[6]}-{data[7]}\n\r'               
                         f'Название практики: {data[8]}\n\rРезюме на hh.ru : {data[9]}\n\rGit: {data[10]}')

        doc = open('users2.db','rb')
        await bot.send_document(message.chat.id, doc)

        await message.answer('Если вы хотите изменить информацию, тогда нажмите /AllCommands')
    else:
        await message.answer('Войдите в профиль!')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['Exit'])
async def exit(message: types.Message):
    if get_Permissiion(message):
        markup = types.InlineKeyboardMarkup()
        exit = types.InlineKeyboardButton('Выход', callback_data='Exit')
        markup.add(exit)
        await message.answer('Можете выйти из профиля', reply_markup=markup)
    else:
        await message.answer('Вы уже вышли из профиля! Чтобы зайти обратно, введите /start')

@dp.callback_query_handler(text='Exit')
async def CallExit(callback: types.CallbackQuery):
    cursor.execute(f'UPDATE AccountingUser SET Permission = "False" WHERE Id == {callback.from_user.id}')
    connect.commit()
    await  bot.send_message(callback.message.chat.id, 'Вы успешно вышли из профиля!')
    await bot.send_message(callback.message.chat.id, 'Чтобы вновь войти в учетную запись пропишите /start')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Phone'], state=None)
async def Phone(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Введите новый телефон: ')
        await Users.Phone.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state = Users.Phone)
async def InputPhone(message: types.Message, state: FSMContext):
    try:
        global phone
        phone = int(message.text)
        markup = types.InlineKeyboardMarkup()
        Ok = types.InlineKeyboardButton('Да', callback_data='Phone')
        Cansel = types.InlineKeyboardButton('Отменить', callback_data='Cansel')
        markup.add(Ok, Cansel)
        await state.finish()
        if (len(message.text) == 11):
            await message.answer(f'Вы уверены, что вы ввели правильный номер телефона ({phone})!',
                                   reply_markup=markup)
        else:
            await message.answer("Длина не соответствует требованиям! Номер должен содержать 11 цифр!")
    except:
        await message.answer('Неверный формат! Введите номер ТОЛЬКО ЦИФРАМИ!')
        await state.finish()

@dp.callback_query_handler(text='Phone')
async def CallPhone(callback: types.CallbackQuery):
    await Delete_MES(callback.message, 0, 1)
    cursor.execute(f"UPDATE AccountingUser SET Phone = '{phone}' WHERE Id == {callback.from_user.id}")
    connect.commit()
    await callback.message.answer('Номер успешно изменен!')

@dp.callback_query_handler(text='Cansel')
async def CallCansel(callback: types.CallbackQuery):
    await callback.message.answer('Операция успешно отменена!')
#------------------------------------------------------------------------------------------------------------------

@dp.message_handler(commands = ['Kurs'],state=None)
async def Kurs(message: types.Message, state: FSMContext):
    if get_Permissiion(message):
        await message.answer('Введите курс: ')
        await Users.Kurs.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.Kurs)
async def InputKurs(message: types.Message, state: FSMContext):
        try:
            kurs = int(message.text)
            if (len(message.text) == 1):
                if (kurs > 0 and kurs < 5):
                    await Update(message, 'Курс успешно сменен!', 'Kurs', kurs)
                    await state.finish()
                else:
                    await message.answer('Не может быть такого курса!')
            else:
                await message.answer('Длина не соответствует требованиям! Номер должен содержать 1 цифру!')
        except:
            await message.answer('Неверный формат! Введите номер ТОЛЬКО ЦИФРОЙ')
        await state.finish()

#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['NameInstitutions'],state=None)
async def NameInstitutions(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Введите новое название учреждения: ')
        await Users.NameInstitutions.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.NameInstitutions)
async def InputNameInstitutions(message: types.Message, state: FSMContext):
    NameInst = message.text
    await Update(message, 'Название учреждения изменено!', 'NameInstitutions', NameInst)
    await state.finish()

#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['InstitutionsTeachers'],state=None)
async def InstitutionsTeachers(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Введите нового куратора от учреждения:')
        await Users.InstitutionsTeachers.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.InstitutionsTeachers)
async def InputInstitutionsTeachers(message: types.Message, state: FSMContext):
    NameTeach = message.text
    await Update(message, 'Название куратора от учреждения изменено!', 'InstitutionsTeachers', NameTeach)
    await state.finish()
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Date_Practic'],state=None)
async def Date_Practic(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Введите новую дату!\n\rСоблюдайте формат(3 пары по 2 цифры, разделенные '
                                          'точкой ): день.месяц.год (пример: 01.12.22)')
        await message.answer('Начало практики: ')
        await Users.Date_Practic_Start.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.Date_Practic_Start)
async def InputDataStart(message: types.Message, state: FSMContext):
    global DataStart
    DataStart = message.text
    if await Validate_Data(message, DataStart):
       await message.answer('Конец практики: ')
       await Users.Date_Practic_End.set()
    else:
        await state.finish()

@dp.message_handler(state=Users.Date_Practic_End)
async def InputDataEnd(message: types.Message, state: FSMContext):
    DataEnd = message.text
    await state.finish()
    if await Validate_Data(message, DataEnd):
        cursor.execute(f"UPDATE AccountingUser SET Date_Start_Practic = '{DataStart}', Date_End_Practic = '{DataEnd}' "
                       f"WHERE Id == {message.from_user.id}")
        connect.commit()
        await message.answer('Дата практики изменена!')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['NamePractic'],state=None)
async def NamePractic(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Введите новое название практики: ')
        await Users.NamePractic.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.NamePractic)
async def InputNamePractic(message: types.Message, state: FSMContext):
    NamePractic = message.text
    await Update(message, 'Название практики изменено!', 'NamePractic', NamePractic)
    await state.finish()
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Resumehh'],state=None)
async def Resumehh(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Вставьте ссылку резюме на hh.ru: ')
        await Users.Resumehh.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.Resumehh)
async def InputResumehh(message: types.Message, state: FSMContext):
    Resumehh = message.text
    await Update(message, 'Ссылка на резюме hh.ru  изменена!', 'Resumehh', Resumehh)
    await state.finish()
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['Git'],state=None)
async def Git(message: types.Message):
    if get_Permissiion(message):
        await message.answer('Вставьте ссылку на полезные материалы(github, gitlub и т.п.): ')
        await Users.Git.set()
    else:
        await message.answer('Войдите в профиль!')

@dp.message_handler(state=Users.Git)
async def InputGit(message: types.Message, state: FSMContext):
    git = message.text
    await Update(message, 'Ссылка Git изменена!', 'Git', git)
    await state.finish()
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    cursor.execute("""CREATE TABLE IF NOT EXISTS AccountingUser(
                    Id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                    Name TEXT,
                    SurName TEXT,
                    Phone INTEGER(11),
                    Kurs INTEGER(1),
                    NameInstitutions TEXT,
                    InstitutionsTeachers TEXT,
                    Date_Start_Practic TEXT(8),
                    Date_End_Practic TEXT(8),
                    NamePractic TEXT,
                    Resumehh TEXT,
                    Git TEXT,
                    Modifier TEXT,
                    Login TEXT NOT NULL,
                    Password TEXT NOT NULL,
                    Permission TEXT
                 )""")
    connect.commit()
    if not get_Permissiion(message):
        markup = types.InlineKeyboardMarkup()
        mes = f'Привет {message.from_user.first_name} {message.from_user.last_name}\n\r/id - посмотреть ваш id'
        await bot.send_message(message.chat.id, mes)
        Reg = types.InlineKeyboardButton('Регистрация', callback_data='Reg')
        Ent = types.InlineKeyboardButton('Войти!', callback_data='Ent')
        markup.add(Reg, Ent)
        await message.answer('Пожалуйста Зарегистрируйтесь или Войдите в профиль', reply_markup=markup)
    else:
        await message.answer('Вы уже вошли в профиль, пожалуйста ознакомьтесь с меню команд /Menu')
#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['id'])
async def start(message: types.Message):
    await message.answer(f'Ваш Id: {message.from_user.id}')
#------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='Reg',state=None)
async def CallReg(callback: types.CallbackQuery,state: FSMContext):
    people_id = callback.from_user.id
    cursor.execute(f'SELECT Id FROM AccountingUser WHERE Id == {people_id}')
    data = cursor.fetchone()
    if data is None:
        await callback.message.answer('Введите логин:')
        await Users.Login.set()
    else:
        await bot.send_message(callback.message.chat.id, 'Такой пользователь уже существует!')
        await state.finish()
    await Delete_MES(callback.message, 0, 2)

@dp.message_handler(state=Users.Login)
async def Login(message: types.Message, state: FSMContext):
    global login
    login = message.text
    await message.answer('Введите пароль:')
    await Users.Password.set()

@dp.message_handler(state=Users.Password)
async def Password(message: types.Message, state: FSMContext):
    global passwd
    passwd = message.text
    await message.answer('Введите пароль еще раз:')
    await Users.Password2.set()

@dp.message_handler(state=Users.Password2)
async def Password2(message: types.Message, state: FSMContext):
    global passwd2
    passwd2 = message.text
    if (passwd2 == passwd):
        user_acc = [message.from_user.id,
                    message.from_user.first_name,
                    message.from_user.last_name,
                    89000000000,
                    3,
                    'СПБ ГБПОУ "Политехнический колледж городского хозяйства"',
                    'Солопова Е.В.',
                    '28.11.22',
                    '21.12.22',
                    'ПМ.04 "Сопровождение и обслуживание программного обеспечения компьютерных систем"',
                    None,
                    None,
                    'User',
                    login,
                    passwd,
                    'False']
        cursor.execute('INSERT INTO AccountingUser VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', user_acc)
        connect.commit()
        await message.answer('Регистрация прошла успешна! Войдите в профиль /start')
    else:
        await message.answer('Неправильный пароль! Повторите попытку снова!')
    await state.finish()
#------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='Ent',state=None)
async def CallEnt(callback: types.CallbackQuery,state: FSMContext):
    if get_Permissiion(callback.message):
        await bot.send_message(callback.message.chat.id, 'Вы уже вошли в профиль!')
        await state.finish()
    else:
        await callback.message.answer('Введите логин:')
        await Users.InputLogin.set()
    await Delete_MES(callback.message, 0, 4)

@dp.message_handler(state=Users.InputLogin)
async def InputLogin(message: types.Message, state: FSMContext):
    global loginUser
    loginUser = message.text
    await message.answer('Введите пароль:')
    await Users.InputPasswdord.set()

@dp.message_handler(state=Users.InputPasswdord)
async def InputPasswdord(message: types.Message, state: FSMContext):
    global passwdUser
    passwdUser = message.text
    people = message.from_user.id
    cursor.execute(f'SELECT Permission, Id, Login, Password FROM AccountingUser '
                   f'WHERE Id = {people} AND Login = "{loginUser}" AND Password = "{passwdUser}"')
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f'UPDATE AccountingUser SET Permission = "True" WHERE Id == {message.from_user.id}')
        connect.commit()
        await message.answer('Вы успешно вошли в профиль!')
        await message.answer( 'Чтобы ознакомится с ботом введите /Menu')
    else:
        await message.answer('Введен неправильный логин или пароль! Возможно вы не зарегистрировались!')
    await state.finish()

#------------------------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['text'])
async def get_user_text(message: types.Message):
    if get_Permissiion(message):
        mes = get_privets(message.text.lower())
        if mes != 'Не найдена':
            await message.answer(mes)
        else:
            await message.reply(f'Пользователь написал:\n{message.text}!')
    else:
        await message.answer('Пожалуйста войдите в учетную запись! /start')

def get_privets(text):
    BOT_MES = {
        'Intents':{
            'Greeting': {
                'Example': ['Привет!','Хай!','Добрый день!','Новый день настал!'
                    ,'Ну, вот поспали — теперь можно и поесть!'],
                'Resposes':['прив','хаюхай', 'добрового времени суток',"hello","привет"],
            },
            'Bue': {
                'Example': ['Пока!', 'Доброй ночи!', 'До завтра!', 'Счастливо!','До скорого!'],
                'Resposes': ['пока', 'спокойной ночи', 'ночи', 'bue'],
            }
        }
    }

    for hello, value in BOT_MES['Intents'].items():
        for examples in value['Resposes']:
            if examples == text:
                return random.choice(BOT_MES['Intents'][hello]['Example'])
    return 'Не найдена'


def main():
      executor.start_polling(dp,skip_updates=True)

if __name__ == "__main__":
    main()