from wave import open 
from struct import Struct
from math import floor

frame_rate = 11025 # 每秒采样率
# 告诉我们每秒有多少次我们想要有一个值，告诉我们声音的波型是如何变化的
# 采样率越高，声音就越清晰，但文件也越大

def encode(x):
    """
    Encode a float x between -1 and 1 as two bytes.
    """
    i = int(16384 * x)
    return Struct('h').pack(i)

def play(sampler, name='song.wav', seconds=8):
    """
    使用sampler生成一个持续时间为seconds的音频文件，命名为song.wav
    sampler是一个函数，它将描述我们试图生成的歌曲的波型
    """
    out_file = open(name, 'wb')
    out_file.setnchannels(1) # 单声道
    out_file.setsampwidth(2) # 每个采样点占用2
    out_file.setframerate(frame_rate) # 采样率
    t = 0 # song.wav的起始点
    while t < seconds * frame_rate: # 采样率乘以持续时间，告诉我们总共有多少个采样点
        sample = sampler(t)
        out_file.writeframes(encode(sample))
        t = t + 1
    out_file.close() # 关闭文件
    
def tri(frequency, amplitude=0.7):
    """
    使用形式参数frequency和amplitude振幅创建一个三角波发生器
    """
    period = floor(frame_rate / frequency) # 计算周期，告诉我们每隔多少个采样点我们就会回到波的起点
    # 举例来说，如果频率是440赫兹，采样率是11025赫兹，那么周期就是25，这意味着每隔25个采样点我们就会回到波的起点
    def sampler(t):
        save_wave = t / period - floor(t / period + 0.5) # 计算t值在周期内的位置，告诉我们当前采样点在波的哪个位置
        # 举个例子，如果t是0，那么save_wave就是0，告诉我们我们在波的起点；如果t是period/2，那么save_wave就是0.5，告诉我们我们在波的中点；如果t是period，那么save_wave又回到了0，告诉我们我们又回到了波的起点
        # sampler函数接受t值，构建锯齿波，计算锯齿波的绝对值，并将其锁放到【-1，1】范围内
        # 三角波的中点就是1，起点和终点都是-1
        tri_wave = 2 * abs(2 * save_wave) - 1
        return amplitude * tri_wave # 将三角波的振幅调整到我们想要的水平
    return sampler


c_frequency = 261.63 # C4音符的频率
e_frequency = 329.63 # E4音符的频率
delta = (e_frequency - c_frequency) / 2 
d_frequency = c_frequency + delta # D4音符的频率
g_frequency = 392.00 # G4音符的频率
low_g_frequency = 196.00 # G3音符的频率
a_frequency = g_frequency + delta # A4音符的频率
b_frequency = g_frequency + delta * 2 # B4音符的频率
low_a_frequency = a_frequency / 2 # A3音符的频率
low_b_frequency = b_frequency / 2 # B3音符的频率


def both(f,g):
    """
    创建一个播放器可以播放和弦
    """
    # 这个函数接受两个sampler函数，并返回一个新的sampler函数，这个新的sampler函数在每个采样点上调用这两个sampler函数，并将它们的结果相加
    return lambda t : f(t) + g(t)

def note(f, start, end, fade=0.01):
    """
    创建一个播放器可以在特定时间段内播放一个音符
    """
    def sampler(t):
        seconds = t / frame_rate # 将当前的时间步转化为秒为单位
        if seconds < start:
            return 0
        elif seconds > end:
            return 0
        elif seconds < start + fade:
            # 在音符开始的前fade秒内，逐渐增加音量
            return f(t) * (seconds - start) / fade
        elif seconds > end - fade:
            # 在音符结束的前fade秒内，逐渐减少音量
            return f(t) * (end - seconds) / fade
        else:
            return f(t)
    return sampler

def mario_at(octave):
    c = tri(c_frequency * octave)
    e = tri(e_frequency * octave)
    g = tri(g_frequency * octave)
    low_g = tri(low_g_frequency * octave)
    return mario(c, e, g, low_g)

def mario(c, e, g, low_g):
    z = 0
    song = note(e, z, z + 1/8)
    z = z + 1/8
    song = both(song, note(e, z, z + 1/8))
    z = z + 1/4
    song = both(song, note(e, z, z + 1/8))
    z = z + 1/4
    song = both(song, note(c, z, z + 1/8))
    z = z + 1/8
    song = both(song, note(e, z, z + 1/8))
    z = z + 1/4
    song = both(song, note(g, z, z + 1/4))
    z = z + 1/2
    song = both(song, note(low_g, z, z + 1/4))
    z = z + 1/2
    return song

def mysong_at(octave):
    e = tri(e_frequency * octave)
    d = tri(d_frequency * octave)
    c = tri(c_frequency * octave)
    low_b = tri(low_b_frequency * octave)
    low_a = tri(low_a_frequency * octave)
    g = tri(g_frequency * octave)
    return mysong(e, d, c, low_b, low_a, g)

def mysong(e, d, c, low_b, low_a, g):
    """
    演奏《爱的回归心线》高潮部分
    在爱的回归线，又期待会相见，天会晴心会暖 阳光在手指间
    """
    z = 1/4
    song = note(e, z, z + 1/4)
    z = z + 1/4
    song = both(song, note(d, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(c, z, z + 1/4))
    z = z + 1/4

    song = both(song, note(e, z, z + 1/2))
    z = z + 1/2 + 1/4
    song = both(song, note(c, z, z + 1/8))
    z = z + 1/8
    song = both(song, note(d, z, z + 1/8 + 1/4))
    z = z + 1/8 + 1/4

    song = both(song, note(d, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(c, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(low_b, z, z + 1/4))
    z = z + 1/4

    song = both(song, note(d, z, z + 1/2))
    z = z + 1/2 + 1/4
    song = both(song, note(low_b, z, z + 1/8))
    z = z + 1/8
    song = both(song, note(c, z, z + 1/8 + 1/4))
    z = z + 1/8 + 1/4

    song = both(song, note(e, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(d, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(c, z, z + 1/4))
    z = z + 1/4

    song = both(song, note(d, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(c, z, z + 1/8))
    z = z + 1/8
    song = both(song, note(low_a, z, z + 1/8 + 1/4))
    z = z + 1/2
    song = both(song, note(c, z, z + 1/8))
    z = z + 1/8

    song = both(song, note(low_b, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(g, z, z + 1/8))
    z = z + 1/8
    song = both(song, note(g, z, z + 1/8 + 1/8))
    z = z + 1/8 + 1/8
    song = both(song, note(d, z, z + 1/4))
    z = z + 1/4
    song = both(song, note(e, z, z + 1/8))
    z = z + 1/8

    song = both(song, note(e, z, z + 1))
    return song

# mario_song_low = mario_at(0.5)
# mario_song = mario_at(1)
# play(both(mario_song_low, mario_song), 'mario.wav', 2)

song = mysong_at(1)
song_high = mysong_at(2)

play(both(song, song_high), 'mysong.wav', 8)