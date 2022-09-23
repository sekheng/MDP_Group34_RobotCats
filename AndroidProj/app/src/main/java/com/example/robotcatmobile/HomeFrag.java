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
import androidx.appcompat.widget.AppCompatButton;
import androidx.appcompat.widget.AppCompatToggleButton;
import androidx.fragment.app.Fragment;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Handler;
import android.os.SystemClock;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.appcompat.widget.AppCompatImageButton;

import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.TextView;

import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;
import com.example.robotcatmobile.home_parts.GridRecycler;
import com.example.robotcatmobile.home_parts.SET_GRID_STATE;

import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;


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
    // const value of robot exploring
    public static final String EXPLORE_VAL = "exploring";
    // const value of robot fastest path
    public static final String FASTEST_VAL = "fastest";
    // const value of robot idle
    public static final String IDLE_VAL = "idle";

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
    // button for explore
    AppCompatButton mExploreButton;
    // textview for explore
    TextView mExploreText;
    // button for fastest
    AppCompatButton mFastestButton;
    // textview for fastest
    TextView mFastestText;
    // get the time now variable
    long mStartTime;
    // thread to handle it
    Handler mStopWatchThread;
    // boolean flags to know whether it runs
    boolean mIsFastest = false;

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

        mExploreButton = view.findViewById(R.id.explore_button);
        mExploreButton.setOnClickListener(view1 -> {
            if (!mIsFastest && mStopWatchThread != null) {
                // this means that it is toggling start/stop
                stopTimeBluetooth();
            }
            else {
                mIsFastest = false;
                // set the status!
                startTimeBluetooth(EXPLORE_VAL);
            }
        });
        mExploreText = view.findViewById(R.id.explore_text);
        mFastestButton = view.findViewById(R.id.fastest_button);
        mFastestButton.setOnClickListener(view1 -> {
            if (mIsFastest && mStopWatchThread != null) {
                // this means that it is toggling start/stop
                stopTimeBluetooth();
            }
            else {
                mIsFastest = true;
                startTimeBluetooth(FASTEST_VAL);
            }
        });
        mFastestText = view.findViewById(R.id.fastest_text);
    }

    void stopTimeBluetooth() {
        stopTime();
        JSONObject jsonObject = new JSONObject();
        try {
            // to send to the robot that it has stopped
            jsonObject.put(STATUS_KEY, IDLE_VAL);
            BluetoothConn.write(jsonObject.toString().getBytes(StandardCharsets.UTF_8));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    void stopTime() {
        sendStatusValue(IDLE_VAL);
    }

    void startTimeBluetooth(String statusStr) {
        sendStatusValue(statusStr);
        // and send the text over in bluetooth
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put(STATUS_KEY, statusStr);
            BluetoothConn.write(jsonObject.toString().getBytes(StandardCharsets.UTF_8));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        startTime();
    }

    void startTime() {
        if (mStopWatchThread == null) {
            mStopWatchThread = new Handler();
        }
        else {
            mStopWatchThread.removeCallbacks(runnable);
        }
        mStopWatchThread.postDelayed(runnable, 0);
        mStartTime = SystemClock.uptimeMillis();
    }

    void sendStatusValue(String statusVal) {
        Intent statusIntent = new Intent(STATUS_KEY);
        statusIntent.putExtra(STATUS_KEY, statusVal);
        LocalBroadcastManager.getInstance(getContext()).sendBroadcast(statusIntent);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        LocalBroadcastManager.getInstance(getContext()).unregisterReceiver(mStatusReceiver);
        if (mStopWatchThread != null) {
            mStopWatchThread.removeCallbacks(runnable);
            mStopWatchThread = null;
        }
    }

    BroadcastReceiver mStatusReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String statusVal = intent.getStringExtra(STATUS_KEY);
            mStatusTxt.setText(statusVal);
            if (statusVal.equalsIgnoreCase(IDLE_VAL)) {
                mStopWatchThread.removeCallbacks(runnable);
                mStopWatchThread = null;
            }
            else {
                if (statusVal.equalsIgnoreCase(EXPLORE_VAL)) {
                    mIsFastest = false;
                } else if (statusVal.equalsIgnoreCase(FASTEST_VAL)) {
                    mIsFastest = true;
                }
                startTime();
            }
        }
    };

    //Stop Watch logic
    public  Runnable runnable = new Runnable() {
        @Override
        public void run() {
            long timeInMilliseconds = SystemClock.uptimeMillis()-mStartTime;
            int Seconds=(int)(timeInMilliseconds/1000);
            int Minutes=Seconds/60;
            Seconds%=60;
            int MilliSeconds=(int)(timeInMilliseconds%1000);

            String text = Minutes + ":" +String.format("%02d",Seconds)+":"
                    +String.format("%03d",MilliSeconds);
            if (mIsFastest) {
                mFastestText.setText(text);
            }
            else {
                mExploreText.setText(text);
            }
            mStopWatchThread.postDelayed(this,0);
        }
    };

}