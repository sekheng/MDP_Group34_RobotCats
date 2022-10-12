package com.example.robotcatmobile.home_parts;

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
import androidx.fragment.app.Fragment;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Handler;
import android.os.SystemClock;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.robotcatmobile.R;
import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;

@RequiresApi(api = Build.VERSION_CODES.N)
public class Frag_timer extends Fragment {
    public static final String EXPLORE_VAL = "exploring";
    // const value of robot fastest path
    public static final String FASTEST_VAL = "fastest";
    // const value of robot idle
    public static final String IDLE_VAL = "idle";
    // to know the status of the robot
    public static final String STATUS_KEY = "status";
    // get the time now variable
    long mStartTime;
    // thread to handle it
    Handler mStopWatchThread;
    // button for explore
    AppCompatButton mExploreButton;
    // textview for explore
    TextView mExploreText;
    // button for fastest
    AppCompatButton mFastestButton;
    // textview for fastest
    TextView mFastestText;
    // boolean flags to know whether it runs
    boolean mIsFastest = false;
    // to change the robot status text
    TextView mStatusTxt;
    // SEND all obstacles in one press
    AppCompatButton mSendAllObsBtn;
    // the grid recycler to interact with
    GridRecycler mGridRecycler;
    public Frag_timer(GridRecycler gridRecycler) {
        mGridRecycler = gridRecycler;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_timer, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        mStatusTxt = view.findViewById(R.id.robot_status);
        IntentFilter statusFilter = new IntentFilter(STATUS_KEY);
        LocalBroadcastManager.getInstance(getContext()).registerReceiver(mStatusReceiver, statusFilter);
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

        mSendAllObsBtn = view.findViewById(R.id.send_all_obs_btn);
        mSendAllObsBtn.setOnClickListener(view1 -> {
            // then send all the obstacles from the grid recycler to the JSON array then bluetooth
            JSONArray jArray = new JSONArray();
            for (int num = 0; num < mGridRecycler.mAllObstacleList.size(); ++num) {
                try {
                    // get the JSON object, then set it in the array
                    GridRecycler.ViewHolder gridObs = mGridRecycler.mAllObstacleList.get(num);
                    JSONObject jsonObject = new JSONObject();
                    jsonObject.put(BluetoothConn.SENDING_TYPE, GridRecycler.OBSTACLE_VALUE);
                    jsonObject.put(GridRecycler.X_KEY,gridObs.mX);
                    jsonObject.put(GridRecycler.Y_KEY,gridObs.mY);
                    if (gridObs.mDirection != Direction.NONE) {
                        jsonObject.put(GridRecycler.DIRECTION_KEY,gridObs.mDirection.toString());
                    }
                    if (!gridObs.mObstacleSymbol.isEmpty()) {
                        jsonObject.put(GridRecycler.SYMBOL_KEY, gridObs.mObstacleSymbol);
                    }
                    jArray.put(jsonObject);
                }
                catch (Exception e) {
                    e.printStackTrace();
                }
            }
            String jArrayStr = jArray.toString();
            BluetoothConn.write(jArrayStr.getBytes(StandardCharsets.UTF_8));
        });
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