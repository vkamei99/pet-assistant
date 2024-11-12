import pyttsx3
from datetime import datetime
import speech_recognition as sr
from random import choice, randint
import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, cardapio_RU
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from decouple import config
import serial
from deep_translator import GoogleTranslator

USERNAME = config('USER')
BOTNAME = config('BOTNAME')
RURL = config('RURL')

opening_text = [
    "Ok, estou no processo.",
    "Beleza, já iniciei.",
    "Só um segundo.",
    "Executando.",
    "Claro! Estou fazendo isso."
]

listening_text = [
    "Estou escutando.",
    "O que deseja?",
    "Eu!",
    ]

#oracle = serial.Serial('COMX', 9600)


def speak(engine, text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


def greet_user(engine):
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(engine, f"Bom dia {USERNAME}")
    elif (hour >= 12) and (hour < 18):
        speak(engine, f"Boa tarde {USERNAME}")
    elif (hour >= 18):
        speak(engine, f"Boa noitinha {USERNAME}")

    speak(engine, f"Eu sou {BOTNAME}. Como posso te ajudar?")


def take_user_input(engine):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escutando....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Reconhecendo...')
        query = r.recognize_google(audio, language='pt-BR')
        if not 'sair' in query or 'pare' in query:
            speak(engine, choice(opening_text))
            #set_oracle(oracle,2)
        # else:
            # hour = datetime.now().hour
            # if hour >= 21 and hour < 6:
            #     speak(engine, "Boa noite, cuide-se!")
            # else:
            #     speak(engine, 'Tenha um bom dia!')
            # exit()
    except Exception:
        query = 'None' 
    return query

#def set_oracle(oracle,state):
    #oracle.write(str(state).encode() + b'\n')

def listen(engine):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='pt-BR')
        print(query)
        if not 'sair' in query or 'pare' in query:
            pass
        else:
            # hour = datetime.now().hour
            # if hour >= 18 and hour < 6:
            #     speak(engine, "Boa noite, cuide-se!")
            # else:
            #     speak(engine, 'Tenha um bom dia!')
            print("Saindo...")
            exit()
            
    except Exception:
        query = 'None' 
    return query


def main():

    esp_ip = "192.168.1.103"
    
    volume = 1.5

    engine = pyttsx3.init('sapi5')

    #tradutor ingles -> portugues
    tradutor = GoogleTranslator(source= "en", target= "pt")

    # Set Rate
    engine.setProperty('rate', 210)

    # Set Volume
    engine.setProperty('volume', volume)

    # Set Voice (Female)
    # The getProperty method returns a list of voices available in the system.
    voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id)
    for voice in voices:
        if "brazil" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    greet_user(engine)

    while True:
        query = listen(engine).lower()
        
        #set_oracle(oracle,0)

        if 'faraday' in query or 'faradai' in query or 'faradei' in query:
            speak(engine, choice(listening_text))

            while True:
                
                #set_oracle(oracle,1)
                query = take_user_input(engine).lower()       

                if 'abrir bloco de notas' in query:
                    open_notepad()
                    break

                elif 'abrir prompt de comando' in query or 'abrir cmd' in query:
                    open_cmd()
                    break
                
                elif 'se apresente' in query or 'apresente-se' in query:
                    speak(engine,
                        f'Olá, eu sou a Faraday, a assistente virtual do PET Elétrica Ufes. Caso deseje minha ajuda basta me chamar que eu atenderei. Se quiser uma lista dos possíveis comandos que eu executo, basta dizer Comandos que explicarei.')
                    break
                
                elif 'abrir camera' in query:
                    open_camera()
                    break

                elif 'ru do dia' in query or 'ru' in query or 'cardápio ru' in query:
                    cardapio = cardapio_RU(RURL, datetime.now().hour)
                    speak(engine, 
                          f'RU, {cardapio}')
                    break

                elif 'acender' in query:
                    url_on = f"http://{esp_ip}/H"
                    response_on = requests.get(url_on)
                    if response_on.status_code == 200:
                        print("LED aceso!")
                    else:
                        print("Falha ao acender o LED.")
                    break

                elif 'apagar' in query:
                    url_on = f"http://{esp_ip}/L"
                    response_on = requests.get(url_on)

                    if response_on.status_code == 200:
                        print("LED apagado!")
                    else:
                        print("Falha ao apagar o LED.")
                    break

                elif 'endereço de ip' in query:
                    ip_address = find_my_ip()
                    speak(engine,
                        f'Seu endereço de IP é: {ip_address}.\n TE EME JOTA')
                    print(f'Seu endereço de IP é: {ip_address}')
                    break

                elif 'wikipedia' in query:
                    speak(engine, 'O quê você quer pesquisar na Wikipedia?')
                    search_query = take_user_input(engine).lower()
                    results = search_on_wikipedia(search_query)
                    speak(engine, f"De acordo com a Wikipedia, {results}")
                    speak(engine, "Estou printando na tela.")
                    print(results)
                    break

                elif 'youtube' in query:
                    speak(engine, 'O quê você quer ver no YouTube?')
                    video = take_user_input(engine).lower()
                    play_on_youtube(video)
                    break

                elif 'pesquisar' in query:
                    speak(engine, 'O que vocÊ quer pesquisar no Google?')
                    query = take_user_input(engine).lower()
                    search_on_google(query)
                    break

                elif 'receba os alunos' in query or 'receba' in query:
                    speak(engine,
                        f'Olá! Sejam bem-vindos ao PET Elétrica. Eu sou a Farady, sua assistente virtual e estou aqui para tornar a sua visita uma experiência fantástica.'\
                        'Estamos ansiosos para mostrar a vocês o emocionante mundo da ciência, experimentação e descoberta.' \
                        'Vocês estão prestes a embarcar em uma jornada emocionante, cheia de curiosidades, aprendizado e diversão. Aqui, a imaginação é o nosso combustível,' \
                        'e as possibilidades são infinitas. Aqui, vocês poderão explorar, fazer perguntas e aprender de uma maneira única e envolvente.')
                    break


                # elif "enviar email" in query:
                #     speak(
                #         engine, "Entre com o email para o qual deseja enviar.")
                #     receiver_address = input("Entre ocm o endereço de email: ")
                #     speak(engine, "Qual deve ser o assunto?")
                #     subject = take_user_input(engine).capitalize()
                #     speak(engine, "Qual é a mensagem?")
                #     message = take_user_input(engine).capitalize()
                #     if send_email(receiver_address, subject, message):
                #         speak(engine, "Email enviado.")
                #     else:
                #         speak(engine,
                #             "Algo deu errado enquanto enviava o email,por favor, cheque o log de erro.")
                #     break

                elif 'piadoca' in query:
                    speak(engine, f"Espero que goste dessa.")
                    joke = get_random_joke()
                    speak(engine, tradutor.translate(joke))
                    speak(engine, "Estou printando na tela.")
                    print(joke)
                    break
                
                elif 'conte uma piada do pastor' in query:
                    with open('piadas.txt', 'r', encoding='utf-8') as file:
                        piadas = file.readlines()
                    piada = choice(piadas)
                    speak(engine, "Espero que goste dessa.")
                    speak(engine, piada)
                    print(f"Piada: {piada}")
                    break

                elif "conselho" in query or 'me de um conselho' in query:
                    speak(engine, f"Aqui vai um conselho para você.")
                    advice = get_random_advice()
                    conselho = tradutor.translate(advice)
                    speak(engine, conselho)
                    speak(engine, "Estou printando na tela.")
                    print(conselho)
                    break

                elif 'notícias' in query or 'fale as ultimas notícias' in query:
                    speak(engine, f"Estou lendo as últimas notícias.")
                    news = get_latest_news()
                    noticia = tradutor.translate(news)
                    speak(engine, news)
                    speak(engine, "Estou printando na tela.")
                    print(news, sep='\n')
                    break

                #elif 'clima' in query or 'como está o clima' in query:
                #    ip_address = find_my_ip()
                #    city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                #    speak(engine, f"Procurando o relatório do tempo de {city}.")
                #    weather, temperature, feels_like = get_weather_report(city)
                #    speak(engine,
                #        f"A temperatura atual é {temperature}, com a sensação térmica de {feels_like}")
                #    speak(engine, f"Também, é falado no relatório que {weather}")
                #    speak(engine, "Estou printando na tela.")
                #    print(
                #        f"Descrição: {weather}\n Temperatura: {temperature}\n Sensação: {feels_like}")
                #    break

                elif 'clima' in query or 'como está o clima' in query:
                    city = "Vitória"
                    
                    speak(engine, f"Procurando o relatório do tempo para {city}.")
                    
                    weather, temperature, feels_like = get_weather_report(city)
                    
                    speak(engine, f"A temperatura atual é {temperature}, com sensação térmica de {feels_like}.")
                    speak(engine, f"No relatório do clima, consta que {tradutor.translate(weather)}.")
                    speak(engine, "Estou printando na tela.")
                    
                    print(f"Descrição: {weather}\nTemperatura: {temperature}°\nSensação: {feels_like}°")
                    break

                elif 'sorteio' in query:
                    speak(engine, 'De quanto a quanto?')
                    while True:
                        query = take_user_input(engine).lower()
                        lims = query.split()
                        if len(lims) > 0:

                            try:
                                inf = int(lims[1])
                                sup = int(lims[3])

                                num = randint(inf, sup)
                                speak(engine, f"Seu número é {num}")
                                print(num)
                                break
                            except ValueError:
                                speak("Desculpe, não consegui entender os números. Certifique-se de que você forneceu números válidos.")
                        
                        else:
                            #set_oracle(oracle,3)
                            speak("Desculpe, não consegui entender os números. Certifique-se de que você forneceu números válidos.")
                    break


                
                elif 'sair' in query:
                    exit()

                elif query != None:
                    speak(engine,
                        'Desculpe, não consegui entender. Você poderia repetir?')

if __name__ == '__main__':
    main()

# variação de volume 
