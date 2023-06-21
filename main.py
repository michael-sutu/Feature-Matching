import cv2
from flask import Flask, request, jsonify
import urllib.request
import os
import random
import json

detector = cv2.SIFT_create()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def match():
    other = json.loads(request.get_data(as_text=True))
    start = request.args.get("start")
    mainName = f"{random.randint(0, 1000000)}.png"
    urllib.request.urlretrieve(start, mainName)
    image1 = cv2.imread(mainName, cv2.IMREAD_GRAYSCALE)
    keypoints1, descriptors1 = detector.detectAndCompute(image1, None)

    passing = []
    for x in range(len(other)):
        try:
            otherName = f"{random.randint(0, 1000000)}.png"
            urllib.request.urlretrieve(other[x]["Image"][0], otherName)
            image2 = cv2.imread(otherName, cv2.IMREAD_GRAYSCALE)
            keypoints2, descriptors2 = detector.detectAndCompute(image2, None)

            matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
            matches = matcher.match(descriptors1, descriptors2) 

            distance_threshold = 200
            good_matches = [match for match in matches if match.distance < distance_threshold]
            print(len(good_matches) / len(matches))
            if((len(good_matches) / len(matches)) > 0.05):
                passing.append(other[x])
            os.remove(otherName)
        except:
            print("an erro has occured")
        
    print(passing)
    os.remove(mainName)
    print("removed")
    min = float("inf")
    max = 0
    total = 0
    print(len(passing))
    for x in range(len(passing)):
        print(passing[x])
        if float(passing[x]["Price"]) > max:
            max = float(passing[x]["Price"])     
        if float(passing[x]["Price"]) < min:
            min = float(passing[x]["Price"])
        total += float(passing[x]["Price"])
    mean = total / len(passing)
    min = mean - ((mean - min) * 0.75)
    max = mean + ((max - mean) * 0.75)
    print(f'Min: {min}, Max: {max}, Total: {total}, Mean: {total / len(passing)}')
    return jsonify({"min": min, "max": max})

if __name__ == '__main__':
    app.run()

# Get highest price, lowest price, and mean.
# New range = mean - ((mean - min) * 0.75) and mean + ((max - mean) * 0.75)
# Final range = ((max - min) * 0.75) then position out of previous range based on condition.
# Round to two decimal places.
