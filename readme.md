# Video Clip Divider  - Reels & Tiktok
## Overview 
The Video Clip Divider is a Python script designed to split longer videos into shorter clips that are perfect for platforms that only allow limited time lenghts like Instagram Reels and TikTok. The script allows users to specify the duration of each clip (part) and handles the division process efficiently, making it easy to create multiple segments from a single edited video.

## Features
- Divides a long video into multiple shorter clips. 
- Allows configuration persistence through a JSON file (`userConfig.json`). 
- Option to save and load user configuration for clip duration, warning messages, and naming conventions. 
- Provides warnings if the video duration is not evenly divisible by the clip duration. 
- Colored terminal output for better readability of messages and warnings.  
## Requirements
- Python 3.x 
- ffmpeg-python library 
- ffmpeg installed on your system  
- ## Installation
1. Ensure you have Python 3.x installed. 
2. Install the required library: `$ pip install ffmpeg-python`
3. Ensure `ffmpeg` is installed and accessible from the command line.

## Usage

1. Run the script:
```shell
$ python video_clip_divider.py
```
2. Follow the on-screen prompts to provide the path to the video file, clip duration, and configuration options.

### Example

1. Provide the path to the video file to divide:
```Shell
PATH to video file to divide > /path/to/video.mp4
```
2. Specify the clip duration (in seconds):
```Shell
Clip duration? (Seconds) > 30
```
3. Choose whether to load the default user configuration:
```Shell
Load default user configuration Y/N ? > N
```
4. Set the persistence option:
```Shell
Should sacrifice start/end clips if the video can not be exactly cropped Y/N ? > Y
```
5. Set the warning option:
```Shell
Should it raise warnings about duration Y/N ? > Y
```
6. Set the naming convention for output files:
```Shell
Output files will be named <NAME>
# Give <NAME> or leave empty for single numeration: 
```
7. Choose whether to save the configuration as default:
```Shell
Save persistence/warn/naming as default? Y/N ? > Y
```

## Configuration

The script creates a `userConfig.json` file to store user preferences for persistence, warnings, and naming conventions. This file is automatically loaded if it exists, and the user has the option to overwrite it.

## Note

To change the default configuration, delete the `userConfig.json` file manually.

## Credits
The Trim version is a modified version of the trim method shown on:
https://github.com/CodingWith-Adam/trim-videos-with-ffmpeg-python
That @CodingWith-Adam does a great job explaining in his youtube channel.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.