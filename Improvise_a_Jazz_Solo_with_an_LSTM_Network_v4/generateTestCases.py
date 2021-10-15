{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "97e2ba70-f7a5-48a9-b651-961d49b0ac17",
   "metadata": {},
   "outputs": [],
   "source": [
    "# New Generate Test Cases \n",
    "from .solutions import *\n",
    "import numpy as np \n",
    "np.random.seed(3)\n",
    "\n",
    "import math \n",
    "\n",
    "from tensorflow.keras.optimizers import Adam\n",
    "from tensorflow.keras.layers import Dense,  LSTM, Reshape\n",
    "\n",
    "# import copy \n",
    "# from keras.callbacks import History \n",
    "# import tensorflow as tf\n",
    "\n",
    "\n",
    "#from grader_support import stdout_redirector\n",
    "#from grader_support import util\n",
    "\n",
    "os.environ['TF_CPP_MIN_LOG_LEVEL']='3'\n",
    "\n",
    "# with suppress_stdout_stderr():\n",
    "n_a = 64 \n",
    "n_values = 90 \n",
    "LSTM_cell = LSTM(n_a, return_state=True) # Used in Step 2.C\n",
    "densor = Dense(n_values, activation='softmax') # Used in Step 2.D\n",
    "x_initializer = np.zeros((1, 1, 90))\n",
    "a_initializer = np.zeros((1, n_a))\n",
    "c_initializer = np.zeros((1, n_a))\n",
    "reshapor = Reshape((1, n_values))  \n",
    "\n",
    "# ================================================================================================\n",
    "# generating the test cases for dj model \n",
    "'''\n",
    "def djmodel_gen():\n",
    "\tm = 60\n",
    "\ta0 = np.zeros((m, n_a))\n",
    "\tc0 = np.zeros((m, n_a))\n",
    "\tdjmodelx = djmodel(Tx = 30 , LSTM_cell=LSTM_cell, densor=densor, reshapor=reshapor)\n",
    "\topt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, decay=0.01)\n",
    "\tdjmodelx.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])\n",
    "\tcp = djmodelx.count_params()\n",
    "\tml = len(djmodelx.layers)\n",
    "\tprint(cp, ml)\n",
    "\treturn (cp, ml)\n",
    "\n",
    "# ================================================================================================\n",
    "'''\n",
    "# GENERATING TEST CASES FOR THE MUSIC INFERENCE MODEL \n",
    "'''\n",
    "def music_inference_model_gen():\n",
    "\tim = music_inference_model(LSTM_cell, densor, Ty=10)\n",
    "\topt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, decay=0.01)\n",
    "\tim.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])\n",
    "\tcp1 = im.count_params()\n",
    "\tml1 = len(im.layers)\n",
    "\tm_out1 = np.asarray((cp1, ml1))\n",
    "\tprint(m_out1)\n",
    "\treturn m_out1\n",
    "'''\n",
    "# ================================================================================================\n",
    "\n",
    "# generating the test cases for predicted_and_sample\n",
    "\n",
    "inference_model = music_inference_model(LSTM_cell, densor, 13)\n",
    "results, indices = predict_and_sample(inference_model, x_initializer, a_initializer, c_initializer)\n",
    "\n",
    "def generateTestCases():\n",
    "\ttestCases = {\n",
    "\t    'djmodel': {\n",
    "\t        'partId': 'iz6sX',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': (30, LSTM_cell, densor, reshapor),\n",
    "\t                'testOutput': (45530, 36)\n",
    "\t            }\n",
    "\t        ]\n",
    "\t    },\n",
    "\t    'music_inference_model': { \n",
    "\t        'partId': 'MtuL2',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': (LSTM_cell, densor, 10),\n",
    "\t                'testOutput': (45530, 32)\n",
    "\t            }\n",
    "\t        ]\n",
    "\t    },\n",
    "\t\t'predict_and_sample': { \n",
    "\t        'partId': 'tkaiA',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': (inference_model, x_initializer, a_initializer, c_initializer),\n",
    "\t                'testOutput': (results, indices)\n",
    "\t            }\n",
    "\t        ]\n",
    "\t    },\n",
    "\t}\n",
    "\treturn testCases\n",
    "\n"
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