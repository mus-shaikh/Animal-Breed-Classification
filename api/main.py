from fastapi import FastAPI,UploadFile,File,Form
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io


app = FastAPI(
    title="Animal Breed Classification"
)


model = tf.keras.models.load_model(
    "saved_model/dog_model.keras"
)


with open(
    "saved_model/labels.json"
) as f:

    labels=json.load(f)



def clean_label(label):

    label = label.lower()

    if "-" in label:
        label = label.split("-",1)[1]

    label = label.replace("_","")
    label = label.replace(" ","")

    return label




@app.post("/validate")

async def validate(

    image:UploadFile=File(...),

    claimed_animal:str=Form(...),

    claimed_category:str=Form(...)

):

    try:


        img = Image.open(

            io.BytesIO(

                await image.read()

            )

        ).convert("RGB")



        img = img.resize(
            (224,224)
        )



        img_array=np.array(img)


        img_array=np.expand_dims(
            img_array,
            axis=0
        )



        prediction=model.predict(
            img_array
        )[0]



        index=int(
            np.argmax(prediction)
        )



        predicted_category=labels[index]



        confidence=float(
            prediction[index]*100
        )



        match = (

            clean_label(claimed_category)

            ==

            clean_label(predicted_category)

        )



        if confidence < 60:

            decision="needs_review"


        elif match:

            decision="accept"


        else:

            decision="reject"




        return {


            "claimed_animal":claimed_animal,


            "claimed_category":claimed_category,


            "predicted_animal":"dog",


            "predicted_category":predicted_category,


            "match":match,


            "confidence":round(confidence,2),


            "decision":decision

        }



    except Exception as e:


        return {

            "error":"Invalid Image",

            "details":str(e)

        }