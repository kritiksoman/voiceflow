import base64
import requests
import pyautogui
from google import genai
import os
import json
from matplotlib import pyplot as plt
# from json_repair import repair_json


API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

instruction = "Click on the create_db.py in the top."

def ocr_agent(instruction):
    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize(pyautogui.size())
    # sc_size = screenshot.size

    # Save the screenshot
    IMAGE_PATH = "multi_tool_agent/sc.png"
    screenshot.save(IMAGE_PATH)


    # Encode image to base64
    with open(IMAGE_PATH, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    # Prepare the request payload
    request_payload = {
        "requests": [
            {
                "image": {"content": encoded_image},  # Encode as base64 if needed
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    # Send request to Google Vision API
    response = requests.post(ENDPOINT, json=request_payload)
    data = response.json()

    def convert_format(bbox):
        xmin = min(bbox, key=lambda x: x["x"])["x"]
        ymin = min(bbox, key=lambda x: x["y"])["y"]
        xmax = max(bbox, key=lambda x: x["x"])["x"]
        ymax = max(bbox, key=lambda x: x["y"])["y"]
        return [xmin, ymin, xmax, ymax]

    # Print detected text
    ocr_text = []
    for annotation in data.get("responses", [])[0].get("textAnnotations", []):
        if "locale" in annotation:
            # Skip the full text annotation, only keep the bounding boxes of individual words
            continue
        ocr_text.append({"text": annotation["description"],
                        "bbox": convert_format(annotation["boundingPoly"]["vertices"])})
        # print(annotation["description"], annotation["boundingPoly"]["vertices"])
        
    # # plot the coordinates on the screenshot
    # for word in ocr_text:
    #     bbox = word["bbox"]
    #     plt.gca().add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], fill=None, edgecolor='red', linewidth=2))
    #     plt.text(bbox[0], bbox[1], word["text"], fontsize=12, color='blue')
    # plt.imshow(screenshot)
    # plt.axis('off')

    word_text = [x for x in ocr_text if len(x["text"]) > 1]
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    action_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"Parse the user input to identify the region where the user wants to click. Click can be 'single', 'double' or 'right'. \nUser input: {instruction}\n Clickable regions: {word_text}. Using the clickable regions, return the JSON output in the format:" + str({"text": "", "bbox": ["xmin", "ymin", "xmax", "ymax"], "click": "single"})
    )

    print(action_response.text)

    s = action_response.text.find("{")
    e = action_response.text.find("}")
    js = action_response.text[s:e+1].replace("'", '"')
    # js = repair_json(action_response.text[s:e+1])
    click_location = json.loads(js)

    x = (click_location['bbox'][0]+click_location['bbox'][2])/2
    y = (click_location['bbox'][1]+click_location['bbox'][3])/2

    print(x, y)

    if click_location['click'] == 'single':
        pyautogui.click(x=x, y=y)
    elif click_location['click'] == 'double':
        pyautogui.doubleClick(x=x, y=y)
    elif click_location['click'] == 'right':
        pyautogui.rightClick(x=x, y=y)
