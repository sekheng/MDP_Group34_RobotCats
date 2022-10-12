package com.example.robotcatmobile.home_parts;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.widget.AppCompatImageButton;
import androidx.fragment.app.Fragment;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.robotcatmobile.R;
import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;

import org.json.JSONException;
import org.json.JSONObject;
@RequiresApi(api = Build.VERSION_CODES.N)
public class Frag_ptz extends Fragment {
    // to send the key of the robot has moved
    public static final String ROBOT_DIRECTION = "robot_direction";
    // constant value of robot going up
    public static final String ROBOT_UP = "up";
    // const value of robot reverse
    public static final String ROBOT_REVERSE = "down";
    // const value of robot going right
    public static final String ROBOT_RIGHT = "right";
    // const value of robot going left
    public static final String ROBOT_LEFT = "left";
    // const value of robot exploring
    public static final String ROBOT_RDU = "right diagonal up";
    public static final String ROBOT_LDU = "left diagonal up";
    public static final String ROBOT_RDD = "right diagonal down";
    public static final String ROBOT_LDD = "left diagonal down";
    // right button
    AppCompatImageButton mRightButton;
    //left button
    AppCompatImageButton mLeftButton;
    // up button
    AppCompatImageButton mForwardButton;
    // down button
    AppCompatImageButton mBackButton;
    AppCompatImageButton mRDUButton;
    AppCompatImageButton mLDUButton;
    AppCompatImageButton mRDDButton;
    AppCompatImageButton mLDDButton;


    public Frag_ptz() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_ptz, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        mRightButton = view.findViewById(R.id.right_btn);
        mRightButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_RIGHT);
        });
        mLeftButton = view.findViewById(R.id.left_btn);
        mLeftButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_LEFT);
        });
        mForwardButton = view.findViewById(R.id.forward_btn);
        mForwardButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_UP);
        });
        mBackButton = view.findViewById(R.id.back_btn);
        mBackButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_REVERSE);
        });
        mLDDButton = view.findViewById(R.id.left_down_btn);
        mLDDButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_LDD);
        });
        mLDUButton = view.findViewById(R.id.left_up_btn);
        mLDUButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_LDU);
        });
        mRDUButton = view.findViewById(R.id.right_up_btn);
        mRDUButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_RDU);
        });
        mRDDButton = view.findViewById(R.id.right_down_btn);
        mRDDButton.setOnClickListener(view1 -> {
            ControlPressedBluetooth(ROBOT_RDD);
        });
    }

    void ControlPressedBluetooth(String toSend) {
        if (GridRecycler.mIsRobotPlaced) {
            // send the turn right button
            // put it in a json!
            JSONObject rightJson = new JSONObject();
            try {
                rightJson.put(ROBOT_DIRECTION, toSend);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            String jsonStr = rightJson.toString();
            BluetoothConn.write(jsonStr.getBytes());
            ControlPressed(toSend);
        }
    }

    void ControlPressed(String toSend) {
        if (GridRecycler.mIsRobotPlaced) {
            Intent jsonIntent = new Intent(ROBOT_DIRECTION);
            jsonIntent.putExtra(ROBOT_DIRECTION, toSend);
            LocalBroadcastManager.getInstance(getContext()).sendBroadcast(jsonIntent);
        }
    }

}