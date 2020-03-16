# tuh-epilepsy

Using a convolutional neural net to predict epilepsy
diagnoses from patient EEG recordings.

## Dataset

The CNN is trained on EEG data from the
[Temple University EEG Corpus](https://www.isip.piconepress.com/projects/tuh_eeg/html/overview.shtml),
which is a collection of EEGs freely available to the
public. We use a subset of EEGs from this corpus
from patients with a diagnosis of either epilepsy or no
epilepsy. Data from patients diagnosed with epilepsy
and patients diagnosed with no epilepsy are contained
in two separate directories and organized by patient
ID. A more in depth description of the dataset can be
found [here](docs/dataset.txt).

## Design

### Data Wrangling

View the code for data wrangling [here](tuh_epilepsy/dataset.py).

There are a number of different ways information can
be extracted from EEG signal data to train a CNN. The
most common method for epilepsy detection is to train
on raw signals (Craik et al., 2019), so I chose to adopt
this method.

The EEG in this dataset was recorded with variable
parameters.

* Sampling Rate: 250, 256, 512
* Reference: Average, Linked Mastoid
* Number of Channels: 24, 26

In order to keep the input parameters consistent across
all instances fed into the CNN, I chose to only use EEGs
recorded with a 250hz sampling rate. This gave me a pretty
even split between EEGs with epilepsy and EEGs with no
epilepsy. I also chose to only use EEGs with an average
reference. For the EEGs that met these criteria, I chose
to only use signal data from the 24 channels shared by all
recordings in the dataset. These channels were:

Fp1-REF, Fp2-REF, F3-REF, F4-REF, C3-REF, C4-REF, P3-REF,
P4-REF, O1-REF, O2-REF, F7-REF, F8-REF, T3-REF, T4-REF,
T5-REF, T6-REF, M1-REF, M2-REF, FZ-REF, CZ-REF, PZ-REF,
ECG1-REF, T1-REF, T2-REF

Because these EEGs have different durations, I selected
a duration of 10 seconds (2500 samples if recorded at 250hz)
to feed into the CNN. Epilepsy is typically diagnosed from
EEG by the observation of approximately 3hz spike waves that
usually last between 5 and 10 seconds (Smith, 2005). I
reasoned that 10 seconds of data would be able to catch these
spikes if they are present. For each EEG recording that met
the criteria above, I split the recording into 10 second
segments and counted each of these segments as a separate
instance.

Applying a 0.9, 0.1 split to the data, I ended up with the
following counts

|       | Epilepsy | No Epilepsy |  Total | 
|-------|----------|-------------|--------| 
| Train | 25812    | 19154       | 44966  | 
| Test  | 2876     | 2121        | 4997   | 

### Neural Net

View the code for training the CNN [here](notebooks/train-cnn.ipynb).

I chose a 1-Dimensional CNN to train on this data,
following the example of Ihsan et al., 2018. A 1D CNN works
well for training on time-series data, where signals recorded
from different channels are not necessarily related. I used
the example in this [Ackermann, 2018](https://blog.goodaudience.com/introduction-to-1d-convolutional-neural-networks-in-keras-for-time-sequences-3a7ff801a2cf)
article as a template for constructing the neural net. I added
four convolutional layers and a final dense layer that predicts
liklihood values for the two possible outputs 
(1=Epilepsy, 0=No Epilepsy).

| Layer Type             | Filters | Kernel Size | Output Shape      | Param # | 
|------------------------|---------|-------------|-------------------|---------| 
| Conv1D                 | 100     | 10          | (None, 2491, 100) | 24100   | 
| Conv1D                 | 100     | 10          | (None, 2482, 100) | 100100  | 
| MaxPooling1D           |         |             | (None, 827, 100)  | 0       | 
| Conv1D                 | 160     | 10          | (None, 818, 160)  | 160160  | 
| Conv1D                 | 160     | 10          | (None, 809, 160)  | 256160  | 
| GlobalAveragePooling1D |         |             | (None, 160)       | 0       | 
| Dropout                |         |             | (None, 160)       | 0       | 
| Dense                  |         |             | (None, 2)         | 322     |

I trained the CNN using a validation split of 0.1 and 50 training
epochs. Interestingly, for all 50 epochs, the model showed a
training accuracy of 0.5736 and a validation accuracy of 0.5773,
showing that multiple training epochs did not improve the accuracy.
Evaluating the model on the testing data gave an accuracy score of
0.5763.

## Discussion

This first pass was largely a test to see if I could train
a CNN with this data and get some kind of predictions out of
it. While I accomplished the goal of training a model, the
trained model did not have very much predictive power for any
of the datasets that were fed in (train, val, or test). There
are a number of different parameters I can tweak to achieve
better predicive power. Because it tends to have large baseline
shifts that obscure the signal, EEG signals are often highpass filtered at
around 0.1hz. I am not sure if these data were previously highpass
filtered, but if it was not, this could have greatly reduced the
neural net's ability to pick out subtle features in the signal.
Additionally, there could have been certain channels that were
not providing helpful information for epilepsy diagnosis. It
would be benefitial to research which scalp locations are most
likely to pick up epileptic spikes and only train on channels
close to these locations. I could have easily attained a much
larger dataset if I figured out a way to downsample recordings
with a higher sampling rate than 250hz. In order to generalize
the use of thie CNN to as many EEG recordings as possible, I
could downsample all recordings to an even lower sampling rate
(100hz for instance) before feeding in the signals to the CNN.
As far as the neural net itself, there are countless parameters
I could have changed or different structures I could have used.
The 1D CNN seemed to be the best type of CNN for time series data,
but besides that I did not have much guidance on how to structure
it. A good future direction would be to look at how Ihsan et al.,
2018 structured their CNN for predicting epilepsy diagnoses. They
claim 99.1±0.9% accuracy for their model and give a fairly detailed
description of the structure. Even though this first pass was
more of an experiment of what would be possible as far as training
a neural network on EEG data, I now have a good framework going
forward for testing out different models and parameters on this
dataset.

## References

Craik, A., He, Y., & Contreras-Vidal, J. L. (2019). Deep learning
for electroencephalogram (EEG) classification tasks: A review.
*Journal of Neural Engineering*, 16(3). https://doi.org/10.1088/1741-2552/ab0ab5

Smith, S. J. M. (2005). EEG in the diagnosis, classification,
and management of patients with epilepsy. *Neurology in Practice*,
76(2). https://doi.org/10.1136/jnnp.2005.069245

Ullah, I., Hussain, M., Qazi, E. ul H., & Aboalsamh, H. (2018).
An automated system for epilepsy detection using EEG brain signals
based on deep learning approach. *Expert Systems with Applications*,
107, 61–71. https://doi.org/10.1016/j.eswa.2018.04.021

