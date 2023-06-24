import cv2
from flask import Flask, request, jsonify
import urllib.request
import os
import random
import json
import traceback

detector = cv2.SIFT_create()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def match():
    try:
        other = json.loads(request.get_data(as_text=True))
        start = request.args.get("start")
        condition = int(request.args.get("condition"))
        mainName = f"{random.randint(0, 1000000)}.png"
        urllib.request.urlretrieve(start, mainName)
        image1 = cv2.imread(mainName, cv2.IMREAD_GRAYSCALE)
        keypoints1, descriptors1 = detector.detectAndCompute(image1, None)

        passing = []
        for x in range(len(other)):
            otherName = f"{random.randint(0, 1000000)}.png"
            urllib.request.urlretrieve(other[x]["Image"][0], otherName)
            image2 = cv2.imread(otherName, cv2.IMREAD_GRAYSCALE)
            keypoints2, descriptors2 = detector.detectAndCompute(image2, None)

            matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
            matches = matcher.match(descriptors1, descriptors2) 

            distance_threshold = 200
            good_matches = [match for match in matches if match.distance < distance_threshold]
            other[x]["Match"] = len(good_matches) / len(matches)
            passing.append(other[x])
            os.remove(otherName)
        os.remove(mainName)
        newPassing = []
        maxScore = max(passing, key=lambda x: x["Match"])
        maxScore = maxScore["Match"]
        for x in range(len(passing)):
            if passing[x]["Match"] > (maxScore * 0.8):
                newPassing.append(passing[x])

        min = float("inf")
        maxValue = 0
        total = 0
        for x in range(len(newPassing)):
            if float(newPassing[x]["Price"]) > maxValue:
                maxValue = float(newPassing[x]["Price"])     
            if float(newPassing[x]["Price"]) < min:
                min = float(newPassing[x]["Price"])
            total += float(newPassing[x]["Price"])
        mean = total / len(newPassing)
        min = mean - ((mean - min) * 0.75)
        maxValue = mean + ((maxValue - mean) * 0.75)

        condPointer = (maxValue - min) * (condition / 100)
        condPointer = min + condPointer
        min = condPointer - ((condPointer - min) * 0.75)
        maxValue = condPointer + ((maxValue - condPointer) * 0.75)
        return jsonify({"min": round(min, 2), "max": round(maxValue, 2)}) 
    except Exception as error: 
        print("An error occurred: ",error)
        traceback.print_exc()
        return jsonify({"min": round(-1, 2), "max": round(-1, 2), "Error": error})

if __name__ == '__main__':
    app.run()
