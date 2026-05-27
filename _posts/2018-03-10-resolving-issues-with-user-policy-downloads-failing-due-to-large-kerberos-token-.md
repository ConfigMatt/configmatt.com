---
layout: post
title: "Resolving issues with user policy downloads failing due to large Kerberos token sizes"
date: 2018-03-10 00:11:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

Hi All!  
First post in a long time, but we just solved an issue in our production environment that others may run in to so I figured I would share the solution.   
We were having issues with some users not receiving an application that was being deployed to a user collection. We could tell that the users were not downloading the policy object that would install the application, because we could see the following errors in the policyagent.log file when attempting to perform a user policy refresh: 

> Synchronous policy assignment request with correlation guid {109B537A-194F-4171-A803- 5022A6C7D27F} for User $UserGUIDHere completed with status 80070005

  
  
We could correlate those errors with the following messages in the IIS log on the management point: 

> CCM_POST /ccm_system_windowsauth/request - 80 - $IPAddressHere ccmhttp - 401 2 5 0

  
  
We checked in with our Microsoft PFE and he said it looked like we were seeing issues due to the large Kerberos tokens some of our users have due to large numbers of group memberships. We have configured a GPO in our environment that increases the max token size, but he pointed out a link to us that matched up with what we were seeing:   
<https://blogs.msdn.microsoft.com/ashishsingh/2010/04/03/windows-authentication-for-accounts-with-large-kerberos-tickets-may-not-work-despite-having-maxtokensize-in-place/>   
  

> The full path of the registry keys is  _HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\HTTP\Parameters_. The keys have to be added as DWORD's. Their description says   
>    
>    
>  MaxFieldLength \- Sets an upper limit for each header. See MaxRequestBytes. This limit translates to approximately 32k characters for a URL. Default Value – 16384, Range 64 - 65534 (64k - 2) bytes   
>    
>    
>  MaxRequestBytes -Determines the upper limit for the total size of the Request line and the headers. Its default setting is 16KB. If this value is lower than MaxFieldLength, the MaxFieldLength value is adjusted.   
>  Default Value – 16384, Range 256 - 16777216 (16MB) bytes

  
We configured the registry keys with the following values:  
MaxFieldLength: 65534  
MaxRequestBytes: 16777216  
  
We also had to reboot the server before the changes would take effect, simply restarting IIS was not enough to see a change in the client behavior.  
  
After reboot we again tried to do a user policy refresh from the client and were successful and no longer saw the 80070005 errors in the policyagent.log
