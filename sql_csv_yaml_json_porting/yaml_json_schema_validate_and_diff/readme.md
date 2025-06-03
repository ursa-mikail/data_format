Assume 2 yaml files:
```
%%writefile old.yaml

bindings:
  - role: roles/cloudkms.viewer
    members:
      - user:alice@example.com

```

```
%%writefile new.yaml

bindings:
  - role: roles/cloudkms.viewer
    members:
      - user:alice@example.com
      - user:bob@example.com
  - role: roles/cloudkms.admin
    members:
      - group:admin-team@example.com

```


And a schema file, in yaml:

``` yaml
%%writefile schema.yaml

type: object
properties:
  bindings:
    type: array
    items:
      type: object
      required: [role, members]
      properties:
        role:
          type: string
        members:
          type: array
          items:
            type: string
required: [bindings]
additionalProperties: false

```