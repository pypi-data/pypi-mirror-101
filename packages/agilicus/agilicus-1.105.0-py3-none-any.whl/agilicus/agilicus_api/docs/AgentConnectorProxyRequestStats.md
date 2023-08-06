# AgentConnectorProxyRequestStats

Statistics related to the requests handled by an AgentConnector's builtin proxy. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**last_request_start_time** | **datetime** | When the last request handled by this proxy was started. Note that the request may still be in flight.  | [optional] 
**bytes_received** | **int** | The number of bytes, including headers, received by the proxy. | 
**bytes_sent** | **int** | The number of bytes, including headers, sent by the proxy. | 
**requests** | [**AgentConnectorProxyRequestStatsDetails**](AgentConnectorProxyRequestStatsDetails.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


