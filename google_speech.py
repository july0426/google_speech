#coding:utf8
import requests,re,json,jsonpath,base64,subprocess,os
'''利用谷歌的语音识别接口，返回识别后的文本'''
def get_result(file_path):
    url = 'https://speech.googleapis.com/v1/speech:recognize?fields=results&key=AIzaSyBrqJW6Nj5Zha2M8hkhP4uH7yjP6nWBv3Q'
    data = {
         "config":{
          "encoding": "amr",
          "languageCode": "en-US",
          "sampleRateHertz": 8000,
          "enableWordTimeOffsets": false
         },
         "audio": {
          "content": encode_audio(file_path)
         }
    }
    res = requests.post(url,data=json.dumps(data))
def encode_audio(file_path):
    with open(file_path,'rb') as f:
        audio_content = f.read()
        return base64.b64encode(audio_content)

def cut_audio(audio_len,file_path):
    temp_file_path = file_path[:-4] + '_cut.flac'
    temp_dir_path = re.sub(r'/[\w-]+\.amr','',file_path)
    temp_dir_path += '/temp'
    print temp_dir_path
    # os.mkdir(temp_dir_path)
    print os.path.exists(temp_dir_path)
    # if not os.path.exists(temp_dir_path):
    #     os.mkdir(temp_dir_path)
    audio_len_int= int(audio_len)
    file_range = audio_len_int/60
    res_list = []
    for i in range(file_range):
        temp_file_path = temp_dir_path +'/'+ 'temp%s.flac' % i
        commond = 'ffmpeg -ss 00:%02d:00 -t 00:%02d:00 -i %s %s' % (i,i+1,file_path,temp_file_path)
        # subprocess.Popen(commond, stdout=subprocess.PIPE, shell=True)
        res_text = get_result(temp_file_path)
        res_list.append(res_text)
        print commond
    last_file = audio_len_int + 1 - file_range * 60
    temp_file_path = temp_dir_path + '/' + 'temp%s.flac' % (file_range + 1)
    commond = 'ffmpeg -ss 00:%02d:00 -t 00:%02d:00 -i %s %s' % (file_range, file_range + 1, file_path, temp_file_path)
    # subprocess.Popen(commond, stdout=subprocess.PIPE, shell=True)
    res_text = get_result(temp_file_path)
    res_list.append(res_text)

def get_audio_len(file_path):
    commond = 'ffprobe %s -print_format json -show_streams -select_streams a -hide_banner -v quiet' % file_path
    p = subprocess.Popen(commond, stdout=subprocess.PIPE, shell=True)
    js = json.loads(p.stdout.read())
    print js['streams'][0]['duration'],type(js)
    return float(js['streams'][0]['duration'])
if __name__ == '__main__':
    file_path = '/users/qiyue/myxuni/speech_caller/539.amr'
    # audio_len = float(get_audio_len(file_path))
    audio_len = 776
    if audio_len >= 60.0:
        cut_audio(audio_len,file_path)
    # cut_audio(file_path)