package com.example.robotcatmobile.bluetooth_parts;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.robotcatmobile.R;

import java.util.ArrayList;

public class PairedRecycler extends RecyclerView.Adapter<PairedRecycler.ViewHolder> {
    // each individual item should be in JSON
    public ArrayList<BluetoothDevice> mLocalDataSet = new ArrayList<>();
    // a flag to know is it discovered or paired
    public boolean mIsDiscovered;

    /*
    constructor to pass bluetooth values here!
     */
    public PairedRecycler(boolean IsDiscovered) {
        mIsDiscovered = IsDiscovered;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // Create a new view, which defines the UI of the list item
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.bluetooth_item_details, parent, false);
        return new ViewHolder(view);
    }

    @SuppressLint("MissingPermission")
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        BluetoothDevice bluetoothDevice = mLocalDataSet.get(position);
        holder.mBluetoothText.setText(bluetoothDevice.getName() + "\n" + bluetoothDevice.getAddress());
        holder.mBTDevice = bluetoothDevice;
    }

    @Override
    public int getItemCount() {
        return mLocalDataSet.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        // text to view the bluetooth name and its address
        public TextView mBluetoothText;
        // and the buttons to access
        public Button mDeviceButton;
        // need a place to reference the device!
        public BluetoothDevice mBTDevice;

        private final BroadcastReceiver mDisconnBR = new BroadcastReceiver() {
            @SuppressLint("MissingPermission")
            @Override
            public void onReceive(Context context, Intent intent) {
                BluetoothDevice mDevice = intent.getParcelableExtra("Device");
                String status = intent.getStringExtra("Status");
                if (mDevice.equals(mBTDevice)) {
                    if (status.equals("connected")) {
                        try {
                            mDeviceButton.setText("Connected");
                        } catch (NullPointerException e) {
                            e.printStackTrace();
                        }
                    } else if (status.equals("disconnected")) {
                        mDeviceButton.setText("Connect");
                        mDeviceButton.setClickable(true);
                    }
                }
            }
        };

        @SuppressLint("MissingPermission")
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            // initialized the widgets
            mBluetoothText = itemView.findViewById(R.id.bluetooth_detail);
            mDeviceButton = itemView.findViewById(R.id.bluetooth_item_button);
            if (mIsDiscovered)
            {
                mDeviceButton.setText("PAIR");
            }
            mDeviceButton.setOnClickListener(view -> {
                // set up pairing or connecting depending on the boolean flag
                BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
                bluetoothAdapter.cancelDiscovery();
                if (mIsDiscovered) {
                    // then start bonding/pairing
                    mBTDevice.createBond();
                }
                else {
                    // do connection!
                    BluetoothConn.instance.startClientThread(mBTDevice);
                    mDeviceButton.setText("Connecting!");
                    mDeviceButton.setClickable(false);
                    IntentFilter connectionStatusIntent = new IntentFilter(BluetoothConn.CONNECTION_STATUS);
                    LocalBroadcastManager.getInstance(view.getContext()).registerReceiver(mDisconnBR, connectionStatusIntent);
                }
            });
        }
    }

}
