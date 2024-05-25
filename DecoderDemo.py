import time
import sound
import Decoder

bpm = 10

# 时间每十六分音符
tps = 60/bpm / 16

decoder = Decoder.Decoder("./scores/0-58-53_SongScore.txt")
sound = sound.sound()
bt = decoder.beat
for x in bt:
    for j in x:
        time.sleep(tps)
        print(j)
        for t in j:
            sound.playSoundScapebyName(*t)
