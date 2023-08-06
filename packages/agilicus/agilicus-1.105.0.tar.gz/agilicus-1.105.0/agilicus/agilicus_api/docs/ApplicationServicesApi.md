# agilicus_api.ApplicationServicesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_application_service**](ApplicationServicesApi.md#create_application_service) | **POST** /v2/application_services | Create an ApplicationService
[**create_application_service_token**](ApplicationServicesApi.md#create_application_service_token) | **POST** /v2/application_services/{app_service_id}/token | create a token for an application service
[**create_file_share_service**](ApplicationServicesApi.md#create_file_share_service) | **POST** /v1/file_share_services | Create an FileShareService
[**create_service_forwarder**](ApplicationServicesApi.md#create_service_forwarder) | **POST** /v1/service_forwarders | Create an ServiceForwarder
[**delete_application_service**](ApplicationServicesApi.md#delete_application_service) | **DELETE** /v2/application_services/{app_service_id} | Remove an ApplicationService
[**delete_file_share_service**](ApplicationServicesApi.md#delete_file_share_service) | **DELETE** /v1/file_share_services/{file_share_service_id} | Remove an FileShareService
[**delete_service_forwarder**](ApplicationServicesApi.md#delete_service_forwarder) | **DELETE** /v1/service_forwarders/{service_forwarder_id} | Remove an ServiceForwarder
[**get_application_service**](ApplicationServicesApi.md#get_application_service) | **GET** /v2/application_services/{app_service_id} | Get a single ApplicationService
[**get_file_share_service**](ApplicationServicesApi.md#get_file_share_service) | **GET** /v1/file_share_services/{file_share_service_id} | Get a single FileShareService
[**get_service_forwarder**](ApplicationServicesApi.md#get_service_forwarder) | **GET** /v1/service_forwarders/{service_forwarder_id} | Get a single ServiceForwarder
[**list_application_services**](ApplicationServicesApi.md#list_application_services) | **GET** /v2/application_services | Get a subset of the ApplicationServices
[**list_file_share_services**](ApplicationServicesApi.md#list_file_share_services) | **GET** /v1/file_share_services | Get a subset of the FileShareServices
[**list_service_forwarders**](ApplicationServicesApi.md#list_service_forwarders) | **GET** /v1/service_forwarders | Get a subset of the ServiceForwarder objects
[**replace_application_service**](ApplicationServicesApi.md#replace_application_service) | **PUT** /v2/application_services/{app_service_id} | Create or update an Application Service.
[**replace_file_share_service**](ApplicationServicesApi.md#replace_file_share_service) | **PUT** /v1/file_share_services/{file_share_service_id} | Create or update an FileShareService.
[**replace_service_forwarder**](ApplicationServicesApi.md#replace_service_forwarder) | **PUT** /v1/service_forwarders/{service_forwarder_id} | Create or update an ServiceForwarder.


# **create_application_service**
> ApplicationService create_application_service(application_service)

Create an ApplicationService

It is expected that owners for an organisation will provide connectivity to an ApplicationService by defining one here, then adding a reference to an Application's Environment in the ApplicationService's `assignments` list. To see the list of ApplicationServices for which a given Application Environment has access, see that Environment's read only `applications_services` list. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    application_service = agilicus_api.ApplicationService() # ApplicationService | 

    try:
        # Create an ApplicationService
        api_response = api_instance.create_application_service(application_service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_service** | [**ApplicationService**](ApplicationService.md)|  | 

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New ApplicationService created |  -  |
**409** | An ApplicationService with the same name already exists for this organisation. The existing ApplicationService is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_application_service_token**
> RawToken create_application_service_token(app_service_id, org_id)

create a token for an application service

Create a token for an application service

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # create a token for an application service
        api_response = api_instance.create_application_service_token(app_service_id, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_application_service_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**RawToken**](RawToken.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | A token has been created |  -  |
**404** | The ApplicationService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_file_share_service**
> FileShareService create_file_share_service(file_share_service)

Create an FileShareService

It is expected that owners for an organisation will provide connectivity to an FileShareService by defining one here, then adding a reference to an Application's Environment in the FileShareService's `assignments` list. To see the list of FileShareServices for which a given Application Environment has access, see that Environment's read only `applications_services` list. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    file_share_service = agilicus_api.FileShareService() # FileShareService | 

    try:
        # Create an FileShareService
        api_response = api_instance.create_file_share_service(file_share_service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_file_share_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service** | [**FileShareService**](FileShareService.md)|  | 

### Return type

[**FileShareService**](FileShareService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New FileShareService created |  -  |
**409** | An FileShareService with the same name already exists for this organisation. The existing FileShareService is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_service_forwarder**
> ServiceForwarder create_service_forwarder(service_forwarder)

Create an ServiceForwarder

Create an ServiceForwarder

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    service_forwarder = agilicus_api.ServiceForwarder() # ServiceForwarder | 

    try:
        # Create an ServiceForwarder
        api_response = api_instance.create_service_forwarder(service_forwarder)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->create_service_forwarder: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder** | [**ServiceForwarder**](ServiceForwarder.md)|  | 

### Return type

[**ServiceForwarder**](ServiceForwarder.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New ServiceForwarder created |  -  |
**409** | An ServiceForwarder with the same name already exists for this organisation. The existing ServiceForwarder is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_application_service**
> delete_application_service(app_service_id, org_id)

Remove an ApplicationService

Remove an ApplicationService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Remove an ApplicationService
        api_instance.delete_application_service(app_service_id, org_id)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Application Service was deleted |  -  |
**404** | Application Service does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_file_share_service**
> delete_file_share_service(file_share_service_id, org_id=org_id)

Remove an FileShareService

Remove an FileShareService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    file_share_service_id = 'file_share_service_id_example' # str | FileShareService unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove an FileShareService
        api_instance.delete_file_share_service(file_share_service_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_file_share_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service_id** | **str**| FileShareService unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | FileShareService was deleted |  -  |
**404** | FileShareService does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service_forwarder**
> delete_service_forwarder(service_forwarder_id, org_id=org_id)

Remove an ServiceForwarder

Remove an ServiceForwarder

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    service_forwarder_id = 'service_forwarder_id_example' # str | Service Forwarder unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove an ServiceForwarder
        api_instance.delete_service_forwarder(service_forwarder_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_service_forwarder: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder_id** | **str**| Service Forwarder unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | IngresssService was deleted |  -  |
**404** | IngresssService does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_service**
> ApplicationService get_application_service(app_service_id, org_id)

Get a single ApplicationService

Get a single ApplicationService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Get a single ApplicationService
        api_response = api_instance.get_application_service(app_service_id, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ApplicationService was found. |  -  |
**404** | The ApplicationService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file_share_service**
> FileShareService get_file_share_service(file_share_service_id, org_id=org_id)

Get a single FileShareService

Get a single FileShareService

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    file_share_service_id = 'file_share_service_id_example' # str | FileShareService unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a single FileShareService
        api_response = api_instance.get_file_share_service(file_share_service_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_file_share_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service_id** | **str**| FileShareService unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**FileShareService**](FileShareService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The FileShareService was found. |  -  |
**404** | The FileShareService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_forwarder**
> ServiceForwarder get_service_forwarder(service_forwarder_id, org_id=org_id)

Get a single ServiceForwarder

Get a single ServiceForwarder

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    service_forwarder_id = 'service_forwarder_id_example' # str | Service Forwarder unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a single ServiceForwarder
        api_response = api_instance.get_service_forwarder(service_forwarder_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_service_forwarder: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder_id** | **str**| Service Forwarder unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ServiceForwarder**](ServiceForwarder.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ServiceForwarder was found. |  -  |
**404** | The ServiceForwarder does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_application_services**
> ListApplicationServicesResponse list_application_services(org_id=org_id, updated_since=updated_since, protocol_type=protocol_type, name=name, hostname=hostname, hostname_or_service_name=hostname_or_service_name, port=port)

Get a subset of the ApplicationServices

Retrieves all ApplicationServices owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)
protocol_type = 'protocol_type_example' # str | ApplicationService protocol type (optional)
name = 'service1' # str | Query the service by name (optional)
hostname = 'hostname_example' # str | ApplicationService hostname query lookup (optional)
hostname_or_service_name = 'hostname_or_service_name_example' # str | Perform a query based on the following       (hostname == hostname_or_service_name)            OR       (servicename == hostname_or_service_name AND hostname == localhost)   (optional)
port = 56 # int | ApplicationService port query lookup (optional)

    try:
        # Get a subset of the ApplicationServices
        api_response = api_instance.list_application_services(org_id=org_id, updated_since=updated_since, protocol_type=protocol_type, name=name, hostname=hostname, hostname_or_service_name=hostname_or_service_name, port=port)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_application_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **updated_since** | **datetime**| query since updated | [optional] 
 **protocol_type** | **str**| ApplicationService protocol type | [optional] 
 **name** | **str**| Query the service by name | [optional] 
 **hostname** | **str**| ApplicationService hostname query lookup | [optional] 
 **hostname_or_service_name** | **str**| Perform a query based on the following       (hostname &#x3D;&#x3D; hostname_or_service_name)            OR       (servicename &#x3D;&#x3D; hostname_or_service_name AND hostname &#x3D;&#x3D; localhost)   | [optional] 
 **port** | **int**| ApplicationService port query lookup | [optional] 

### Return type

[**ListApplicationServicesResponse**](ListApplicationServicesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved ApplicationServices |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_file_share_services**
> ListFileShareServicesResponse list_file_share_services(org_id=org_id, name=name, connector_id=connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids)

Get a subset of the FileShareServices

Retrieves all FileShareServices owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'service1' # str | Query the service by name (optional)
connector_id = '1234' # str | connector id in query (optional)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_ids = ['[\"q20sd0dfs3llasd0af9\"]'] # list[str] | The list of org ids to search for. Each org will be searched for independently. (optional)

    try:
        # Get a subset of the FileShareServices
        api_response = api_instance.list_file_share_services(org_id=org_id, name=name, connector_id=connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_file_share_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the service by name | [optional] 
 **connector_id** | **str**| connector id in query | [optional] 
 **updated_since** | **datetime**| query since updated | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_ids** | [**list[str]**](str.md)| The list of org ids to search for. Each org will be searched for independently. | [optional] 

### Return type

[**ListFileShareServicesResponse**](ListFileShareServicesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved FileShareServices |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_service_forwarders**
> ListServiceForwardersResponse list_service_forwarders(org_id=org_id, name=name, app_service_id=app_service_id, connector_id=connector_id, app_service_connector_id=app_service_connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids)

Get a subset of the ServiceForwarder objects

Retrieves all ServiceForwarder objects owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'service1' # str | Query the service by name (optional)
app_service_id = 'app_service_id_example' # str | Application Service unique identifier (optional)
connector_id = '1234' # str | connector id in query (optional)
app_service_connector_id = '1234' # str | application service connector id in query (optional)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_ids = ['[\"q20sd0dfs3llasd0af9\"]'] # list[str] | The list of org ids to search for. Each org will be searched for independently. (optional)

    try:
        # Get a subset of the ServiceForwarder objects
        api_response = api_instance.list_service_forwarders(org_id=org_id, name=name, app_service_id=app_service_id, connector_id=connector_id, app_service_connector_id=app_service_connector_id, updated_since=updated_since, limit=limit, org_ids=org_ids)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->list_service_forwarders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the service by name | [optional] 
 **app_service_id** | **str**| Application Service unique identifier | [optional] 
 **connector_id** | **str**| connector id in query | [optional] 
 **app_service_connector_id** | **str**| application service connector id in query | [optional] 
 **updated_since** | **datetime**| query since updated | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_ids** | [**list[str]**](str.md)| The list of org ids to search for. Each org will be searched for independently. | [optional] 

### Return type

[**ListServiceForwardersResponse**](ListServiceForwardersResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved ServiceForwarder objects |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_application_service**
> ApplicationService replace_application_service(app_service_id, application_service=application_service)

Create or update an Application Service.

Create or update an Application Service.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
application_service = agilicus_api.ApplicationService() # ApplicationService |  (optional)

    try:
        # Create or update an Application Service.
        api_response = api_instance.replace_application_service(app_service_id, application_service=application_service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **application_service** | [**ApplicationService**](ApplicationService.md)|  | [optional] 

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ApplicationService was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | Application Service does not exist. |  -  |
**409** | The provided Application Service conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_file_share_service**
> FileShareService replace_file_share_service(file_share_service_id, file_share_service=file_share_service)

Create or update an FileShareService.

Create or update an FileShareService.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    file_share_service_id = 'file_share_service_id_example' # str | FileShareService unique identifier
file_share_service = agilicus_api.FileShareService() # FileShareService |  (optional)

    try:
        # Create or update an FileShareService.
        api_response = api_instance.replace_file_share_service(file_share_service_id, file_share_service=file_share_service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_file_share_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_share_service_id** | **str**| FileShareService unique identifier | 
 **file_share_service** | [**FileShareService**](FileShareService.md)|  | [optional] 

### Return type

[**FileShareService**](FileShareService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The FileShareService was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | FileShareService does not exist. |  -  |
**409** | The provided FileShareService conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_service_forwarder**
> ServiceForwarder replace_service_forwarder(service_forwarder_id, service_forwarder=service_forwarder)

Create or update an ServiceForwarder.

Create or update an ServiceForwarder.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    service_forwarder_id = 'service_forwarder_id_example' # str | Service Forwarder unique identifier
service_forwarder = agilicus_api.ServiceForwarder() # ServiceForwarder |  (optional)

    try:
        # Create or update an ServiceForwarder.
        api_response = api_instance.replace_service_forwarder(service_forwarder_id, service_forwarder=service_forwarder)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->replace_service_forwarder: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_forwarder_id** | **str**| Service Forwarder unique identifier | 
 **service_forwarder** | [**ServiceForwarder**](ServiceForwarder.md)|  | [optional] 

### Return type

[**ServiceForwarder**](ServiceForwarder.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ServiceForwarder was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | ServiceForwarder does not exist. |  -  |
**409** | The provided ServiceForwarder  conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

