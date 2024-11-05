# Alteon-TechData-Anonymizer #
The Alteon TechData Anonymizer is a specialized solution designed to remove or mask sensitive information within technical data (TechData) from Alteon devices.

## Table Of Contents ###
- [Description](#description)
- [Pre Requisites](#Pre-Requisites)
- [How To Use](#how-to-use)
- [Disclaimer](#Disclaimer)

## Description ##
*	For organizations that cannot send internal sensitive data over the internet - Radware developed an Anonymizer tool.
*	This Anonymizer helps maintain data privacy and security by anonymizing fields that contain confidential information, such as IP addresses, usernames, certificates, and other sensitive parameters.
*	The Anonymizer allows organizations to safely share diagnostic data for troubleshooting, reporting, or support purposes without exposing sensitive details.
*	This solution is ideal for ensuring compliance with data protection policies and simplifying data handling processes in secure environments.
*	The Anonymizer is designated for the Alteon techdata file which stores a bunch of logs in it.
*	The Anonymizer goes through the logs that are in the techdata and chooses the relevant logs.
*	In addition – the Anonymizer goes through a file called **custom_words_to_remove.txt** and removes all sensitive words from the relevant logs.
*	The Anonymizer processes only the relevant logs and moves them to a specific folder, the rest of logs will not be processed and not be moved to the specific folder.
*	This tool is written in Python.

## Pre Requisites ##
Python3.10 and above

## How To Use ##
1.	Get the files with git or download them manually, example how to get that using git command from the Cyber-Controller:

```
git clone https://github.com/Radware/Alteon-TechData-Anonymizer.git
cd Alteon-TechData-Anonymizer
```

2.	Populate the file **custom_words_to_remove.txt** with your relevant sensitive information such as application names, users etc. separated by space or new line, the Anonymizer ignores case sensitive, so you don’t have to provide the exact name.
Important – don’t change the name of this file (custom_words_to_remove.txt).

3.	Grant executable permission to the following file:

```
chmod +x Anonymizer.py
```

4.	Run the Anonymizer.py file, for example:

```
py Anonymizer.py
```

5.	In the window that opened choose the techdata file (the suffix should be “tgz”).
6.	Now the tool is waiting to your input, there are 2 options to choose:

    a.	Type **1** in the terminal to replace all IP addresses in all files with “x.x.x.x”.
        For example – 10.10.10.10 will be x.x.x.x.

    b.	Type **2** in the terminal to replace the first 3 octets in the IP addresses that in the **configuration files** with a random IP address, it would be beneficial to our support to understand the configuration better.
        For example – 10.10.10.10 will be 45.70.90.10.

    Note: The IP addresses in the rest files will be x.x.x.x.

8.	The directory **Anonymized_from_[date]_[time]** will be created in the current folder where the Anonymizer.py file is located.
9.	After the script has finished running, explore some files to make sure that your sensitive information is not there.

    Note: There are some files without a suffix, even though you can open them by notepad, notepad++, etc.

## Disclaimer ##
There is no warranty, expressed or implied, associated with this product. Use at your own risk.
