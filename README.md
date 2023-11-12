# QACheck

Data and Codes for ["QACHECK: A Demonstration System for Question-Guided Multi-Hop Fact-Checking"](https://arxiv.org/abs/2310.07609) (EMNLP 2023, System Demonstrations).

## System Overview

We introduce the **Question-guided Multi-hop Fact-Checking (QACheck)** system, which provides an explainable fact-checking process by asking and answering a series of relevant questions. 

![The general framework of QACheck](./framework.png)

<!-- <img src="./framework.png" align="left" alt="drawing" width="2000px"/> -->

- **Claim Verifier** $\mathcal{D}$: determine the sufficiency of the existing context to validate the claim, i.e., $\mathcal{D}(c, C) \rightarrow \{\text{True}, \text{False}\}$. 

- **Question Generator** $\mathcal{Q}$: generate the next question that is necessary for verifying the claim, i.e., $Q(c, C) \rightarrow q$.

- **Question-Answering Model** $\mathcal{A}$: answer the question and provide the supported evidence, i.e., $\mathcal{A}(q) \rightarrow a, e$.

- **Validator** $\mathcal{V}$: validate the usefulness of the newly-generated (Q, A) pair based on the existing context and the claim, i.e., $\mathcal{V}(c, \{q, a\}, C) \rightarrow \{\text{True}, \text{False}\}$.

- **Reasoner** $\mathcal{R}$: utilize the relevant context to justify the veracity of the claim and outputs the final label, i.e., $\mathcal{R}(c, C) \rightarrow \{\text{Supported}, \text{Refuted}\}$.

## Demo System

Coming Soon...

## Reference
Please cite the paper in the following format if you use this dataset during your research.

```
@inproceedings{PanQACheck23,
  author       = {Liangming Pan, Xinyuan Lu, Min-Yen Kan, Preslav Nakov},
  title        = {QACHECK: A Demonstration System for Question-Guided Multi-Hop Fact-Checking},
  booktitle    = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing System Demonstrations Track (EMNLP 2023 Demo Track)},
  address      = {Singapore},
  year         = {2023},
  month        = {Dec}
}
```

## Q&A
If you encounter any problem, please either directly contact the [Liangming Pan](liangmingpan@ucsb.edu) or leave an issue in the github repo.


