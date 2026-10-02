# AWS Lambda complex tariff uploader for PVOutput

Turn a simple YAML configuration into complex time-of-use electricity tariff logic and automatically publish the current import and export prices to PVOutput extended parameters.

This is useful when PVOutput's built-in tariff configuration is not flexible enough for real-world plans with overlapping time periods, seasonal rates, weekday/weekend rules, public holidays, free-energy windows, EV rates, changing feed-in tariffs, or date-limited special offers. Define the rules once in `config.yaml`; the Lambda works out which tariff applies now and sends the resolved values to PVOutput every few minutes.

Inspired by Adam Petrovic's `pvoutput-tariff` project, adapted for a lightweight AWS Lambda deployment and separate import/export tariff calculation.

Because it runs as a tiny scheduled AWS Lambda, it is effectively free for this workload in normal low-volume use, requires no always-on server, container, NAS, Raspberry Pi or Home Assistant instance, and nothing needs to stay running at home. AWS executes it in the cloud every few minutes, calculates the current tariff, updates PVOutput, and stops again.

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


## Python 3.13 release

The current Lambda runtime target is Python 3.13.

The dependency layer is rebuilt from `requirements-layer.txt` and contains `requests`, `holidays`, `python-dateutil`, and `PyYAML`. The old committed layer ZIP is legacy only and is not the source of truth for new builds.

No credentials are stored in this repository. PVOutput API key and system ID continue to be supplied in the Lambda event.
