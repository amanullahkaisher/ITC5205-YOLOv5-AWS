# ITC5205 Assignment 2 – YOLOv5 Object Detection System on AWS

**Student Name:** Amanulla Kaisher  
**Student ID:** 250053  
**Unit:** ITC5205 Cloud Computing  

## Project Overview

This project is a cloud-based object detection system using YOLOv5 and AWS.

The main goal of this project was to run an object detection model using different AWS services and build a complete working system. I first installed and tested YOLOv5 on an EC2 instance. After confirming that the model was working, I used Docker to create a container image and uploaded it to Amazon ECR. The container was then used to create an AWS Lambda function.

Amazon S3 is used to store the input and output images. API Gateway is connected with Lambda so the detection process can be started through an API request. IAM is used for permissions and API security, while CloudWatch is used to check logs and performance.

The final system can detect an object from an image, save the detected image in S3, and return the detection result.

---

## AWS Services Used

The following AWS services were used in this project:

- Amazon EC2
- Amazon S3
- Amazon ECR
- AWS Lambda
- Amazon API Gateway
- AWS IAM
- Amazon CloudWatch

Other technologies used:

- Python
- YOLOv5
- PyTorch
- Docker
- Flask
- Boto3

---

## System Workflow

The system works in the following way:

1. The input image is stored in Amazon S3.
2. A POST request is sent through API Gateway.
3. API Gateway triggers the Lambda function.
4. Lambda downloads the image from S3.
5. YOLOv5 runs object detection on the image.
6. The detected image is created.
7. Lambda uploads the result back to S3.
8. The detection details are returned as a JSON response.

The basic workflow is:

```text
User
  |
  v
API Gateway
  |
  v
AWS Lambda
  |
  v
Amazon S3
  |
  v
YOLOv5 Detection
  |
  v
Output Image
```

---

## Project Structure

```text
ITC5205-YOLOv5-AWS/
│
├── code/
│   ├── app.py
│   ├── Dockerfile
│   ├── lambda_function.py
│   └── requirements.txt
│
├── deploy/
│   ├── deploy.sh
│   └── test_api.sh
│
└── README.md
```

The `code` folder contains the main application files.

The `deploy` folder contains the scripts used for deployment and API testing.

---

## EC2 Setup

I used an Amazon EC2 instance to install and test YOLOv5 before deploying it to Lambda.

**Instance Name:** `ITC5205-YOLOv5`  
**Instance Type:** `t3.medium`  
**Operating System:** Ubuntu 24.04 LTS  
**Region:** `us-east-1`

YOLOv5 was successfully tested on the EC2 instance. This helped me confirm that object detection was working correctly before moving to the Lambda deployment.

---

## Amazon S3

Amazon S3 is used to store the input image and the final detected image.

**S3 Bucket:**

```text
itc5205-yolov5-kaiser
```

**Input Image:**

```text
s3://itc5205-yolov5-kaiser/input/download.jpg
```

**Output Image:**

```text
s3://itc5205-yolov5-kaiser/output/lambda-result.jpg
```

Lambda downloads the input image from S3, processes it using YOLOv5, and uploads the final image back to the output folder.

---

## Docker and Amazon ECR

At first, I tried to use a normal ZIP-based Lambda deployment. However, YOLOv5 and PyTorch require large dependencies, so this method was not suitable.

For this reason, I used Docker to package the application.

The Docker image was uploaded to the following ECR repository:

```text
itc5205-yolov5-kaiser
```

The ECR image was then used to create the Lambda function.

---

## AWS Lambda

The Lambda function used in this project is:

```text
ITC5205-YOLOv5-Kaiser-Container
```

Final Lambda configuration:

```text
Architecture: x86_64
Memory: 2048 MB
Timeout: 5 minutes
Ephemeral Storage: 512 MB
```

The Lambda function performs the main object detection process. It downloads the image from S3, runs YOLOv5, creates the detected image, uploads the result to S3, and returns the detection information.

---

## API Gateway

The Lambda function is connected to Amazon API Gateway.

**API Name:**

```text
ITC5205-YOLOv5-API
```

**Method and Route:**

```text
POST /detect
```

When an authorized request is sent to this route, API Gateway triggers the Lambda function.

---

## API Security

IAM authorization is enabled on the `POST /detect` route.

I tested the API without authentication and received:

```text
HTTP 403 Forbidden
```

I then tested it again using an IAM-authenticated request. The request was successful and the Lambda function returned the object detection result.

This means the API cannot be accessed by an unauthorized request.

No AWS passwords, secret keys, or access credentials are stored in this repository.

---

## Final Detection Result

The final end-to-end test was successful.

YOLOv5 detected:

```text
Object: car
Confidence: 0.84
```

The final detected image was stored at:

```text
s3://itc5205-yolov5-kaiser/output/lambda-result.jpg
```

The successful Lambda response was:

```json
{
  "status": "success",
  "message": "YOLOv5 detection completed by AWS Lambda",
  "detections": [
    {
      "object": "car",
      "confidence": 0.84
    }
  ],
  "output": "s3://itc5205-yolov5-kaiser/output/lambda-result.jpg"
}
```

---

## Performance Testing

I used CloudWatch logs to check the performance of the Lambda function.

With **1024 MB memory**, the cold execution results were:

```text
Execution Duration: 9548.08 ms
Initialization Duration: 9999.23 ms
Maximum Memory Used: 702 MB
```

A warm execution was much faster:

```text
Execution Duration: 1331.42 ms
Maximum Memory Used: 736 MB
```

This showed the difference between a cold start and a warm Lambda execution.

---

## Performance Improvement

To improve the performance, I increased the Lambda memory from **1024 MB to 2048 MB**.

After this change, the cold execution results were:

```text
Execution Duration: 4459.40 ms
Initialization Duration: 2751.88 ms
Maximum Memory Used: 711 MB
```

Compared with the previous configuration, the initialization time was reduced by approximately **72%**, and the cold execution time was reduced by approximately **53%**.

This showed that increasing the Lambda memory helped the YOLOv5 application run faster.

---

## Scalability Testing

I also tested the system with **5 concurrent API requests**.

All 5 requests completed successfully.

```text
Concurrent Requests: 5
Successful Requests: 5
```

CloudWatch showed new Lambda log streams during this test. This provided evidence that Lambda was able to handle multiple requests at the same time.

---

## Monitoring and Logging

Amazon CloudWatch was used to monitor the Lambda function.

CloudWatch helped me check:

- Lambda execution
- Cold and warm starts
- Execution duration
- Memory usage
- Errors
- Concurrent executions

The application also logs important steps such as downloading the image, running object detection, and uploading the final result.

---

## Challenges and Solutions

During the project, I faced a few technical problems.

One of the main problems was the Lambda deployment size. YOLOv5 and PyTorch were too large for a simple ZIP deployment. I solved this by using a Docker container and Amazon ECR.

I also had storage problems while building Docker images on EC2. I removed unnecessary files from the Docker build and used CPU-only PyTorch packages to reduce the image size.

Another problem was the Lambda output image path. The application initially could not find the final image. I fixed this by using the Lambda temporary storage path:

```text
/tmp/lambda-result.jpg
```

The Lambda cold start was also quite slow at 1024 MB memory. After testing the performance in CloudWatch, I increased the memory to 2048 MB, which improved the execution time.

---

## Conclusion

This project successfully created a working YOLOv5 object detection system using AWS.

I used EC2 to set up and test YOLOv5, S3 to store the images, ECR to store the Docker container, Lambda to run the detection process, API Gateway to provide the API, IAM for security, and CloudWatch for monitoring.

The final system successfully detected a car with a confidence score of **0.84** and stored the detected image in S3.

I also tested the security, performance, and scalability of the system. Increasing the Lambda memory improved the performance, and the system successfully handled five concurrent requests.

Overall, this project helped me understand how different AWS services can be connected to deploy and manage a machine-learning application in the cloud.

---

## Author

**Amanulla Kaisher**  
**Student ID:** 250053  
**ITC5205 Cloud Computing**
