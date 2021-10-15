{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6d278972-fddf-4d5b-9cd4-40fb669f1216",
   "metadata": {},
   "outputs": [],
   "source": [
    "from music_utils import * \n",
    "from preprocess import * \n",
    "from tensorflow.keras.utils import to_categorical\n",
    "\n",
    "from collections import defaultdict\n",
    "from mido import MidiFile\n",
    "from pydub import AudioSegment\n",
    "from pydub.generators import Sine\n",
    "import math\n",
    "\n",
    "#chords, abstract_grammars = get_musical_data('data/original_metheny.mid')\n",
    "#corpus, tones, tones_indices, indices_tones = get_corpus_data(abstract_grammars)\n",
    "#N_tones = len(set(corpus))\n",
    "n_a = 64\n",
    "x_initializer = np.zeros((1, 1, 90))\n",
    "a_initializer = np.zeros((1, n_a))\n",
    "c_initializer = np.zeros((1, n_a))\n",
    "\n",
    "def load_music_utils(file):\n",
    "    chords, abstract_grammars = get_musical_data(file)\n",
    "    corpus, tones, tones_indices, indices_tones = get_corpus_data(abstract_grammars)\n",
    "    N_tones = len(set(corpus))\n",
    "    X, Y, N_tones = data_processing(corpus, tones_indices, 60, 30)   \n",
    "    return (X, Y, N_tones, indices_tones, chords)\n",
    "\n",
    "\n",
    "def generate_music(inference_model, indices_tones, chords, diversity = 0.5):\n",
    "    \"\"\"\n",
    "    Generates music using a model trained to learn musical patterns of a jazz soloist. Creates an audio stream\n",
    "    to save the music and play it.\n",
    "    \n",
    "    Arguments:\n",
    "    model -- Keras model Instance, output of djmodel()\n",
    "    indices_tones -- a python dictionary mapping indices (0-77) into their corresponding unique tone (ex: A,0.250,< m2,P-4 >)\n",
    "    temperature -- scalar value, defines how conservative/creative the model is when generating music\n",
    "    \n",
    "    Returns:\n",
    "    predicted_tones -- python list containing predicted tones\n",
    "    \"\"\"\n",
    "    \n",
    "    # set up audio stream\n",
    "    out_stream = stream.Stream()\n",
    "    \n",
    "    # Initialize chord variables\n",
    "    curr_offset = 0.0                                     # variable used to write sounds to the Stream.\n",
    "    num_chords = int(len(chords) / 3)                     # number of different set of chords\n",
    "    \n",
    "    print(\"Predicting new values for different set of chords.\")\n",
    "    # Loop over all 18 set of chords. At each iteration generate a sequence of tones\n",
    "    # and use the current chords to convert it into actual sounds \n",
    "    for i in range(1, num_chords):\n",
    "        \n",
    "        # Retrieve current chord from stream\n",
    "        curr_chords = stream.Voice()\n",
    "        \n",
    "        # Loop over the chords of the current set of chords\n",
    "        for j in chords[i]:\n",
    "            # Add chord to the current chords with the adequate offset, no need to understand this\n",
    "            curr_chords.insert((j.offset % 4), j)\n",
    "        \n",
    "        # Generate a sequence of tones using the model\n",
    "        _, indices = predict_and_sample(inference_model)\n",
    "        indices = list(indices.squeeze())\n",
    "        pred = [indices_tones[p] for p in indices]\n",
    "        \n",
    "        predicted_tones = 'C,0.25 '\n",
    "        for k in range(len(pred) - 1):\n",
    "            predicted_tones += pred[k] + ' ' \n",
    "        \n",
    "        predicted_tones +=  pred[-1]\n",
    "                \n",
    "        #### POST PROCESSING OF THE PREDICTED TONES ####\n",
    "        # We will consider \"A\" and \"X\" as \"C\" tones. It is a common choice.\n",
    "        predicted_tones = predicted_tones.replace(' A',' C').replace(' X',' C')\n",
    "\n",
    "        # Pruning #1: smoothing measure\n",
    "        predicted_tones = prune_grammar(predicted_tones)\n",
    "        \n",
    "        # Use predicted tones and current chords to generate sounds\n",
    "        sounds = unparse_grammar(predicted_tones, curr_chords)\n",
    "\n",
    "        # Pruning #2: removing repeated and too close together sounds\n",
    "        sounds = prune_notes(sounds)\n",
    "\n",
    "        # Quality assurance: clean up sounds\n",
    "        sounds = clean_up_notes(sounds)\n",
    "\n",
    "        # Print number of tones/notes in sounds\n",
    "        print('Generated %s sounds using the predicted values for the set of chords (\"%s\") and after pruning' % (len([k for k in sounds if isinstance(k, note.Note)]), i))\n",
    "        \n",
    "        # Insert sounds into the output stream\n",
    "        for m in sounds:\n",
    "            out_stream.insert(curr_offset + m.offset, m)\n",
    "        for mc in curr_chords:\n",
    "            out_stream.insert(curr_offset + mc.offset, mc)\n",
    "\n",
    "        curr_offset += 4.0\n",
    "        \n",
    "    # Initialize tempo of the output stream with 130 bit per minute\n",
    "    out_stream.insert(0.0, tempo.MetronomeMark(number=130))\n",
    "\n",
    "    # Save audio stream to fine\n",
    "    mf = midi.translate.streamToMidiFile(out_stream)\n",
    "    mf.open(\"output/my_music.midi\", 'wb')\n",
    "    mf.write()\n",
    "    print(\"Your generated music is saved in output/my_music.midi\")\n",
    "    mf.close()\n",
    "    \n",
    "    # Play the final stream through output (see 'play' lambda function above)\n",
    "    # play = lambda x: midi.realtime.StreamPlayer(x).play()\n",
    "    # play(out_stream)\n",
    "    \n",
    "    return out_stream\n",
    "\n",
    "\n",
    "def predict_and_sample(inference_model, x_initializer = x_initializer, a_initializer = a_initializer, \n",
    "                       c_initializer = c_initializer):\n",
    "    \"\"\"\n",
    "    Predicts the next value of values using the inference model.\n",
    "    \n",
    "    Arguments:\n",
    "    inference_model -- Keras model instance for inference time\n",
    "    x_initializer -- numpy array of shape (1, 1, 78), one-hot vector initializing the values generation\n",
    "    a_initializer -- numpy array of shape (1, n_a), initializing the hidden state of the LSTM_cell\n",
    "    c_initializer -- numpy array of shape (1, n_a), initializing the cell state of the LSTM_cel\n",
    "    Ty -- length of the sequence you'd like to generate.\n",
    "    \n",
    "    Returns:\n",
    "    results -- numpy-array of shape (Ty, 78), matrix of one-hot vectors representing the values generated\n",
    "    indices -- numpy-array of shape (Ty, 1), matrix of indices representing the values generated\n",
    "    \"\"\"\n",
    "    \n",
    "    ### START CODE HERE ###\n",
    "    pred = inference_model.predict([x_initializer, a_initializer, c_initializer])\n",
    "    indices = np.argmax(pred, axis = -1)\n",
    "    results = to_categorical(indices, num_classes=90)\n",
    "    ### END CODE HERE ###\n",
    "    \n",
    "    return results, indices\n",
    "\n",
    "\n",
    "def note_to_freq(note, concert_A=440.0):\n",
    "  '''\n",
    "  from wikipedia: http://en.wikipedia.org/wiki/MIDI_Tuning_Standard#Frequency_values\n",
    "  '''\n",
    "  return (2.0 ** ((note - 69) / 12.0)) * concert_A\n",
    "\n",
    "def ticks_to_ms(ticks, tempo, mid):\n",
    "    tick_ms = math.ceil((60000.0 / tempo) / mid.ticks_per_beat)\n",
    "    return ticks * tick_ms\n",
    "\n",
    "def mid2wav(file):\n",
    "    mid = MidiFile(file)\n",
    "    output = AudioSegment.silent(mid.length * 1000.0)\n",
    "\n",
    "    tempo = 130 # bpm\n",
    "\n",
    "    for track in mid.tracks:\n",
    "        # position of rendering in ms\n",
    "        current_pos = 0.0\n",
    "        current_notes = defaultdict(dict)\n",
    "\n",
    "        for msg in track:\n",
    "            current_pos += ticks_to_ms(msg.time, tempo, mid)\n",
    "            if msg.type == 'note_on':\n",
    "                if msg.note in current_notes[msg.channel]:\n",
    "                    current_notes[msg.channel][msg.note].append((current_pos, msg))\n",
    "                else:\n",
    "                    current_notes[msg.channel][msg.note] = [(current_pos, msg)]\n",
    "\n",
    "\n",
    "            if msg.type == 'note_off':\n",
    "                start_pos, start_msg = current_notes[msg.channel][msg.note].pop()\n",
    "\n",
    "                duration = math.ceil(current_pos - start_pos)\n",
    "                signal_generator = Sine(note_to_freq(msg.note, 500))\n",
    "                #print(duration)\n",
    "                rendered = signal_generator.to_audio_segment(duration=duration-50, volume=-20).fade_out(100).fade_in(30)\n",
    "\n",
    "                output = output.overlay(rendered, start_pos)\n",
    "\n",
    "    output.export(\"./output/rendered.wav\", format=\"wav\")"
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