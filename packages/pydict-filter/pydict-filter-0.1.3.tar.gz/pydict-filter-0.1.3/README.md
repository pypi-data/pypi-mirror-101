# py-dict-filter
This package allowed you to perform smart filtering for your dictionary.
## deny_filter(filtering_dict, filter_list, current_path="")
When you use this method, you specify which fields to filter out. For example, we have next dictionary:
```
{
    "top_key_1": "top_value",
    "top_key_2": {
        "middle_key_1": "middle_value",
        "middle_key_2": "middle_value",
        "middle_key_3": "middle_value"
    },
    "top_key_3": [
        {
            "middle_key_4": "middle_value",
            "middle_key_5": "middle_value"
        }
    ],
    "top_key_4": "top_value"
}
```

If you want to deny some fields, you need to add these fields in the filter_list. Here cases filter string and examples:
- Deny top level fields: `top_key_1`, `top_key_3` etc.
- Deny all top level fields: `*`
- Deny fields from nested dict: `top_key_2.middle_key_2`, `top_key_3.middle_key_5`
- Deny all fields from nested dict: `top_key_2.*`, `top_key_3.*`

For example if you call this method with example dictionary as filtering_dict and `filter_list=["top_key_4", "top_key_3.middle_key_4", "top_key_2.*"]`
you will get next result:

```
{
    "top_key_1": "top_value",
    "top_key_3": [
        {
            "middle_key_5": "middle_value"
        }
    ],
    "top_key_2": {}
}
```

## allow_filter(filtering_dict, filter_list, current_path=""):
When you use this method, you specify which fields should be present in a dictionary. For example, we have next dictionary:
```
{
    "top_key_1": "top_value",
    "top_key_2": {
        "middle_key_1": "middle_value",
        "middle_key_2": "middle_value",
        "middle_key_3": "middle_value",
        "middle_key_4": {
            "low_level_key_1": "low_value",
            "low_level_key_2": "low_value"
        }
    },
    "top_key_3": [
        {
            "middle_key_4": "middle_value",
            "middle_key_5": "middle_value"
        }
    ],
    "top_key_4": "top_value"
}
```

If you want to deny some fields, you need to add this fields in the filter_list. Here cases filter string and examples:
- Allow top level fields: `top_key_1`, `top_key_3` etc.
- Allow all top level fields: `*`
- Allow fields from nested dict: `top_key_2.middle_key_2`, `top_key_3.middle_key_5`, `top_key_2.middle_key_4.low_level_key_2`
- Allow all fields from nested dict: `top_key_2.*`, `top_key_3.*`, `top_key_2.middle_key_4.*`

For example if you call this method with example dictionary as filtering_dict and `filter_list=["top_key_1", "top_key_2", 
"top_key_3", "top_key_3.*", "top_key_2.middle_key_1", "top_key_2.middle_key_2", "top_key_2.middle_key_4.*"]`
you will get next result:

```
{
    "top_key_1": "top_value",
    "top_key_3": [
        {
            "middle_key_4": "middle_value",
            "middle_key_5": "middle_value"
        }
    ],
    "top_key_2": {
        "middle_key_2": "middle_value",
        "middle_key_1": "middle_value"
    }
}
```

**PAY ATTENTION!** Despite the fact that all fields for `top_key_2.middle_key_4` were allowed, they did not present in the result. 
This happened because `top_key_2.middle_key_4` was not allowed in `top_key_2` dictionary.

## none_values_filter(filtering_dict, filter_list, current_path="", recursive=True, is_reversed=False)
When you use this method, you specify which fields should be checked and depend on `is_reversed`, method will allow or deny None values for these fields. <br>
If `is_reversed=False`, the method will remove None fields that present in the filter_list. <br>
If `is_reversed=True`, the method will remove None fields that not present in the filter_list. <br>
If `recursive=True`, the method will check all dictionary fields.<br>
If `recursive=False`, the method will check only top-level dictionary fields.<br>

For example, we have next dictionary:
```
{
    "top_key_1": "top_value",
    "top_key_2": {
        "middle_key_1": "middle_value",
        "middle_key_2": None,
        "middle_key_3": None,
        "middle_key_4": {
            "low_level_key_1": "low_value",
            "low_level_key_2": None
        }
    },
    "top_key_3": [
        {
            "middle_key_4": "middle_value",
            "middle_key_5": None
        }
    ],
    "top_key_4": None
}
```
If you want to deny (is_reversed=False) or allow (is_reversed=True) None value for some fields, you need to add this fields in the `filter_list`. Here cases filter string and examples:
- Allow or deny top level fields: `top_key_1`, `top_key_4` etc.
- Allow or deny all top level fields: `*`
- Allow or deny fields from nested dict: `top_key_2.middle_key_2`, `top_key_3.middle_key_5`, `top_key_2.middle_key_4.low_level_key_2`
- Allow or deny all fields from nested dict: `top_key_2.*`, `top_key_3.*`, `top_key_2.middle_key_4.*`

For example if you call this method with example dictionary as filtering_dict and `filter_list=["top_key_1", "top_key_2", 
"top_key_3", "top_key_3.*", "top_key_2.middle_key_1", "top_key_2.middle_key_2", "top_key_2.middle_key_4.*"]`, recursive=True, is_reversed=False
you will get next result:

```
{
    "top_key_1": "top_value",
    "top_key_3": [
        {
            "middle_key_4": "middle_value"
        }
    ],
    "top_key_2": {
        "middle_key_3": None,
        "middle_key_1": "middle_value",
        "middle_key_4": {
            "low_level_key_1": "low_value"
        }
    }
}
```
