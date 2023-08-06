# ServiceForwarderSpec

The configurable properties of a ServiceForwarder. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the service forwarder. This value must be unique within an organisation.  | 
**org_id** | **str** | The organisation which owns this service forwarder. | 
**bind_address** | **str** | The local bind address that local applications will forward to in order to access the service forwarder.  bind_address default is localhost.  | [optional] 
**port** | **int** | The transport-layer port on which to access the service forwarder. exclusiveMinimum: 0 exclusiveMaximum: 65536  | 
**protocol** | **str** | The transport-layer protocol being fowarded to the remote application service.  | [optional] [default to 'tcp']
**application_service_id** | **str** | The application service id that this service forwarder connects to.  | 
**connector_id** | **str** | Unique identifier | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


