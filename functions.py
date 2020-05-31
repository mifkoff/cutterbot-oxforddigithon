import re

import html2text
import requests
import trafilatura

import config
import content
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from fuzzywuzzy import process
from moviepy.editor import *
import time
import tldextract
from gtts import gTTS
from numpy import log as ln
from pydub import AudioSegment
from langdetect import detect
from content import url_expression, emojies, audio_file_name

youtube_video_en = 'https://www.youtube.com/watch?v=NUDMfaytP9s'
youtube_video_ru = 'https://www.youtube.com/watch?v=TgYYyingKgs'
youtube_video_korzh = 'https://www.youtube.com/watch?v=FikAr8UValg'
youtube_video_lebedev = 'https://www.youtube.com/watch?v=WNjsBSQiqjo'


def get_page_text(url):
    downloaded = trafilatura.fetch_url(url=url)
    title = downloaded[1]
    downloaded = downloaded[0]
    h = html2text.HTML2Text()
    h.ignore_links = True
    extracted_data = trafilatura.extract(downloaded)
    if extracted_data is not None:
        page_text_output = h.handle(extracted_data).replace('\n', ' ').replace('  ', ' ').strip()
        print('page_text_output len:', len(page_text_output))
        return h.handle(trafilatura.extract(downloaded)).replace('\n', ' ').replace('  ', ' ').strip(), title
    else:
        return '', ''


def is_url(url):
    if re.match(url_expression, url):
        return True
    else:
        return False


def speed_change(audio, speed=1.0):
    octaves = ln(speed)/ln(2)
    new_audio = audio._spawn(audio.raw_data, overrides={
         "frame_rate": int(audio.frame_rate * (2.0 ** octaves))
      })
    return new_audio.set_frame_rate(44100)


def get_source(url):
    return tldextract.extract(url=url).domain.capitalize()


def text_to_speech(text):
    language = detect(text=text)
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save(audio_file_name)
    pydub_audio = AudioSegment.from_mp3(audio_file_name)
    pydub_audio = pydub_audio.fade_in(2000).fade_out(3000)
    pydub_audio = speed_change(audio=pydub_audio, speed=1.25)
    pydub_audio.export(audio_file_name, format="mp3")


def get_summary(text):
    if len(text) > 0:
        r = requests.post(
            "https://api.deepai.org/api/summarization",
            data={
                'text': text,
            },
            headers={'api-key': config.deepai_api_key}
        )
        print('len:', len(r.json()['output']))
        return str(r.json()['output'])
    else:
        return False


def video_id_extractor(url):
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0].split('&')[0]
    elif 'youtube.com' in url:
        return url.split('/watch?v=')[-1].split('?')[0].split('&')[0]
    else:
        return False


def get_subclips_list(file_name, summary_timings):
    _subclips_list = []
    for timing in summary_timings:
        _subclips_list.append(VideoFileClip(file_name, audio=True).subclip(timing['start'], timing['end']))
    return _subclips_list


def get_video_subtitles(video_id):
    subtitles = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=content.languages)
    video_text = [x['text'] for x in subtitles]
    summary_output = get_summary(text=' \n'.join(video_text))
    summary_output_list = summary_output.split('\n')
    summary_timings = []
    for phrase in summary_output_list:
        match_phrase = process.extractOne(query=phrase, choices=video_text)
        for timecode in subtitles:
            if timecode['text'] == match_phrase[0]:
                summary_timings.append({
                    'start': timecode['start'],
                    'end': timecode['start'] + timecode['duration']
                })
    print('video_id:', video_id)
    print('subtitles:', subtitles)
    print('video_text:', video_text)
    print('summary_output:', summary_output)
    return summary_timings  # TODO separate functions


def get_video_summary(url):
    start_time = time.time()

    yt_summary_timings = get_video_subtitles(video_id=video_id_extractor(url=url))
    yt_file_name = 'youtube_video_{timestamp}.mp4'.format(
        timestamp=time.time()
    )
    yt = YouTube(url).streams[0].download()

    subclips_list = get_subclips_list(file_name=yt, summary_timings=yt_summary_timings)
    print('summary_timings:', yt_summary_timings)
    print('yt:', yt)
    print('subclips_list:', subclips_list)
    final_video = concatenate_videoclips(subclips_list)
    final_video.write_videofile('final_video.mp4',
                                codec='libx264',
                                audio_codec='aac',
                                temp_audiofile='temp-audio.m4a',
                                remove_temp=True
                                )
    print('Speed in sec:', time.time()-start_time)


def prettify_output(text):
    return text.replace('\n', '\n\n').replace('\\', '\n') + '\n\n'
