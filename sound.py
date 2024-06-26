# import pyaudio
import wave
import threading
import pygame
import sys
import os
import pyaudio

class sound:
    # p = pyaudio.PyAudio()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(64)
    pressDict = {i: False for i in range(36)}
    keyDict = {
        pygame.K_1: "c",
        pygame.K_2: "d",
        pygame.K_3: "e",
        pygame.K_4: "f",
        pygame.K_5: "g",
        pygame.K_6: "a",
        pygame.K_7: "b",
        pygame.K_8: "c1",
        pygame.K_9: "d1",
        pygame.K_0: "e1",
        pygame.K_MINUS: "f1",

        pygame.K_EQUALS: 'g1',
        pygame.K_q: 'a1',
        pygame.K_w: 'b1',
        pygame.K_e: 'c2',
        pygame.K_r: 'd2',
        pygame.K_t: 'e2',
        pygame.K_y: 'f2',
        pygame.K_u: 'g2',
        pygame.K_i: 'a2',
        pygame.K_o: 'b2',
        pygame.K_p: 'c3',
        pygame.K_a: 'd3',
        pygame.K_s: 'e3',
        pygame.K_d: 'f3',
        pygame.K_f: 'g3',
        pygame.K_g: 'a3',
        pygame.K_h: 'b3',

        pygame.K_j: 'c4',
        pygame.K_k: 'd4',
        pygame.K_l: 'e4',
        pygame.K_z: 'f4',
        pygame.K_x: 'g4',
        pygame.K_c: 'a4',
        pygame.K_v: 'b4',
        pygame.K_b: 'c5'

    }
    keyDict2 = {
        0: 'c',
        1: 'c#',
        2: 'd',
        3: 'd#',
        4: 'e',
        5: 'f',
        6: 'f#',
        7: 'g',
        8: 'g#',
        9: 'a',
        10: 'a#',
        11: 'b'
    }

    def playSoundScapebyName(self, pitch, town):
        s = self.keyDict2[pitch]
        filenames = []

        if town == 0:
            filenames.append("./audios/" + s + ".wav")
        elif town == 1:
            if s[-1] == '#':
                s = s[:-1] + '4#'
                t = "./audios/" + s + ".wav"
                filenames.append(t)
            else:
                t = "./audios/" + s + "4.wav"
                filenames.append(t)
        else:
            filenames.append("./audios/" + s + ".wav")
            if s[-1] == '#':
                s = s[:-1] + '4#'
                t = "./audios/" + s + ".wav"
                filenames.append(t)
            else:
                t = "./audios/" + self.keyDict2[pitch] + "4.wav"
                filenames.append(t)

        for fileName in filenames:
            if os.path.exists(fileName):
                # self.pressDict[fileName] = True
                # threading.Thread(target=self.play, args=(fileName, fileName)).start()
                sound1 = pygame.mixer.Sound(fileName)
                sound1.play()

    def playSoundScape(self, key):
        fileName = "./audios/" + str(self.keyDict[key]) + ".wav"
        if os.path.exists(fileName):
            # self.pressDict[key] = True
            # threading.Thread(target=self.play, args=(fileName, key)).start()
            sound1 = pygame.mixer.Sound(fileName)
            sound1.play()

    def stop(self):
        pygame.mixer.music.stop()

    def play(self, path, key):
        CHUNK = 1024
        # 从目录中读取语音
        wf = wave.open(path, 'rb')
        # read data
        data = wf.readframes(CHUNK)
        # 创建播放器
        p = self.p

        # 获得语音文件的各个参数
        FORMAT = p.get_format_from_width(wf.getsampwidth())
        CHANNELS = wf.getnchannels()
        RATE = wf.getframerate()
        # print(self.keyDict[key], end=' ')
        sys.stdout.flush()
        # 打开音频流， output=True表示音频输出

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        frames_per_buffer=CHUNK,
                        output=True,
                        )
        # play stream (3) 按照1024的块读取音频数据到音频流，并播放
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)
            if not self.pressDict[key]:
                break

# pygame.init()
# p = pyaudio.PyAudio()

# screen = pygame.display.set_mode((500, 304))
# pygame.display.set_caption('My-Piano')  # 设置窗口标题
# pygame.display.update()  # 显示内容


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         if event.type == pygame.KEYDOWN:
#             key = event.key
#             if (key == pygame.K_ESCAPE):
#                 pygame.quit()
#
#             elif key in keyDict.keys():
#                 fileName = "./audios/" + str(keyDict[key]) + ".wav"
#                 if os.path.exists(fileName):
#                     pressDict[key] = True
#                     threading.Thread(target=play, args=(fileName, key)).start()
#
#
#         elif event.type == pygame.KEYUP:
#             # time.sleep(0.5)
#             key = event.key
#             pressDict[key] = False
