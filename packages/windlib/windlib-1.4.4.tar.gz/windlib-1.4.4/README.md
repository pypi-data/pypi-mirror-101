# **Windlib**

A useful functions library, Created by SNWCreations.

This is a useful functions library for everyone.

If you have any questions, please give me feedback in issues.

But I may not reply in time, please forgive me.

#### English / [简体中文](https://github.com/SNWCreations/windlib/blob/main/README-zh_Hans.md)

---

## **Usage**

***Tip: If you use the "import windlib" method to import my function, then the function name in the example below should be changed to "windlib.\<function name\>"
If you use the "from windlib import \<function name\>" method, the "windlib" prefix is not required.***

### **typeof - Detect the type of a variable.**

    For example, I define a variable "a" as 10 (this is an integer number, that is, "int") and call this function with the following method:

    typeof(a)

    This function returns the string 'int'.

---

### **check_os - Check the OS information.**

Through the "platform" module, the system label (the first parameter) provided in the call parameter is compared with the current system label.

The function "platform.system()" may return a string, which is a system label that can be used for comparison.

If your python works support multiple systems, then you can combine the supported system types into a list, and then call this function.

    For example, if a work supports Windows, Mac OS, Jython (Python in Java Virtual Machine) and Linux, then the labels of these three systems can be defined as support_list: ['win32','darwin','linux','Java']

    Then, call it through the following method:

    check_os(support_list)


**Default parameters:**

---

slient - executes without generating any information.

The default value is True. The valid values are True or False.

auto_exit - If the obtained system type is not what you want,it will decide whether to terminate the process according to this variable.

If the process is terminated, an error value of "1" will be returned.

The default value is False. The valid values are True or False.

---

### **os_info - Get the OS information.**

Get detailed information about the system, **excluding information about computer accessories.**

The full information will saved as variable "os_version".

If the "slient" parameter is False, a prompt will be generated when the function finishes.

---

### **extract - Unzip the compressed files.**

Unzip the compressed files.

Support ".zip" ".gz" ".tar" ".rar" files.

".tar.gz" format will support in next version.

The "rarfile" library is required for support the rar files.

You can download the "rarfile" library at https://sourceforge.net/projects/rarfile.berlios/files/latest/download .

If the "slient" parameter is False, a prompt will be generated when the function finishes.

---

### **get_file - Download a file from Internet.**

Download a file from the Internet.

If the "show_progress" parameter is True, progress will be displayed when downloading. The default value of this parameter is False.

If the "slient" parameter is False, a prompt will be generated when the function finishes.

---

### **get_os_partition - Get the drive letter of the system.**

Get the drive letter of the partition where the system is located.

Will return a variable "os_partition". (The content may be any letter from A-Z)

---

### **file_exists - Check if the file exists.**

Check if the file exists.

If the "auto_exit" parameter is True, the program will exit when the target file cannot be found.

If the "slient" parameter is False, a prompt will be generated when the function finishes.

---

### **find_files_with_the_specified_extension - Find the file with the specified extension name in targeted folder.**

Find the file with the specified extension name in targeted folder, and add the file name to the **"file_list"** list.

*The default value of parameter "folder" is '.' (Current dir).*

The "file_type" variable must be an extension, and does not need to carry ".".

For example "txt" "jar" "md" "class".

Cannot be ".txt" ".jar" ".md" ".class".

If the "slient" parameter is False, a prompt will be generated when the function finishes.

---

### **find_str_in_file - Find the string in a file.**

Find target string in a file.

"filename" parameter **must** be a valid file name (can be absolute or relative path).

If the "slient" parameter is False, a prompt will be generated when the function finishes.

---

## Copyright (C) 2021 SNWCreations. All rights reserved.
