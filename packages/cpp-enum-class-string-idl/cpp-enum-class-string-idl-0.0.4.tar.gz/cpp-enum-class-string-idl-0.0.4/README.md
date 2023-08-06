# cpp-enum-class-string-idl

```shell
python3 -m cpp_enum_class_string_idl MyEnums.yaml
```

MyEnums.yaml
```yaml
interfaces:
  - MyEnum.yaml
  - MyOtherEnum.yaml
```

MyEnum.yaml
```yaml
name: MyEnum
type: int
values:
  - Value0
  - Value1
```

MyEnum.h
```cpp
#pragma once

/*
 * generated code from cpp-enum-class-string-idl
 */

enum class MyEnum : int {
    Value0,
    Value1,
    Count
};

const char* enum_to_string(const MyEnum value);
```

MyEnum.cpp
```cpp
#include "MyEnum.h"

/*
 * generated code from cpp-enum-class-string-idl
 */

const char* _MyEnum[] = {
    "Value0",
    "Value1"
};

const char* enum_to_string(const MyEnum value) {
    if (MyEnum::Count == value) {
        return "";
    }

    return _MyEnum[static_cast<int>(value)];
}
```
