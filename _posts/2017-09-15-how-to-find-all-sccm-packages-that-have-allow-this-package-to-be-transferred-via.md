---
layout: post
title: "How to find all SCCM packages that have \"Allow this package to be transferred via multicast\" enabled using Powershell"
date: 2017-09-15 03:35:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
tags:
  - "ConfigMgr"
  - "SCCM"
  - "Powershell"
---

This post was based on a question I came across online that I thought might be simple, but it wasn't as straightforward as I had hoped when looking at the Powershell output for Get-CMPackage.  
  
What the person was trying to do is list all packages that were enabled for transfer via multicast. I took a test package from my lab environment and listed all of it's properties using Powershell:  
  
Get-CMPackage -Id $ID | Select-Object -Property *  
  
Although there is no obvious property for multicast transfer, I could see that every time I checked or unchecked the box for multicast transfer, the value for the PkgFlags property was changed.  
  
I took a look at the MSDN documentation for the [SMS_PackageBaseClass](<https://msdn.microsoft.com/en-us/library/cc146062.aspx>) and found that while there are some values listed for PkgFlags, there was no value listed for handling multicast transfer:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg6JnGFTijnwlSCcvrG4kWL1oLjjmcVwuhVw7qQ9KW1PE750gj7Sxg45ts74VQSXFklu5V06dYDoEC9iK6dxLkAFQbUQaWQipOe6i0YiYkVqdNl7-w-aX0vCc3Y9-RPggKyAZtbNddJhg4/s640/pkgflags.PNG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg6JnGFTijnwlSCcvrG4kWL1oLjjmcVwuhVw7qQ9KW1PE750gj7Sxg45ts74VQSXFklu5V06dYDoEC9iK6dxLkAFQbUQaWQipOe6i0YiYkVqdNl7-w-aX0vCc3Y9-RPggKyAZtbNddJhg4/s1600/pkgflags.PNG>)

I stumbled across an old post on [MyITForum](<http://www.myitforum.com/forums/Scripting-SCCM-Distribution-Point-Setting-m228044.aspx>) that explained that the multicast value (27) was undocumented.  
  
I was able to take that information and combine it with a post [Greg Ramsey ](<https://gregramsey.net/2013/02/14/how-to-list-packages-that-are-configured-to-use-a-package-share-in-configmgr-2012/>)had made on checking package properties with Powershell and put together this short snippet of code:  
  
Get-CMPackage | ForEach-Object {  
if ($_.pkgflags -eq ($_.pkgflags -bor 0x8000000)) {  
"$($_.name)"  
}  
}  
  
If you run that bit of Powershell it will list the names of each package that is configured for Multicast.
