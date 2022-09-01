package com.example.robotcatmobile;

import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.appcompat.widget.AppCompatImageButton;
import android.widget.TextView;

import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;
import com.example.robotcatmobile.home_parts.GridLabelRecycler;
import com.example.robotcatmobile.home_parts.GridRecycler;
import com.example.robotcatmobile.home_parts.SpanningLinearLayoutManager;

import org.json.JSONException;
import org.json.JSONObject;


/**
 * A simple {@link Fragment} subclass.
 * Use the {@link HomeFrag#newInstance} factory method to
 * create an instance of this fragment.
 */
public class HomeFrag extends Fragment {
    static final String STATUS_KEY = "status";

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    RecyclerView mGridLayout;
    // the vertical labels
    RecyclerView mVerticalLabels;
    // the horizontal labels
    RecyclerView mHorizontalLabels;

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

    public HomeFrag() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment home.
     */
    // TODO: Rename and change types and number of parameters
    public static HomeFrag newInstance(String param1, String param2) {
        HomeFrag fragment = new HomeFrag();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
        IntentFilter statusFilter = new IntentFilter(STATUS_KEY);
        LocalBroadcastManager.getInstance(getContext()).registerReceiver(mStatusReceiver, statusFilter);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        /*
        // get the grid layout
        mGridLayout = view.findViewById(R.id.grid);
        GridRecycler gridRecycler = new GridRecycler();
        mGridLayout.setAdapter(gridRecycler);
        // span count in this case is the number of columns
        mGridLayout.setLayoutManager(new GridLayoutManager(getContext(), GridRecycler.COLUMNS));
        mGridLayout.getViewTreeObserver().addOnGlobalLayoutListener(() -> {
            // this means that the grid layout has finished
            int widthOfGridLayout = mGridLayout.getWidth();
            int height = mGridLayout.getHeight();
            //mVerticalLabels.setMinimumHeight(mGridLayout.getHeight() / 2);
            //mHorizontalLabels.setMinimumWidth(mGridLayout.getWidth());
        });

        mVerticalLabels = view.findViewById(R.id.grid_verticalLabels);
        GridLabelRecycler verticalLabelRecycler = new GridLabelRecycler(true);
        mVerticalLabels.setAdapter(verticalLabelRecycler);
        mVerticalLabels.setLayoutManager(new SpanningLinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL,false));

        mHorizontalLabels = view.findViewById(R.id.grid_horizontalLabels);
        GridLabelRecycler horizontalLabelRecycler = new GridLabelRecycler(false);
        mHorizontalLabels.setAdapter(horizontalLabelRecycler);
        mHorizontalLabels.setLayoutManager(new SpanningLinearLayoutManager(getContext(), LinearLayoutManager.HORIZONTAL,false));
         */
        mStatusTxt = view.findViewById(R.id.robot_status);

        mRightButton = view.findViewById(R.id.right_btn);
        mRightButton.setOnClickListener(view1 -> {
            // send the turn right button
            // put it in a json!
            JSONObject rightJson = new JSONObject();
            try {
                rightJson.put("tr","tr");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            BluetoothConn.write(rightJson.toString().getBytes());
        });
        mLeftButton = view.findViewById(R.id.left_btn);
        mLeftButton.setOnClickListener(view1 -> {
            // send the turn right button
            // put it in a json!
            JSONObject rightJson = new JSONObject();
            try {
                rightJson.put("tl","tl");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            BluetoothConn.write(rightJson.toString().getBytes());
        });
        mForwardButton = view.findViewById(R.id.forward_btn);
        mForwardButton.setOnClickListener(view1 -> {
            // send the turn right button
            // put it in a json!
            JSONObject rightJson = new JSONObject();
            try {
                rightJson.put("f","f");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            BluetoothConn.write(rightJson.toString().getBytes());
        });
        mBackButton = view.findViewById(R.id.back_btn);
        mBackButton.setOnClickListener(view1 -> {
            // send the turn right button
            // put it in a json!
            JSONObject rightJson = new JSONObject();
            try {
                rightJson.put("r","r");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            BluetoothConn.write(rightJson.toString().getBytes());
        });
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