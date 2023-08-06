# Condition

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**geo_bounding_box** | **object** | Check if points geo location lies in a given area | [optional] 
**geo_radius** | **object** | Check if geo point is within a given radius | [optional] 
**match** | **object** | Check if point has field with a given value | [optional] 
**range** | **object** | Check if points value lies in a given range | [optional] 
**must** | [**[Condition], none_type**](Condition.md) | All conditions must match | [optional] 
**must_not** | [**[Condition], none_type**](Condition.md) | All conditions must NOT match | [optional] 
**should** | [**[Condition], none_type**](Condition.md) | At least one of thous conditions should match | [optional] 
**key** | **str** |  | [optional] 
**has_id** | **[int]** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


