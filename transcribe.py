from pydub import AudioSegment
import os
import tempfile
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path, include_timestamps=False):
    transcript = ""
    try:
        file_extension = os.path.splitext(file_path)[-1].replace(".", "").lower()
        audio = AudioSegment.from_file(file_path, format=file_extension)

        max_file_size = 25 * 1024 * 1024  # 25 MB in bytes
        chunk_length_ms = (max_file_size // (audio.frame_rate * audio.sample_width)) * 1000  # duration in ms

        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                chunk.export(temp_file.name, format="mp3")
                with open(temp_file.name, 'rb') as audio_file:
                    if include_timestamps:
                        response = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            response_format="verbose_json",
                            timestamp_granularities=["word"]
                        )
                        words = response.to_dict()['words']
                        for word_info in words:
                            start = word_info['start']
                            word = word_info['word']
                            transcript += f"[{start:.2f}] {word} "
                    else:
                        response = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            response_format="text"
                        )
                        transcript += response
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

def main(speech_file, create_summary_flag, include_timestamps):
    full_transcription = transcribe_audio(speech_file, include_timestamps)
    
    if create_summary_flag:
        summary = create_summary(full_transcription)
        with open("summary.txt", "w") as file:
            file.write(summary)
    
    with open("transcription.txt", "w") as file:
        file.write(full_transcription)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe an audio file using OpenAI's Speech-to-Text API and optionally create a summary")
    parser.add_argument("path", help="File path for the audio file to be transcribed")
    parser.add_argument("--sum", action="store_true", help="Flag to indicate if a summary should be created")
    parser.add_argument("--time", action="store_true", help="Flag to indicate if timestamps should be included")
    args = parser.parse_args()

    main(args.path, args.sum, args.time)
