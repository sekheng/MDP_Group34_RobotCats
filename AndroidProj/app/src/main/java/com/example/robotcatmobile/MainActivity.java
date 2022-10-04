package com.example.robotcatmobile;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.MenuItem;
import android.widget.Toast;

import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationBarView;

@RequiresApi(api = Build.VERSION_CODES.N)
public class MainActivity extends AppCompatActivity implements NavigationBarView.OnItemSelectedListener {
    HomeFrag homeFragment = new HomeFrag();
    BluetoothFrag bluetoothFrag = new BluetoothFrag();

    boolean retryConnection = false;
    Handler reconnectionHandler = new Handler();

    ProgressDialog mConnectDialog;

    Runnable mReconnectionRunnable = new Runnable() {
        @Override
        public void run() {
            try {
                if (!BluetoothConn.BluetoothConnectionStatus) {
                    // start connection and pray hard
                    BluetoothConn.instance.startClientThread(BluetoothConn.instance.mDevice);
                    Toast.makeText(getApplicationContext(), "Reconnection Success", Toast.LENGTH_SHORT).show();
                }
                reconnectionHandler.removeCallbacks(mReconnectionRunnable);
                retryConnection = false;
            } catch (Exception e) {
                Toast.makeText(getApplicationContext(), "Failed to reconnect, trying in 5 second", Toast.LENGTH_SHORT).show();
            }
        }
    };

    final String HOME_FRAG_TAG = "HOME";
    final String BT_FRAG_TAG = "BT";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // the bottom navigation
        BottomNavigationView bottomNavigationView = findViewById(R.id.bottomNavigationView);
        bottomNavigationView.setOnItemSelectedListener(this);
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.add(R.id.flFragment,homeFragment,HOME_FRAG_TAG);
        ft.add(R.id.flFragment,bluetoothFrag,BT_FRAG_TAG);
        ft.commitNow();
        bottomNavigationView.setSelectedItemId(R.id.home_tab);
        IntentFilter connectionStatusIntent = new IntentFilter(BluetoothConn.CONNECTION_STATUS);
        LocalBroadcastManager.getInstance(getApplicationContext()).registerReceiver(mDisconnBR, connectionStatusIntent);
        mConnectDialog = new ProgressDialog(MainActivity.this);
        mConnectDialog.setMessage("Waiting for other device to reconnect...");
        mConnectDialog.setCancelable(false);
        mConnectDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", (dialog, which) -> dialog.dismiss());
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        LocalBroadcastManager.getInstance(getApplicationContext()).unregisterReceiver(mDisconnBR);
    }

    /*
        To change the fragment which will replace the main page!
         */
    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        switch (item.getItemId()) {
            case R.id.home_tab:
                ft.show(getSupportFragmentManager().findFragmentByTag(HOME_FRAG_TAG));
                ft.hide(getSupportFragmentManager().findFragmentByTag(BT_FRAG_TAG));
                break;
            case R.id.bluetooth_tab:
                ft.show(getSupportFragmentManager().findFragmentByTag(BT_FRAG_TAG));
                ft.hide(getSupportFragmentManager().findFragmentByTag(HOME_FRAG_TAG));
                break;
        }
        ft.commit();
        return true;
    }

    private final BroadcastReceiver mDisconnBR = new BroadcastReceiver() {
        @SuppressLint("MissingPermission")
        @Override
        public void onReceive(Context context, Intent intent) {
            BluetoothDevice mDevice = intent.getParcelableExtra("Device");
            String status = intent.getStringExtra("Status");

            if(status.equals("connected")){
                try {
                    mConnectDialog.dismiss();
                } catch(NullPointerException e){
                    e.printStackTrace();
                }

                Log.d(BluetoothFrag.TAG, "mDisconnBR: Device now connected to " + mDevice.getName());
                Toast.makeText(getApplicationContext(), "Device now connected to "+mDevice.getName(), Toast.LENGTH_LONG).show();
            }
            else if(status.equals("disconnected") && !retryConnection){
                Log.d(BluetoothFrag.TAG, "mDisconnBR: Disconnected from "+mDevice.getName());
                Toast.makeText(getApplicationContext(), "Disconnected from "+mDevice.getName(), Toast.LENGTH_LONG).show();
                try {
                    mConnectDialog.show();
                }catch (Exception e){
                    Log.d(BluetoothFrag.TAG, "BluetoothPopUp: mBroadcastReceiver5 Dialog show failure");
                }
                retryConnection = true;
                reconnectionHandler.postDelayed(mReconnectionRunnable, 5000);
            }
        }
    };

}