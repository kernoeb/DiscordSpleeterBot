import asyncio, discord, os, requests, urllib.request, shutil, configparser

config = configparser.ConfigParser()
config.read('token.ini')

# TOKEN
token = config['DEFAULT']['token']

client = discord.Client()

@client.event
@asyncio.coroutine
def on_message(message):
    rep = message.content
    rep2 = rep.split()

    try:
        command = rep2[0].lower()
        params = rep2[0:]
    except IndexError:
        command = ""
        params = ""


    if command == "!split" and message.guild is not None:
        try:
            # GET PARAMS
            a = params[1] 
            music = params[2]

            try:
                os.mkdir("dl/")
            except OSError as error:
                pass

            try:
                os.mkdir("music/")
            except OSError as error:
                pass

            downloading_txt = "Downloading your file... :hourglass_flowing_sand:"
            print(downloading_txt)
            tmp = yield from message.channel.send(downloading_txt)

            # DOWNLOAD FILE
            urllib.request.urlretrieve(music, "dl/" + a + ".mp3")

            downloaded_txt = "Downloaded, please wait while spl[ee]ting your music... :hourglass:"
            print(downloaded_txt)
            yield from tmp.edit(content=downloaded_txt)

            # SPL[EE]TING
            command_os = "spleeter separate -i 'dl/{}.mp3' -o music/{}".format(a, a)
            os.system(command_os)

            spleeted_txt = "Spl[ee]ted, please wait while uploading... :hourglass:"
            print(spleeted_txt)
            yield from tmp.edit(content=spleeted_txt)

            f = "music/" + a + "/" + a + "/vocals.wav"
            f2 = "music/" + a + "/" + a + "/accompaniment.wav"

            # POST FILES
            files = {'file': ('vocals.wav', open(f, 'rb')),}
            response = requests.post('https://0x0.st/', files=files)

            vocals_uploaded_txt = "Vocals uploaded, please wait while uploading accompaniments... :hourglass:"
            print(vocals_uploaded_txt)
            yield from tmp.edit(content=vocals_uploaded_txt)

            files = {'file': ('accompaniment.wav', open(f2, 'rb')),}
            response2 = requests.post('https://0x0.st/', files=files)

            # SEND LINKS
            final_message = "Vocals: {}\nAccompaniments: {}".format(response.text, response2.text)
            yield from message.channel.send(final_message)
            yield from tmp.delete()

            os.remove("dl/" + a + ".mp3")
            shutil.rmtree("music/" + a)

        except IndexError:
            yield from message.channel.send("Erreur!")


client.run(token)