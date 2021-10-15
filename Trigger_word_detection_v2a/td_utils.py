{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4d828f9c-c953-4f05-995f-babbf90d57c7",
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "from scipy.io import wavfile\n",
    "import os\n",
    "from pydub import AudioSegment\n",
    "\n",
    "# Calculate and plot spectrogram for a wav audio file\n",
    "def graph_spectrogram(wav_file):\n",
    "    rate, data = get_wav_info(wav_file)\n",
    "    nfft = 200 # Length of each window segment\n",
    "    fs = 8000 # Sampling frequencies\n",
    "    noverlap = 120 # Overlap between windows\n",
    "    nchannels = data.ndim\n",
    "    if nchannels == 1:\n",
    "        pxx, freqs, bins, im = plt.specgram(data, nfft, fs, noverlap = noverlap)\n",
    "    elif nchannels == 2:\n",
    "        pxx, freqs, bins, im = plt.specgram(data[:,0], nfft, fs, noverlap = noverlap)\n",
    "    return pxx\n",
    "\n",
    "# Load a wav file\n",
    "def get_wav_info(wav_file):\n",
    "    rate, data = wavfile.read(wav_file)\n",
    "    return rate, data\n",
    "\n",
    "# Used to standardize volume of audio clip\n",
    "def match_target_amplitude(sound, target_dBFS):\n",
    "    change_in_dBFS = target_dBFS - sound.dBFS\n",
    "    return sound.apply_gain(change_in_dBFS)\n",
    "\n",
    "# Load raw audio files for speech synthesis\n",
    "def load_raw_audio(path):\n",
    "    activates = []\n",
    "    backgrounds = []\n",
    "    negatives = []\n",
    "    for filename in os.listdir(path + \"activates\"):\n",
    "        if filename.endswith(\"wav\"):\n",
    "            activate = AudioSegment.from_wav(path + \"activates/\" + filename)\n",
    "            activates.append(activate)\n",
    "    for filename in os.listdir(path + \"backgrounds\"):\n",
    "        if filename.endswith(\"wav\"):\n",
    "            background = AudioSegment.from_wav(path + \"backgrounds/\" + filename)\n",
    "            backgrounds.append(background)\n",
    "    for filename in os.listdir(path + \"negatives\"):\n",
    "        if filename.endswith(\"wav\"):\n",
    "            negative = AudioSegment.from_wav(path + \"negatives/\" + filename)\n",
    "            negatives.append(negative)\n",
    "    return activates, negatives, backgrounds"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
