# Eclipse Mosquitto configs

Configurations for eclipse mosquitto to run the broker in various environments.

## Available configurations

- `mosquitto.conf`: Default configuration for the main broker on the rover
- `mosquitto-arm.conf`: Configuration for the arm. This configuration bridges the broker to the main broker on ther rover.

## Running Mosquitto 

You can follow the instructions here for installing mosquitto and for placing the configs.

https://github.com/mcgill-robotics/rover-2025/wiki/MQTT:-Installation-and-Set-Up

Alternatively you can use docker/podman (these commands are specifically for Linux)

**Run the default config:**

`docker run -it --replace --name mosquitto -p 1883:1883 -p 9001:9001 -v "$PWD/config:/mosquitto/config:Z" docker.io/eclipse-mosquitto`

**Run mosquitto with the arm config from this directory:**

`docker run -it --replace --name mosquitto -p 1883:1883 -p 9001:9001 -v "$PWD/config:/mosquitto/config:Z" docker.io/eclipse-mosquitto mosquitto -c /mosquitto/config/mosquitto-arm.conf`