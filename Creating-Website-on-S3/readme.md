Lab overview
In this lab, you practice using AWS Command Line Interface (AWS CLI) commands from an Amazon Elastic Compute Cloud (Amazon EC2) instance to:

Create an Amazon Simple Storage Service (Amazon S3) bucket.

Create a new AWS Identity and Access Management (IAM) user that has full access to the Amazon S3 service.

Upload files to Amazon S3 to host a simple website for the Café & Bakery.

Create a batch file that can be used to update the static website when you change any of the website files locally.

## Steps

Warning: Permanently added '34.xx.xx.xx' (ED25519) to the list of known hosts.
   ,     #_
   ~\_  ####_        Amazon Linux 2
  ~~  \_#####\
  ~~     \###|       AL2 End of Life is 2026-06-30.
  ~~       \#/ ___
   ~~       V~' '->
    ~~~         /    A newer version of Amazon Linux is available!
      ~~._.   _/
         _/ _/       Amazon Linux 2023, GA and supported until 2028-03-15.
       _/m/'           https://aws.amazon.com/linux/amazon-linux-2023/
### 1 check the user
[ec2-user@ip-10-200-0-72 ~]$ sudo su -l ec2-user
Last login: Sat Mar 14 00:02:37 UTC 2026 from 245.46.61.190.ufinet.com.co on pts/0
[ec2-user@ip-10-200-0-72 ~]$ pwd
/home/ec2-user
### 2 configure abd update AWS CLI
[ec2-user@ip-10-200-0-72 ~]$ aws configure
AWS Access Key ID [None]: Hidden
AWS Secret Access Key [None]: Hidden
Default region name [None]: us-west-2
Default output format [None]: json
[ec2-user@ip-10-200-0-72 ~]$
### 3 Create an S3 bucket using the AWS CLI
### The following is an example of the command to create a new S3 bucket. You can use twhitlock256 as your bucket name, or you can replace <twhitlock256> with a bucket name that you prefer to use for this lab. 

### aws s3api create-bucket --bucket <bucketname> --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2

[ec2-user@ip-10-200-0-72 ~]$ aws s3api create-bucket --bucket aws13032026restart
 --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
{
    "Location": "http://aws13032026restart.s3.amazonaws.com/"
}
[ec2-user@ip-10-200-0-72 ~]$

### confirm bucket creation

[ec2-user@ip-10-200-0-72 ~]$ aws s3 ls
2026-03-14 00:13:41 aws13032026restart
[ec2-user@ip-10-200-0-72 ~]$

### 4 Create a new IAM user that has full access to Amazon S3
### Create user
[ec2-user@ip-10-200-0-72 ~]$ aws iam create-user --user-name awsS3user
{
    "User": {
        "UserName": "awsS3user",
        "Path": "/",
        "CreateDate": "2026-03-14T00:18:15Z",
        "UserId": "AIDAVIHSPG7SMPNRHTXPW",
        "Arn": "arn:aws:iam::361285760996:user/awsS3user"
    }
}
[ec2-user@ip-10-200-0-72 ~]$
### create login profile
[ec2-user@ip-10-200-0-72 ~]$ aws iam create-login-profile --user-name awsS3user --password Training123!
{
    "LoginProfile": {
        "UserName": "awsS3user",
        "CreateDate": "2026-03-14T00:18:44Z",
        "PasswordResetRequired": false
    }
}
[ec2-user@ip-10-200-0-72 ~]$

### 5 ind the AWS managed policy that grants full access to Amazon S3, run the following command:
### aws iam list-policies --query "Policies[?contains(PolicyName,'S3')]"

### grant the awsS3user user full access to the S3 bucket, replace <policyYouFound> in following command with the appropriate PolicyName from the results, and run the adjusted command:

{
        "PolicyName": "AmazonS3FullAccess",
        "PermissionsBoundaryUsageCount": 0,
        "CreateDate": "2015-02-06T18:40:58Z",
        "AttachmentCount": 0,
        "IsAttachable": true,
        "PolicyId": "hidden",
        "DefaultVersionId": "v2",
        "Path": "/",
        "Arn": "hidden",
        "UpdateDate": "2021-09-27T20:16:37Z"
    }

### aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/<policyYouFound> --user-name awsS3user

aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --user-name awsS3user

### 6 Extract the files that you need for this lab
### cd ~/sysops-activity-files
### tar xvzf static-website-v2.tar.gz
### cd static-website


[ec2-user@ip-10-200-0-72 ~]$ aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --user-name awsS3user
[ec2-user@ip-10-200-0-72 ~]$ cd ~/sysops-activity-files
[ec2-user@ip-10-200-0-72 sysops-activity-files]$ tar xvzf static-website-v2.tar.gz
static-website/
static-website/css/
static-website/css/styles.css
static-website/images/
static-website/images/Cafe-Owners.png
static-website/images/Cake-Vitrine.png
static-website/images/Coffee-and-Pastries.png
static-website/images/Coffee-Shop.png
static-website/images/Cookies.png
static-website/images/Cup-of-Hot-Chocolate.png
static-website/images/Strawberry-&-Blueberry-Tarts.png
static-website/images/Strawberry-Tarts.png
static-website/index.html
[ec2-user@ip-10-200-0-72 sysops-activity-files]$ tar xvzf static-website-v2.tar.gz
static-website/
static-website/css/
static-website/css/styles.css
static-website/images/
static-website/images/Cafe-Owners.png
static-website/images/Cake-Vitrine.png
static-website/images/Coffee-and-Pastries.png
static-website/images/Coffee-Shop.png
static-website/images/Cookies.png
static-website/images/Cup-of-Hot-Chocolate.png
static-website/images/Strawberry-&-Blueberry-Tarts.png
static-website/images/Strawberry-Tarts.png
static-website/index.html
[ec2-user@ip-10-200-0-72 sysops-activity-files]$

### 7 Upload files to Amazon S3 by using the AWS CLI
### aws13032026restart
### aws s3 website s3://<my-bucket>/ --index-document index.html
### aws s3 cp /home/ec2-user/sysops-activity-files/static-website/ s3://<my-bucket>/ --recursive --acl public-read
### aws s3 ls <my-bucket>

aws s3 website s3://aws13032026restart/ --index-document index.html
aws s3 cp /home/ec2-user/sysops-activity-files/static-website/ s3://aws13032026restart/ --recursive --acl public-read

Result: 

[ec2-user@ip-10-200-0-72 sysops-activity-files][ec2-user@ip-10-200-0-72 sysops-activity-files]$ aws s3 cp /home/ec2-user/sysops-activity-files/static-website/ s3://aws13032026restart/ --recursive --acl public-read
Completed 256.0 KiB/21.0 MiB (2.6 MiB/s) with 1Completed 512.0 KiB/21.0 MiB (5.2 MiB/s) with 1Completed 768.0 KiB/21.0 MiB (7.7 MiB/s) with 1Completed 1.0 MiB/21.0 MiB (10.2 MiB/s) with 10Completed 1.2 MiB/21.0 MiB (12.6 MiB/s) with 10Completed 1.5 MiB/21.0 MiB (14.6 MiB/s) with 10Completed 1.8 MiB/21.0 MiB (16.9 MiB/s) with 10Completed 1.8 MiB/21.0 MiB (16.6 MiB/s) with 10upload: static-website/css/styles.css to s3://aws13032026restart/css/styles.css
Completed 1.8 MiB/21.0 MiB (16.6 MiB/s) with 9 Completed 2.0 MiB/21.0 MiB (18.8 MiB/s) with 9 Completed 2.3 MiB/21.0 MiB (21.0 MiB/s) with 9 Completed 2.3 MiB/21.0 MiB (18.7 MiB/s) with 9 upload: static-website/images/Coffee-Shop.png to s3://aws13032026restart/images/Coffee-Shop.png
Completed 2.3 MiB/21.0 MiB (18.7 MiB/s) with 8 Completed 2.5 MiB/21.0 MiB (19.6 MiB/s) with 8 Completed 2.8 MiB/21.0 MiB (20.3 MiB/s) with 8 Completed 3.0 MiB/21.0 MiB (21.9 MiB/s) with 8 Completed 3.3 MiB/21.0 MiB (23.5 MiB/s) with 8 Completed 3.5 MiB/21.0 MiB (25.2 MiB/s) with 8 Completed 3.8 MiB/21.0 MiB (26.7 MiB/s) with 8 Completed 4.0 MiB

[ec2-user@ip-10-200-0-72 sysops-activity-files]$ aws s3 ls aws13032026restart
                           PRE css/
                           PRE images/
2026-03-14 00:41:53       2980 index.html
[ec2-user@ip-10-200-0-72 sysops-activity-files]$

### On the AWS Management Console, on the Amazon S3 console, choose your bucket name.
### Choose the Properties tab. At the bottom of the this tab, note that Static website hosting is Enabled. Running the aws s3 website AWS CLI command turns on the static website hosting for an Amazon S3 bucket. This option is usually turned off by default. To open the URL on a new page, choose the Bucket website endpoint URL that displays. 

### 8 Create a batch file to make updating the website repeatable

[ec2-user@ip-10-200-0-72 sysops-activity-files]$ history
    1  pwd
    2  aws configure
    3  aws s3api create-bucket --bucket <MyWebPageBucket> --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
    4  aws s3api create-bucket --bucket <MyWebPageBucketrestar> --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
    5  aws s3api create-bucket --bucket MyWebPageBucketrestar --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
    6  aws s3api create-bucket --bucket Aws13032026restart --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
    7  aws s3api create-bucket --bucket aws13032026restart --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
    8  aws s3 ls
    9  aws iam create-user --user-name awsS3user
   10  aws iam create-login-profile --user-name awsS3user --password Training123!
   11  aws iam list-policies --query "Policies[?contains(PolicyName,'S3')]"
   12  aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --user-name awsS3user
   13  cd ~/sysops-activity-files
   14  tar xvzf static-website-v2.tar.gz
   15  aws s3 website s3://<my-bucket>/ --index-document index.html
   16  aws s3 ls
   17  aws s3 website s3://aws13032026restart/ --index-document index.html
   18  aws s3 cp /home/ec2-user/sysops-activity-files/static-website/ s3://aws13032026restart/ --recursive --acl public-read
   19  aws s3 ls <my-bucket>
   20  aws s3 lsaws s3 aws13032026restart
   21  aws s3 ls aws13032026restart
   22  history
[ec2-user@ip-10-200-0-72 sysops-activity-files]$ cd ~
[ec2-user@ip-10-200-0-72 ~]$ pwd
/home/ec2-user
[ec2-user@ip-10-200-0-72 ~]$

## run touch update-website.sh
## vi vi update-website.sh
## add the standard first line of a bash file and then add the s3 cp line from your history
### #!/bin/bash
aws s3 cp /home/ec2-user/sysops-activity-files/static-website/ s3://aws13032026restart/ --recursive --acl public-read
### :wq and then press Enter.
### chmod +x update-website.sh
### run ls -la you will got -rwxrwxr-x  1 ec2-user ec2-user 130 Mar 14 00:48 update-website.sh
### local copy of the index.html file in a text editor, run the following command:
### vi sysops-activity-files/static-website/index.html
### find what you want to change with /
### press i for insert
### To update the website, run your batch file.