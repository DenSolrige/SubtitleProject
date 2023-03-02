from youtube_transcript_api import YouTubeTranscriptApi

video_link = "https://www.youtube.com/watch?v=JvORLgvlJ8w"
video_id = video_link.split("=")[1]
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
transcript = transcript_list.find_generated_transcript(['ja']).fetch()

text = ""

with open("parsedsubtitles/"+video_id+".txt","w",encoding="utf-8") as f:
   for line in transcript:
    f.write(line['text']+" "+str(line['start'])+" "+str(line['duration'])+"\n") 