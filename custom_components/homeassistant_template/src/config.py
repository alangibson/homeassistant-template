from homeassistant.const import Platform


UPDATE_INTERVAL = 5

# A list of the platforms you're using, in order they should be loaded
# A list is here: https://developers.home-assistant.io/docs/core/entity
PLATFORMS = [Platform.SENSOR, Platform.WEATHER]

# Retry on initial data update failure or not
FIRST_REFRESH_RETRY_ON_FAILURE = True

# True if your device has a unique id, False if not
DEVICE_HAS_UNIQUE_ID = True

# One of hub, device or service
#
# This also needs to be set in the manifest.json integration_type property.
#
# https://developers.home-assistant.io/docs/creating_integration_manifest/#integration-type
# https://developers.home-assistant.io/blog/page/6/?_highlight=hub#differentiating-hubs-devices-and-services
INTEGRATION_TYPE = 'device'

# If your entities need to fetch data before being written to Home Assistant for the first time, pass update_before_add=True 
UPDATE_BEFORE_ADD = True

# Restore sensor state after restart?
RESTORE_SENSOR = True