
Creating a HomeAssistant integration is a tedious and frustrating, but 
ultimately rewarding, experience. This template aims to make the process 
straightforward, without requiring you to learn the HomeAssistant architecture
from the ground up.

# Assumptions

This is an opinionated template, which means it make some assumptions.

- Each entry in your integration's configuration will represent one physical device
  (i.e. your integration_type in manifest.json will be 'device')
- You want to poll your device for data at regular intervals
  (i.e. your iot_class in mainifest.json ends with '_polling')
- You want to configure the integration using the UI
  (i.e. users are not required to manually edit configuration.yaml)

# Usage

## Manifest

- Set iot_class in manifest.json to either cloud_polling or local_polling
- Add your Python 3rd party library requirements to manifest.json

## Configuration

### Platforms

- The platform types you will use should in the PLATFORMS list in __init__.py

### IOT Class

- If iot_class ends with *_polling, then you should use a DataUpdateCoordinator

See: https://developers.home-assistant.io/docs/creating_integration_manifest/#iot-class

### 