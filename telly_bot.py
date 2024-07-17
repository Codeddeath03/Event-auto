from email import message
import logging
from unicodedata import name
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import pygsheets
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()
cwd = os.getcwd()
PORT = int(os.environ.get('PORT', 5000))
print(cwd)
client = pygsheets.authorize(service_account_file=r"ctelly/ftel/data.json")
print(client.spreadsheet_titles())

async def start(update: Update, context: str(ContextTypes.DEFAULT_TYPE)):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def upcoming_events(update: Update, context: str(ContextTypes.DEFAULT_TYPE)):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Upcoming Events coming soon")  


async def ping(update: Update, context: str(ContextTypes.DEFAULT_TYPE)):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")   

async def register_event(update: Update, context: str(ContextTypes.DEFAULT_TYPE)): ## event_name registeration 'function_name cumming soon'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")  

async def event_details(update: Update, context: str(ContextTypes.DEFAULT_TYPE)): ## event_details info function 'name cumming soon'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="coming soon")  

async def event_faqs(update: Update, context: str(ContextTypes.DEFAULT_TYPE)): ## event_faqs info function 'name cumming soon'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="coming soon")  

async def event_he(update: Update, context: ContextTypes.DEFAULT_TYPE,wsht,title):
     try:
       print(len(context.args))
     except:
        print("nahi hoga isse") 
     try: #catching the arguments for name
       if len(context.args) == 7 :
        count = 0
        found =  False
        registered = False
        name = context.args
        print(name)
        name = "{} {}".format(name[0],name[1])
        name = name.lower()
        print(name)
        roll_no = context.args[2]
        email= context.args[3]
        branch = context.args[4]
        year = context.args[5]
        phno = context.args[6]
        t_id = update.message.from_user['id']
        t_list = wsht.get_col(8)
        name_list = wsht.get_col(2)
        print(name_list)
        print(name)
        for i in t_list:
         print(i.lower())
         count+=1
         if str(t_id) == i:
          if str(name.lower()) == wsht.cell("B{}".format(count)).value :
           print("caught")
           name_details = wsht.get_row(count)
           pprint(name_details)
           print("You are registered for the event")
           found = True
           if "yes" == (str(wsht.cell("I{}".format(count)).value)).lower(): 
                await context.bot.send_message(chat_id=update.effective_chat.id, 
                  text="You are already registered for {}".format(title))
                return
          else:
              await context.bot.send_message(chat_id=update.effective_chat.id, 
                  text="You are already registered for {}".format(title))
              return        
          break
         print(count)
        if found == False :
            row = wsht.rows
            wsht.insert_rows(row, number=1, 
            values=[None,name,email,roll_no,branch,year,phno,t_id,"yes"], inherit=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, 
         text="{}! successfully registered for {}!".format(name,title))
            print(wsht.rows)
        elif found == True and registered == False:
            wsht.cell("I{}".format(count)).set_value("yes")
            name_details = wsht.cell("B{}".format(count)).value
            await context.bot.send_message(chat_id = update.effective_chat.id,text="You are successfully registered with name {} for {}".format(name_details,title))
       elif len(context.args) == 2 and "register" not in context.args:
        count = 0
        found =  False
        registered = False
        name = context.args
        print(name)
        name = "{} {}".format(name[0],name[1])
        name = name.lower()
        print(name)
        t_id = update.message.from_user['id']
        t_list = wsht.get_col(8)
        name_list = wsht.get_col(2)
        print(t_list)
        print(name)
        for i in name_list:
         print("ii:",i)
         count+=1
         if name == i.lower():
          found = True       
          print(wsht.cell("H{}".format(count)).value)
          print("kya hua?")
          if  (str(wsht.cell("I{}".format(count)).value)).lower() == "yes"  and str(t_id) == wsht.cell("H{}".format(count)).value: 
           print("caught")
           name_details = wsht.get_row(count)
           pprint(name_details)
           print("You are registered for the event")
           await context.bot.send_message(chat_id = update.effective_chat.id,text="You are already registered for {}".format(title))
           return
          elif (str(wsht.cell("I{}".format(count)).value)).lower()  == "yes"  and str(t_id) != wsht.cell("H{}".format(count)).value:      
           print(wsht.cell("H8").value)     
           if  str(wsht.cell("H{}".format(count)).value) == "null":
             wsht.cell("h{}".format(count)).set_value(t_id)
             await context.bot.send_message(chat_id = update.effective_chat.id,text="You are already registered for {}".format(title))
             return
           await context.bot.send_message(chat_id = update.effective_chat.id,text="This name is associated to different telegram id")
           return
          elif (str(wsht.cell("I{}".format(count)).value)).lower() == "no"  and str(t_id) != wsht.cell("H{}".format(count)).value: 
                print("greatest no")
                print(str(t_id))
                print(wsht.cell("H{}".format(count)).value)
                if  str(wsht.cell("H{}".format(count)).value) == "null" :
                  wsht.cell("h{}".format(count)).set_value(t_id)
                  break
                await context.bot.send_message(chat_id = update.effective_chat.id,text="This name is associated to different telegram id")
                return
          break

        if found == True and registered == False:
            wsht.cell("I{}".format(count)).set_value("yes")
            name_details = wsht.cell("B{}".format(count)).value
            pprint(name_details)
            print("You are registered for the event")
            await context.bot.send_message(chat_id = update.effective_chat.id,text="You are successfully registered with name {} for {}".format(name_details,title))
            #row = wsht.rows
            #wsht.insert_rows(row, number=1, 
            #values=[None,name,None,None,None,None,None,t_id], inherit=True)
        elif  found == False:
         await context.bot.send_message(chat_id=update.effective_chat.id, 
         text="I'll register you to {}"
         "\nPls type /{} name surname roll_no email branch year phone_no".format(title,title))   

       elif len(context.args) == 1 and (str((context.args)[0]).lower()) == "register":
         count = 0
         found =  False
         registered = False
         name = context.args
         t_id = update.message.from_user['id']
         t_list = wsht.get_col(8)
         print(t_list)
         for i in t_list:
          print(t_id)
          print("ii:",i)
          count+=1
          if str(t_id) == i:
           if "yes" == (str(wsht.cell("I{}".format(count)).value)).lower(): 
            print("caught")
            name_details = wsht.get_row(count)
            pprint(name_details)
            print("You are registered for the event")
            await context.bot.send_message(chat_id = update.effective_chat.id,text="You are already registered for {}".format(title))
            registered = True
           found = True 
           break

         if found == True and registered == False:
            wsht.cell("I{}".format(count)).set_value("yes")
            name_details = wsht.cell("B{}".format(count)).value
            pprint(name_details)
            print("You are registered for the event")
            await context.bot.send_message(chat_id = update.effective_chat.id,text="You are successfully registered with name {} for {}".format(name_details,title))
           
         elif  found == False:
          await context.bot.send_message(chat_id=update.effective_chat.id, 
          text="I'll register you to {}"
          "\nPls type /{} name surname roll_no email branch year phone_no".format(title,title))  

       elif len(context.args) == 0:    
         print("poop")
         await context.bot.send_message(chat_id=update.effective_chat.id,text="Type \n1)/{} register"
         "\n2)/{} name surname roll_no email branch year phone_no\nUse command 2 if registering first time for a CSI event".format(title))
     except:
        pass



async def python_workshop(update: Update, context: ContextTypes.DEFAULT_TYPE): 
   sht = client.open_by_url("https://docs.google.com/spreadsheets/d/") #event name sheet
   # opens a worksheet by its name/title
   print(sht.worksheets()) 
   wsht = sht.worksheet("title", "Form Responses 1")
   print(wsht.rows)
   print(wsht.cols)
   await event_he(update,context,wsht,sht.title)


async def django_workshop(update: Update, context: ContextTypes.DEFAULT_TYPE): 
   print(client.spreadsheet_titles())
   sht = client.open_by_url("https://docs.google.com/spreadsheets/d/") #event name sheet
   # opens a worksheet by its name/title
   print(sht.worksheets()) 
   wsht = sht.worksheet("title", "Form Responses 1")
   print(wsht.rows)
   print(wsht.cols)
   await event_he(update,context,wsht,sht.title)
   
    
if __name__ == '__main__':
    token= os.environ['token']
    herokuWebUrl= os.environ['url']
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    python_workshop_handler = CommandHandler('python_workshop', python_workshop)
    django_workshop_handler = CommandHandler('django_workshop', django_workshop)
    ping_handler = CommandHandler('ping', ping) 
    upcoming_handler = CommandHandler('upcoming', upcoming_events) 
    application.add_handler(start_handler)
    application.add_handler(ping_handler)
    application.add_handler(python_workshop_handler)
    application.add_handler(upcoming_handler)
    application.add_handler(django_workshop_handler)
    application.run_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=token,webhook_url=herokuWebUrl + token)
