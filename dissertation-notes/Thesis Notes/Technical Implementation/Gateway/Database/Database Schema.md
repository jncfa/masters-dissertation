## Proposal of Schema for Database
#gateway #database

Link in: https://dbdiagram.io/d/6057e47becb54e10c33c8789
or 

```sql
//schema for for dbdiagram.io



Enum mqtt_access_type {
  read
  write
  readwrite
  deny
}

Enum pair_event {
  pairing
  unpairing
}

Table mqtt_clients {
  device_id uuid
  role_id int
  last_connection timestamp
  
  Indexes {
    (device_id, role_id) [pk]
  }  
}

Table patients {
  id uuid [primary key] // auto-increment
  alias text
}

Table smartboxes {
  id uuid [primary key] // auto-increment
  alias text
}

Table biostickers {
  id uuid [pk] // auto-increment
  alias text
  mac_addr macaddr
}

Table biosticker_pair_events {
  smartbox_id uuid
  biosticker_id uuid
  timestamp timestamp 
  pair_event pair_event
  Indexes {
    (smartbox_id, biosticker_id , timestamp) [pk]
  }
}

Table patient_pair_events {
  smartbox_id uuid
  patient_id uuid
  
  timestamp timestamp 
  pair_event pair_event
  Indexes {
    (smartbox_id, patient_id , timestamp) [pk]
  }
}




Table sensor_temperature {
  biosticker_id int
  timestamp timestamp
  temperature float
  Indexes {
    (biosticker_id , timestamp) [pk]
  }
}

Table sensor_ecg {
  biosticker_id int
  timestamp timestamp
  data json
  Indexes {
    (biosticker_id , timestamp) [pk]
  }
}

Table sensor_respiration {
  biosticker_id int
  timestamp timestamp
  data json
  Indexes {
    (biosticker_id , timestamp) [pk]
  }
}

Table sensor_pulseoximetry {
  biosticker_id int
  timestamp timestamp
  data json
  Indexes {
    (biosticker_id , timestamp) [pk]
  }
}

Table sensor_imu {
  biosticker_id int
  timestamp timestamp
  data json
  pose_description text
  Indexes {
    (biosticker_id , timestamp) [pk]
  }
}


Table mqtt_roles {
  role_id int [pk]
  role_name text
}

Table mqtt_role_permissions {
  permission_id int [pk]
  role_id int
  topic_wildcard text
  access_type mqtt_access_type

  Indexes {
    (role_id, topic_wildcard )
  }
  
}


Ref: "mqtt_roles"."role_id" < "mqtt_role_permissions"."role_id"

Ref: "smartboxes"."id" < "biosticker_pair_events"."smartbox_id"

Ref: "biostickers"."id" < "biosticker_pair_events"."biosticker_id"

Ref: "sensor_temperature"."biosticker_id" < "biostickers"."id"

Ref: "sensor_ecg"."biosticker_id" > "biostickers"."id"

Ref: "sensor_imu"."biosticker_id" > "biostickers"."id"

Ref: "mqtt_roles"."role_id" < "mqtt_clients"."role_id"

Ref: "mqtt_clients"."device_id" - "smartboxes"."id"

Ref: "smartboxes"."id" < "patient_pair_events"."smartbox_id"

Ref: "patients"."id" < "patient_pair_events"."patient_id"

Ref: "biostickers"."id" < "sensor_respiration"."biosticker_id"

Ref: "biostickers"."id" < "sensor_pulseoximetry"."biosticker_id"
```
