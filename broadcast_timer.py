import pygame.mixer
import schedule
import time
import wave
import threading

#時間設定
time_list = ['08:55', '08:56', '08:57', '08:58']

#再生するWavファイル設定
wfile_list = ['okiro.wav', 'kanki.wav', 'kanki.wav', 'okiro.wav']

#アラーム処理
def Alarm(se, nn, nall):
    target_time = time_list[nn]
    target_wav = wfile_list[nn]
    print("Alerm_"+str(nn)+"  放送実施時間: "+target_time, flush=True)
    wf = wave.open(target_wav, "r")
    wav_length = float(wf.getnframes()) / wf.getframerate()
    wf.close
    pygame.mixer.init() #初期化
    pygame.mixer.music.load(target_wav) #読み込み
    pygame.mixer.music.play(1) #ループ再生（引数を1にすると1回のみ再生）
    time.sleep(wav_length + 0.25) #再生時間，待ってあげないと再生が実施されないようです．
    pygame.mixer.music.stop() #終了
    if nn >= (nall-1):
        se.set()
    

def main():
    tlist_leng = len(time_list)
    wlist_leng = len(wfile_list)

    if tlist_leng != wlist_leng:
        print("(time_list size: "+str(tlist_leng)+") != (wfile_lsit size: "+str(wlist_leng)+")" )
        exit()

    print("放送回数："+str(tlist_leng))
    print("", flush=True)

    for ii in range(tlist_leng):
        time_target = time_list[ii]
        stop_event = threading.Event()
        schedule.every().day.at(time_target).do(Alarm, stop_event, ii, tlist_leng)
 
    while not stop_event.is_set():
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
           print (e)
           exit()

    print("全放送を終了しました")



#-------------------------------------------
if __name__ == '__main__':
    main()
