---
layout: post
title: "Configuration Manager policy and content downloads failing over the VPN AKA  Error: 0x80200024, Description The job is not making progress."
date: 2020-04-15 02:59:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

Yet another bizarre troubleshooting exercise today that I think is worth sharing since due to the Covid-19 pandemic more and more users are working from home and using the VPN.  
  
We were alerted to this by our application deployment teams who noticed higher than normal numbers of computers reporting an unknown status during deployments. We were able to make a correlation that the majority of these devices were users at home connected via VPN (PaloAlto GlobalProtect in our case).  
  
Upon inspecting the datatransferservice.log on some of the client workstations, it was apparent that the policies for the deployment were not successfully being downloaded, with the BITS job reporting error 0x8020024. We also noticed this same error in ccmsetup.log for clients that were attempting to perform a client upgrade (we also installed ConfigMgr build 2002 the previous weekend):  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8M340ZhgKMlpQEHsiI0-FWlzF5ZT3aQSMUBwuxjBmMQ0pFYg9ygwtzsflpXAUvUvik8-k88mIuwCh5L6METJv6A063ZnJbzYF6KAqtpIYTRz5cTwsrO947QFjsXf4W8noBZpv1t45OwQ/s640/BITS1.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8M340ZhgKMlpQEHsiI0-FWlzF5ZT3aQSMUBwuxjBmMQ0pFYg9ygwtzsflpXAUvUvik8-k88mIuwCh5L6METJv6A063ZnJbzYF6KAqtpIYTRz5cTwsrO947QFjsXf4W8noBZpv1t45OwQ/s1600/BITS1.png>)

  
  
  
  
  
  
  
  
  
  
  
  
  
I started reviewing the traffic logs using Wireshark to try and get a better idea of what was happening at the network level, and once I isolated the traffic it became pretty apparent where things were going wrong:  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhA9GuVh3ZyNTVsQ_CBbSFy5afdcU17x5goLH4siOKguKjpmn5AM3zOn2qNEEcP7jGMCMCDAD6IzxkGUAIRSmXzwo-k4TOlW-TtcPMV6Q-29Rnp8ggLp-nQ97BUnOs5KYV-qdXPSKemQAs/s640/BITS2.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhA9GuVh3ZyNTVsQ_CBbSFy5afdcU17x5goLH4siOKguKjpmn5AM3zOn2qNEEcP7jGMCMCDAD6IzxkGUAIRSmXzwo-k4TOlW-TtcPMV6Q-29Rnp8ggLp-nQ97BUnOs5KYV-qdXPSKemQAs/s1600/BITS2.png>)

  
We can see the original GET request for the file, and then an immediate response from the server of HTTP 416 which corresponds with "requested range not satisfiable. Doing some Google searching turned up a few different forum threads (unrelated to ConfigMgr) where PaloAlto firewalls were blocking multithreaded downloads and sending the 416 response as if they were the server iteself. We were able to point our security team to a knowledge base article from [PaloAlto ](<https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClJsCAK>)with the necessary configuration changes.  
  
Once they made the change to the firewall, our downloads started to complete almost immediately, and the unknown computer count on our deployments began to decrease rapidly.
