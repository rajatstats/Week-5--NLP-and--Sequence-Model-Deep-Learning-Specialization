{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6b37eba1-30c2-42ea-8c53-985e73342fdd",
   "metadata": {},
   "outputs": [],
   "source": [
    "def inference_model(LSTM_cell, densor, n_x = 90, n_a = 64, Ty = 100):\n",
    "    \"\"\"\n",
    "    Uses the trained \"LSTM_cell\" and \"densor\" from model() to generate a sequence of values.\n",
    "    \n",
    "    Arguments:\n",
    "    LSTM_cell -- the trained \"LSTM_cell\" from model(), Keras layer object\n",
    "    densor -- the trained \"densor\" from model(), Keras layer object\n",
    "    n_x -- number of unique values\n",
    "    n_a -- number of units in the LSTM_cell\n",
    "    Ty -- number of time steps to generate\n",
    "    \n",
    "    Returns:\n",
    "    inference_model -- Keras model instance\n",
    "    \"\"\"\n",
    "    \n",
    "    # Define the input of your model with a shape \n",
    "    x0 = Input(shape=(1, n_x))\n",
    "    \n",
    "    # Define s0, initial hidden state for the decoder LSTM\n",
    "    a0 = Input(shape=(n_a,), name='a0')\n",
    "    c0 = Input(shape=(n_a,), name='c0')\n",
    "    a = a0\n",
    "    c = c0\n",
    "    x = x0\n",
    "\n",
    "    ### START CODE HERE ###\n",
    "    # Step 1: Create an empty list of \"outputs\" to later store your predicted values (≈1 line)\n",
    "    outputs = []\n",
    "    \n",
    "    # Step 2: Loop over Ty and generate a value at every time step\n",
    "    for t in range(Ty):\n",
    "        \n",
    "        # Step 2.A: Perform one step of LSTM_cell (≈1 line)\n",
    "        a, _, c = LSTM_cell(x, initial_state=[a, c])\n",
    "        \n",
    "        # Step 2.B: Apply Dense layer to the hidden state output of the LSTM_cell (≈1 line)\n",
    "        out = densor(a)\n",
    "\n",
    "        # Step 2.C: Append the prediction \"out\" to \"outputs\" (≈1 line)\n",
    "        outputs.append(out)\n",
    "        \n",
    "        # Step 2.D: Set the prediction \"out\" to be the next input \"x\". You will need to use RepeatVector(1). (≈1 line)\n",
    "        x = RepeatVector(1)(out)\n",
    "        \n",
    "    # Step 3: Create model instance with the correct \"inputs\" and \"outputs\" (≈1 line)\n",
    "    inference_model = Model(inputs=[x0, a0, c0], outputs=outputs)\n",
    "    ### END CODE HERE ###\n",
    "    \n",
    "    return inference_model\n",
    "\n",
    "\n",
    "inference_model = inference_model(LSTM_cell, densor)\n",
    "\n",
    "\n",
    "x1 = np.zeros((1, 1, 90))\n",
    "x1[:,:,35] = 1\n",
    "a1 = np.zeros((1, n_a))\n",
    "c1 = np.zeros((1, n_a))\n",
    "predicting = inference_model.predict([x1, a1, c1])\n",
    "\n",
    "\n",
    "indices = np.argmax(predicting, axis = -1)\n",
    "results = to_categorical(indices, num_classes=90)"
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