# AWS Order Processing System - Blue Ocean
The AWS Serverless E-Commerce Order Processing System is a cloud-native application designed using AWS serverless services. The system allows users to submit e-commerce orders through a web interface and processes those orders using an event-driven architecture.

# Architecture
The architecture of the order processing system is built completely using AWS serverless services, which means customers don't need to worry about managing servers as in traditional models. This architecture operates as follows:</br>
• A s3 static website in used for data input.</br>
• When the client sends data it moves to the API Gateway, which based on http_method of /POST send to the create order lambda function.</br>
• The Lambda function create a entry in Dynamo db and sends a message to the SQS queue, where it awaits processing by another backend logic component in the system.</br>
• The process lambda function receive object from queue and send order status as notification emails via SNS.</br>
• There is a getorder function which based on http_method of /GET can view all data from dynamodb.</br>

<img width="868" height="390" alt="AWS-Order-Processing" src="https://github.com/user-attachments/assets/8c85f6e4-b338-431a-a826-3289e05ecca2" />

# Implementation Steps
<b>Create s3 bucket</b></br>
• Create a s3 bucket and upload the index.html file as object.</br>
• Uncheck block all public access.</br>
• Update bucket policy to allow all access. refer s3accesspolicy.txt </br>
• Under s3 property enable static website hosting option.</br>
<img width="1597" height="412" alt="image" src="https://github.com/user-attachments/assets/a548cb07-3b08-461a-86ba-2eb2340c6901" />



<b>Create SQS Queue</b></br>
The SQS FIFO (First-In-First-Out) queue ensures that order messages are processed in the exact order they are received. This is crucial for maintaining the sequence of operations and ensuring that orders are handled correctly and efficiently, providing fault tolerance and decoupling the processing steps.

<img width="1683" height="687" alt="image" src="https://github.com/user-attachments/assets/aa015ebb-ad36-4c9f-a796-e44c61f09b92" />


• Select a standard queue and name the queue</br>

<b> Create SNS Topic </b></br>
The Simple Notification Service (SNS) delivers notifications to the admin. Whenever an order is received, SNS ensures that a real-time alert is sent to the administrator, keeping them updated with the order details.
<img width="1616" height="552" alt="image" src="https://github.com/user-attachments/assets/25231197-c61e-493b-b04d-5d6774201810" />

• In SNS, select Standard and enter SNS name and create topic</br>
• Create a new subscription for SNS</br>
• Select Protocol: Email</br>
• Endpoint: enter your email</br>
• Click Create subscription</br>
• Login your email</br>
• Check email from AWS from Inbox or Spam</br>
• Click Confirm subscription to subscribe.</br>

<b>Create DynamoDB to store order information</b></br>
DynamoDB is used to store order details, with each order being saved in this highly scalable, low-latency NoSQL database. It provides quick and reliable access to order data, ensuring that the information is always available for further processing or querying as needed</br>
• In DynamoDB, click Create table</br>
• Enter Table name, Partition key and Sort key</br>
• Click Create table</br>
<img width="1626" height="227" alt="image" src="https://github.com/user-attachments/assets/7e7ab07e-6162-421b-9bed-768321da7907" />

<b>Lambda function</b></br>
This step will create a Python script on the Lambda function to process order messages from the SQS queue, send an email to the user, and store order information in DynamoDB.</br>
• Repeat this step for 3 lambda function. </br>
• Create lambda function with pyhton 3.14.
• Download the lambda_function code file.</br>
• Delete all the existing code in lambda function.</br>
• Copy the code from the downloaded Python file and paste it into lambda_function.py in the console.</br>
• In the Lambda function code, update the following sections:Update the name of the DynamoDB table, Update the QueueUrl, Update the TopicArn,  Click *Deploy *</br>
• Click Test **-> **Configure test event</br>
• Enter Event name</br>
• Template: select apigateway-aws-proxy</br>
• Copy the contents of the JsonForTestEvent.json file and paste it into the Event JSON. Then click Save</br>
• Click Test</br>
• If the result returns a status code of 200, it means the code is correct. If not, check the code or the IAM role of the Lambda</br>


<b>Create IAM policy for Lambda function</b></br>
This step will create an IAM policy to allow Lambda to call APIs for SQS, SNS, and DynamoDB. The policy is wide and used buy all lambda function. to improvise you can maintain principle of Least privilege access and separate policy based on access required. Example. Create Order need Put access on dynamo db and SQS only, whereas process lambda need SNS access and read item/ delete on SQS to process order. The. get order lambda needs read access dynamo db </br>
• Access IAM – click Policies **– click **Create policy</br>
• Select JSON</br>
• Use IAM Policy from CustomLambdaPolicy.json</br>
• After updating the ARNs of SQS, SNS, and DynamoDB in the IAM Policy editor, click Next.</br>
• Enter IAM policy name and click Create policy</br>

• Go back to Lambda, navigate to the Configuration tab, click Permissions, and then click on the Role name of the Lambda to assign the IAM policy you just created to the Lambda's IAM role.</br>
• In IAM Role of Lambda, click Add permissions -> Attach policies</br>
• Type the name of the IAM policy you created earlier, check the box next to the IAM policy, and click Add permissions.</br>
<img width="1598" height="596" alt="image" src="https://github.com/user-attachments/assets/92b4aafb-008c-44fd-9005-9243356d9aa4" />


<b>Create API Gateway</b></br>
API Gateway acts as the entry point for the order processing system. It receives order data through a POST request, ensuring secure and reliable transmission to the backend for further processing. This service functions as a bridge between external client applications and internal services, enabling seamless and efficient communication.</br>
• In API Gateway create http API.</br>
• In API create a route /orders (reference /blueocean-createorders)</br>
• Create http_method GET and POST and integrate respective lambda to it</br>
<img width="1768" height="510" alt="image" src="https://github.com/user-attachments/assets/c7aa1bc5-3f23-4e6a-985e-d017b337f875" />

• Add CORS policy to API, Remember to deploy all API Gateway
<img width="1608" height="511" alt="image" src="https://github.com/user-attachments/assets/1157a9f6-976e-4e2d-b7fa-80e472b02b39" />


• Return to Lambda, Verify in trigger</br>
<img width="1358" height="773" alt="image" src="https://github.com/user-attachments/assets/b40eadfb-0df0-4b10-b444-d613f810d505" />

<b>SQS Trigger</b></br>
• For Process Order lambda add trigger to the sqs</br>

<img width="1362" height="767" alt="image" src="https://github.com/user-attachments/assets/260fa61d-29e9-4be6-b99a-421b1351eb54" />



<b>Test Case</b></br>
• Load the website from the s3 static website URL and test.</br>
• Data will be added to Dynamo db and Email notification sent to email address.</br>
• For get data user api gateway address and test.</br>

<b>Clean up</b></br>
After completing the lab, you can delete the following resources:</br>
• Delete the API Gateway</br>
• Delete the Lambda Function</br>
• Delete the SNS Topic</br>
• Delete the SQS Queue</br>
• Delete the DynamoDB Table</br>

<b>Conclusion</b></br>
Through this setup, we understand how to design and deploy an order processing system entirely based on AWS serverless architecture. With this architecture, we no longer have to worry about managing servers or scaling the components within the system.





