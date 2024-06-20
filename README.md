# Voice Cloning with Coqui XTTS-v2

## Overview

This project involves the development of a voice cloning application using the XTTS-v2 model from Coqui.ai. Leveraging advanced AI models and machine learning algorithms, this application can generate highly personalized and natural-sounding synthetic voices from user-provided samples. The project demonstrates the ability to produce accurate voice replicas and highlights the potential applications and ethical considerations of voice cloning technology.

## Features

- **Upload Audio Samples**: Users can upload an audio file (in .wav format) containing the sample voice to be cloned.
- **Text-to-Speech**: Enter a string of text to be synthesized into speech using the cloned voice.
- **Language Selection**: Choose the language for the synthesized speech from a drop-down menu.
- **Voice Selection**: Select one of the uploaded audio files for cloning.
- **High-Quality Output**: Generates audio files in .wav format that accurately reproduce the entered text using the cloned voice.

## Architecture

The application operates on a two-tier architecture comprising a backend server and a frontend interface. The backend, developed with Python and a series of libraries, handles the processing and synthesis tasks, while the frontend, built with Streamlit, provides a user-friendly interface for interactions.

## Installation

Ensure to have Python 9, ffmpeg and a CUDA version of PyTorch installed

To set up the project locally, follow these steps:

1. **Clone the repository**:  
   git clone https://github.com/edoardotavassi/ACA_project.git  
   cd ACA_project

2. **Create and activate a virtual environment**:  
   python3 -m venv venv  
   source venv/bin/activate

3. **Install dependencies**:  
   pip install -r requirements.txt

## Usage
1. **Start the system**:  
   ./start.sh

2. **Stop the system**:  
   ./stop.sh

## Ethical Considerations

The development and deployment of voice cloning technology come with significant ethical considerations, including:

- **Informed Consent**: Ensure that individuals fully understand how their voice will be used, stored, and any associated risks before cloning their voice.
- **Privacy**: Implement robust encryption protocols to protect voice data both at rest and in transit, and store data in secure environments with restricted access.
- **Transparency**: Clearly inform users when they are interacting with synthetic voices.
- **Preventing Misuse**: Develop guidelines and regulations to detect synthetic voices and penalize misuse, promoting international cooperation to address global threats.

## Future Developments

Key areas for future development include:

- **Distributed Parallel Computation**: Implementing technologies like Celery to enable distributed task queues for parallel processing, improving scalability and reducing processing times.
- **Speech-to-Text Integration**: Adding a speech-to-text channel within the application framework to allow users to convert spoken input directly into text.
- **Optimization**: Enhancing the model’s ability to handle a broader range of accents and languages, and optimizing processing times.

## Contributors

- Edoardo Toma Tavassi
- Alessandro Troiano

## Acknowledgments

This project was developed as part of the Advanced Computer Architectures course under the supervision of Prof. Christian Pilato, Academic Year 2023-24.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References

- [Coqui XTTS-v2](https://huggingface.co/coqui/XTTS-v2)
- [Common Voice Dataset](https://commonvoice.mozilla.org/en/datasets)
- [SpeechBrain Speaker Verification](https://huggingface.co/speechbrain/spkrec-resnet-voxceleb)