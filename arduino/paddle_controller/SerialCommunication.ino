#define ANGLE_PRECISION 0.1
#define CLOSED_ANGLE 90
#define MAX_CHANNEL 5
#define ANGLE_LIMIT 360
#define STOP_INTERVAL 185

void serialCommunication() {
  if (Serial.available() > 0) {
    String serialReadout = Serial.readString();
    execCmd(serialReadout);
  }
}

void execCmd(String serialReadout) {
  if(!cmdCH(serialReadout)) {
    Serial.print("ERROR: Invalid command.\n");
  }
}


int cmdCH(String serialReadout) {
  String readoutPrefix = serialReadout.substring(0, 2);
  if (readoutPrefix == "CH" || readoutPrefix == "ch") {
    unsigned short channel = serialReadout[2] - '0';
    if (channel > 0 && channel <= MAX_CHANNEL) {
      float angle = serialReadout.substring(4, 12).toFloat();
      changeAngle(channel, angle);
    }
    else {
      Serial.print("ERROR: Invalid channel. Acceptable channels range from 1 to ");
      Serial.print(MAX_CHANNEL);
      Serial.print("\n");
    }
    return 1;
  }
  else {
    return 0;
  }
}

void changeAngle(unsigned short channel, float angle) {
  if (abs(angle) <= ANGLE_LIMIT){
    float newAngle = CLOSED_ANGLE + angle;
    boards[channel - 1]->write(newAngle);
    delay(STOP_INTERVAL);
    boards[channel - 1]->write(CLOSED_ANGLE);
    Serial.print("Channel ");
    Serial.print(channel);
    Serial.print(" set to ");
    Serial.print(angle);
    Serial.print(" degrees.\n");
  }
  else {
    Serial.print("ERROR: Invalid angle. Acceptable angles range from ");
    Serial.print(-ANGLE_LIMIT);
    Serial.print( " to ");
    Serial.print(ANGLE_LIMIT);
    Serial.print(" degrees.\n");
  }
}
