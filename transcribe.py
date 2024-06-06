from pydub import AudioSegment
import os
import tempfile
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_timestamp(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def transcribe_audio(file_path):
    transcript = ""
    try:
        file_extension = os.path.splitext(file_path)[-1].replace(".", "").lower()
        audio = AudioSegment.from_file(file_path, format=file_extension)

        chunk_length_ms = 1 * 60 * 1000  # 1 minute in milliseconds
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                chunk.export(temp_file.name, format="mp3")
                with open(temp_file.name, 'rb') as audio_file:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                    timestamp = format_timestamp(i)
                    transcript_chunk = response.text if response else ""
                    transcript += f"[{timestamp}] {transcript_chunk}\n"
            os.remove(temp_file.name)
    except Exception as e:
        print(f"An error occurred: {e}")
    return transcript

def create_summary(transcription_text):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following transcription:\n\n{transcription_text}"},
            ],
            model="gpt-3.5-turbo"
        )
        summary = response.choices[0].message.content.strip() if response else "Summary generation failed."
    except Exception as e:
        print(f"An error occurred while generating the summary: {e}")
        summary = "Summary generation failed."
    return summary

def main(speech_file, create_summary_flag):
    full_transcription = transcribe_audio(speech_file)
    
    if create_summary_flag:
        summary = create_summary(full_transcription)
        with open("summary.txt", "w") as file:
            file.write(summary)
    
    with open("transcription.txt", "w") as file:
        file.write(full_transcription)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe an audio file using OpenAI's Speech-to-Text API")
    parser.add_argument("path", help="File path for the audio file to be transcribed")
    parser.add_argument("--sum", action="store_true", help="Flag to indicate if a summary should be created")
    args = parser.parse_args()

    main(args.path, args.sum)
