Files: _AAREADME.txt
Database: TUH EEG Epilepsy Corpus
Version: v1.0.0

----
Change Log:

(20180409): cleaned up the documentation as part of our major release
            and changed the release number to v1.0.0

(20180118): v0.0.2 was created by re-mapping v0.0.1 of this corpus
	    using TUH EEG v1.1.0.
----

This file contains some basic statistics about the TUH EEG Epilepsy
Corpus, a corpus developed to motivate the development of new methods
for automatic analysis of EEG files using machine learning. This
corpus is a subset of the TUH EEG Corpus and contains sessions from
patients with epilepsy. To balance the corpus, some sessions are
provided from patients that do not have epilepsy.

When you use this specific corpus in your research or technology development, 
we ask that you reference the corpus using this publication:

 Veloso, L., McHugh, J. R., von Weltin, E., Obeid, I., & Picone,
 J. (2017). Big Data Resources for EEGs: Enabling Deep Learning
 Research. In I. Obeid & J. Picone (Eds.), Proceedings of the IEEE
 Signal Processing in Medicine and Biology Symposium
 (p. 1). Philadelphia, Pennsylvania, USA: IEEE.

This publication can be retrieved from:

https://doi.org/https://www.isip.piconepress.com/publications/conference_presentations/2017/ieee_spmb/data/

Our preferred reference for the TUH EEG Corpus, from which this
seizure corpus was derived, is:

 Obeid, I., & Picone, J. (2016). The Temple University Hospital EEG
 Data Corpus. Frontiers in Neuroscience, Section Neural Technology,
 10, 196. http://doi.org/http://dx.doi.org/10.3389/fnins.2016.00196

v1.0.0 of the TUH EEG Epilepsy Corpus was based on v1.1.0 of the
TUH EEG Corpus.

FILENAME STRUCTURE:

 A typical filename in this corpus is:

  edf/epilepsy/01_tcp_ar/003/00000355/s003_2013_01_04/00000355_s003_t000.edf

 The first segment, "edf/", is a directory name for the directory containing
 the data, which consists of edf files (*.edf) and EEG reports (*.txt).

 The second segment denotes either patients with epilepsy ("/epilepsy") or
 patients with without epilepsy ("/no_epilepsy").

 The third segment ("/01_tcp_ar") denotes the type of channel configuration
 for the EEG. "/01_tcp_ar" refers to an AR reference configuration.

 The fourth segment ("003") is a three-digit identifier meant to keep
 the number of subdirectories in a directory manageable. This follows
 the TUH EEG v1.1.0 convention.

 The fifth segment ("/00000355") denotes an anonymized patient ID. The
 IDs are consistent across all of our databases involving Temple
 Hospital EEG data.

 The sixth segment ("/s003_2013_01_04") denotes the session number
 ("s003"), and the date the EEG was archived at the hospital
 ("01/04/2013"). The archive date is not necessarily the date the EEG
 was recorded (which is available in the EDF header), but close to
 it. EEGs are usually archived within a few days of being recorded.

 The seventh, or last, segment is the filename
 ("00000355_s003_t000.edf"). This includes the patient number, the
 session number and a token number ("t000").  EEGs are split into a
 series of files starting with *t000.edf, *t001.edf, ...  These
 represent pruned EEGs, so the original EEG is split into these
 segments, and uninteresting parts of the original recording were
 deleted (common in clinical practice).

 There are two types of files in this release: *.edf represents the signal
 data, and *.txt represents the EEG report.

 Sessions were sorted into epilepsy and no epilepsy categories by searching
 the associated EEG reports for indications as to a epilepsy/no epilepsy 
 diagnosis based on clinical history, medications at the time of recording, 
 and EEG features associated with epilepsy such as spike and sharp waves. 

BASIC STATISTICS:

  |-------------------------------------------------------|
  | Description |  Epilepsy   | No Epilepsy |    Total    |
  |-------------+-------------+-------------+-------------|
  | Patients    |         133 |         104 |         237 |
  |-------------+-------------+-------------+-------------|
  | Sessions    |         428 |         133 |         561 |
  |-------------+-------------+-------------+-------------|
  | Files       |       1,360 |         288 |       1,648 |
  |-------------------------------------------------------|

---
If you have any additional comments or questions about the data,
please direct them to help@nedcdata.org.

Best Regards,
 
Eva von Weltin
NEDC Data Resources Development Manager
