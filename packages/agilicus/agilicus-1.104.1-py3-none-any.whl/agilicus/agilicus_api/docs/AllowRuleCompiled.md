# AllowRuleCompiled

An object that provides the methods and paths that will be allowed for a particular host. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**paths** | **list[str]** | A list of HTTP paths  | [optional] 
**methods** | **list[str]** | The HTTP methods to allow. If any of the listed methods are matched, then this portion of the rule matches.  | [optional] 
**any_auth_user** | **bool** | If true, the authorization scope allows any authenticated user the methods/paths outlined in this rule. If false, the user does not require authentication.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


