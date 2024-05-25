import time
import sound
import Decoder

bpm = 15

# 时间每十六分音符
tps = 60/bpm / 16

decoder = Decoder.Decoder(r'D:\source\repos\2024Hackathon_MusicScoreMaker\2024Hackathon_MusicScoreMaker\bin\Release\net8.0-windows8.0\22-18-53_SongScore.info')
sound = sound.sound()
bt = decoder.beat
for x in bt:
    for j in x:
        time.sleep(tps)
        print(j)
        for t in j:
            sound.playSoundScapebyName(*t)
