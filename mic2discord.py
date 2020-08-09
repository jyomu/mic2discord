import discord
import pyaudio
import time


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content == "!join":
            if message.guild != None:
                vc = await message.guild.voice_channels[0].connect()
                source = myAudioSource()
                vc.play(source, after=lambda e: print('done', e))
        if message.content == "!down":
            await self.close()


class myAudioSource(discord.AudioSource):
    def __init__(self):
        self.p = pyaudio.PyAudio()
        print("input from:" + self.p.get_default_input_device_info()['name'])

        FORMAT = pyaudio.paInt16  # 16bit
        FRAMERATE = 48000
        self.CHUNK = 960

        self.istream = self.p.open(format=FORMAT,
                                   rate=FRAMERATE,
                                   channels=self.p.get_default_input_device_info()[
                                       'maxInputChannels'],
                                   input=True,
                                   frames_per_buffer=self.CHUNK)
        self.istream.start_stream()

    def read(self):
        return self.istream.read(self.CHUNK)

    def is_opus(self):
        return False

    def cleanup(self):
        self.istream.stop_stream()
        self.istream.close()
        self.p.terminate()


if __name__ == "__main__":
    client = MyClient()
    client.run('NzI1NTg5NTEwMzg5NDk3OTA3.XvSJhA.iAg-zwVZz1hTXOL4oe_SyO2HME0')
