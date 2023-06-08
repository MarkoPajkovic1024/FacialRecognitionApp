# EB CLI Installer

## 1. Overview

This repository hosts scripts to generate self-contained installations of the [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html).

### 1.1. Prerequisites

You will need to have the following prerequisites installed before running the install script.

* **Git**
  * If not already installed you can download git from the [Git downloads page](https://git-scm.com/downloads).
* **Python**
  * We recommend that you install Python using the [pyenv](https://github.com/pyenv/pyenv) Python version manager. Alternately, you can download Python from the [Python downloads page](https://www.python.org/downloads/).
* **virtualenv**
  * Follow the [virtualenv documentation](https://virtualenv.pypa.io/en/latest/installation.html) to install virtualenv.


## 2. Quick start

### 2.1. Clone this repository

Use the following:

```
git clone https://github.com/aws/aws-elastic-beanstalk-cli-setup.git
```

### 2.2. Install/Upgrade the EB CLI

#### MacOS/Linux
On **Bash** or **Zsh**:

```
python ./aws-elastic-beanstalk-cli-setup/scripts/ebcli_installer.py
```

#### Windows
In **PowerShell** or in a **Command Prompt** window:

```
python .\aws-elastic-beanstalk-cli-setup\scripts\ebcli_installer.py
```

### 2.3. After installation

On Linux and macOS, the output contains instructions to add the EB CLI (and Python) executable file to the shell's `$PATH` variable, if it isn't already in it.

## 3. Usage

The `ebcli_installer.py` Python script will install the [awsebcli](https://pypi.org/project/awsebcli/) package in a virtual environment to prevent potential conflicts with other Python packages.

For most use cases you can execute the `ebcli_installer.py` script with no arguments.

```
python ./aws-elastic-beanstalk-cli-setup/scripts/ebcli_installer.py
```







# Deploying a Django application to Elastic Beanstalk

## 1. Prerequisites

To use any AWS service, including Elastic Beanstalk, you need to have an AWS account and credentials. [AWS]([https://aws.amazon.com/](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)).

### 1.1. Prerequisites

To follow this tutorial, you should have all of the Common Prerequisites for Python installed, including the following packages:

* ** Python 3.7 or later **

pip

virtualenv

awsebcli


# Useful Command Line commands

## 1. IMPORTANT: Please be sure you are in your virtual env and have installed EB Per above instructions. Otherwise eb commands wont work
## 2. These are instructions for windows. Mac users please add yours here!
* **pip freeze**
  * This lets you see all the libraries that are currently loaded in your virtual env.  This is a good debug tool.
* **App modifictions**
  Run the below lines each time make modification to app.  these will ensure the changes are loaded ono the all
  * python manage.py migrate
  * python manage.py makemigrations
  * python manage.py makemigrations Facial_Recognition_App
  * python manage.py migrate --run-syncdb
* **eb deploy**
  * This will deploy the app on to AWS EB server (This will take a couple of mins.
* **eb open**
  * This will launch the app on your web.

# Useful resource links:

* **AWS EB**
  This repository hosts scripts to generate self-contained installations of the [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html).
* **EB Git Repo**
  [EB Git Repo](https://github.com/aws/aws-elastic-beanstalk-cli-setup)
