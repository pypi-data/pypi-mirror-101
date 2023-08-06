# pcpt-cde


Utility tool for the pingcloud cde environment, using this tool you can do following: 

  - Show summary of eks cluster, autoscale groups scheduled actions & s3 bucket details
  - Setup ssm session with management node
  - Delay scheduled action to scale-in(min:max 0:0) by number(1-5) of hours
  - Scale-out autoscale groups to scheduled scale-out min:max value
  - Scale-in autoscale groups to min:max 0:0

## cli & stdout
Get help

```sh
$ pcpt-cde -h

usage: pcpt-cde [-h] -p PROFILE_NAME [-s] [-d HOURS_TO_ADD] [-o] [-i] [-v]

Utility tool for the pingcloud cde environment

optional arguments:
  -h, --help       show this help message and exit
  -p PROFILE_NAME  aws profile name, example: coral-stage, coral-stage-eu1
  -s               show environment details
  -d HOURS_TO_ADD  delay start of existing scale-in scheduler by number of hours: range(1,720), example: 720 for 30 days
  -o               scale-out worker node asg, retrives scale-out values from the existing scheduler
  -i               scale-in worker node asg, sets min:max to 0:0
  -v               show program's version number and exit

```

Create session with coral-stage management node

```sh
$ pcpt-cde -p coral-stage

2021-04-08 10:18:34 - Checking aws configuration for profile name: coral-stage
2021-04-08 10:18:34 - start saml session
credentials are not expired skipping
2021-04-08 10:18:34 - Looking for instance id with tag value suffix management-server
2021-04-08 10:18:37 - Starting ssm session with instance: i-0bec1da4996e7daca

Starting session with SessionId: botocore-session-1617841060-0f11dc5306fec2281
```

Get a summary of cde environment
```sh
$ pcpt-cde -p coral-stage -s

+--------------+--------+---------+----------------------------------+
| Cluster Name | Status | Version |            created on            |
+--------------+--------+---------+----------------------------------+
|    stage     | ACTIVE |   1.15  | 2020-08-28 08:09:21.645000+10:00 |
+--------------+--------+---------+----------------------------------+
+---------+-----------------------------------------------------------------+
| Purpose |                         S3 Bucket Name                         |
+---------+-----------------------------------------------------------------+
|  Backup |  cust-stage-coral-3-0610e4b4-4c2b-4-s3backupbucket-zujz6tgvejwd |
|   Log   | cust-stage-coral-3-0610e4b4-4c2b-4929-s3logbucket-1tgryd47uspdu |
+---------+-----------------------------------------------------------------+
+------------------------------------------+--------------+-----+-----+---------+----------------------+--------------------------------------+
|           WorkerNode asg name            | InstanceType | Min | Max | Desired | Scale-in action name | Scale-in action start datetime (UTC) |
+------------------------------------------+--------------+-----+-----+---------+----------------------+--------------------------------------+
| eks-0cbc47b6-b505-ccb1-cc3c-8e519e7ab589 |  c5.2xlarge  |  1  |  5  |    1    |    PingCloudStop     |      2021-04-10 00:30:28+00:00       |
| eks-64bc47b6-b756-0c89-416e-8fd1006fd436 |  r5.xlarge   |  1  |  3  |    1    |    PingCloudStop     |      2021-04-10 00:30:29+00:00       |
| eks-7ebc47b6-b74f-94b8-3224-6be63b918882 |  r5.xlarge   |  1  |  3  |    1    |    PingCloudStop     |      2021-04-10 00:30:31+00:00       |
| eks-80bc47b6-b832-b43c-4657-9cf3cefcff7f |  c5.2xlarge  |  1  |  5  |    2    |    PingCloudStop     |      2021-04-10 00:30:32+00:00       |
| eks-a4bc47b6-b579-26cf-a497-8832429174e0 |  c5.2xlarge  |  1  |  5  |    2    |    PingCloudStop     |      2021-04-10 00:30:34+00:00       |
| eks-d6bc47b6-b753-46a7-82fa-b5f35f2ed119 |  r5.xlarge   |  1  |  3  |    1    |    PingCloudStop     |      2021-04-10 00:30:36+00:00       |
+------------------------------------------+--------------+-----+-----+---------+----------------------+--------------------------------------+```

Delay scale-in scheduled action by 2 days
```sh
$ pcpt-cde -d 48

Updated, action scale-in of asg: eks-6aba197d-e073-8a35-a6a6-75922300f25f to start on 2020-10-17 00:00:00+00:00
Updated, action scale-in of asg: eks-8cba197f-9a9d-f741-8e2c-fb905ab89a9c to start on 2020-10-17 00:00:00+00:00

$ pcpt-cde -a
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
|           WorkerNode asg name            | InstanceType | Min | Max | Desired | Scale-in action name | Scale-in action start date |
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
| eks-6aba197d-e073-8a35-a6a6-75922300f25f | m5a.4xlarge  |  1  |  2  |    1    |       scale-in       | 2020-10-17 00:00:00+00:00  |
| eks-8cba197f-9a9d-f741-8e2c-fb905ab89a9c | m5a.4xlarge  |  1  |  2  |    2    |       scale-in       | 2020-10-17 00:00:00+00:00  |
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
```

Scale-in all asg to min:max 0:0
```sh
$  pcpt-cde -i

Updated, asg: eks-6aba197d-e073-8a35-a6a6-75922300f25f to min:max 0:0
Updated, asg: eks-8cba197f-9a9d-f741-8e2c-fb905ab89a9c to min:max 0:0

$ pcpt-cde -a
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
|           WorkerNode asg name            | InstanceType | Min | Max | Desired | Scale-in action name | Scale-in action start date |
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
| eks-6aba197d-e073-8a35-a6a6-75922300f25f | m5a.4xlarge  |  0  |  0  |    0    |       scale-in       | 2020-10-17 00:00:00+00:00  |
| eks-8cba197f-9a9d-f741-8e2c-fb905ab89a9c | m5a.4xlarge  |  0  |  0  |    0    |       scale-in       | 2020-10-17 00:00:00+00:00  |
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
```

Scale-out all asg to min:max value of scale-out scheduled action
```sh
$  pcpt-cde -o

Updated, asg: eks-6aba197d-e073-8a35-a6a6-75922300f25f to min:max 2:1
Updated, asg: eks-8cba197f-9a9d-f741-8e2c-fb905ab89a9c to min:max 2:1

$ pcpt-cde -a
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
|           WorkerNode asg name            | InstanceType | Min | Max | Desired | Scale-in action name | Scale-in action start date |
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
| eks-6aba197d-e073-8a35-a6a6-75922300f25f | m5a.4xlarge  |  1  |  2  |    1    |       scale-in       | 2020-10-17 00:00:00+00:00  |
| eks-8cba197f-9a9d-f741-8e2c-fb905ab89a9c | m5a.4xlarge  |  1  |  2  |    1    |       scale-in       | 2020-10-17 00:00:00+00:00  |
+------------------------------------------+--------------+-----+-----+---------+----------------------+----------------------------+
```

### Installation

Install the dependencies on mac

- Install python3 & pip3
- Copy pcpt-cde.py and requirements.txt from the repo
- Update the permission of the script
```sh
$ chmod +x pcpt-cde.py
```
- Update/Copy aws configuration ref: https://gitlab.corp.pingidentity.com/ping-cloud-private-tenant/ping-cloud-tools/-/tree/master/shared-config
- Install and configure saml2aws ref:  https://confluence.pingidentity.com/display/PDA/Connect+to+a+CDE+and+CodeCommit+through+SSO+in+command+line|
- Install Python libs
```sh
$ pip3 install -r /path/to/requirements.txt
```
- create alias
```sh
$ alias pcpt-cde=python3 /path/to/pcpt-cde.py
```
- check version
```sh
$ pcpt-cde -v
```

### Dependencies

| Name | Note |
| ------ | ------ |
| saml2aws | Install and configure saml2aws ref: https://confluence.pingidentity.com/display/PDA/Connect+to+a+CDE+and+CodeCommit+through+SSO+in+command+line|
| aws configuration | For aws configuration ref: https://gitlab.corp.pingidentity.com/ping-cloud-private-tenant/ping-cloud-tools/-/tree/master/shared-config|
| Python3 | Only compatible with python3, available on management node |
| Python modules | Install depended modules in requirements.txt before executing this script (Check installation section for instruction) |
| IAM Policy | autoscaling:DeleteScheduledAction |
| IAM Policy | autoscaling:Describe*|
| IAM Policy | autoscaling:Put*|
| IAM Policy | autoscaling:UpdateAutoScalingGroup|


### Assumptions

| Name | Note |
| ------ | ------ |
| Autoscale Groups Tag | AWS autoscale group tag match cluster name |
| Scheduled Actions | Scheduled action already exists |


### Todos

 - Show R53 recordsets
 - Make package available on pipy


### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


License
----

