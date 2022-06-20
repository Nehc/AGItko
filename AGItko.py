import os
import sys
import torch
import telebot
from transformers import AutoTokenizer, AutoModelForCausalLM

if len(sys.argv)>1:
    token = sys.argv[1]
else:
    token = os.getenv('TG_TOKEN')
    if not token: 
        print('bot token needed...')
        quit()

model_name = "Nehc/AGIRussia"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
# turn on cuda if GPU is available
use_cuda = torch.cuda.is_available()

if use_cuda:
    model.cuda()

bot = telebot.TeleBot(token)

print(f'Main cicle whith cuda is {use_cuda} start...')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Бот обучен на корпусе диалогов из рускоязычных групп тематики AGI (Artificial general intelegense), можно говорить с ним на тему ИИ, сознания, мышления и смежные темы.")

@bot.message_handler(content_types='text')
def message_reply(message):
    src = 'data/' + str(message.chat.id)
    try:    
        with open(src, 'r') as cont_file:
            context = cont_file.read()+'\n'
    except FileNotFoundError:
        context = ''    
    
    text = context+f"<IN>{message.text}\n<OUT>"
    inpt = tokenizer.encode(text, return_tensors="pt")    
    
    T_IN = tokenizer.encode('<IN>')[0]
    T_OUT = tokenizer.encode('<OUT>')[0]
    T_END = tokenizer.encode('<END>')[0]
    T_PAD = tokenizer.encode('|PAD|')[0]

    # Run eval step for caption
    with torch.no_grad():
        out = model.generate(inpt.cuda(), max_length=500, do_sample=True, top_k=5, top_p=0.95, temperature=1, eos_token_id=T_END, pad_token_id=T_PAD)
    
    out_tokens = torch.where(out[0]==T_OUT)
    last_repl = out[0][out_tokens[0][-1]+1:-1]
    repl = tokenizer.decode(last_repl)
    bot.reply_to(message, repl)
    in_tokens = torch.where(out[0]==T_IN)
    if len(in_tokens[0])<=2 or len(out[0])<=200:
        context = out[0]                        
    else: 
        context = out[0][in_tokens[0][-3]:]

    with open(src, 'w') as new_file:
        new_file.write(tokenizer.decode(context))

#bot.polling(interval=3, timeout=45)
bot.infinity_polling()
