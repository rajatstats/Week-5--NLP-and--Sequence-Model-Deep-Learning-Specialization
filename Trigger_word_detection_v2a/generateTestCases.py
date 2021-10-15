{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b6ad2b6e-389a-408b-a01a-df9d10d1df60",
   "metadata": {},
   "outputs": [],
   "source": [
    "# New Generate Test Cases \n",
    "import numpy as np \n",
    "import math \n",
    "import os,sys\n",
    "sys.path.append('../')\n",
    "os.environ['TF_CPP_MIN_LOG_LEVEL']='2'\n",
    "\n",
    "from td_utils import *\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "\n",
    "from pydub import AudioSegment\n",
    "\n",
    "class suppress_stdout_stderr(object):\n",
    "    '''\n",
    "    A context manager for doing a \"deep suppression\" of stdout and stderr in \n",
    "    Python, i.e. will suppress all print, even if the print originates in a \n",
    "    compiled C/Fortran sub-function.\n",
    "       This will not suppress raised exceptions, since exceptions are printed\n",
    "    to stderr just before a script exits, and after the context manager has\n",
    "    exited (at least, I think that is why it lets exceptions through).      \n",
    "\n",
    "    '''\n",
    "    def __init__(self):\n",
    "        # Open a pair of null files\n",
    "        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]\n",
    "        # Save the actual stdout (1) and stderr (2) file descriptors.\n",
    "        self.save_fds = [os.dup(1), os.dup(2)]\n",
    "\n",
    "    def __enter__(self):\n",
    "        # Assign the null pointers to stdout and stderr.\n",
    "        os.dup2(self.null_fds[0],1)\n",
    "        os.dup2(self.null_fds[1],2)\n",
    "\n",
    "    def __exit__(self, *_):\n",
    "        # Re-assign the real stdout/stderr back to (1) and (2)\n",
    "        os.dup2(self.save_fds[0],1)\n",
    "        os.dup2(self.save_fds[1],2)\n",
    "        # Close all file descriptors\n",
    "        for fd in self.null_fds + self.save_fds:\n",
    "            os.close(fd)\n",
    "\n",
    "with suppress_stdout_stderr():\n",
    "  from solutions import *\n",
    "\n",
    "# import copy \n",
    "# from keras.callbacks import History \n",
    "# import tensorflow as tf\n",
    "sys.path.append('../../')\n",
    "\n",
    "from grader_support import stdout_redirector\n",
    "from grader_support import util\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "# This grader is for the Emojify assignment\n",
    "\n",
    "mFiles = [\n",
    "    \"is_overlapping.py\",\n",
    "    \"insert_audio_clip.py\",\n",
    "    \"insert_ones.py\",\n",
    "    \"create_training_example.py\",\n",
    "    \"model.py\"\n",
    "]\n",
    "\n",
    "np.random.seed(3)\n",
    "\n",
    "# generating the testCases for is_overlapping\n",
    "overlap1 = is_overlapping((900, 2500), [(2000, 2550), (260, 949)])\n",
    "overlap2 = is_overlapping((2306, 2307), [(824, 1532), (1900, 2305), (3424, 3656)])\n",
    "\n",
    "# generating the test cases for the insert_audio_clip\n",
    "# (2732, 3452), (4859, 5579)\n",
    "a = AudioSegment.from_wav(\"activate.wav\")\n",
    "b = AudioSegment.from_wav(\"background.wav\")\n",
    "audio_clip, segment_time = insert_audio_clip(b, a, [(3790, 4400)])\n",
    "audio_clip.export('test.wav', format = 'wav')\n",
    "\n",
    "inserted = graph_spectrogram('test.wav')\n",
    "\n",
    "# generate the testCases for insert_ones\n",
    "arr1 = insert_ones(np.zeros((1, Ty)), 9)\n",
    "\n",
    "# generate the test Cases for create_training_example\n",
    "\n",
    "n = AudioSegment.from_wav(\"negative.wav\")\n",
    "\n",
    "A = []\n",
    "N = []\n",
    "A.append(a)\n",
    "N.append(n)\n",
    "\n",
    "with stdout_redirector.stdout_redirected():\n",
    "    a, s = create_training_example(b, A, N)\n",
    "\n",
    "\n",
    "# generating the test cases for the model \n",
    "with suppress_stdout_stderr():\n",
    "    model = model(input_shape = (Tx, n_freq))\n",
    "    ml = len(model.layers)\n",
    "    cp = model.count_params()\n",
    "    mi = len(model.inputs)\n",
    "    mo = len(model.outputs)\n",
    "\n",
    "def generateTestCases():\n",
    "\ttestCases = {\n",
    "\t    'is_overlapping': {\n",
    "\t        'partId': 'S8DvY',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': ((900, 2500), [(2000, 2550), (260, 949)]),\n",
    "\t                'testOutput': overlap1\n",
    "\t            },\n",
    "                {\n",
    "                    'testInput': ((2306, 2307), [(824, 1532), (1900, 2305), (3424, 3656)]),\n",
    "                    'testOutput': overlap2\n",
    "                }\n",
    "\t        ]\n",
    "\t    },\n",
    "\t    'insert_audio_clip': { \n",
    "\t        'partId': 'BSIWi',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': (\"activate.wav\", \"background.wav\"),\n",
    "\t                'testOutput': inserted\n",
    "\t            }\n",
    "\t        ]\n",
    "\t    },\n",
    "\t    'insert_ones': { \n",
    "\t        'partId': '2Kdnr',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': (np.zeros((1, Ty)), 9) ,\n",
    "\t                'testOutput': arr1\n",
    "\t            }\n",
    "\t        ]\n",
    "\t    },\n",
    "\t    'create_training_example': { \n",
    "\t        'partId': 'v097u',\n",
    "\t        'testCases': [\n",
    "\t            {\n",
    "\t                'testInput': (b, A, N),\n",
    "\t                'testOutput': (a,s)\n",
    "\t            }\n",
    "\t        ]\n",
    "\t    },\n",
    "      'model': { \n",
    "          'partId': '0Txcd',\n",
    "          'testCases': [\n",
    "              {\n",
    "                  'testInput': (Tx, n_freq),\n",
    "                  'testOutput': np.asarray([cp, ml, mi, mo])\n",
    "              }\n",
    "          ]\n",
    "       }\n",
    "       }\n",
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
