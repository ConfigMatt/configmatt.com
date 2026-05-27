---
layout: post
title: "Cloud Management Gateway - Finally connected"
date: 2017-06-22 22:52:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
tags:
  - "Cloud Management Gateway"
  - "Azure"
  - "CMG"
  - "SCCM"
---

Hi All, Back with an update to my previous blog post regarding issues we experienced when setting up our cloud management gateway. I was finally able to work through my remaining problems with Microsoft Support, so I figured it would be helpful to share my findings. Here are a few things that we wound up doing: Removed and rebuilt the CMG using a new SSL certificate. The previous certificate, while it was able to build the instance was build with a CNG (cryptographic next generation) template which is not supported by Configuration Manager. After rebuilding the CMG, we began seeing this error in the SMS_CloudConnector.log file:  
  
ERROR: Failed to build Http connection bc3945e0-708c-403d-881a-03469c4cc4a8 with server xxx.CLOUDAPP.NET:443. Exception: System.Net.WebException: The remote server returned an error: (990) BGB Session Ended.~~ at System.Net.HttpWebRequest.GetResponse()~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.HttpConnection.Send(Boolean isProxyData, Byte[] data, Int32& statusCode, Byte[]& payload)~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.ConnectionBase.Start()~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.ConnectionManager.MaintainConnections()   
  
We decided to tackle the errors in SMS_CloudConnector.log that indicated the connector role was unable to connect on port 10140, even though according to the documentation that port (and the rest of the range, 10124-10156) were only required if running more than one VM instance for the CMG. This required a firewall change to allow the connection to be built. We also removed and re-added the Cloud Proxy Connector role and then we finally began seeing a connection being created and maintained in the log files. After that, our client was still showing errors in the locationservices.log on our test client, here are a few for example (and for easier Googling):  
  
Failed to refresh Site Signing Certificate over HTTP with error 0x87d0027e. Failed to send management point list Location Request Message to XXX.CLOUDAPP.NET/CCM_Proxy_MutualAuth/72057594037928290 LSUpdateInternetManagementPoints: Failed to retrieve internet MPs from MP XXX.CLOUDAPP.NET/CCM_Proxy_MutualAuth/72057594037928290 with error 0x87d00231, retaining previous list.  
  
We restarted the WWW Publishing Service on the CMG server (we likely could have just restarted the Cloud Management Gateway via the SCCM console as well) and after that our client was able to connect. I was able to deploy an application that I had previously distributed to our Cloud Distribution Point, then refresh policy on the client to begin the installation over the internet. I am still seeing some issues with performing software update scans against our Software Update Point/WSUS server. I'll make sure to make a new blog post with the solution to that once I have it figured out. Hope this helps someone out there struggling to get their CMG up and running. -Matt
