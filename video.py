from kivy.uix.videoplayer import VideoPlayer
import m3u8
import requests
#http://bsn246u6-i.akamaihd.net/hls/live/237201/Live2N24CMS/03.m3u8

m3u8_obj = m3u8.load('http://bsn246u6-i.akamaihd.net/hls/live/237201/Live2N24CMS/03.m3u8')
print str(m3u8_obj)
print m3u8_obj.segments
print m3u8_obj.target_duration
t = requests.get('http://bsn246u6-i.akamaihd.net/hls/live/237201/Live2N24CMS/20161004T125034-03-227477.ts')
print t

player = VideoPlayer(source='http://bsn246u6-i.akamaihd.net/hls/live/237201/Live2N24CMS/20161004T125034-03-227630.ts')
player.state = 'play'