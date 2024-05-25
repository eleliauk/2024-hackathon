import time
import sound
import Decoder
import threading

bpm = 25

# 时间每十六分音符
tps = 60/ bpm / 16

decoder = Decoder.Decoder("scores/in.info")
sound = sound.sound()
bt = decoder.beat

for x in bt:

    for j in x:
        time.sleep(tps)
        for t in j:
            sound.playSoundScapebyName(t[0],t[1])

            # threading.Thread(target= sound.playSoundScapebyName, args =(t[0],t[1])).start()