# Azure Python DicomClient SDK

DICOM-Client is a Python-based client library to simplify interacting with DICOM Server.

- It hides the complexities of building URLs, working with HTTP Verbs, and reading DCM metadata.
- It is comprised of about 500 lines of Python code.
- Users of this package can interact with DICOM server using a very simple set of methods that upload, download, and delete DCM Files.
- The code comes with a set of integration test that can also be used as an example on how to use the library.
- The DICOM client assumes you have a DICOM server with an endpoint.
- The DICOM client also supports authentication in the form of an OAUTH2 token. 
- It has been tested extensively against DICOM server.
  - [microsoft/dicom-server](https://github.com/microsoft/dicom-server)


### Build Status 
(*Currently Private Build Badges*)

Main: [![Build Status](https://dev.azure.com/CSECodeHub/378940%20-%20PWC%20Health%20OSIC%20Platform%20-%20DICOM/_apis/build/status/dicom-client-python%20release%20pipeline?branchName=main)](https://dev.azure.com/CSECodeHub/378940%20-%20PWC%20Health%20OSIC%20Platform%20-%20DICOM/_build/latest?definitionId=36&branchName=main)

Dev: [![Build Status](https://dev.azure.com/CSECodeHub/378940%20-%20PWC%20Health%20OSIC%20Platform%20-%20DICOM/_apis/build/status/dicom-client%20integration%20and%20dev%20release?branchName=main)](https://dev.azure.com/CSECodeHub/378940%20-%20PWC%20Health%20OSIC%20Platform%20-%20DICOM/_build/latest?definitionId=28&branchName=main)


Latest Version: [![PyPi Distribution](https://img.shields.io/pypi/v/dicom-client-python.svg)](https://pypi.python.org/pypi/dicom-client-python/)

## Table of Contents

* [About The Project](#about-the-project)
    * [Built With](#built-with)
* [Getting Started](#gettting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Authentication](#authentication)
    * [Python Request Library](#python-request-library)
    * [Errors and Exceptions](#errors-and-exceptions)
    * [Integration Tests](#integration-tests)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)


## About The Project

**DICOM-Client** is the Python-based package (helper library) that application
developers can use to communicate with a Dicom Server backend. DICOM Server
backends is an international standard related to the exchange, storage and
communication of digital medical images and other related digital data. 


**DICOM-Client** simplifies interaction with DICOM Server. Microsoft provides an
open source implementation of DICOM server. DICOM-Client encapsulates the
complexities of interacting with DICOM server. DICOM-Client building URLs,
working with HTTP Verbs, HTTP headers, messsage bodies, and reading DCM
metadata. Developers focus on storing and retrieving medical images, calling
methods that insert, delete, and download medical images.


### Built With

**DICOM-Client** is built with Python 3.7. It is about 500 lines of code that
focuses on simplicity and performance. It is optimized to interact with
compliant DICOM servers. Developers focus on medical image files, study ids,
series ids, and instance ids.  Six easy-to-call methods comprise the **DICOM-Client** SDK.

**DICOM Server** is the web service backend that DICOM-Client communicates with.

[See official
documenation](https://github.com/microsoft/dicom-server/tree/master/docs) for a
deep dive on what DICOM Server offers.

**DICOM-Client** uses Python Requests, a well-known Python package that is
optimized for handling HTTP traffic. The requests library is the de facto
standard for making HTTP requests in Python. 

- DICOM-Client abstracts the complexities of making requests behind a beautiful,
simple API so that you can focus on interacting with DICOM services and
consuming data in your application.
- There are four core methods that make up **DICOM-Client**. 
    - An interface has been defined to simplify interaction with
      **DICOM-Client**. 
    - The purpose of these methods is to upload, download, and
      delete DCM files from DICOM Server. 
    - No knowledge of http and DICOM Server's REST-based API is required.

```python
class DicomClientInterface(ABC):
    @abstractmethod
    def __init__(self, base_url, token_cache):
        pass
    @abstractmethod
    def upload_dicom_folder(self, folder_name):
        pass
    @abstractmethod
    def upload_dicom_file(self, file_name):
        pass
    @abstractmethod
    def delete_dicom(self, study_id, series_id=None, instance_id=None):
        pass
    @abstractmethod
    def download_dicom(self, output_folder, study_id, series_id=None, instance_id=None):
        pass
    @abstractmethod
    def get_patient_study_ids(self, patient_id):
        pass
```

## Getting Started

To install and run the various tests for the **DICOM-Client** SDK, simply issue
the following commands:

```bash
$ git clone our_git_url
$ python3 -m venv .venv
$ pip install -r requirements.txt 
$ pytest tests
```

### Prerequisites

The DICOM-Client depends on a number of other technologies and components to
be in place. The most obvious dependency is DICOM server, which represents
the endpoint that DICOM-Client will connect to when it wishes to upload,
download, or delete medical images.

Although it isn't a requirement, DICOM server can be configured to require **Azure Active Directory Authentication (Azure AD)**.   When called by the DICOM-Client, the DICOM server would expect to receive a Bearer Token in the HTTP authorization header. The needed steps to configure Azure AD to work with DICOM Server and DICOM Client is provided in the **Authentication** section below.

The DICOM-Client takes a dependency on Python, version 3.7 and above. The latest version of Python can be downloaded here: https://www.python.org/downloads/. In addition, you will need to pip install a number of Python Packages. See requirements.txt the complete list. Some important packages include pydicom, requests, pandas, pytest, pylint, black, adal - to name a few.

### Installation

After cloning the repo and installing dependencies as explained in the getting started section, you are ready to start using the DICOM-Client SDK.


### Authentication

DICOM Server can be configured to require authentication tokens, OAUTH2 tokens. These tokens need to be passed by the DICOM-Client, which will place bearer tokens in HTTP requeststo access OAuth 2.0 protected resources such as DICOM Server.

High level details on configuring authentication can be found here:

[See official documenation](https://github.com/microsoft/dicom-server/blob/master/docs/how-to-guides/enable-authentication-with-tokens.md)

The DICOM-Client relies on the environment variables to retrieve the needed service principal credentials. Service Pricipal credentials are used to retrieve an OAUTH2 token, which are then passed to DICOM Server.

The DICOM-Client relies on an environment variable called AUTH_CONNECTION_INFO. It looks like this.


```
AUTH_CONNECTION_INFO=$'{'authority': 'https://login.microsoftonline.com/dde82865-7143-4a84-950e-c9007506f8bb', 'client_id': 'ea698e79-3718-66ef-b5e8-42adb1a9e46a', 'client_secret': 'mI60hP~oMhwK3Ddde8E1TEJ7R.w6-3N4J~', 'oauth_resource': 'api://abc43379-3718-46ef-b5e8-42adb1a9e46a'}' 
```

---
| Element | Value  |
|:-------------------- |:--------------------  |
| authority | https://login.microsoftonline.com/dabcd865-7143-4a84-950e-c9007506f8bb  |
| client_id | ea698e79-3718-66ef-b5e8-42adbd1abc46a  |
| client_secret | mIadfa3MhwK3Ddde8E1TEJ7R.w6-3N4J~  |
| oauth_resource | api://abc43379-3718-46ef-b5e8-42adb339e46a  |
---
> Note that the _tenant ID is embedded in the URL for authority,
> "dabcd865-7143-4a84-950e-c9007506f8bb"
---

**Step 1 -** Follow the instructions [here](https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/active-directory/develop/quickstart-register-app.md)

This step is where you register the client application and results in getting a client ID.
- You will enter a _Name_ for the _client application_.
  - It will be the user-facing display name for this application (this can be changed later).
- You will see, _"Supported account types, Who can use this application or access
  this API?"_
  - Select the following: _(•) Accounts in this organizational directory only
    (Microsoft only - Single tenant)_
  - You will not need to provide a _Redirect URI_
- You will be able to retrieve _client id_, and _tenant id_.

**Step 2 -** Once the client application is registered, you will be brought to the client application details page where there are two more selections to be made from the left and you pain:

- Certificates and secrets
  - Used to generate the client secret
  - Client secret can be generated by selecting, "New Client Secret"
- Expose an API
  - Used to generate the application ID URI (oauth_resource)
  - Application ID URI can be set at the top of this page


**Step 3 -**  Now you have everything you need to construct the environment variable, AUTH_CONNECTION_INFO.

The following graphic can help you understand how all the pieces fit together:

![image](docs/images/ad.png)

**Azure App Services**

DICOM Server can be configured to run on any suitable web service backend infrastructure. DICOM Server has been tested across a number of back cans, such as Kubernetes and the Azure App Service. For illustration purposes we will focus on configuration for Azure app services.

Azure App Services has the built-in capability to support active directory. It is a simple matter of linking the client app registration in Azure Active Directory into Azure App Services as seen in the diagram below.

You can read more here:

[See documenation](https://github.com/microsoft/dicom-server/blob/master/docs/how-to-guides/enable-authentication-with-tokens.md)

Here is a conceptual diagram.

![](docs/images/adappservice.png)


### Python Request Library

**Requests** is an elegant and simple HTTP library for Python, built for human
beings. There’s no need to manually add query strings to your URLs, or to
form-encode your POST data. Keep-alive and HTTP connection pooling are 100%
automatic, thanks to urllib3.

While it is important to realize that the Python **Requests** library is used to
communicate with DICOM Server, the DICOM-Client abstracts away the need to know
anything about the Python **Requests** library.


### Errors and Exceptions


In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a **ConnectionError** exception.

- **Response.raise_for_status()** will raise an **HTTPError** if the HTTP request returned an unsuccessful status code.
- If a request times out, a **Timeout** exception is raised.
- If a request exceeds the configured number of maximum redirections, a **TooManyRedirects** exception is raised.
- All exceptions that **Requests** explicitly raises inherit from **requests.exceptions.RequestException.**
-  It seems best to go from specific to general down the stack of errors to get the desired error to be caught, so the specific ones don't get masked by the general one.

Here is the correct way to trap errors in Python when using the requests package:

```python
response = None
try:
   response = requests_session.post(
         url, body, headers=headers, verify=False
   )
   response.raise_for_status()
   return response
except requests.exceptions.HTTPError as errh:
   logging.error("Http Error: %s", errh)
   raise errh from None
except requests.exceptions.ConnectionError as errc:
   logging.error("Error Connecting: %s", errc)
   raise errc from None
except requests.exceptions.Timeout as errt:
   logging.error("Timeout Error: %s", errt)
   raise errt from None
except requests.exceptions.RequestException as err:
   logging.error("Unknown error type: %s", err)
   raise err from None
return response
```

**Response Codes from DICOM Server**

The following table provides a list of response codes that origninate from the DICOM Server.

| Service Status | HTTP/1.1 Status Codes | STOW-RS Description  |
|:-------------------- |:-------------------- |:--------------------  |
| Failure | 400 - Bad Request | This indicates that the STOW-RS Service was unable to store any instances due to bad syntax.  |
|  | 401 - Unauthorized | This indicates that the STOW-RS Service refused to create or append any instances because the client is not authorized.  |
|  | 403 - Forbidden | This indicates that the STOW-RS Service understood the request, but is refusing to fulfill it (e.g., an authorized user with insufficient privileges).  |
|  | 409 - Conflict | This indicates that the STOW-RS Service request was formed correctly but the service was unable to store any instances due to a conflict in the request (e.g., unsupported SOP Class or StudyInstanceUID mismatch).  |
|  | 503 - Busy | This indicates that the STOW-RS Service was unable to store any instances because it was out of resources.  |
| Warning | 202 - Accepted | This indicates that the STOW-RS Service stored some of the instances but warnings or failures exist for others.  |
|  |  | Additional information regarding this error can be found in the XML response message body.  |
| Success | 200 - OK | This indicates that the STOW-RS Service successfully stored all the instances.  |

**Failure Reasons**

It is possible to retrieve more detailed failure explanations by viewing response.text.

| Status Code (hexadecimal) | Status Code (decimal) | Meaning  |
|:-------------------- |:-------------------- |:--------------------  |
| A7xx | 42752 - 43007 | Refused out of Resources  |
| A9xx | 43264 - 43519 | Error: Data Set does not match SOP Class  |
| Cxxx | 49152 - 53247 | Error: Cannot understand  |
| C122 | 49442 | Referenced Transfer Syntax not supported  |
| 110 | 272 | Processing failure  |
| 122 | 290 | Referenced SOP Class not supported  |

**Retrieving the Failure Reasons**

The code snippet below demonstrates how to identify the failure code by parsing
_response.text_, which is in JSON format.


```python

# Do an upload now
response = None
try:
    response = dicom_client.upload_dicom_file("./tests/sample_media/input/bad_dcm_file/temp.dcm")
except requests.exceptions.HTTPError as errh:
    # There are more detailed errror codes embedded as JSON in response.text
    # See http://dicom.nema.org/medical/dicom/current/output/chtml/part18/sect_I.2.2.html
    logging.error("Http Error: %s", errh)
    assert errh.response.status_code == 409
    assert (
        json.loads(errh.response.text)["00081198"]["Value"][0]["00081197"]["Value"][0]
        == 43264
    )
except requests.exceptions.ConnectionError as errc:
    logging.error("Error Connecting: %s", errc)
    raise errc from None
except requests.exceptions.Timeout as errt:
    logging.error("Timeout Error: %s", errt)
    raise errt from None
except requests.exceptions.RequestException as err:
    logging.error("Unknown error type: %s", err)
    raise err from None
except Exception as err:
    logging.error("Unknown error type: %s", err)
    raise err from None

```



### Testing

A full suite of integration tests have been written. These tests run all the
major components of DicomClient().

The tests can be found here:

> ./tests/integration/test_dicom_client.py

```Python
def test_upload_file(self):
def test_oauth_token(self):
def test_dicom_client(self):
def test_query_by_patient_id(self):
def test_upload_bad_file(self):
def test_delete_file(self):
def test_delete_upload_download(self):
def test_delete_study_ids(self):
def clean_output_folder(self):
```

**Running the integration tests**

```
cd ./tests/integration
python test_dicom_client.py
```

## Usage

The following steps can get you started. Many of the details that you will need
to complete the steps have been outlined earlier in this README.

1. Provision a DICOM Server.
1. Setup active directory credentials as explained in the authentication section.
1. Provision AUTH_CONNECTION_INFO as an environment variable.
1. Follow the pip install instructions outlined above.

There are four core methods that make up DICOM-Client. An interface has been
defined to simplify interaction with DicomClient(). The purpose of these methods
is to upload, download, and delete DCM files from DICOM Server:

```python
class DicomClientInterface(ABC):
    @abstractmethod
    def __init__(self, base_url, token_cache):
        pass
    @abstractmethod
    def upload_dicom_folder(self, folder_name):
        pass
    @abstractmethod
    def upload_dicom_file(self, file_name):
        pass
    @abstractmethod
    def delete_dicom(self, study_id, series_id=None, instance_id=None):
        pass
    @abstractmethod
    def download_dicom(self, output_folder, study_id, series_id=None, instance_id=None):
        pass
    @abstractmethod
    def get_patient_study_ids(self, patient_id):
        pass
```

## Roadmap
  - [x] ~~Performance optimizations~~
  - [x] ~~Read failure reasons~~
  - [ ] Video Tutorials



## Contributing

We gladly accept community contributions.

- Issues: Please report bugs using the Issues section of GitHub
- Forums: Interact with the development teams on StackOverflow or the Microsoft Azure Forums
- Source Code Contributions: Please see [CONTRIBUTING.md][contributing] for instructions on how to contribute code.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## License

MIT License

Copyright (c) Microsoft Corporation. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

# Trademark

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft's Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

# Security Reporting Instructions

Please see [SECURITY_REPORTING.md][SECURITY_REPORTING.md] for instructions on how to report security issues.
