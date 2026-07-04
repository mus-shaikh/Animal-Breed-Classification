# Animal Sub-Type Image Validation System

## Overview

Animal Sub-Type Image Validation System is a computer vision based machine learning application that verifies whether an uploaded animal image matches the animal and sub-type selected by a surveyor.

During field surveys, users may correctly identify the animal but select the wrong sub-type. This system detects such cases by predicting the actual sub-type from the image and comparing it with the claimed sub-type.

The application returns:

- Predicted animal sub-type
- Confidence percentage
- Match status
- Decision: accept, reject, or needs_review


## Problem Statement

Survey records contain:

- Animal image
- Claimed animal
- Claimed category/sub-type

The goal is to verify whether the claimed information matches the image.

Example:

Input:

```
claimed_animal = dog

claimed_category = GoldenRetriever
```

Output:

```json
{
    "claimed_animal": "dog",
    "claimed_category": "GoldenRetriever",
    "predicted_animal": "dog",
    "predicted_category": "n02099601-golden_retriever",
    "match": true,
    "confidence": 99.96,
    "decision": "accept"
}
```


# Dataset

## Stanford Dogs Dataset

The Stanford Dogs Dataset was used for training and evaluation.

The dataset contains images of different dog breeds collected from ImageNet.

Animal selected:

```
Dog
```

Sub-types:

Examples:

```
Golden Retriever

Labrador Retriever

Chihuahua

Beagle

German Shepherd
```


Dataset structure:

```
dataset/

├── train/
│
│   ├── breed_1/
│   ├── breed_2/
│   └── ...
│

└── test/

    ├── breed_1/
    ├── breed_2/
    └── ...
```


The test dataset was kept separate from training and used for model evaluation.


# Tech Stack

## Programming Language

```
Python
```

## Machine Learning

```
TensorFlow
Keras
MobileNetV2 Transfer Learning
```

## API Development

```
FastAPI
Uvicorn
```

## Other Libraries

```
NumPy

Pillow

Scikit-learn

Matplotlib
```


# Model Approach

Transfer learning was used instead of training a CNN from scratch.

MobileNetV2 pretrained on ImageNet was selected because:

- Requires less training data
- Faster training
- Lightweight architecture
- Good performance for image classification


Architecture:

```
Input Image

      |

Image Resize
224 x 224

      |

MobileNetV2
(Pretrained Feature Extractor)

      |

Global Average Pooling

      |

Dense Layer

      |

Softmax Classifier

      |

Breed Prediction
```


# Training Pipeline


Steps:

```
1. Load Stanford Dogs dataset

2. Resize images to 224x224

3. Load MobileNetV2 pretrained model

4. Freeze base layers

5. Add custom classifier layers

6. Train model

7. Evaluate on test data

8. Save trained model
```


Generated files:

```
saved_model/

├── dog_model.keras

└── labels.json
```


# Evaluation Metrics

The model was tested using the held-out test dataset.

Metrics generated:

```
Accuracy

Precision

Recall

F1 Score

Confusion Matrix
```


Example:

```
                 precision   recall   f1-score

GoldenRetriever     0.92      0.91      0.91

Labrador            0.89      0.88      0.88

Chihuahua           0.95      0.94      0.94
```


# Decision Logic

The API does not only classify images. It validates the surveyor claim.

Logic:

```
if confidence < 60%

        needs_review


else if predicted subtype == claimed subtype

        accept


else

        reject
```


Example wrong sub-type:

Input:

```
Image:

Golden Retriever


Claim:

Dog - Labrador
```


Output:

```json
{
    "predicted_category":"golden_retriever",

    "match":false,

    "confidence":97.4,

    "decision":"reject"
}
```


# Project Structure

```
Animal-Subtype-Validation/

│
├── api/
│
│   └── main.py
│

├── saved_model/
│
│   ├── dog_model.keras
│   └── labels.json
│

├── notebook/
│
│   └── training.ipynb
│

├── confusion_matrix.png

├── requirements.txt

└── README.md
```



# Installation and Setup Guide


## 1. Clone Repository


```bash
git clone <your-github-repository-link>
```


Move inside project:

```bash
cd Animal-Subtype-Validation
```



# 2. Create Conda Environment


```bash
conda create -n animal_validation python=3.10
```


Activate environment:

```bash
conda activate animal_validation
```



# 3. Install Dependencies


```bash
pip install -r requirements.txt
```



# 4. Verify Model Files


Make sure these files exist:

```
saved_model/

├── dog_model.keras

└── labels.json
```



# 5. Run FastAPI Server


Run:

```bash
uvicorn api.main:app --reload
```


Expected output:

```
Application startup complete

Uvicorn running on:

http://127.0.0.1:8000
```



# 6. Open API Documentation


Open browser:

```
http://127.0.0.1:8000/docs
```


FastAPI Swagger UI will open.



# 7. Test API


Select:

```
POST /validate
```


Click:

```
Try it out
```


Upload:

```
dog image
```


Enter:

```
claimed_animal:

dog
```


Example:

```
claimed_category:

GoldenRetriever
```


Click:

```
Execute
```



# API Response Example


```json
{
    "claimed_animal": "dog",

    "claimed_category": "GoldenRetriever",

    "predicted_animal": "dog",

    "predicted_category": "n02099601-golden_retriever",

    "match": true,

    "confidence": 99.96,

    "decision": "accept"
}
```



# Testing Wrong Sub-Type Case


Upload Golden Retriever image.


Enter:

```
claimed_category:

Chihuahua
```


Response:

```json
{
    "claimed_category":"Chihuahua",

    "predicted_category":"golden_retriever",

    "match":false,

    "confidence":99.2,

    "decision":"reject"
}
```


This validates the main requirement:

Correct animal but wrong sub-type detection.



# Failure Analysis


The model may confuse visually similar breeds.

Examples:

```
Golden Retriever vs Labrador Retriever

Similar coat color, face structure, and body shape.
```


To handle uncertain cases:

Low confidence predictions are sent to:

```
needs_review
```

instead of making a wrong decision.



# Future Improvements


Possible improvements:

```
1. Add object detection before classification

2. Add non-dog image rejection

3. Fine tune MobileNetV2 deeper layers

4. Add Grad-CAM explainability

5. Dockerize FastAPI service

6. Deploy API on cloud
```


# Conclusion


This project demonstrates an end-to-end computer vision workflow:

```
Image Dataset

      |

Deep Learning Model

      |

Confidence Based Validation

      |

FastAPI Deployment
```


It solves the real-world problem of detecting incorrect animal sub-type selection during field surveys.