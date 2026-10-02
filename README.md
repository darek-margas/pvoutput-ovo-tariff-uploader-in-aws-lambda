# AWS Lambda OVO tariff to PVOutput uploader

Uploads the current import and export tariff to PVOutput extended parameters.

## Python 3.13

This repository is now set up for AWS Lambda Python 3.13.

The dependency layer is rebuilt from source with:

- requests
- holidays
- python-dateutil
- PyYAML

No API keys, passwords, tokens, or production event values are stored in the repository.

## Configuration

The Lambda receives private values in the invocation event:

```json
{
  "timezone": "Australia/Sydney",
  "api_key": "your PVOutput API key",
  "system_id": "your PVOutput system id"
}
```

Tariff periods and PVOutput extended parameter numbers stay in `config.yaml`.

## Release

The current runtime release is `py3.13`.

Changing `VERSION` rebuilds:

- `UploaderModules-py3.13.zip` - Lambda layer
- `UploadTariff2PVO-py3.13.zip` - function package
