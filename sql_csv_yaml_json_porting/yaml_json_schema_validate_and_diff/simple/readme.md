

Assume 2 yaml files:
```
%%writefile old.yaml

name: Alice
age: 30
role: admin
```

```
%%writefile new.yaml

name: Alice
age: 31
role: user
location: Earth
```

And a schema file, either in json or yaml:

``` json
%%writefile schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "age", "role"],
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer",
      "minimum": 0
    },
    "role": {
      "type": "string",
      "enum": ["admin", "user", "guest"]
    },
    "location": {
      "type": "string"
    }
  },
  "additionalProperties": false
}

```

``` yaml
%%writefile schema.yaml

$schema: http://json-schema.org/draft-07/schema#
type: object
required:
  - name
  - age
  - role
properties:
  name:
    type: string
  age:
    type: integer
    minimum: 0
  role:
    type: string
    enum: [admin, user, guest]
  location:
    type: string
additionalProperties: false

```

# Standardize Terraform-based keyset and crypto policy management

| Issue                                                       | Solution                                                                              |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **1. Only 2 endpoints supported**                           | Abstract keyset creation via a **Terraform module** so it's reusable and scalable     |
| **2. GTFP (Governance Technical Firewall Process?) delays** | Minimize changes to core infra by isolating keysets in `tfvars` or YAML               |
| **3. Duplicated resources per environment**                 | Use **workspaces** or **for\_each** to manage multiple environments in one module     |
| **4. Unvalidated JSON policies**                            | Define policies in **YAML** and validate with a **Python tool**, then convert to JSON |


```
poc/
├── main.tf
├── modules/
│   └── keyset/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev.tfvars
│   ├── prod.tfvars
├── policies/
│   ├── policy1.yaml
│   ├── policy2.yaml
│   └── schema.yaml
├── tools/
│   └── validate_and_render.py

```



