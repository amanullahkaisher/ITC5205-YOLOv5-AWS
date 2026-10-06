FROM public.ecr.aws/lambda/python:3.12

RUN dnf -y install git mesa-libGL glib2 && dnf clean all

RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch torchvision

RUN git clone --depth 1 https://github.com/ultralytics/yolov5.git /var/task/yolov5

RUN pip install --no-cache-dir -r /var/task/yolov5/requirements.txt boto3 opencv-python-headless

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/lambda_function.py

CMD ["lambda_function.lambda_handler"]
