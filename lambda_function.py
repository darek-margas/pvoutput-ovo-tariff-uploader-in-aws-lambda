import json
def lambda_handler(event, context):

  from datetime import datetime, time
  import yaml
  import holidays
  import requests 
  import time as time_module
  import dateutil.tz

  # configuration options
  config_path = 'config.yaml'                   # this is static anyway
  timezone = event['timezone']                  # JSON from event
  api_key = event['api_key']
  system_id = event['system_id']

  # Helper function to check if current time is within a specified period
  def is_time_in_period(current_time, start_str, end_str):
    start_time = time(*map(int, start_str.split(':')))
    end_time = time(*map(int, end_str.split(':')))
    # Handle overnight periods
    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:  # Overnight period, e.g., 22:00-06:00
        return start_time <= current_time or current_time <= end_time

  def is_public_holiday(public_holidays, current_date):
    if not public_holidays:
        return False

    country, state = public_holidays.get('country'), public_holidays.get('region')
    return current_date in holidays.country_holidays(country, state)

  # Function to load tariff information from a YAML file
  def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

  def get_current_tariff(tariff_config, public_holidays, current_datetime):
    offpeak = tariff_config.pop('offpeak', None)
    for _, tariff in tariff_config.items():
        periods = tariff.get('times', [])
        if any(is_time_in_period(current_datetime.time(), period['start'], period['end']) for period in periods):
            if 'start_date' not in tariff and 'end_date' not in tariff:
                return tariff['price']
            else:
                is_weekday = (current_datetime.weekday() < 5)
                is_weekend = (current_datetime.weekday() >= 5)
                is_holiday = is_public_holiday(public_holidays, current_datetime.date())
                weekdays_only = tariff.get('weekdays_only', False)
                weekends_only = tariff.get('weekends_only', False)

                if not is_holiday and (
                    (weekdays_only and is_weekday) or 
                    (weekends_only and is_weekend) or 
                    (not weekdays_only and not weekends_only)
                ):
                    if tariff['start_date'] <= current_datetime.date() <= tariff['end_date']:
                        return tariff['price']

    return offpeak['price']
    
  def get_current_export_tariff(export_tariff_config, public_holidays, current_datetime):
    offpeak = export_tariff_config.pop('offpeak', None)
    for tariff_name, tariff in export_tariff_config.items():
        periods = tariff.get('times', [])
        if any(is_time_in_period(current_datetime.time(), period['start'], period['end']) for period in periods):
            if 'start_date' not in tariff and 'end_date' not in tariff:
                return tariff['price']
            else:
                is_weekday = (current_datetime.weekday() < 5)
                is_weekend = (current_datetime.weekday() >= 5)
                is_holiday = is_public_holiday(public_holidays, current_datetime.date())
                weekdays_only = tariff.get('weekdays_only', False)
                weekends_only = tariff.get('weekends_only', False)
                if not is_holiday and (
                    (weekdays_only and is_weekday) or 
                    (weekends_only and is_weekend) or 
                    (not weekdays_only and not weekends_only)
                ):
                    if 'start_date' in tariff and 'end_date' in tariff:
                        if tariff['start_date'] <= current_datetime.date() <= tariff['end_date']:
                            return tariff['price']
                    else:
                        return tariff['price']
    return offpeak['price']

  def send_price_to_pvoutput(api_key, system_id, import_param, export_param, price, export_t, now):
    date_str = now.strftime('%Y%m%d')
    # pvoutput expects a data feed sent to an extended parameter every 5 minutes
    # e.g. 00, 05, 10, ..., 55
    minute = now.minute - now.minute % 5
    time_str = f"{now.hour:02d}:{minute:02d}"

    url = "https://pvoutput.org/service/r2/addstatus.jsp"
    headers = {
        'X-Pvoutput-Apikey': api_key,
        'X-Pvoutput-SystemId': system_id,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f"{import_param}={price}&{export_param}={export_t}&d={date_str}&t={time_str}"
    response = requests.post(url, headers=headers, data=data)
    return response

  def main():
    config = load_config(config_path)
    current_datetime = datetime.now(dateutil.tz.gettz(timezone))
    current_import_tariff = get_current_tariff(config.get('tariffs'), config.get('public_holidays'), current_datetime)
    current_export_tariff = get_current_export_tariff(config.get('export_tariffs'), config.get('public_holidays'), current_datetime)
    response = send_price_to_pvoutput(api_key, system_id, config['pvoutput']['import_param'], config['pvoutput']['export_param'], current_import_tariff, current_export_tariff, current_datetime)
    print(f"Sent import tariff {current_import_tariff}c and export tariff {current_export_tariff}c to PVOutput. Response: {response.status_code} - {response.text} at {current_datetime}")
       
    return response.status_code

  main()
