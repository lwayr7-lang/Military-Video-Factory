import os, requests, random, asyncio
from g4f.client import Client
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

# 1. جلب لقطات احترافية من Pexels
def get_raw_videos():
    api_key = os.getenv('PEXELS_API_KEY')
    headers = {"Authorization": api_key}
    # البحث عن لقطات حربية، طائرات، أو عمليات ليلية
    queries = ['military cinematic', 'soldier mission', 'fighter jet', 'night vision warfare']
    q = random.choice(queries)
    url = f"https://api.pexels.com/videos/search?query={q}&per_page=15&orientation=landscape"
    r = requests.get(url, headers=headers).json()
    if not os.path.exists("temp"): os.makedirs("temp")
    for i, v in enumerate(r['videos']):
        v_url = v['video_files'][0]['link']
        with open(f"temp/v{i}.mp4", 'wb') as f:
            f.write(requests.get(v_url).content)

# 2. كتابة سيناريو فيلم طويل بالذكاء الاصطناعي
def get_story():
    client = Client()
    prompt = "Write a 600-word intense military mission briefing. Make it cinematic, realistic, and professional. English language."
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

# 3. تحويل النص لصوت سينمائي (روبوت صوتي متطور)
async def make_audio(text):
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("mission_audio.mp3")

# 4. المونتاج والدمج (الإنتاج النهائي)
def assemble_video():
    clips = [VideoFileClip(f"temp/{f}") for f in os.listdir("temp") if f.endswith(".mp4")]
    audio = AudioFileClip("mission_audio.mp3")
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # تكرار الفيديو إذا كان الصوت أطول من اللقطات المتاحة
    if final_clip.duration < audio.duration:
        final_clip = concatenate_videoclips([final_clip] * int(audio.duration/final_clip.duration + 1))
    
    final_video = final_clip.set_audio(audio).set_duration(audio.duration)
    # إخراج الفيديو النهائي
    final_video.write_videofile("final_mission_video.mp4", fps=24, codec="libx264", audio_codec="aac")

# تشغيل "المصنع" بالترتيب
get_raw_videos()
story = get_story()
asyncio.run(make_audio(story))
assemble_video()
