import boto3
import json
import os
import cv2
# Document
# documentName = "C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\images\\Doclaynet1.jpg"

# # Amazon Textract client
# textract = boto3.client('textract')

# # Call Amazon Textract
# with open(documentName, "rb") as document:
#     response = textract.detect_document_text(
#         Document={
#             'Bytes': document.read(),
#         }
#     )

# ids = [231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250]
ids = [int(id) for id in os.listdir("C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\textract_results\\Doclaynet") if id.isdigit()]
print(ids)
dict={}
for id in ids:    
    f = json.load(open('C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\textract_results\\Doclaynet\\{}\\detectDocumentTextResponse.json'.format(id),'r'))
    response = f

    img = cv2.imread("C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\images\\Doclaynet\\{}.png".format(id))
    height, width, channels = img.shape
    #print(response)

    # Detect columns and print lines
    bboxes=[]
    for item in response["Blocks"]:
        if item["BlockType"] == "WORD":
            top = item["Geometry"]["BoundingBox"]["Top"] * height
            left = item["Geometry"]["BoundingBox"]["Left"] * width
            bottom = top + item["Geometry"]["BoundingBox"]["Height"] * height
            right = left + item["Geometry"]["BoundingBox"]["Width"] * width
            bboxes.append([top, bottom, left, right])
            
    # lines.sort(key=lambda x: x[0])
    # for line in lines:
    #     print(line[1])
    # print(line_bbox)

    # Draw lines
    order = 0
    for bbox in bboxes:
        cv2.rectangle(img, (int(bbox[2]), int(bbox[0])), (int(bbox[3]), int(bbox[1])), (0, 255, 0), 1)
        # cv2.putText(img, str(order), (int(bbox[2]), int(bbox[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        order += 1
    os.makedirs("C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\results\\Doclaynet", exist_ok=True)    
    cv2.imwrite("C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\results\\Doclaynet\\{}_ws.jpg".format(id), img)

    dict[id]=bboxes
    print("Done with {}".format(id))

json.dump(dict, open("C:\\Users\\ramak\\Documents\\Reading-Order-AWS\\Doclaynet_words.json", 'w'))