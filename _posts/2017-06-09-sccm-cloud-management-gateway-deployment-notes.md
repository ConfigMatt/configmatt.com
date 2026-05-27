---
layout: post
title: "SCCM Cloud Management Gateway Deployment Notes"
date: 2017-06-09 01:57:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
tags:
  - "ConfigMgr"
  - "Azure"
  - "Cloud Management Gateway"
  - "CMG"
  - "SCCM"
---

Hi All,  
  
I've been working this week on getting the new Cloud Management Gateway that was introduced in Configuration Manager 1610 deployed. I ran in to a few issues during the deployment that I figured would be worth writing a blog post about, maybe they will help someone else out there if they encounter the same issue.  
  
The first problem we had during the setup was manifested by the following errors in Cloudmgr.log:  
  
ERROR: TaskManager: Task [CreateDeployment for service ORGCMG] has failed. Exception System.TypeLoadException, Could not load type 'System.Runtime.Diagnostics.ITraceSourceStringProvider' from assembly 'System.ServiceModel.Internals, Version=4.0.0.0, Culture=neutral, PublicKeyToken=...  
  
ERROR: Exception occured for service ORGCMG : System.TypeLoadException: Could not load type 'System.Runtime.Diagnostics.ITraceSourceStringProvider' from assembly 'System.ServiceModel.Internals, Version=4.0.0.0, Culture=neutral, PublicKeyToken=.'.~~ at System.ServiceModel.Channels.TextMessageEncoderFactory..ctor(MessageVersion version, Encoding writeEncoding, Int32 maxReadPoolSize, Int32 maxWritePoolSize, XmlDictionaryReaderQuotas quotas)~~ at System.ServiceModel.Channels.HttpTransportDefaults.GetDefaultMessageEncoderFactory()~~ at System.ServiceModel.Channels.HttpChannelFactory`1..ctor(HttpTransportBindingElement bindingElement, BindingContext context)~~ at System.ServiceModel.Channels.HttpsChannelFactory`1..ctor(HttpsTransportBindingElement httpsBindingElement, BindingContext context)~~ at System.ServiceModel.Channels.HttpsTransportBindingElement.BuildChannelFactory[TChannel](BindingContext context)~~ at System.ServiceModel.Channels.Binding.BuildChannelFactory[TChannel](BindingParameterCollection parameters)~~ at System.ServiceModel.Channels.ServiceChannelFactory.BuildChannelFactory(ServiceEndpoint serviceEndpoint, Boolean useActiveAutoClose)~~ at System.ServiceModel.ChannelFactory.CreateFactory()~~ at System.ServiceModel.ChannelFactory.OnOpening()~~ at System.ServiceModel.Channels.CommunicationObject.Open(TimeSpan timeout)~~ at System.ServiceModel.ChannelFactory.EnsureOpened()~~ at System.ServiceModel.ChannelFactory`1.CreateChannel(EndpointAddress address, Uri via)~~ at Microsoft.ConfigurationManager.AzureManagement.ServiceManagementHelper.CreateServiceManagementChannel(ServiceEndpoint endpoint, X509Certificate2 cert)~~ at Microsoft.ConfigurationManager.AzureManagement.ManagementOperation.InitializeChannel(X509Certificate2 certificate)~~ at Microsoft.ConfigurationManager.CloudServicesManager.CreateDeploymentTask.CheckAzureAccess()~~ at Microsoft.ConfigurationManager.CloudServicesManager.CreateDeploymentTask.Start(Object taskState).  
  
The strange thing here was that the true error message wasn't being displayed, just some error text that looked like it was coming from .net. The resolution for this wound up being that we were missing the .net 4.5.2 pre-requisite from our site server, so we weren't able to see the true error. I'm not sure how we managed to install the current branch version of SCCM with a missing pre-requisite, but it was definitely not there.  
  
Once we install .net 4.5.2 we were getting some meaningful errors reported in CloudMgr.log:  
ERROR: Communication exception occured. Http Status Code: BadRequest, Error Message: The private key for the remote desktop certificate cannot be accessed. This may happen for CNG certificates that are not supported for Remote Desktop., Exception Message: The remote server returned an unexpected response: (400) Bad Request..  
  
This problem was found to be caused by the private key in our CMG certificate not being marked as exportable, even though the template we generated it with was configured with the option to export the private key. We confirmed the private key issue by running "certutil -store my" from a command prompt after importing the certificate.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiHtgRTofrCW0k4twXFn-NuPtZvVYENNWz4Q4qMm0_PAfv_TVN3L9oJ7lT9aH7eypW_G9Orh7_M3EpgPRcnaWyuDTl_CtGaGbzKfBGtXncY6x_fTYLZ1qMcSm1SXKtR1CMzwhYlFkWRK18/s320/Certutil.PNG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiHtgRTofrCW0k4twXFn-NuPtZvVYENNWz4Q4qMm0_PAfv_TVN3L9oJ7lT9aH7eypW_G9Orh7_M3EpgPRcnaWyuDTl_CtGaGbzKfBGtXncY6x_fTYLZ1qMcSm1SXKtR1CMzwhYlFkWRK18/s1600/Certutil.PNG>)

  
We took this issue to our folks that manage our PKI and they were able to correct the problem with the certificate utility OpenSSL to export and then re-attach the private key. Once we then ran the CMG setup wizard with the corrected certificate it was able to communicate properly to Azure and spawn the instances for the service.  
  
The next step is to add the Cloud Proxy Connector Role to a site system, typically I have heard recommendations that this service should be added to a management point server, so that is what we elected to do. Once we starting checking the SMS_Cloud_ProxyConnectory.log we were seeing a constant stream of errors for it failing to communicate with the Azure instances:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgw1jAJjgglwjEKAHRjMm4HLlgLxg6-3yrqq0LWyG0xMUeEV5vjL0CmD3_fXtHL5SKVmL9JE7ruw_zgQeNpHenmHnYSaredRnzXUKsLjeKB22idRh0MzMg_jeHzx8YfHfCVlesrTV9KlW8/s400/CloudConnector.PNG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgw1jAJjgglwjEKAHRjMm4HLlgLxg6-3yrqq0LWyG0xMUeEV5vjL0CmD3_fXtHL5SKVmL9JE7ruw_zgQeNpHenmHnYSaredRnzXUKsLjeKB22idRh0MzMg_jeHzx8YfHfCVlesrTV9KlW8/s1600/CloudConnector.PNG>)

  
  
Here is the error text:  
ERROR: Failed to build Tcp connection 41320a1b-5250-4f4f-b95a-0fccac4ef817 with server .CLOUDAPP.NET:10141. Exception: System.Net.WebException: TCP CONNECTION: Failed to authenticate with proxy server ---> System.IO.IOException: Unable to read data from the transport connection: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond. ---> System.Net.Sockets.SocketException: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond~~ at System.Net.Sockets.NetworkStream.Read(Byte[] buffer, Int32 offset, Int32 size)~~ --- End of inner exception stack trace ---~~ at System.Net.Sockets.NetworkStream.Read(Byte[] buffer, Int32 offset, Int32 size)~~ at System.Net.FixedSizeReader.ReadPacket(Byte[] buffer, Int32 offset, Int32 count)~~ at System.Net.Security.SslState.StartReceiveBlob(Byte[] buffer, AsyncProtocolRequest asyncRequest)~~ at System.Net.Security.SslState.StartSendBlob(Byte[] incoming, Int32 count, AsyncProtocolRequest asyncRequest)~~ at System.Net.Security.SslState.ProcessReceivedBlob(Byte[] buffer, Int32 count, AsyncProtocolRequest asyncRequest)~~ at System.Net.Security.SslState.StartReceiveBlob(Byte[] buffer, AsyncProtocolRequest asyncRequest)~~ at System.Net.Security.SslState.StartSendBlob(Byte[] incoming, Int32 count, AsyncProtocolRequest asyncRequest)~~ at System.Net.Security.SslState.ForceAuthentication(Boolean receiveFirst, Byte[] buffer, AsyncProtocolRequest asyncRequest)~~ at System.Net.Security.SslState.ProcessAuthentication(LazyAsyncResult lazyResult)~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.TcpConnection.Connect()~~ --- End of inner exception stack trace ---~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.TcpConnection.Connect()~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.ConnectionBase.Start()~~ at Microsoft.ConfigurationManager.CloudConnection.ProxyConnector.ConnectionManager.MaintainConnections()  
  
After looking at the errors being generated we noticed the connection attempts were all happening on ports 10140/10141/10125/10126. Looking over the [CMG documentation](<https://docs.microsoft.com/en-us/sccm/core/clients/manage/plan-cloud-management-gateway>) for ports in use, it calls out that these ports are used when you are using multiple instances to run the CMG, but if you deploy just a single instance it will use only port 443. We were able to confirm with our security team that the ports for multiple instances were being blocked by our firewall. We removed our multiple instance CMG and set it up again this time specifying a single instance to build out in Azure and once the management point picked up the change in DNS resolution to the new IP address of the rebuilt instance it was able to connect successfully.  
  
Now that I appeared to have a fully function CMG, I configured a test client to use internet communications only and tried to perform a policy check. This failed due to what I believe is an issue with the SSL certificate that we have installed on the management point. Once I have a solution to that issue I will update this post with more information, but I thought it would be helpful to others to get these first few errors I encountered out on the web and indexed by Google so they can be found.
