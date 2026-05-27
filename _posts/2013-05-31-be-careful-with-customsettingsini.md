---
layout: post
title: "Be careful with customsettings.ini"
date: 2013-05-31 03:07:00 +0000
author: Matt Atkinson
categories: ["MDT"]
---

Just a quick post on something I ran in to the other day while setting up a new deployment share. I attended the Microsoft Management Summit in Las Vegas this year and came back with big plans on how I could improve my deployment share using task sequence IDs in customsettings.ini. One of the things I had done was added domain join to the default section so it would no longer prompt the tech to enter credentials for joining the domain or even ask whether or not they wanted the machine to be a domain member, since all machines we image are domain joined 100% of the time. I added the SkipDomainJoin=YES line to the default section and it worked as intended when imaging machines, but when I tried to run a capture task sequence it would automatically bypass the capture image screen even though for that task sequence I had set SkipCature=NO.  
What I was able to determine was that since a capture task sequence would naturally not be able to join the domain, forcing a domain join in the default settings caused the capture portion of the sequence not to run. The solution was to move the domain join settings to the task sequence ID subsections and out of default.  
  
I'll post more of what this looks like soon, but wanted to get it posted while it was still fresh in my mind.
