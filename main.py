import os
import ffmpeg
import json
import math

def view():
    # Scape codes for colored test
    DefA = "\u001b[0m"
    Fred = "\u001b[31m"
    YWarn = "\u001b[33m"
    BInfo = "\u001b[34m"
    
    path = input("PATH to video file to divide > ")
    duration = int(input("Clip duration? (Seconds) > "))
    if os.path.exists("userConfig.json"):
        loadConfig = input("Load default user configuration Y/N ? > ")
        if loadConfig.upper() == "Y":
            with open('userConfig.json') as confFile:
                Confdata = json.load(confFile)
                persistence = Confdata["persistence"]
                warn = Confdata["warn"]
                naming = Confdata["naming"]
    else:
        persistence = input("Should sacrifice start/end clips if the video can not be exactly cropped Y/N ? > ")
        warn = input("Should it raise warnings about duration Y/N ? > ")
        naming = input("Output files will be named  <NAME>#, give <NAME> or leave empty for single numeration: ")
    
    persistence = True if persistence == "Y" or persistence == True else False
    warn = True if warn == "Y" or warn == True else False
    
    Confdata = {'persistence': persistence, 'warn': warn, 'naming': naming}
    
    print(BInfo + "Note: To change default config, delete 'userConfig.json' manually :) " + DefA)
    if not os.path.exists("userConfig.json"):
        
        saving = input(BInfo + "Save persistence/warn/naming as default? Y/N ? > " + DefA)
        if saving.upper() == "Y":
            with open('userConfig.json', 'w') as confFile:
                json.dump(Confdata, confFile)
    
    input_stream = getInputStream(path)
    videoLength = getDuration(path)
    
    if not persistence and (videoLength % duration) != 0:
        print(f"{Fred}No can't do, disable persistence or make sure that video duration can be exactly divisible in {duration}{DefA}")
    else:
        makeClips(path, duration, naming, warn)
    
    return None

def makeClips(path, duration, naming, warn):
    # Scape codes:
    YWarn = "\u001b[33m"
    BInfo = "\u001b[34m"
    DefA = "\u001b[0m"
    PSum = "\u001b[35m"
    
    input_stream = getInputStream(path)
    videoLength = getDuration(path)
    
    # Calculate number of clips:
    clipsNo = math.ceil(videoLength / duration)
    
    # Calculate remainder:
    theoretical = videoLength * clipsNo
    startOfLast = (clipsNo - 1) * duration
    remainder = videoLength - startOfLast
    
    if warn and ((videoLength % duration) != 0):
        print(f"{YWarn}Your video WILL not be evenly divided, last clip will have duration of {remainder} seconds!{DefA}")
    
    clipping = []
    for i in range(clipsNo):
        # Make a list of start and end times:
        if i == 0: 
            start = 0
            end = duration
        else:
            start = clipping[i-1][1]
            end = start + duration
            if (end) > videoLength:
                end = videoLength - 0.01
                round(end, 2)
        clipTimes = (start, end, i)
        clipping.append(clipTimes)

    summary = []
    for clip in clipping:
        numb = clip[2]
        clipName = str(naming) + str(numb)
        trimStart = clip[0]
        trimEnd = clip[1]
        verbose = trim(path, clipName, trimStart, trimEnd)
        print(verbose)
        summary.append(verbose)
        
    print(PSum + "Summary of outputs: ")
    print("*" * 70)
    for line in summary: 
        print(BInfo+ line)
    
    return None

def trim(path, out_file, start, end):
    '''Note, this is a modified version of: https://github.com/CodingWith-Adam/trim-videos-with-ffmpeg-python,
    which CodingWith-Adam does a great work explaining in his YT channel.'''
    
    if os.path.exists(out_file):
        os.remove(out_file)

    input_stream = getInputStream(path)
    in_file_duration = getDuration(path)
    print(in_file_duration)

    pts = "PTS-STARTPTS"
    video = input_stream.trim(start=start, end=end).setpts(pts)
    audio = (input_stream
             .filter_("atrim", start=start, end=end)
             .filter_("asetpts", pts))
    video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
    out_fileMP4 = str(out_file + ".mp4")
    output = ffmpeg.output(video_and_audio, out_fileMP4, format="mp4")
    output.run()

    out_file_probe_result = ffmpeg.probe(out_fileMP4)
    out_file_duration = out_file_probe_result.get("format", {}).get("duration", None)
    
    verbose = f"Se creo el archivo {out_file} con duración de {out_file_duration}"
    return verbose

def getDuration(path):
    in_file_probe_result = ffmpeg.probe(path)
    in_file_duration = float(in_file_probe_result.get("format", {}).get("duration", None))
    if in_file_duration is None:
        raise Exception("Video duration UNKNOWN, failed to process")
    else:
        return in_file_duration

def getInputStream(path):
    try:
        input_stream = ffmpeg.input(path)
        return input_stream
    except:
        raise Exception("PATH should INCLUDE the video such as C:/user/videos/ThatVideo.mp4")

if __name__ == "__main__":
    view()
