# agilicus_api.ResourcesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_resources**](ResourcesApi.md#list_resources) | **GET** /v1/resources | List all Resources


# **list_resources**
> ListResourcesResponse list_resources(limit=limit, org_id=org_id, resource_type=resource_type, name_slug=name_slug, name=name, resource_id=resource_id, page_at_id=page_at_id)

List all Resources

List all Resources matching the provided query parameters. Perform keyset pagination by setting the page_at_id parameter to the id for the next page to fetch. Set it to `\"\"` to start from the beginning. 

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
    api_instance = agilicus_api.ResourcesApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
resource_type = 'fileshare' # str | The type of resource to query for (optional)
name_slug = 'smy-application1234' # str | The slug of the resource to query for (optional)
name = 'my-application' # str | The name of the resource to query for (optional)
resource_id = 'owner' # str | The id of the resource to query for (optional)
page_at_id = 'foo@example.com' # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)

    try:
        # List all Resources
        api_response = api_instance.list_resources(limit=limit, org_id=org_id, resource_type=resource_type, name_slug=name_slug, name=name, resource_id=resource_id, page_at_id=page_at_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ResourcesApi->list_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **resource_type** | **str**| The type of resource to query for | [optional] 
 **name_slug** | **str**| The slug of the resource to query for | [optional] 
 **name** | **str**| The name of the resource to query for | [optional] 
 **resource_id** | **str**| The id of the resource to query for | [optional] 
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional] 

### Return type

[**ListResourcesResponse**](ListResourcesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Query succeeded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

