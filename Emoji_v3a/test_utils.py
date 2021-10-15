{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "79f2ccc2-5c87-4349-b6fa-bada861f2047",
   "metadata": {},
   "outputs": [],
   "source": [
    "from termcolor import colored\n",
    "\n",
    "from tensorflow.keras.layers import Input\n",
    "from tensorflow.keras.layers import Conv2D\n",
    "from tensorflow.keras.layers import MaxPooling2D\n",
    "from tensorflow.keras.layers import Dropout \n",
    "from tensorflow.keras.layers import Conv2DTranspose\n",
    "from tensorflow.keras.layers import concatenate\n",
    "from tensorflow.keras.layers import ZeroPadding2D\n",
    "from tensorflow.keras.layers import Dense\n",
    "from tensorflow.keras.layers import LSTM\n",
    "from tensorflow.keras.layers import RepeatVector\n",
    "\n",
    "\n",
    "# Compare the two inputs\n",
    "def comparator(learner, instructor):\n",
    "    for a, b in zip(learner, instructor):\n",
    "        if tuple(a) != tuple(b):\n",
    "            print(colored(\"Test failed\", attrs=['bold']),\n",
    "                  \"\\n Expected value \\n\\n\", colored(f\"{b}\", \"green\"), \n",
    "                  \"\\n\\n does not match the input value: \\n\\n\", \n",
    "                  colored(f\"{a}\", \"red\"))\n",
    "            raise AssertionError(\"Error in test\") \n",
    "    print(colored(\"All tests passed!\", \"green\"))\n",
    "\n",
    "# extracts the description of a given model\n",
    "def summary(model):\n",
    "    model.compile(optimizer='adam',\n",
    "                  loss='categorical_crossentropy',\n",
    "                  metrics=['accuracy'])\n",
    "    result = []\n",
    "    for layer in model.layers:\n",
    "        descriptors = [layer.__class__.__name__, layer.output_shape, layer.count_params()]\n",
    "        if (type(layer) == Conv2D):\n",
    "            descriptors.append(layer.padding)\n",
    "            descriptors.append(layer.activation.__name__)\n",
    "            descriptors.append(layer.kernel_initializer.__class__.__name__)\n",
    "        if (type(layer) == MaxPooling2D):\n",
    "            descriptors.append(layer.pool_size)\n",
    "            descriptors.append(layer.strides)\n",
    "            descriptors.append(layer.padding)\n",
    "        if (type(layer) == Dropout):\n",
    "            descriptors.append(layer.rate)\n",
    "        if (type(layer) == ZeroPadding2D):\n",
    "            descriptors.append(layer.padding)\n",
    "        if (type(layer) == Dense):\n",
    "            descriptors.append(layer.activation.__name__)\n",
    "        if (type(layer) == LSTM):\n",
    "            descriptors.append(layer.input_shape)\n",
    "            descriptors.append(layer.activation.__name__)\n",
    "            descriptors.append(layer.return_sequences)\n",
    "        if (type(layer) == RepeatVector):\n",
    "            descriptors.append(layer.n)\n",
    "        result.append(descriptors)\n",
    "    return result\n"
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
