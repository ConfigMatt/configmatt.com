---
layout: post
title: "Monitoring potentially dangerous deployments using System Center Configuration Manager + Powershell"
date: 2017-05-26 21:42:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
tags:
  - "ConfigMgr"
  - "SCCM"
  - "Powershell"
---

Update 8/26/2019: Updated GitHub gists, replaced broken images, and added pre-requisite steps. Latest versions of the script will be uploaded to my GitHub repository: <https://github.com/ConfigMatt/ConfigMattScripts>  
  
I've always been concerned about the potential for applications or task sequences to be deployed accidentally to the wrong collection or inadvertently made mandatory when they should only be available as an optional install. Config Manager has no built in method to alert you about potentially dangerous deployments that have been created, so it's up to the community to build our own tools to add this functionality.  
  
I had previously devised a method for generating email alerts utilizing WMI event subscriptions to query for every time a deployment was created and run a Powershell script to gather some data about the deployment and send an email alert if the deployment met some specific criteria. This method, while it works, generates additional overhead and resource consumption on the SCCM site server even when no deployments have been created due to the constant WMI queries.  
  
When researching alternate methods to accomplish the same goal with less resource utilization, a fellow administrator recommended that I check out a feature in Config Manager which has existed in the product for some time, but I personally had never made use of: Status Filter Rules. I also did not find very much information online about other people making use of this feature, but I was able to find enough documentation to piece together a functional alerting system for deployments. Although this is only setup to send an email when there is a deployment to a collection with greater than a certain number of computers, the sky is the limit on what you do, you could just as easily set the script to automatically delete the deployment as well. In this instance I just wanted to have it give me a chance to catch these deployments to investigate whether or not they were done in error, all remediation would still need to be done manually. Depending on the size of your environment and the client policy check interval, it's still possible that clients could perform a policy update and install an application that was deployed in error.  
  
First, we have two important pre-requisites that need to be completed before the script will be able to function.  
  
1\. Windows Remote Server Admin Tools (RSAT) needs to be installed on your site server to enable the cmdlets for querying the deployment creator information from Active Directory.  
2\. You need to import the certificate used to digitally sign the ConfigurationManager Powershell module to the trusted publisher store of the site server. More details on this step are located in [this TechNet article](<https://blogs.technet.microsoft.com/microsoft_denmark_premier_field_engineering_config_manager_blog/2013/01/30/running-configuration-manager-2012-powershell-scripts-as-a-service-account-or-local-system/>).  
  
There are 2 pieces to the alerting system, the Status Filter Rules themselves, and the Powershell scripts that are triggered by the rules. Since the rules are based upon Configuration Manager status messages, I created 2 separate rules, one for Application deployments, and one for Packages and Task Sequence deployments.  
  
You access the Status Filter Rules from the Administration pane of the admin console, then by going to Overview>Site Configuration>Sites. Right click on your primary site where you want to setup the rule and select Status Filter Rules from the right click menu:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgbvZQ4oQlWrRaTSe3aOnCyjrs6YFytiUHHM7Ttt0KdK4-7orkFuWVRBqLkzTQZcH07fBRBqB5uwmyyW5-Qt-C6OvARJykwjMXLZdRKuiIKYMOillMlHB3e9tjg1Ucl_rrRBqNwaj8bDec/s1600/0.jpg)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgbvZQ4oQlWrRaTSe3aOnCyjrs6YFytiUHHM7Ttt0KdK4-7orkFuWVRBqLkzTQZcH07fBRBqB5uwmyyW5-Qt-C6OvARJykwjMXLZdRKuiIKYMOillMlHB3e9tjg1Ucl_rrRBqNwaj8bDec/s1600/0.jpg>)

  

  

  

  
  
Once you are in the Status Filter Rules, click on the create button to setup a new rule. Once you are in the wizard there are 2 tabs, the first tab defines the trigger conditions you want to check and the second tab defines the actions that you want to take when the trigger occurs. Here are some screenshots from my rule to alert me on an application deployment:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFEQ16-FWZjyM-23BlmGy3E7nVfKLhKDjYpqBgJ5szYzWLdgGA3qMder18XSpYSuWVXqVnGLfs9tExtYBITW1N3zNLNDbxp4-wX8CXdIqxiTQGp0sc4KO6EW14vHQrjtGCZ6GPoT8Q7jM/s1600/1.jpg)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFEQ16-FWZjyM-23BlmGy3E7nVfKLhKDjYpqBgJ5szYzWLdgGA3qMder18XSpYSuWVXqVnGLfs9tExtYBITW1N3zNLNDbxp4-wX8CXdIqxiTQGp0sc4KO6EW14vHQrjtGCZ6GPoT8Q7jM/s1600/1.jpg>)

  
  
You can see we are triggering this rule anytime the message ID 30226 is generated. 30226 means that an Application deployment has been created.  
  
Here is the second tab:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnI98QopBUDvnSYuK0GHNJ9RKd5p7EUct1SFM6asX_J1f5XfCW9-HJSX5MwyJrIbIK1hDF8eUcM8Wk0AYZa9XWujfH0TfRfBFnGuhold0BM80Qqd3TTSkflQssl2Gmv5U5zC1EFjHyxpY/s1600/2.jpg)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnI98QopBUDvnSYuK0GHNJ9RKd5p7EUct1SFM6asX_J1f5XfCW9-HJSX5MwyJrIbIK1hDF8eUcM8Wk0AYZa9XWujfH0TfRfBFnGuhold0BM80Qqd3TTSkflQssl2Gmv5U5zC1EFjHyxpY/s1600/2.jpg>)

  
  
It is essentially just the "Run Program" field, with the following command to run a Powershell script that exists on the Site Server in the D:\Scripts\DeploymentMonitor directory:  
  
c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe -executionpolicy bypass D:\Scripts\DeploymentMonitor\ApplicationDeploymentMonitor.ps1 -AssignmentID %msgis02 -creator %msgis01  
  
The %msgis02 parameter is the second field that is inserted in the status message, and in this instance it is equal to the deployment ID, %msgis01 is the username of the person who created the deployment. More info about the various parameters that can be passed to your program are available here:  
  
https://technet.microsoft.com/en-us/library/bb693758.aspx  
  

  
Here is the content of ApplicationDeploymentMonitor.ps1, something to note is that I do not claim to be an expert at Powershell, this code works perfectly for me, but I'm sure there is a lot of room for improvement:  
  
  
  
  
You need to configure the script values including site code, mail servers, and warning threshold to match what is appropriate for your environment. In my script, I want to get an email for any deployment to more than 500 computers, but you may want to adjust that lower or higher as needed.  
  
Since we a different message ID for package and task sequence deployments, I created a second rule to alert me when those are deployed. Here are the screenshots of that rule, including message ID 30006:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-EqaEPrNwB7c70jb9shsHpJH8cjyS_HdzVw3T2wEjCOSy5c_esGm20g5C8nPOdanh9p9mXaWCDmFraGvV4x6HZ9Fe7XtklltnLOKVmZYZ2bYyYq-LBrWy3tIXyfS-znXQAzrZfdtIip4/s1600/3.jpg)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-EqaEPrNwB7c70jb9shsHpJH8cjyS_HdzVw3T2wEjCOSy5c_esGm20g5C8nPOdanh9p9mXaWCDmFraGvV4x6HZ9Fe7XtklltnLOKVmZYZ2bYyYq-LBrWy3tIXyfS-znXQAzrZfdtIip4/s1600/3.jpg>)

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi_cvH8uuF2T7mq96pJaErUHUy22fGgaWQvCfnFqd6acVY8clBOWcH5JORaAfRnL_pwJ7E3h3TyN233M33xTDo7pqwsk6UnXZaZ5WCooTZuC_6vNavIos1uRD7InOUYGaszh8jybQRkAIE/s1600/4.jpg)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi_cvH8uuF2T7mq96pJaErUHUy22fGgaWQvCfnFqd6acVY8clBOWcH5JORaAfRnL_pwJ7E3h3TyN233M33xTDo7pqwsk6UnXZaZ5WCooTZuC_6vNavIos1uRD7InOUYGaszh8jybQRkAIE/s1600/4.jpg>)

  
  
Here is my command that I am running in order to pass the parameter to my Powershell script:  
  
c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe -executionpolicy bypass D:\Scripts\DeploymentMonitor\PackageDeploymentMonitor.ps1 -assignmentID %msgis02 -creator %msgis01  
  
And here is the content of the PackageDeploymentMonitor.ps1 script:   
  
  
Here is the text of an email alert that was generated during the testing of this script, so that you have an idea of what to expect:  
  
TEST FileZilla FTPClient 3.5.2 is being Installed on 1 assets.  
  
The deployment type is Available and will become available at 6/22/2016 3:27:00 PM.  
  
The Assignment ID is {B7DC5AA8-C14C-4E54-AB3A-97776054645B}.  
  
Hopefully this will be helpful to other administrators out there, If you've got feedback or questions about the setup of the alerting rule, please feel free to send me a message.
