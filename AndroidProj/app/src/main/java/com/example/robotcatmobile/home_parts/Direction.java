package com.example.robotcatmobile.home_parts;
/**
 * To hold the direction that the robot/obstacle is facing!
 */
public enum Direction {
    NONE (-360),
    NORTH(0),
    EAST(90),
    SOUTH(180),
    WEST(270);

    int mValue = 0;
    Direction(int value) {
        mValue = value;
    }

    public int getValue() {
        return mValue;
    }
}
