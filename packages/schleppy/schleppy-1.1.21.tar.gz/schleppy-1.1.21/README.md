# schleppy
Utilities for traversing and transforming data structures

Inspired by Hapi framework for .js (especially the Hoek plugin), I really missed some of these utilities in python so decided to port them over.

### reach(source, pattern, [options])

[Insipred by Hoek.reach](https://github.com/hapijs/hoek/blob/master/API.md#reachobj-chain-options)

Converts an object key chain string to reference

- `options` - optional settings
    - `separator` - string to split chain path on, defaults to '.'
    - `default` - value to return if the path or value is not present, default is `None`
    - `strict` - if `true`, will throw an error on missing member, default is `False`

A pattern including negative numbers will work like negative indices on an
array.

If pattern is `False-y`, the object itself will be returned.

```python
from schleppy import reach

pattern = 'a.b.c'
source_obj = {'a' : {'b' : { 'c' : 1}}}

reach(source_obj, pattern) # returns 1

pattern = 'a.b.-1'
source_obj = {'a' : {'b' : [2,3,6]}}

reach(source_obj, pattern) # returns 6
```





### transform(source, transform, [options])

[Insipred by Hoek.transform](https://github.com/hapijs/hoek/blob/master/API.md#transformobj-transform-options)

Transforms an existing object into a new one based on the supplied `obj` and `transform` map. `options` are the same as the `reach` options. The first argument can also be an array of objects. In that case the method will return an array of transformed objects. Note that `options.separator` will be respected for the keys in the transform object as well as values.

```python
from schleppy import transform

source = {
    'address': {
        'one': '123 main street',
        'two': 'PO Box 1234'
    },
    'title': 'Warehouse',
    'state': 'CA'
}

result = transform(source, {
    'person.address.lineOne': 'address.one',
    'person.address.lineTwo': 'address.two',
    'title': 'title',
    'person.address.region': 'state'
})
# Results in
# {
#     'person': {
#         'address': {
#             'lineOne': '123 main street',
#             'lineTwo': 'PO Box 1234',
#             'region': 'CA'
#         }
#     },
#     'title': 'Warehouse'
# }
```
