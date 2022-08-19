package com.example.robotcatmobile.bluetooth_parts;

import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.robotcatmobile.R;

public class BluetoothDetailHolder extends RecyclerView.ViewHolder {
    // text to view the bluetooth name and its address
    private TextView mBluetoothText;
    // and the buttons to access
    private Button mDeviceButton;

    public BluetoothDetailHolder(@NonNull View itemView) {
        super(itemView);
        // initialized the widgets
        mBluetoothText = itemView.findViewById(R.id.bluetooth_detail);
        mDeviceButton = itemView.findViewById(R.id.bluetooth_item_button);
    }
}
