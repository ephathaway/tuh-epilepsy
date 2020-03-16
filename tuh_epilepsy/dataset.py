from os import listdir
from os.path import join, splitext

import numpy as np
import edfpy

from sys import path
path.insert(0, '.')
from tuh_epilepsy.resources import data_dir


class Dataset:

    def __init__(self):
        self.target_channels = [
            'Fp1-REF', 'Fp2-REF', 'F3-REF',
            'F4-REF', 'C3-REF', 'C4-REF',
            'P3-REF', 'P4-REF', 'O1-REF',
            'O2-REF', 'F7-REF', 'F8-REF',
            'T3-REF', 'T4-REF', 'T5-REF',
            'T6-REF', 'M1-REF', 'M2-REF',
            'FZ-REF', 'CZ-REF', 'PZ-REF',
            'ECG1-REF', 'T1-REF', 'T2-REF',
            ]

    def extract_signals(self, edf: edfpy.EDF) -> np.array:
        """
        Read input file path as `EDF` class,
        read in signal data and convert EEG
        channels to np.array.

        Return np.array with signal data from
        EEG channels.
        """
        signals = edf.get_physical_samples()
        signals_list = []
        for channel in self.target_channels:
            signals_list.append(signals[channel])
        signals_array = np.array(signals_list)
        return(signals_array)

    def split_signals(self, signals: np.array, num_samples: int):
        """
        Split `signals` into 10 sec. segments.
        Return a list of np.arrays with signal
        segments with shape
        (num_channels, 10*sampling_rate).
        """
        total_samples = signals.shape[1]
        num_segments = total_samples // num_samples
        split_signals = []
        for seg in range(num_segments):
            start_idx = seg * num_samples
            end_idx = (seg + 1) * num_samples
            split_signals.append(signals[:,start_idx:end_idx])
        return split_signals

    def get_subject_data(self, top_dir: str) -> dict:
        """
        Iterate through all directories and
        subdirectories of patients with
        epilepsy. Read signals from each
        .edf file, reformat signals as np.array
        and add to a dict with filenames as keys.

        Return dict {filename: signals}.
        """
        data_dict = {}
        for idx in listdir(top_dir):
            idx_dir = join(top_dir, idx)
            for patient in listdir(idx_dir):
                patient_dir = join(idx_dir, patient)
                for sess in listdir(patient_dir):
                    sess_dir = join(patient_dir, sess)
                    for file in listdir(sess_dir):
                        base, ext = splitext(file)
                        if ext == '.edf':
                            edf_path = join(sess_dir, file)
                            data_dict[base] = edf_path
        return data_dict

    def __call__(self):
        """
        Read signals from each .edf file in
        epilepsy and no_epilepsy directories.
        Split signals into 10 sec. segments.
        Append each segment to `features`
        list and append diagnosis for recording
        to `answers` list. Shuffle features and
        answers with same random state.

        Return shuffled np.arrays (features, answers)
        """
        epilepsy_dir = join(data_dir, 'edf', 'epilepsy', '01_tcp_ar')
        no_epilepsy_dir = join(data_dir, 'edf', 'no_epilepsy', '01_tcp_ar')
        epilepsy_dict = self.get_subject_data(epilepsy_dir)
        no_epilepsy_dict = self.get_subject_data(no_epilepsy_dir)

        features = []
        answers = []

        for path in epilepsy_dict.values():
            edf = edfpy.EDF.read_file(path)
            if edf.sampling_rates[0] == 250.0:
                signals = self.extract_signals(edf)
                split_signals = self.split_signals(signals, num_samples=2500)
                for seg in split_signals:
                    assert seg.shape == (24, 2500)
                    features.append(seg)
                    answers.append(1)

        for path in no_epilepsy_dict.values():
            edf = edfpy.EDF.read_file(path)
            if edf.sampling_rates[0] == 250.0:
                signals = self.extract_signals(edf)
                split_signals = self.split_signals(signals, num_samples=2500)
                for seg in split_signals:
                    assert seg.shape == (24, 2500)
                    features.append(seg)
                    answers.append(0)

        # Convert features and answers to arrays
        features = np.array(features)
        answers = np.array(answers)

        # Generate random permuatation `p` of indices from `answers` array
        p = np.random.permutation(len(answers))
        # Shuffle feature and answers by indexing with array `p`
        shuffled_features = features[p]
        shuffled_answers = answers[p]

        assert shuffled_features.shape[0] == shuffled_answers.shape[0]

        return shuffled_features, shuffled_answers
