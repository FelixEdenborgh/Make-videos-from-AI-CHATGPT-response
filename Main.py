import openai
import time
from PIL import Image, ImageFont, ImageDraw

from gtts import gTTS


import random
from moviepy.editor import *
import ffmpeg




openai.api_key = "Your api key here"

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text
folder = "Folder path to save the response by making it into an image"


def makeTxtFile():
    number = 0
    number = number + 1
    name = f"Daily motivation quote {number}.txt"
    prompt = "Can you give me 1 daily motivation quote?"
    response = generate_response(prompt)
    print(response)

    file_path = folder + "/" + name
    with open(file_path, "w") as file:
        file.write(response)
    time.sleep(2)


# Call to make a txt file from the quote



def ConvertToMp3():
    # path of folder containing input text files
    input_folder = folder

    # path of folder to save output mp3 files
    output_folder = "mp3 folder path for saving"

    # get list of text files in input folder
    input_files = os.listdir(input_folder)

    try:
        # open first text file in folder
        file = open(os.path.join(input_folder, input_files[0]), 'r')
        try:
            # read text from file
            text = file.read()
            # convert text to speech
            tts = gTTS(text)
        finally:
            # close the file explicitly
            file.close()

        # save speech as mp3 file in output folder
        output_file = os.path.join(output_folder, input_files[0][:-4] + '.mp3')
        tts.save(output_file)

    except IOError as e:
        print("Error: {}".format(e))


ConvertToMp3()


def get_max_line_length(lines, font):
    max_length = 0
    for line in lines:
        length = font.getlength(line)
        if length > max_length:
            max_length = length
    return max_length

def CreateAImageWithTheDailyQuoteWrittenOnIt():
    # Define input and output folders
    input_folder = folder
    output_folder = "img folder path for saving"

    # Define font and font size
    font = ImageFont.truetype("arial.ttf", 36)

    # Define max width and height of text area
    max_width, max_height = 600, 600

    # Random color number
    random_number = random.randint(0, 255)

    # Loop over input files in input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            # Read text from file
            with open(os.path.join(input_folder, filename), 'r') as file:
                text = file.read()

            # Create image with text
            image = Image.new(mode='RGB', size=(800, 600), color=(random_number, random_number, random_number))
            draw = ImageDraw.Draw(image)

            # Wrap text based on max width and height
            words = text.split(' ')
            lines = []
            line = ''
            for word in words:
                if draw.textbbox((0, 0), line + word, font=font)[2] <= max_width and \
                        draw.multiline_textbbox((0, 0), line + word, font=font)[3] <= max_height:
                    line += word + ' '
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)

            # Write wrapped text to image
            x, y = 100, 100
            for line in lines:
                draw.multiline_text((x, y), line, font=font, fill=(0, 0, 0))
                y += draw.textbbox((x, y), line, font=font)[3]

            # Save image to output folder
            output_filename = os.path.splitext(filename)[0] + ".jpg"
            output_path = os.path.join(output_folder, output_filename)
            image.save(output_path)
            file.close()

CreateAImageWithTheDailyQuoteWrittenOnIt()


def CombineImageWithMp3(number):
    # Replace the placeholder with the path to your folder
    folder_path = "mp3 folder path for reading"

    # Get the list of file names in the folder
    file_names_mp3 = os.listdir(folder_path)

    # Get the first file name in the folder (or print a message if the folder is empty)
    if len(file_names_mp3) > 0:
        first_file_name_mp3 = file_names_mp3[0]
        print("The first file name in the folder is:", first_file_name_mp3)
    else:
        print("The folder is empty.")

    # Replace the placeholder with the path to your folder
    folder_path = "img folder path for reading"

    # Get the list of file names in the folder
    file_names_image = os.listdir(folder_path)

    # Get the first file name in the folder (or print a message if the folder is empty)
    if len(file_names_image) > 0:
        first_file_name_image = file_names_image[0]
        print("The first file name in the folder is:", first_file_name_image)
    else:
        print("The folder is empty.")


    # Replace the placeholders with the paths to your image and mp3 files + getting the first file in the folder
    image_path = "image folder path" + first_file_name_image
    mp3_path = "mp3 folder path" + first_file_name_mp3

    # Name of the movie, start from 0
    string_movie = str(number)
    # Replace the placeholders with the desired output file name and extension
    output_path = f"save movei to this fodlder/{string_movie}.mp4"

    # Load the image file using ffmpeg
    input_image = ffmpeg.input(image_path)

    # Load the audio file using ffmpeg
    input_audio = ffmpeg.input(mp3_path)

    # Create the video by overlaying the image over a black background and adding the audio
    video = ffmpeg.output(input_image, input_audio, output_path, vcodec='libx264', acodec='copy', strict='experimental')

    # Run the ffmpeg command to create the video
    ffmpeg.run(video)

numbers = 0

while(True):
    makeTxtFile()
    ConvertToMp3()
    CreateAImageWithTheDailyQuoteWrittenOnIt()
    CombineImageWithMp3(numbers)
    numbers = numbers + 1
