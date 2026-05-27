---
layout: post
title: "Digging in to the new System Center Updates Publisher Preview"
date: 2017-07-04 06:12:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

Lo and behold Microsoft has finally released a new version of the System Center Updates Publisher (AKA SCUP) that was last updated in 2011. It is now known simply as System Center Updates Publisher, and includes a release month indicator for each new version (currently June Preview). I don't see any info that indicates this is unsupported by Microsoft despite the Preview designation.  
  
You can read the official blog post from Microsoft announcing the new version [here.](<https://blogs.technet.microsoft.com/enterprisemobility/2017/07/03/system-center-updates-publisher-june-2017-preview-is-now-available/>)  
  
The main focus for the update according to Microsoft was enabling the use of SCUP on Windows 10 and Server 2016, but I wanted to dig in to the tool a little bit and see what else was new under the hood, and I did in fact find that they fixed or at least improved some of the more annoying quirks that existed in the 2011 version.  
  
First thing that I noticed was fixed was that when you launch the installer it now properly prompts for elevation in a UAC prompt, where the 2011 version simply threw an error that it needed administrator permissions in order to install and required you to launch the installation from an administrator command prompt. It also does a pre-requisite check for .NET 4.5.2 and will direct you to install it if it is missing.  
  
The installation process itself is completely silent and I had to check the Start menu to see the new icon and program group.  
  
One other change that I noticed is that the application is now 64-bit and installs in C:\Program Files\Microsoft\UpdatesPublisher by default, where the 2011 version was a 32-bit app.  
  
Upon first launch, SCUP now performs an update check to see if there are any newer version, lending weight to the theory that they will be updating SCUP more frequently than they have previously done.The log file for SCUP is still located in the users temp folder (C:\Users\$username\AppData\Local\Temp\UpdatesPublisher.log) and here we can see the update check as it is happening:  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjL00SmBnUeLxji-Coj3ST-bfz3QG9eaMOHiQJcx25NoQd7clT19tFM4nUKN_bpPHq4EKJbCNwoC6oAyKQ4pOYGM1MWMVq2wUrEIzMFib2eZ5F9rfaht_7tWA9ebKjLUuEUh8p5_K1CluE/s400/UpdatesCheckLogFile.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjL00SmBnUeLxji-Coj3ST-bfz3QG9eaMOHiQJcx25NoQd7clT19tFM4nUKN_bpPHq4EKJbCNwoC6oAyKQ4pOYGM1MWMVq2wUrEIzMFib2eZ5F9rfaht_7tWA9ebKjLUuEUh8p5_K1CluE/s1600/UpdatesCheckLogFile.JPG>)

  
Once you are in the main window for the application, you can see that most of the user interface remains largely the same with the exception that the main panes are now known as workspaces. Here is the old UI (top) and the new UI (bottom)  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh47onNI5CzXI4gjHUtpGrG_NEVxIui29nyJ9gRjY6u85Pp4hWGbp0Wikh764KRve2W_AttYO2WNlnPG4BT3ekf7DUKEUqNqpCoDScGGG5uHE1WCpNbY6wtjKIPaNx_V143ivCbEijnSwg/s400/2011MainWindow.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh47onNI5CzXI4gjHUtpGrG_NEVxIui29nyJ9gRjY6u85Pp4hWGbp0Wikh764KRve2W_AttYO2WNlnPG4BT3ekf7DUKEUqNqpCoDScGGG5uHE1WCpNbY6wtjKIPaNx_V143ivCbEijnSwg/s1600/2011MainWindow.JPG>)

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEitbnKtK-FR2kr7jkd5hGiLn_t9yRlCJoUFkYT6Xkda8PxieaOE2e4uUqhUl4nwuPliKGa_fkSoBFk8lJVKVPq0GNBU8fDssJCDhcvVKwsA4yzguJhzKGuuEWV0jtDse8EUX_OAIEvX4pk/s400/MainWindow.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEitbnKtK-FR2kr7jkd5hGiLn_t9yRlCJoUFkYT6Xkda8PxieaOE2e4uUqhUl4nwuPliKGa_fkSoBFk8lJVKVPq0GNBU8fDssJCDhcvVKwsA4yzguJhzKGuuEWV0jtDse8EUX_OAIEvX4pk/s1600/MainWindow.JPG>)

  
They did add some new sections to the options menu that are helpful. First up, here is the new advanced options page which has given you a button to change the database location, in the 2011 version this simply showed a read-only file path that could only be changed by modifying the config files directly:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiZssMZiPlt8NjZFhS23MXwBOWJWE61BwFYjgUPtKKgYad9D0sUC10xyG-f89DNg4lb2txZEQwa4-w3d8aWlnxaCj0vBFS9JRws_ZW03so3yueMOIkOPYpl37pGCFqwyYuEwdc4rKgTQp4/s400/OptionsAdvanced.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiZssMZiPlt8NjZFhS23MXwBOWJWE61BwFYjgUPtKKgYad9D0sUC10xyG-f89DNg4lb2txZEQwa4-w3d8aWlnxaCj0vBFS9JRws_ZW03so3yueMOIkOPYpl37pGCFqwyYuEwdc4rKgTQp4/s1600/OptionsAdvanced.JPG>)

  

Next, here are the new logging options, which let you configure a maximum log file size, as well as a slider with 6 (!) levels to set the amount of log detail you want. Why they went with a slider that has no context as to what you are getting when you choose one of the options I have no idea, but I'd wager that this will be improved in a future update. In my brief testing, this seemed to function more as an on/off switch where anything other than all the way to the right didn't seem to generate any log entries at all.

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiXOwQHPMZJPoEhUzEHZEHDNqHBr3bixA5PQu7m-rKr0ch68bW4UyCJlGr3BS3C1IIMRfzLLZPNnGjX-21bI5IMhyX9UUojDlIOZXGacAYE4MA-Afnjiaj0UqKO4vCs46lMEb0rGXnH8YQ/s320/OptionsLogging.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiXOwQHPMZJPoEhUzEHZEHDNqHBr3bixA5PQu7m-rKr0ch68bW4UyCJlGr3BS3C1IIMRfzLLZPNnGjX-21bI5IMhyX9UUojDlIOZXGacAYE4MA-Afnjiaj0UqKO4vCs46lMEb0rGXnH8YQ/s1600/OptionsLogging.JPG>)

  

  

Finally, there is an updates section to the options menu that allows you to opt out of checking for updates, or opting out of preview builds if you desire:  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEghy7PKmffvcBhAk58z9pluaIWT7w1Z-cGjgvIo1MtVE2uFG21Fc8e0kQN2n3duhfrhm15MHqi0ik-Lg8-dURqJHEuK7VMeri9TO5gOiPPuOnCXaWutKjxh0vDesBzd8iQXeKzp83SrB_k/s320/OptionsUpdates.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEghy7PKmffvcBhAk58z9pluaIWT7w1Z-cGjgvIo1MtVE2uFG21Fc8e0kQN2n3duhfrhm15MHqi0ik-Lg8-dURqJHEuK7VMeri9TO5gOiPPuOnCXaWutKjxh0vDesBzd8iQXeKzp83SrB_k/s1600/OptionsUpdates.JPG>)

  

Another common issue that folks run in to when using SCUP in a large environment is that it is only able to be ran by one user at a time on a given machine, if a second user tries to launch the application it will simply fail to launch and give no indication that there was an error. I tested this scenario with the new release of SCUP and was pleasantly surprised to find that they have added an error dialog to give you an indication of what the problem is:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhHF7YOV0-m-Jyx_dJWleooUoNzQIwhyLbd-RLuQLRKPyB7vVgxkJMZx_W27pxoqLOY4WTYMvJ43WMp2fXQwfzGxK3sAVK-nlNAdK_09sME6PLe_Vk9qB32DhS5B2bx7iRY0RxXAjHGrvM/s400/FailedToStartErrorMultipleUsers.JPG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhHF7YOV0-m-Jyx_dJWleooUoNzQIwhyLbd-RLuQLRKPyB7vVgxkJMZx_W27pxoqLOY4WTYMvJ43WMp2fXQwfzGxK3sAVK-nlNAdK_09sME6PLe_Vk9qB32DhS5B2bx7iRY0RxXAjHGrvM/s1600/FailedToStartErrorMultipleUsers.JPG>)

  

I also wanted to take a look at the format of the SCUP.exe.config file (now known as UpdatesPublisher.exe.config) to see if there were any changes made to it and was surprised to see that the structure of the file has changed significantly. You can see the embedded version of each file below with the old version on top and the new version on the bottom. The new config file (while still being written in XML) is significantly shorter and contains some new references to an "Entity Framework" that didn't exist before. It seems that most of the configuration data must have been moved in to the database itself.

  

  
  
While that is all of the changes in the new version of SCUP that I have noticed so far, I plan to spend some additional time investigating it in my lab environment over the next week or so, so check back for any updates to this post. As always, please reach out and connect with me using the Twitter or LinkedIn links on the right side of this page, I'd love to hear some feedback on my posts if they are helpful to you. Thanks! Matt
