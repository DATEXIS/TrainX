# TrainX - Named Entity Linking with Active Sampling and Bi-Encoders
[ACL Anthology](https://aclanthology.org/2020.coling-demos.12.pdf)

**Tom Oberhauser, Tim Bischoff, Karl Brendel, Maluna Menke, Tobias Klatt, Amy Siu, Felix Alexander Gers, Alexander Löser**

We demonstrate TrainX, a system for Named Entity Linking for medical experts.
It combines state-of-the-art entity recognition and linking architectures, such as Flair and fine-tuned Bi-Encoders based on BERT, with an easy-to-use interface for healthcare professionals.
We support medical experts in annotating training data by using active sampling strategies to forward informative samples to the annotator.
We demonstrate that our model is capable of linking against large knowledge bases, such as UMLS (3.6 million entities), and supporting zero-shot cases, where the linker has never seen the entity before.
Those zero-shot capabilities help to mitigate the problem of rare and expensive training data that is a common issue in the medical domain.

## How to start?

A small overview video can be found [here](https://www.youtube.com/watch?v=XAt94UNEEQ4).

We've provided a basic docker-compose configuration besides a sample knowledge-base and a mention document. Simply start the application by executing `docker-compose up --build`.
