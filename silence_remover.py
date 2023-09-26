import argparse
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm  # Import tqdm for the progress bar
from colorama import Fore, Style  # Import colorama for text colors
import time  # Import the time module for measuring processing time

# Define ANSI escape codes for text colors
RED_TEXT = "\033[91m"
GREEN_TEXT = "\033[92m"
RESET_TEXT = "\033[0m"

# ...

def remove_silence_audio(input_audio, output_audio_path, silence_threshold=90, min_silence_duration=10):

    # Record the start time
    start_time = time.time()
    
    # Load the audio file using pydub
    audio_data = AudioSegment.from_file(input_audio)

    # Get the original audio length in seconds
    original_length_seconds = len(audio_data) / 1000.0

    # Split the audio on silence
    non_silent_audio = split_on_silence(audio_data, silence_thresh=-silence_threshold, min_silence_len=min_silence_duration, keep_silence=False)


   # Initialize a counter for chunks (cuts)
    cut_count = 0

    # Concatenate the non-silent audio segments
    result_audio = AudioSegment.empty()
    for chunk in tqdm(non_silent_audio, unit="chunk", ascii=False, ncols=100):
        if chunk.duration_seconds < min_silence_duration / 1000:
            # Skip short non-silent chunks
            continue

        result_audio += chunk
        cut_count += 1

    # Export the processed audio as the specified format (mp3, wav, etc.)
    result_audio.export(output_audio_path, format="wav")

     # Calculate the total time cut in seconds
    total_time_cut_seconds = original_length_seconds - (len(result_audio) / 1000.0)

        # Calculate the processing time in seconds
    processing_time = time.time() - start_time

        # Print the processing time in seconds
    print(f"Processing time: {processing_time:.2f} seconds")

     # Print a completion message
    print("Audio processing complete. Output saved to:", output_audio_path)

    # Print the original audio length in red
    print(f"{Fore.RED}Original audio length: {original_length_seconds:.2f} seconds{Style.RESET_ALL}")

    # Print the new length after removing silence
    print(f"New audio length after removing silence: {(len(result_audio) / 1000.0):.2f} seconds")

    # Print the number of cuts (times the silence threshold is met)
    print(f"{Fore.GREEN}Number of audio cuts (silence threshold met):", cut_count)
    
    # Print the total time cut in green
    print(f"Total time cut: {total_time_cut_seconds:.2f} seconds{Style.RESET_ALL}")



def remove_silence_from_file(input_path, output_path, silence_threshold=100, min_silence_duration=10):
    _, extension = os.path.splitext(input_path)

    if extension.lower() == ".mp3" or extension.lower() == ".wav":
        # Process audio file
        remove_silence_audio(input_path, output_path, silence_threshold, min_silence_duration)
    else:
        print("Unsupported file format.")



def main():
    parser = argparse.ArgumentParser(description="Remove silence from audio or video files.")
    parser.add_argument("input_file", help="Input audio or video file to process")
    parser.add_argument("output_file", help="Output file where processed audio or video will be saved")
    parser.add_argument("--threshold", type=int, default=90, help="Silence threshold in dBFS (default: 100)")
    parser.add_argument("--min_silence", type=int, default=10, help="Minimum silence gap duration (default: 10ms)")
    args = parser.parse_args()

    # Remove silence from the input file and save to the output file
    remove_silence_from_file(args.input_file, args.output_file, args.threshold, args.min_silence)

if __name__ == "__main__":
    main()
