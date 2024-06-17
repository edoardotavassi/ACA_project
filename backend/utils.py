# backend/utils.py

import numpy as np
import lameenc

def split_text(text, max_length=200):
    """
    Splits a given text into chunks of words, where each chunk has a maximum length specified by `max_length`.

    Args:
        text (str): The text to be split into chunks.
        max_length (int, optional): The maximum length of each chunk. Defaults to 200.

    Returns:
        list: A list of chunks, where each chunk is a string of words.

    Example:
        >>> text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, urna id aliquet lacinia, urna nunc tincidunt urna, nec aliquet urna urna id urna."
        >>> split_text(text, max_length=30)
        ['Lorem ipsum dolor sit amet,', 'consectetur adipiscing elit.', 'Sed euismod, urna id', 'aliquet lacinia, urna nunc', 'tincidunt urna, nec aliquet', 'urna urna id urna.']
    """
    # Split the text into individual words
    words = text.split()
    
    # Initialize variables
    current_chunk = []  # Current chunk of words
    chunks = []  # List to store the chunks
    current_length = 0  # Current length of the chunk
    
    # Iterate over each word in the text
    for word in words:
        # Check if adding the current word to the chunk exceeds the maximum length
        if current_length + len(word) + len(current_chunk) > max_length:
            # If it exceeds, add the current chunk to the list of chunks
            chunks.append(' '.join(current_chunk))
            
            # Start a new chunk with the current word
            current_chunk = [word]
            
            # Update the current length
            current_length = len(word)
        else:
            # If it doesn't exceed, add the current word to the current chunk
            current_chunk.append(word)
            
            # Update the current length
            current_length += len(word)
    
    # Add the last chunk to the list of chunks
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    # Return the list of chunks
    return chunks

def encode_wav_to_mp3(wav_data_array, sample_rate=24000):
    """
    Encodes a WAV data array to MP3 format.

    Args:
        wav_data_array (numpy.ndarray): The input WAV data array.
        sample_rate (int, optional): The sample rate of the WAV data. Defaults to 24000.

    Returns:
        bytes: The encoded MP3 data.

    """
    def float32_to_pcm16(float32_array):
        """
        Converts a float32 array to a pcm16 array.

        Args:
            float32_array (numpy.ndarray): The input float32 array.

        Returns:
            numpy.ndarray: The converted pcm16 array.

        """
        # Clip the values of the float32 array between -1.0 and 1.0
        float32_array = np.clip(float32_array, -1.0, 1.0)
        
        # Convert the float32 array to int16 array by scaling the values to the range of -32767 to 32767
        int16_array = (float32_array * 32767).astype(np.int16)
        
        # Return the converted int16 array
        return int16_array

    # Convert the float32 array to pcm16 array
    pcm16_array = float32_to_pcm16(wav_data_array)
    
    # Convert the pcm16 array to bytes
    wav_data = pcm16_array.tobytes()
    
    # Create an instance of the encoder
    encoder = lameenc.Encoder()
    
    # Set the bit rate to 128 kbps
    encoder.set_bit_rate(128)
    
    # Set the sample rate of the WAV data
    encoder.set_in_sample_rate(sample_rate)
    
    # Set the number of channels based on the shape of the WAV data array
    encoder.set_channels(1 if len(wav_data_array.shape) == 1 else wav_data_array.shape[1])
    
    # Set the quality of the encoding
    encoder.set_quality(2)

    # Encode the WAV data to MP3 format
    mp3_data = encoder.encode(wav_data)
    
    # Flush the encoder to finalize the encoding
    mp3_data += encoder.flush()

    # Return the encoded MP3 data
    return mp3_data
