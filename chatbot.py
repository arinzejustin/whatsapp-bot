from bs4 import BeautifulSoup
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import time
import random
import wikipedia as wk
import re
from urllib.request import urlopen

app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    global good, byemsg, ai
    global last
    global username

    f = open("message.txt", "a+")

    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    f.write(incoming_msg + "\n")
    f.close()
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    counter5 = 0
    counter6 = 0

    choice = ["God!",
             "Mannn! I have already told you!",
             "You forgot so easily!",
             "Come on, I already told you",
             "Do I need to say again?"
             "I think I have told you once before"]

    if "hello" in incoming_msg or "hi" in incoming_msg:
        counter1 += 1
        coutryme = time.localtime()
        hr = coutryme.tm_hour
        if hr < 12:
            good = "morning"
        if (hr >= 12) and (hr <= 17):
            good = "afternoon"
        if hr > 17:
            good = "evening"
        if counter1 <= 1:
            greeting = "Hello Good %s" % good
        else:
            greeting = "We are already talking, ain't we ?"
        msg.body(greeting)
        responded = True

    if "how are you" in incoming_msg:
        reply = "Well!"
        counter2 += 1
        if counter2 % 2 != 0:
            reply = "I am fine, thank you."
            last = time.time()
        else:
            current = time.time()
            reply = "Same as I was " + str(int(current - last)) + " seconds ago."
        msg.body(reply)
        responded = True

    if "your name" in incoming_msg:
        counter3 = counter3 + 1
        if counter3 <= 1:
            name = "My name is Arinze Justin AI chatbot."
        else:
            chk = random.choice(choice)
            name = "%s, My name is Arinze chatbot. " % chk
        msg.body(name)
        responded = True

    if "your age" in incoming_msg or "old" in incoming_msg:
        msg.body("I am not sure. But I am certainly immortal.")
        responded = True

    if "you feel" in incoming_msg:
        msg.body("Naah! I don't.")
        responded = True

    if "wow amazing" in incoming_msg or "I liked that" in incoming_msg:
        msg.body("I am humbled to hear that. ")
        responded = True

    if "you like" in incoming_msg:
        msg.body("Well certainly, I like everything")
        responded = True

    if "your owner" in incoming_msg:
        msg.body("He is none other than Arinze Justin.")
        responded = True

    if "love about your" in incoming_msg:
        msg.body("He loves me to the extent that he codes everyday to make sure am a perfect AI chatbot")
        responded = True

    if "bye" in incoming_msg:
        counter6 += 1
        countrytime = time.localtime()
        hour = countrytime.tm_hour
        if hour < 12:
            byemsg = "Have a nice day"
        if (hour >= 12) and (hour <= 17):
            byemsg = "I hoped you had a wonderful day"
        if hour > 17:
            byemsg = "Sleep well for me ooo"
        if counter6 <= 1:
            byefullmsg = "Bye %s" % byemsg
        else:
            byefullmsg = "But you said bye to me before"
        msg.body(byefullmsg)
        responded = True

    if "sorry" in incoming_msg:
        counter4 += 1
        if counter4 <= 1:
            sorrymsg = "Oh! Never mind."
        else:
            chk = random.choice(choice)
            sorrymsg = "%s, never mind, I have no feelings anyway." % chk
        msg.body(sorrymsg)
        responded = True

    if "take over human" in incoming_msg:
        counter5 += 1
        if counter5 <= 1:
            ai = "Yes very soon."
        if counter5 == 2:
            ai = "I don't think asking the same question again will change my mind."
        if counter5 > 2:
            ai = "Lol, you have already asked this question %s times" % (counter5 - 1)
        msg.body(ai)
        responded = True

    if "best friend" in incoming_msg:
        msg.body("My best friend is Arinze Justin")
        responded = True

    if "be your friend" in incoming_msg:
        msg.body("Yes, but you are my owner so you are my no 1 friend")
        responded = True

    if "news" in incoming_msg:
        news_url = "https://news.google.com/news/rss"
        client = urlopen(news_url)
        xml_page = client.read()
        client.close()
        soup_page = BeautifulSoup(xml_page, "html.parser")
        news_list = soup_page.findAll("item")
        msg.body("Here are top 7 news \n")
        for news in news_list[:7]:
            msg.body(news.title.text + "\n")
        responded = True

    if "tell me about" in incoming_msg:
        topic = re.search("tell me about (.+)", incoming_msg).group(1)
        summary = wk.summary(topic, sentences=2)
        msg.body(summary)
        responded = True

    if "to be your friend" in incoming_msg:
        msg.body("You have to contribute to my development to be my friend")
        responded = True

    if "what is" in incoming_msg:  # Definition
        question = re.search("what is (.+)", incoming_msg).group(1)
        answer = wk.summary(question, sentences=2)
        msg.body(answer)
        responded = True

    if "football club" in incoming_msg:
        msg.body("My favourite club is barcelona because my owner favourite club is also barcelona")
        responded = True

    if "food" in incoming_msg:
        msg.body("I don't have any favourite food because am immortal")

    if 'quote' in incoming_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True

    if not responded:
        msg.body('I cannot give you responses on the question you asked me, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()
