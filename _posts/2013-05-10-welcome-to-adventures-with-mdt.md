---
layout: post
title: "Welcome To Adventures with MDT"
date: 2013-05-10 22:25:00 +0000
author: Matt Atkinson
categories: ["MDT"]
---

Welcome to my new blog "Adventures with MDT". This blog will focus on Windows operating system deployment and specifically the [Microsoft Deployment Toolkit](<http://technet.microsoft.com/en-us/solutionaccelerators/dd407791.aspx>).  
  
Let me go ahead and provide some background on how I got started with MDT and operating system deployment in general. When I started with my current employer in 2008 we had very poor operating system deployment methods. Typically a technician would open a new PC and modify the existing factory OS (Windows XP at the time) installation to add needed programs or customizations, remove manufacturer installed bloatware and clone the disk using a hard drive duplicator to the drives from any other identical machines that had been purchased at the same. No Sysprep was done so many of the machines had duplicate SIDs, we had no way to deploy the same image to different hardware models, and we were lucky if someone was willing to take the time to create a Norton Ghost image of the drive so we could image more identical machines later. All around, a horrible process resulting in lots of wasted time, poorly configured machines, and frustrated users.  
  
  
Once I had progressed beyond basic help desk duties it was a logical move for me to improve our OS deployment process. My first attempts were crude, but still an improvement over the old ways. I began doing customized Windows XP installations using a combination of [nLite](<http://www.nliteos.com/>) to automate the installation of Windows, and scripted application installs that occurred after Windows setup. Once completed, we would run Sysprep and then capture a disk image which we could then deploy over the network using Novell Zenworks.  
  
This continued until it was time to start seriously looking at our migration plan to Windows 7. I had attended a Microsoft presentation to introduce Windows 7 and it was there that I first heard of the Microsoft Deployment Toolkit. I was quite impressed when I learned what MDT could do, and could hardly believe that Microsoft would give such a great product away for no cost. I didn't have to consider licensing, or even ask management for new hardware to run it on, it ran fine on a spare desktop PC that I had sitting around.  
  
Once I began using MDT it really opened my eyes to how much I enjoyed OS deployment, and client management in general. We have since also migrated to System Center Configuration Manager approximately a year ago which although I still consider myself new to, has really changed the way our organization looks at client management as a whole.  
  
So, to close out this first post, thanks for reading and I sincerely hope you will benefit from reading about my adventures with MDT. Please check back for new posts where I'll be providing tutorials on using the product, and solutions to problems that I have worked through.
