# AWS Lambda complex tariff uploader for PVOutput

This project adds proper time-based electricity pricing to PVOutput for tariffs that cannot be represented by a simple peak/off-peak schedule.

Many modern electricity plans now include things such as free-energy periods, EV charging windows, weekday-only peaks, seasonal rules and different rates depending on the time of day. PVOutput can store tariff information, but keeping those rates aligned with a more complicated retail plan quickly becomes awkward if it has to be managed manually.

This Lambda automates that job. It determines which tariff should apply at a given time and updates PVOutput accordingly, allowing PVOutput's cost calculations to follow the real electricity plan much more closely. The tariff logic is kept in code rather than being tied to a particular retailer, so the schedules and rates can be adapted to other plans without changing the overall design.

Like the GoodWe uploader, it is designed to run entirely in AWS Lambda. There is nothing to install or maintain at home, no dependency on Home Assistant or another local server, and the workload is small enough to sit comfortably within the AWS free tier. Once configured, it simply runs in the background and keeps PVOutput's tariff state aligned with the actual billing periods.

The goal is not to replace PVOutput's own calculations, but to give them accurate tariff inputs when the real-world tariff is more complicated than PVOutput's standard configuration can conveniently express.

Inspired by Adam Petrovic's `pvoutput-tariff` project, adapted for a lightweight AWS Lambda deployment and separate import/export tariff calculation.

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
