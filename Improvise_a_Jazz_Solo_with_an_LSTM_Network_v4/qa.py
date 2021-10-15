{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e254f209-8844-488f-94e5-3ba14910d798",
   "metadata": {},
   "outputs": [],
   "source": [
    "'''\n",
    "Author:     Ji-Sung Kim, Evan Chow\n",
    "Project:    deepjazz\n",
    "Purpose:    Provide pruning and cleanup functions.\n",
    "\n",
    "Code adapted from Evan Chow's jazzml, https://github.com/evancchow/jazzml \n",
    "with express permission.\n",
    "'''\n",
    "from itertools import zip_longest\n",
    "import random\n",
    "\n",
    "from music21 import *\n",
    "\n",
    "#----------------------------HELPER FUNCTIONS----------------------------------#\n",
    "\n",
    "''' Helper function to down num to the nearest multiple of mult. '''\n",
    "def __roundDown(num, mult):\n",
    "    return (float(num) - (float(num) % mult))\n",
    "\n",
    "''' Helper function to round up num to nearest multiple of mult. '''\n",
    "def __roundUp(num, mult):\n",
    "    return __roundDown(num, mult) + mult\n",
    "\n",
    "''' Helper function that, based on if upDown < 0 or upDown >= 0, rounds number \n",
    "    down or up respectively to nearest multiple of mult. '''\n",
    "def __roundUpDown(num, mult, upDown):\n",
    "    if upDown < 0:\n",
    "        return __roundDown(num, mult)\n",
    "    else:\n",
    "        return __roundUp(num, mult)\n",
    "\n",
    "''' Helper function, from recipes, to iterate over list in chunks of n \n",
    "    length. '''\n",
    "def __grouper(iterable, n, fillvalue=None):\n",
    "    args = [iter(iterable)] * n\n",
    "    return zip_longest(*args, fillvalue=fillvalue)\n",
    "\n",
    "#----------------------------PUBLIC FUNCTIONS----------------------------------#\n",
    "\n",
    "''' Smooth the measure, ensuring that everything is in standard note lengths \n",
    "    (e.g., 0.125, 0.250, 0.333 ... ). '''\n",
    "def prune_grammar(curr_grammar):\n",
    "    pruned_grammar = curr_grammar.split(' ')\n",
    "\n",
    "    for ix, gram in enumerate(pruned_grammar):\n",
    "        terms = gram.split(',')\n",
    "        terms[1] = str(__roundUpDown(float(terms[1]), 0.250, \n",
    "            random.choice([-1, 1])))\n",
    "        pruned_grammar[ix] = ','.join(terms)\n",
    "    pruned_grammar = ' '.join(pruned_grammar)\n",
    "\n",
    "    return pruned_grammar\n",
    "\n",
    "''' Remove repeated notes, and notes that are too close together. '''\n",
    "def prune_notes(curr_notes):\n",
    "    for n1, n2 in __grouper(curr_notes, n=2):\n",
    "        if n2 == None: # corner case: odd-length list\n",
    "            continue\n",
    "        if isinstance(n1, note.Note) and isinstance(n2, note.Note):\n",
    "            if n1.nameWithOctave == n2.nameWithOctave:\n",
    "                curr_notes.remove(n2)\n",
    "\n",
    "    return curr_notes\n",
    "\n",
    "''' Perform quality assurance on notes '''\n",
    "def clean_up_notes(curr_notes):\n",
    "    removeIxs = []\n",
    "    for ix, m in enumerate(curr_notes):\n",
    "        # QA1: ensure nothing is of 0 quarter note len, if so changes its len\n",
    "        if (m.quarterLength == 0.0):\n",
    "            m.quarterLength = 0.250\n",
    "        # QA2: ensure no two melody notes have same offset, i.e. form a chord.\n",
    "        # Sorted, so same offset would be consecutive notes.\n",
    "        if (ix < (len(curr_notes) - 1)):\n",
    "            if (m.offset == curr_notes[ix + 1].offset and\n",
    "                isinstance(curr_notes[ix + 1], note.Note)):\n",
    "                removeIxs.append((ix + 1))\n",
    "    curr_notes = [i for ix, i in enumerate(curr_notes) if ix not in removeIxs]\n",
    "\n",
    "    return curr_notes"
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