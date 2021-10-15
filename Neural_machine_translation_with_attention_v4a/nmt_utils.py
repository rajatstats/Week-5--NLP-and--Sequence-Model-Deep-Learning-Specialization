{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7c4ae940-8090-4289-b269-96ee9a08691e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from faker import Faker\n",
    "import random\n",
    "from tqdm import tqdm\n",
    "from babel.dates import format_date\n",
    "from tensorflow.keras.utils import to_categorical\n",
    "import tensorflow.keras.backend as K\n",
    "from tensorflow.keras.models import Model\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "fake = Faker()\n",
    "Faker.seed(12345)\n",
    "random.seed(12345)\n",
    "\n",
    "# Define format of the data we would like to generate\n",
    "FORMATS = ['short',\n",
    "           'medium',\n",
    "           'long',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'full',\n",
    "           'd MMM YYY', \n",
    "           'd MMMM YYY',\n",
    "           'dd MMM YYY',\n",
    "           'd MMM, YYY',\n",
    "           'd MMMM, YYY',\n",
    "           'dd, MMM YYY',\n",
    "           'd MM YY',\n",
    "           'd MMMM YYY',\n",
    "           'MMMM d YYY',\n",
    "           'MMMM d, YYY',\n",
    "           'dd.MM.YY']\n",
    "\n",
    "# change this if you want it to work with another language\n",
    "LOCALES = ['en_US']\n",
    "\n",
    "def load_date():\n",
    "    \"\"\"\n",
    "        Loads some fake dates \n",
    "        :returns: tuple containing human readable string, machine readable string, and date object\n",
    "    \"\"\"\n",
    "    dt = fake.date_object()\n",
    "\n",
    "    try:\n",
    "        human_readable = format_date(dt, format=random.choice(FORMATS),  locale='en_US') # locale=random.choice(LOCALES))\n",
    "        human_readable = human_readable.lower()\n",
    "        human_readable = human_readable.replace(',','')\n",
    "        machine_readable = dt.isoformat()\n",
    "        \n",
    "    except AttributeError as e:\n",
    "        return None, None, None\n",
    "\n",
    "    return human_readable, machine_readable, dt\n",
    "\n",
    "def load_dataset(m):\n",
    "    \"\"\"\n",
    "        Loads a dataset with m examples and vocabularies\n",
    "        :m: the number of examples to generate\n",
    "    \"\"\"\n",
    "    \n",
    "    human_vocab = set()\n",
    "    machine_vocab = set()\n",
    "    dataset = []\n",
    "    Tx = 30\n",
    "    \n",
    "\n",
    "    for i in tqdm(range(m)):\n",
    "        h, m, _ = load_date()\n",
    "        if h is not None:\n",
    "            dataset.append((h, m))\n",
    "            human_vocab.update(tuple(h))\n",
    "            machine_vocab.update(tuple(m))\n",
    "    \n",
    "    human = dict(zip(sorted(human_vocab) + ['<unk>', '<pad>'], \n",
    "                     list(range(len(human_vocab) + 2))))\n",
    "    inv_machine = dict(enumerate(sorted(machine_vocab)))\n",
    "    machine = {v:k for k,v in inv_machine.items()}\n",
    " \n",
    "    return dataset, human, machine, inv_machine\n",
    "\n",
    "def preprocess_data(dataset, human_vocab, machine_vocab, Tx, Ty):\n",
    "    \n",
    "    X, Y = zip(*dataset)\n",
    "    \n",
    "    X = np.array([string_to_int(i, Tx, human_vocab) for i in X])\n",
    "    Y = [string_to_int(t, Ty, machine_vocab) for t in Y]\n",
    "    \n",
    "    Xoh = np.array(list(map(lambda x: to_categorical(x, num_classes=len(human_vocab)), X)))\n",
    "    Yoh = np.array(list(map(lambda x: to_categorical(x, num_classes=len(machine_vocab)), Y)))\n",
    "\n",
    "\n",
    "\n",
    "    return X, np.array(Y), Xoh, Yoh\n",
    "\n",
    "def string_to_int(string, length, vocab):\n",
    "    \"\"\"\n",
    "    Converts all strings in the vocabulary into a list of integers representing the positions of the\n",
    "    input string's characters in the \"vocab\"\n",
    "    \n",
    "    Arguments:\n",
    "    string -- input string, e.g. 'Wed 10 Jul 2007'\n",
    "    length -- the number of time steps you'd like, determines if the output will be padded or cut\n",
    "    vocab -- vocabulary, dictionary used to index every character of your \"string\"\n",
    "    \n",
    "    Returns:\n",
    "    rep -- list of integers (or '<unk>') (size = length) representing the position of the string's character in the vocabulary\n",
    "    \"\"\"\n",
    "    \n",
    "    #make lower to standardize\n",
    "    string = string.lower()\n",
    "    string = string.replace(',','')\n",
    "    \n",
    "    if len(string) > length:\n",
    "        string = string[:length]\n",
    "        \n",
    "    rep = list(map(lambda x: vocab.get(x, '<unk>'), string))\n",
    "    \n",
    "    if len(string) < length:\n",
    "        rep += [vocab['<pad>']] * (length - len(string))\n",
    "    \n",
    "    #print (rep)\n",
    "    return rep\n",
    "\n",
    "\n",
    "def int_to_string(ints, inv_vocab):\n",
    "    \"\"\"\n",
    "    Output a machine readable list of characters based on a list of indexes in the machine's vocabulary\n",
    "    \n",
    "    Arguments:\n",
    "    ints -- list of integers representing indexes in the machine's vocabulary\n",
    "    inv_vocab -- dictionary mapping machine readable indexes to machine readable characters \n",
    "    \n",
    "    Returns:\n",
    "    l -- list of characters corresponding to the indexes of ints thanks to the inv_vocab mapping\n",
    "    \"\"\"\n",
    "    \n",
    "    l = [inv_vocab[i] for i in ints]\n",
    "    return l\n",
    "\n",
    "\n",
    "EXAMPLES = ['3 May 1979', '5 Apr 09', '20th February 2016', 'Wed 10 Jul 2007']\n",
    "\n",
    "def run_example(model, input_vocabulary, inv_output_vocabulary, text):\n",
    "    encoded = string_to_int(text, TIME_STEPS, input_vocabulary)\n",
    "    prediction = model.predict(np.array([encoded]))\n",
    "    prediction = np.argmax(prediction[0], axis=-1)\n",
    "    return int_to_string(prediction, inv_output_vocabulary)\n",
    "\n",
    "def run_examples(model, input_vocabulary, inv_output_vocabulary, examples=EXAMPLES):\n",
    "    predicted = []\n",
    "    for example in examples:\n",
    "        predicted.append(''.join(run_example(model, input_vocabulary, inv_output_vocabulary, example)))\n",
    "        print('input:', example)\n",
    "        print('output:', predicted[-1])\n",
    "    return predicted\n",
    "\n",
    "\n",
    "def softmax(x, axis=1):\n",
    "    \"\"\"Softmax activation function.\n",
    "    # Arguments\n",
    "        x : Tensor.\n",
    "        axis: Integer, axis along which the softmax normalization is applied.\n",
    "    # Returns\n",
    "        Tensor, output of softmax transformation.\n",
    "    # Raises\n",
    "        ValueError: In case `dim(x) == 1`.\n",
    "    \"\"\"\n",
    "    ndim = K.ndim(x)\n",
    "    if ndim == 2:\n",
    "        return K.softmax(x)\n",
    "    elif ndim > 2:\n",
    "        e = K.exp(x - K.max(x, axis=axis, keepdims=True))\n",
    "        s = K.sum(e, axis=axis, keepdims=True)\n",
    "        return e / s\n",
    "    else:\n",
    "        raise ValueError('Cannot apply softmax to a tensor that is 1D')\n",
    "        \n",
    "\n",
    "def plot_attention_map(modelx, input_vocabulary, inv_output_vocabulary, text, n_s = 128, num = 7):\n",
    "    \"\"\"\n",
    "    Plot the attention map.\n",
    "  \n",
    "    \"\"\"\n",
    "    attention_map = np.zeros((10, 30))\n",
    "    layer = modelx.get_layer('attention_weights')\n",
    "\n",
    "    Ty, Tx = attention_map.shape\n",
    "    \n",
    "    human_vocab_size = 37\n",
    "    \n",
    "    # Well, this is cumbersome but this version of tensorflow-keras has a bug that affects the \n",
    "    # reuse of layers in a model with the functional API. \n",
    "    # So, I have to recreate the model based on the functional \n",
    "    # components and connect then one by one.\n",
    "    # ideally it can be done simply like this:\n",
    "    # layer = modelx.layers[num]\n",
    "    # f = Model(modelx.inputs, [layer.get_output_at(t) for t in range(Ty)])\n",
    "    #\n",
    "    \n",
    "    X = modelx.inputs[0] \n",
    "    s0 = modelx.inputs[1] \n",
    "    c0 = modelx.inputs[2] \n",
    "    s = s0\n",
    "    c = s0\n",
    "    \n",
    "    a = modelx.layers[2](X)  \n",
    "    outputs = []\n",
    "\n",
    "    for t in range(Ty):\n",
    "        s_prev = s\n",
    "        s_prev = modelx.layers[3](s_prev)\n",
    "        concat = modelx.layers[4]([a, s_prev]) \n",
    "        e = modelx.layers[5](concat) \n",
    "        energies = modelx.layers[6](e) \n",
    "        alphas = modelx.layers[7](energies) \n",
    "        context = modelx.layers[8]([alphas, a])\n",
    "        # Don't forget to pass: initial_state = [hidden state, cell state] (≈ 1 line)\n",
    "        s, _, c = modelx.layers[10](context, initial_state = [s, c]) \n",
    "        outputs.append(energies)\n",
    "\n",
    "    f = Model(inputs=[X, s0, c0], outputs = outputs)\n",
    "    \n",
    "\n",
    "    s0 = np.zeros((1, n_s))\n",
    "    c0 = np.zeros((1, n_s))\n",
    "    encoded = np.array(string_to_int(text, Tx, input_vocabulary)).reshape((1, 30))\n",
    "    encoded = np.array(list(map(lambda x: to_categorical(x, num_classes=len(input_vocabulary)), encoded)))\n",
    "\n",
    "    \n",
    "    r = f([encoded, s0, c0])\n",
    "        \n",
    "    for t in range(Ty):\n",
    "        for t_prime in range(Tx):\n",
    "            attention_map[t][t_prime] = r[t][0, t_prime]\n",
    "\n",
    "    # Normalize attention map\n",
    "    row_max = attention_map.max(axis=1)\n",
    "    attention_map = attention_map / row_max[:, None]\n",
    "\n",
    "    prediction = modelx.predict([encoded, s0, c0])\n",
    "    \n",
    "    predicted_text = []\n",
    "    for i in range(len(prediction)):\n",
    "        predicted_text.append(int(np.argmax(prediction[i], axis=1)))\n",
    "        \n",
    "    predicted_text = list(predicted_text)\n",
    "    predicted_text = int_to_string(predicted_text, inv_output_vocabulary)\n",
    "    text_ = list(text)\n",
    "    \n",
    "    # get the lengths of the string\n",
    "    input_length = len(text)\n",
    "    output_length = Ty\n",
    "    \n",
    "    # Plot the attention_map\n",
    "    plt.clf()\n",
    "    f = plt.figure(figsize=(8, 8.5))\n",
    "    ax = f.add_subplot(1, 1, 1)\n",
    "\n",
    "    # add image\n",
    "    i = ax.imshow(attention_map, interpolation='nearest', cmap='Blues')\n",
    "\n",
    "    # add colorbar\n",
    "    cbaxes = f.add_axes([0.2, 0, 0.6, 0.03])\n",
    "    cbar = f.colorbar(i, cax=cbaxes, orientation='horizontal')\n",
    "    cbar.ax.set_xlabel('Alpha value (Probability output of the \"softmax\")', labelpad=2)\n",
    "\n",
    "    # add labels\n",
    "    ax.set_yticks(range(output_length))\n",
    "    ax.set_yticklabels(predicted_text[:output_length])\n",
    "\n",
    "    ax.set_xticks(range(input_length))\n",
    "    ax.set_xticklabels(text_[:input_length], rotation=45)\n",
    "\n",
    "    ax.set_xlabel('Input Sequence')\n",
    "    ax.set_ylabel('Output Sequence')\n",
    "\n",
    "    # add grid and legend\n",
    "    ax.grid()\n",
    "\n",
    "    #f.show()\n",
    "    \n",
    "    return attention_map\n"
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