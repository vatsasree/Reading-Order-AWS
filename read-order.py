import boto3
import json
import os
import cv2
# Document
# documentName = r"C:\Users\ramak\Documents\Reading-Order-AWS\images\1.jpg"

# # Amazon Textract client
# textract = boto3.client('textract')

# # Call Amazon Textract
# with open(documentName, "rb") as document:
#     response = textract.detect_document_text(
#         Document={
#             'Bytes': document.read(),
#         }
#     )

f = json.load(open(r'C:\Users\ramak\Documents\Reading-Order-AWS\1\detectDocumentTextResponse.json','r'))
response = f

img = cv2.imread(r"C:\Users\ramak\Documents\Reading-Order-AWS\images\1.jpg")
height, width, channels = img.shape
#print(response)

# Detect columns and print lines
columns = []
lines = []
line_bbox = []
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        column_found=False
        print("#####")
        print("Columns", columns)
        for index, column in enumerate(columns):
            print("columnn", column)
            print("In for loop")
            bbox_left = item["Geometry"]["BoundingBox"]["Left"]
            bbox_right = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
            bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]/2
            
            column_centre = column['left'] + column['right']/2
            
            #get bbox coordinates for line bounding box in image pixels
            bbox_top = item["Geometry"]["BoundingBox"]["Top"]
            bbox_bottom = item["Geometry"]["BoundingBox"]["Top"] + item["Geometry"]["BoundingBox"]["Height"]
            bbox_left1 = item["Geometry"]["BoundingBox"]["Left"]
            bbox_right1 = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
        
            #convert unnormalized bbox coordinates to image pixels
            bbox_top = int(bbox_top * height)
            bbox_bottom = int(bbox_bottom * height)
            bbox_left1 = int(bbox_left1 * width)
            bbox_right1 = int(bbox_right1 * width)
            line_bbox.append([bbox_top, bbox_bottom, bbox_left1, bbox_right1])

            print("bbox_center", bbox_centre)
            print("column_left", column['left'])
            print("column_right", column['right'])
            print("OR")
            print("column_center", column_centre)
            print("bbox_left", bbox_left)
            print("bbox_right", bbox_right)

            if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                print("line inside column")
                #Bbox appears inside the column
                lines.append([index, item["Text"]])
                column_found=True
                break
        if not column_found:
            print("Not in for loop")
            columns.append({'left':item["Geometry"]["BoundingBox"]["Left"], 'right':item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
            lines.append([len(columns)-1, item["Text"]])
            print("col, line", columns, lines)

lines.sort(key=lambda x: x[0])
# for line in lines:
#     print(line[1])
# print(line_bbox)

# Draw lines
order = 0
for bbox in line_bbox:
    # print(order, bbox)
    # cv2.rectangle(img, (bbox[2], bbox[0]), (bbox[3], bbox[1]), (0, 255, 0), 2)
    cv2.putText(img, str(order), (bbox[2]-10, bbox[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,0, 0), 2)
    order += 1
os.makedirs(r"C:\Users\ramak\Documents\Reading-Order-AWS\results", exist_ok=True)    
cv2.imwrite(r"C:\Users\ramak\Documents\Reading-Order-AWS\results\1.jpg", img)