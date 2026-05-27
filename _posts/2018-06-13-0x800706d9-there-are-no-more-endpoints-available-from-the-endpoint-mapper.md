---
layout: post
title: "0x800706d9 - There are no more endpoints available from the endpoint mapper"
date: 2018-06-13 02:46:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

Just adding a quick post with a recent issue we ran in to on some of our endpoint devices. When trying to download SCCM client policy, we were seeing the error message "0x800706d9 \- There are no more endpoints available from the endpoint mapper" in the datatransferservice.log.  
  
Coincidentally, these devices had been recently upgraded to Windows 10.  
  
The root cause for the issue turned out to be that the Windows Firewall service was disabled. At some point a technician must have decided that was a necessary change, but (at least in Windows 10) BITS downloads will fail unless the Windows Firewall service is running.
