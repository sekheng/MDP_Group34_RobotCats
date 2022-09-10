package com.example.robotcatmobile;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.widget.AppCompatToggleButton;
import androidx.fragment.app.Fragment;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.appcompat.widget.AppCompatImageButton;

import android.widget.RadioGroup;
import android.widget.TextView;

import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;
import com.example.robotcatmobile.home_parts.GridRecycler;
import com.example.robotcatmobile.home_parts.SET_GRID_STATE;

import org.json.JSONException;
import org.json.JSONObject;


/**
 * A simple {@link Fragment} subclass.
 * create an instance of this fragment.
 */
public class HomeFrag extends Fragment {
    // to know the status of the robot
    public static final String STATUS_KEY = "status";
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

    // the grid UI
    RecyclerView mGridLayout;

    // to change the robot status text
    TextView mStatusTxt;
    // right button
    AppCompatImageButton mRightButton;
    //left button
    AppCompatImageButton mLeftButton;
    // up button
    AppCompatImageButton mForwardButton;
    // down button
    AppCompatImageButton mBackButton;
    // radio group for obstacles
    RadioGroup mToggleGroups;

    public HomeFrag() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        IntentFilter statusFilter = new IntentFilter(STATUS_KEY);
        LocalBroadcastManager.getInstance(getContext()).registerReceiver(mStatusReceiver, statusFilter);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false);
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // get the grid layout
        mGridLayout = view.findViewById(R.id.grid);
        GridRecycler gridRecycler = new GridRecycler();
        mGridLayout.setAdapter(gridRecycler);
        // span count in this case is the number of columns
        mGridLayout.setLayoutManager(new GridLayoutManager(getContext(), GridRecycler.COLUMNS));

        mStatusTxt = view.findViewById(R.id.robot_status);

        mRightButton = view.findViewById(R.id.right_btn);
        mRightButton.setOnClickListener(view1 -> {
            if (GridRecycler.mIsRobotPlaced) {
                // send the turn right button
                // put it in a json!
                JSONObject rightJson = new JSONObject();
                try {
                    //rightJson.put("tr","tr");
                    rightJson.put(ROBOT_DIRECTION, ROBOT_RIGHT);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                BluetoothConn.write(rightJson.toString().getBytes());
                // send a message to move right
                Intent jsonIntent = new Intent(ROBOT_DIRECTION);
                jsonIntent.putExtra(ROBOT_DIRECTION, rightJson.toString());
                LocalBroadcastManager.getInstance(getContext()).sendBroadcast(jsonIntent);
            }
        });
        mLeftButton = view.findViewById(R.id.left_btn);
        mLeftButton.setOnClickListener(view1 -> {
            if (GridRecycler.mIsRobotPlaced) {
                // send the turn right button
                // put it in a json!
                JSONObject rightJson = new JSONObject();
                try {
                    //rightJson.put("tl","tl");
                    rightJson.put(ROBOT_DIRECTION, ROBOT_LEFT);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                BluetoothConn.write(rightJson.toString().getBytes());
                // send a message to say that it turns left
                Intent jsonIntent = new Intent(ROBOT_DIRECTION);
                jsonIntent.putExtra(ROBOT_DIRECTION, rightJson.toString());
                LocalBroadcastManager.getInstance(getContext()).sendBroadcast(jsonIntent);
            }
        });
        mForwardButton = view.findViewById(R.id.forward_btn);
        mForwardButton.setOnClickListener(view1 -> {
            if (GridRecycler.mIsRobotPlaced) {
                // send the turn right button
                // put it in a json!
                JSONObject rightJson = new JSONObject();
                try {
                    //rightJson.put("f","f");
                    rightJson.put(ROBOT_DIRECTION, ROBOT_UP);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                BluetoothConn.write(rightJson.toString().getBytes());
                // then send a message to move forward
                Intent jsonIntent = new Intent(ROBOT_DIRECTION);
                jsonIntent.putExtra(ROBOT_DIRECTION, rightJson.toString());
                LocalBroadcastManager.getInstance(getContext()).sendBroadcast(jsonIntent);
            }
        });
        mBackButton = view.findViewById(R.id.back_btn);
        mBackButton.setOnClickListener(view1 -> {
            if (GridRecycler.mIsRobotPlaced) {
                // send the turn right button
                // put it in a json!
                JSONObject rightJson = new JSONObject();
                try {
                    //rightJson.put("r","r");
                    rightJson.put(ROBOT_DIRECTION, ROBOT_REVERSE);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                BluetoothConn.write(rightJson.toString().getBytes());
                // send a message to move backwards
                Intent jsonIntent = new Intent(ROBOT_DIRECTION);
                jsonIntent.putExtra(ROBOT_DIRECTION, rightJson.toString());
                LocalBroadcastManager.getInstance(getContext()).sendBroadcast(jsonIntent);
            }
        });
        mToggleGroups = view.findViewById(R.id.toggle_groups);

        for (int j = 0; j < mToggleGroups.getChildCount(); j++) {
            final AppCompatToggleButton toggleButton = (AppCompatToggleButton) mToggleGroups.getChildAt(j);
            toggleButton.setOnCheckedChangeListener((compoundButton, b) -> {
                String toggleButtonTxt = compoundButton.getText().toString();
                    if (b) {
                        for (int i = 0; i < mToggleGroups.getChildCount(); i++) {
                            final AppCompatToggleButton otherToggle = (AppCompatToggleButton)mToggleGroups.getChildAt(i);
                            if (compoundButton != otherToggle)
                                otherToggle.setChecked(false);
                        }
                       // then set the state
                        for (SET_GRID_STATE state:SET_GRID_STATE.values()) {
                            if (toggleButtonTxt.contains(state.toString())) {
                                GridRecycler.curInteractState = state;
                                break;
                            }
                        }
                    }
                    else {
                        // then check and ensure that the buttons matched with the undex
                        if (toggleButtonTxt.contains(GridRecycler.curInteractState.toString()))
                        {
                            GridRecycler.curInteractState = SET_GRID_STATE.NONE;
                        }
                    }
                }
            );
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        LocalBroadcastManager.getInstance(getContext()).unregisterReceiver(mStatusReceiver);
    }

    BroadcastReceiver mStatusReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            mStatusTxt.setText(intent.getStringExtra(STATUS_KEY));
        }
    };
}