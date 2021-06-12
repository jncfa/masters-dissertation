---
tags: #security #smartbox #gateway 
---

# WoW-IoT MQTT Communication Specification

## Security
- The MQTT standard to be used in all communications is [version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html).
- To authenticate and encrypt communication between devices, the communication will be secured using [TLS v1.2](https://tools.ietf.org/html/rfc5246).
	- In order to use TLS, each device will have a unique [X.509 v3](https://tools.ietf.org/html/rfc5280). 
		- Each device must also have its own [UUID](https://tools.ietf.org/html/rfc4122), which will be named `$device_uuid$`. 
		- The subject for each certificate must have the following fields, where `$device_type$` must either be `gateway`, `smartbox` or `devx` (only in development environment, not for production), depending on identity of the certificate holder: 
		
		[TODO]: If the ACM is ported to AWS, does this format still apply?

		```yaml
		- CN: "$device_type$-$device_uuid$.local" # Subject.CommonName
		- OU: "WoW-IoT" # Subject.OrganizationalUnit
		- O: "Instituto de Sistemas de Robotica" # Subject.Organization
		- L: "Coimbra" # Subject.Locality
		- S: "Coimbra" # Subject.StateOrProvinceName
		- C: "PT" # Subject.CountryName
		```
		
- Each smartbox must only have permission to publish and subscribe in its own endpoints / topics, *e.g*, topics like  `smartbox/$device_uuid$/...`, restricting the access to endpoints of other smartboxes / MQTT clients. 
  
## Communication Properties

- All messages exchanged must be in JSON format, and must have the following structure:

    ```json
    {
        "client_id": $smartbox_id, 
        "timestamp": $timestamp,
        "message_type": $message_type,
        "payload": {
            //...
        }, 
    }
    ```
  
  - The field `payload` must contain the message's content. The field `message_type` defines the type of message sent, and must be one of the following:
  
    ```json
    "message_type" := { 
        /* Sensor measurements */
        "MEASUREMENT_TEMPERATURE",          // medida de temperatura
        "MEASUREMENT_IMU",                  // ...    do IMU
        "MEASUREMENT_ECG",                  // ...    do ECG 
        "MEASUREMENT_PULSEOXIMETRY",        // ...    de oximetria de pulso    
        "MEASUREMENT_RESPIRATION",          // ...    da freq respiratória

        /* Redundancy */
        "SYNC_REQ",                  		// Pacote com o timestamp da última comunicação recebida
        "SYNC_REP",                 		// Pacote que contem as mensagens em atraso
		
		"STATUS_REQ",						// Mensagem a pedir o estado dos clientes ligados ao broker
		"STATUS_REP"						// Mensagem com o estado de um dado cliente
    }
    ```

### Status Endpoint
- The broker should reserve an topic, `status`, which is used to request the status of every smartbox / MQTT client currently connected to the broker.
	- The only clients capable of requesting the status of all clients should be `developer` clients. 
	- To request the status of all devices, the `developer` should send a message (`STATUS_REQ`) with an **empty payload** in the topic `status`.
	- The devices should reply (`STATUS_REP`) on the topic `status/$device_uuid$/` with their current state.
		- The payload format for this message is:
		
	  ```json
	  "payload": {
            "connectedAt" : 1234123.1 //timestamp of the start of the connection
        } 
	  ```
	
### Smartbox Sensor Endpoints
- Each smartbox must publish the sensor data acquired to different endpoints, depending on the type of sensor data to be transmitted:
	
	- Temperature: `smartbox/$device_uuid$/temperature`;
		- The payload format for this message is:
	
	  ```json
	  "payload": {
            "temperature" : 10.0, //temperature measurement
		  	"is_celsius" : true // indication if measurement is in celsius or fahrenheit 
        } 
	  ```
	
	- Inertial Measurement Unit (IMU): `smartbox/$device_uuid$/imu`;
		- The payload format for this message is:
			 [TODO]: Should this topic be splitted in 2 since we won't be able to get both measurements at the same time?
		
	  ```json
	  "payload": {
			"imu": {
				"linear_acceleration": {"x": 0.00, "y": 0.00, "z": 0.00}, // accelerometer measurement
				"angular_velocity": {"x": 0.00, "y": 0.00, "z": 0.00} // gyroscope measurement
			}
		  	"pose_description" : "SITTING"
		} 
	  ```
	
	- Electrocardiogram (ECG): `smartbox/$device_uuid$/ecg`;
		- The payload format for this message is:
	  ```json
	  "payload": {
            "ecg" : 10 //ecg measurement
        } 
	  ```
	
	- Pulse Oximetry: `smartbox/$device_uuid$/pulseoximetry`;
		- The payload format for this message is:
	  ```json
	  "payload": {
            "spo2" : 10.0 //spo2 measurement
        } 
	  ```
	
	- Heart Rate: `smartbox/$device_uuid$/heartrate`;
		- The payload format for this message is:
	  ```json
	  "payload": {
            "bpm" : 10.0 //bpm measurement
        } 
	  ```
	
	- Respiration Rate: `smartbox/$device_uuid$/respiration`;
		- The payload format for this message is:
	  ```json
	  "payload": {
			"respiration" : 10.0 //respiration rate measurement in % (?)
		} 
	  ```
 
## Redundancy
 - When initiating the connection, the smartbox must define an [KeepAlive](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html#_Toc3901045) interval and a [Will Message](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc479576982);
   - The topic used for publishing the will message must be `smartbox/$smartbox_uuid$/ltt`.
   - The content of the Will Message will be defined later.
 - When the smartbox reconnects to the broker after a unexpected disconnection, the broker must send a sync request (`SYNC_REQ`) to the smartbox in the topic `smartbox/$smartbox_id$/sync`. The smartbox must reply (`SYNC_REP`) by sending every measure registered after the given timestamp in the topic `smartbox/$smartbox_id$/sync/response`.
	 - The following example shows the message flow for a given sync request:
  
        ```json
        /* Pedido de sincronização 
        * Publicado pelo servidor no tópico: smartbox/123e4567-e89b-12d3-a456-426655440000/sync
        */
        {
            "client_id": "123e4567-e89b-12d3-a456-426655440000", 
            "timestamp": 1614884856,
            "message_type": "SYNC_REQ",
            "payload": {
                "lastMessageTimestamp": 16148840000
            }, 
        }

        /* Resposta ao pedido de sincronização 
        * Publicado pela smartbox no tópico: smartbox/123e4567-e89b-12d3-a456-426655440000/sync/response
        */
        {
            "client_id": "123e4567-e89b-12d3-a456-426655440000",
            "timestamp": 1614884856,
            "message_type": "SYNC_RESP",
            "payload": {
                [
                    /* Lista de mensagens em backlog (estas não precisam de conter o client_id) */
                    {   
                        "timestamp": 16148840000,
                        "message_type": "MEASUREMENT_TEMPERATURE",
                        "payload": {
                            "data": 10.3
                        }
                    }, 
                    {   
                        "timestamp": 16148840001,
                        "message_type": "MEASUREMENT_TEMPERATURE",
                        "payload": {
                            "data": 10.4
                        }
                    }, 
                    
                    /* ... */
                ]
            }, 
        }
        ```