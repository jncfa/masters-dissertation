# MQTT Authorization Plugin Data

## Setting up plugin

## Access Type
```c
int access_type = pow(2, 0) 	// 1st bit - read access
				+ pow(2, 1) 	// 2nd bit - write access
				+ pow(2, 2); 	// 3rd bit - subscribe access
```

- Careful setting up the plugin, authentication callback may not be called depending on the config: https://github.com/eclipse/mosquitto/issues/2183
