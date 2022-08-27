package com.example.robotcatmobile;

import static android.content.Context.LAYOUT_INFLATER_SERVICE;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.collection.ArraySet;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Handler;
import android.provider.Settings;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;
import android.widget.Toast;

import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;
import com.example.robotcatmobile.bluetooth_parts.ChatPopup;
import com.example.robotcatmobile.bluetooth_parts.PairedRecycler;

import java.util.Set;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link BluetoothFrag#newInstance} factory method to
 * create an instance of this fragment.
 */
public class BluetoothFrag extends Fragment {
    private static final String TAG = "Bluetooth Frag";


    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    private static final int REQUEST_ENABLE_BT = 1;

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    // for the paired UI recycler
    RecyclerView mPairedRecycler;
    // for the discovered UI recycler
    RecyclerView mDiscoveredRecycler;
    // the text for the bluetooth
    TextView mBluetoothStatusTxt;
    // bluetooth search button
    Button mSearchButton;
    // debug button
    Button mDebugButton;

    // array of discovered bluetooth devices
    Set<BluetoothDevice> mArrayDiscoveredBTDevices = new ArraySet<>();
    // array of paired bluetooth devices
    Set<BluetoothDevice> mArrayPairedBTDevices = new ArraySet<>();
    // the bluetooth connection to handle all the threads!
    BluetoothConn myBluetoothConn;

    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;

    boolean retryConnection = false;
    Handler reconnectionHandler = new Handler();

    ProgressDialog mConnectDialog;

    Runnable mReconnectionRunnable = new Runnable() {
        @Override
        public void run() {
            try {
                if (!BluetoothConn.BluetoothConnectionStatus) {
                    // start connection and pray hard
                    myBluetoothConn.startClientThread(BluetoothConn.instance.mDevice);
                    Toast.makeText(getContext(), "Reconnection Success", Toast.LENGTH_SHORT).show();
                }
                reconnectionHandler.removeCallbacks(mReconnectionRunnable);
                retryConnection = false;
            } catch (Exception e) {
                Toast.makeText(getContext(), "Failed to reconnect, trying in 5 second", Toast.LENGTH_SHORT).show();
            }
        }
    };


    public BluetoothFrag() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment bluetooth.
     */
    // TODO: Rename and change types and number of parameters
    public static BluetoothFrag newInstance(String param1, String param2) {
        BluetoothFrag fragment = new BluetoothFrag();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // fun fact: there is nothing in there for now......
        // and im not sure how to populate the arguments in there
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
        // this discover intent is to be notified when the bluetooth device is found
        IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        getContext().registerReceiver(BluetoothDeviceFound, discoverDevicesIntent);

        // this is to know that it is starting to discovered
        IntentFilter startDiscoverIntent = new IntentFilter(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
        getContext().registerReceiver(StartDiscoverBR, startDiscoverIntent);
        // this is to know that it is finished discovering
        IntentFilter finishDiscoverIntent = new IntentFilter(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
        getContext().registerReceiver(EndDiscoverBR, finishDiscoverIntent);

        IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
        getContext().registerReceiver(mBluetoothStateBR, BTIntent);

        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_BOND_STATE_CHANGED);
        getContext().registerReceiver(mBondedBR, filter);

        IntentFilter discoverIntent = new IntentFilter(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED);
        getContext().registerReceiver(mDiscoverabilityBR, discoverIntent);

        IntentFilter connectionStatusIntent = new IntentFilter(BluetoothConn.CONNECTION_STATUS);
        LocalBroadcastManager.getInstance(getContext()).registerReceiver(mDisconnBR, connectionStatusIntent);


        mConnectDialog = new ProgressDialog(getContext());
        mConnectDialog.setMessage("Waiting for other device to reconnect...");
        mConnectDialog.setCancelable(false);
        mConnectDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });
    }

    /*
    To render this page
     */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_bluetooth, container, false);
    }

    /*
    So that findViewById will work and get the UI element from fragment_bluetooth
     */
    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        // then get the recycler element
        mPairedRecycler = view.findViewById(R.id.pairedDeviceRecycler);
        mDiscoveredRecycler = view.findViewById(R.id.discoveredDeviceRecycler);
        mBluetoothStatusTxt = view.findViewById(R.id.bluetooth_txt);
        mDebugButton = view.findViewById(R.id.bluetooth_debug);

        LocationManager locationManager = (LocationManager) getContext().getSystemService(Context.LOCATION_SERVICE);
        boolean isGpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);
        if (!isGpsEnabled) {
            getContext().startActivity(new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS));
        }


        // Handling permissions.
        checkBTPermissions();

        mDebugButton.setOnClickListener(view1 -> {
            BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
            // to just open the window if bluetooth is enabled!
            if (bluetoothAdapter.isEnabled()) {
                // then open up the chat window!
                // inflate the layout of the popup window
                LayoutInflater inflater = (LayoutInflater)
                       getContext().getSystemService(LAYOUT_INFLATER_SERVICE);
                View popupView = inflater.inflate(R.layout.bluetooth_chat_popup, null);

                // create the popup window
                int width = LinearLayout.LayoutParams.WRAP_CONTENT;
                int height = LinearLayout.LayoutParams.WRAP_CONTENT;
                boolean focusable = true; // lets taps outside the popup also dismiss it
                final PopupWindow popupWindow = new ChatPopup(popupView, width, height);

                // show the popup window
                // which view you pass in doesn't matter, it is only used for the window tolken
                popupWindow.showAtLocation(view, Gravity.CENTER, 0, 0);

                // dismiss the popup window when touched
                popupView.setOnTouchListener((v, event) -> {
                    popupWindow.dismiss();
                    return true;
                });

            } else {
                Toast.makeText(getContext(), R.string.bluetooth_not_supported, Toast.LENGTH_SHORT).show();
            }
        });
        mSearchButton = view.findViewById(R.id.bluetooth_search);

        mSearchButton.setOnClickListener(view1 -> {
            checkBTPermissions();
            // bluetooth to search
            // clear the array
            BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
            if (bluetoothAdapter.isEnabled()) {
                if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
                }
                if (bluetoothAdapter.isDiscovering()) {
                    // disable discovering first!
                    bluetoothAdapter.cancelDiscovery();
                }
                else {
                    if (!bluetoothAdapter.startDiscovery()) {
                        Toast.makeText(getContext(), "Unable to start discover", Toast.LENGTH_SHORT);
                    } else {
                        mArrayDiscoveredBTDevices.clear();
                    }
                }
            }
            else
            {
                Toast.makeText(getContext(), "Please turn on Bluetooth first!", Toast.LENGTH_SHORT).show();
            }
        });

        // set up the adapter and the recyclers
        PairedRecycler pairedRecycler = new PairedRecycler(false);
        mPairedRecycler.setAdapter(pairedRecycler);
        mPairedRecycler.setLayoutManager(new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false));

        PairedRecycler discoveredRecycler = new PairedRecycler(true);
        mDiscoveredRecycler.setAdapter(discoveredRecycler);
        mDiscoveredRecycler.setLayoutManager(new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false));

        // to get the bluetooth stuff
        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        checkBTPermissions();
        // get all the discovered devices
        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();
        mArrayPairedBTDevices.clear();
        mArrayPairedBTDevices.addAll(pairedDevices);
        refreshPairedRecycler(false);

        myBluetoothConn = new BluetoothConn(getContext(), getActivity());
        changeBluetoothStatus(bluetoothAdapter.isEnabled());

        // because in order to make it work with the AMD tools,
        // have to make itself discoverable 1st
        Button discoverableButton = view.findViewById(R.id.bluetooth_discoverable);
        discoverableButton.setOnClickListener(view1 -> {
            // then open up a filter to make itself discoverable
            Intent discoverableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
            discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 600);
            startActivity(discoverableIntent);
        });
    }

    void refreshPairedRecycler(boolean isDiscovery) {
        if (isDiscovery) {
            PairedRecycler discoverAdapter = (PairedRecycler) mDiscoveredRecycler.getAdapter();
            discoverAdapter.mLocalDataSet.clear();
            discoverAdapter.mLocalDataSet.addAll(mArrayDiscoveredBTDevices);
            discoverAdapter.notifyDataSetChanged();
        } else {
            PairedRecycler theRecyclerData = (PairedRecycler) mPairedRecycler.getAdapter();
            theRecyclerData.mLocalDataSet.clear();
            theRecyclerData.mLocalDataSet.addAll(mArrayPairedBTDevices);
            theRecyclerData.notifyDataSetChanged();
        }
    }

    /*
    this only changes the bluetooth status text
     */
    void changeBluetoothStatus(boolean isOn)
    {
        mBluetoothStatusTxt.setText("Bluetooth: " + (isOn ? "ON" : "OFF"));
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        // to unregister all the listeners
        getContext().unregisterReceiver(BluetoothDeviceFound);
        getContext().unregisterReceiver(StartDiscoverBR);
        getContext().unregisterReceiver(EndDiscoverBR);
        getContext().unregisterReceiver(mBondedBR);
        getContext().unregisterReceiver(mDiscoverabilityBR);
    }

    // the most important
    @RequiresApi(api = Build.VERSION_CODES.M)
    private void checkBTPermissions() {
        if(Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP){
            int permissionCheck = getContext().checkSelfPermission("Manifest.permission.ACCESS_FINE_LOCATION");
            permissionCheck += getContext().checkSelfPermission("Manifest.permission.ACCESS_COARSE_LOCATION");
            if (permissionCheck != 0) {
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);
            }
        } else {
            Log.d(TAG, "checkBTPermissions: No need to check permissions. SDK version < LOLLIPOP.");
        }
    }


    private final BroadcastReceiver BluetoothDeviceFound = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            if(action.equals(BluetoothDevice.ACTION_FOUND)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (!mArrayPairedBTDevices.contains(device)) {
                    mArrayDiscoveredBTDevices.add(device);
                    refreshPairedRecycler(true);
                }
            }
        }
    };

    private final BroadcastReceiver StartDiscoverBR = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            mSearchButton.setText("Cancel Search!");
        }
    };

    private final BroadcastReceiver EndDiscoverBR = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            mSearchButton.setText("Search");
        }
    };

    private final BroadcastReceiver mBluetoothStateBR = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (action.equals(BluetoothAdapter.getDefaultAdapter().ACTION_STATE_CHANGED)) {
                final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR);
                switch (state) {
                    case BluetoothAdapter.STATE_OFF:
                        Log.d(TAG, "mBluetoothStateBR: STATE OFF");
                        break;
                    case BluetoothAdapter.STATE_TURNING_OFF:
                        Log.d(TAG, "mBluetoothStateBR: STATE TURNING OFF");
                        break;
                    case BluetoothAdapter.STATE_ON:
                        Log.d(TAG, "mBluetoothStateBR: STATE ON");
                        break;
                    case BluetoothAdapter.STATE_TURNING_ON:
                        Log.d(TAG, "mBluetoothStateBR: STATE TURNING ON");
                        break;
                }
            }
        }
    };

    private BroadcastReceiver mBondedBR = new BroadcastReceiver() {
        @SuppressLint("MissingPermission")
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            if(action.equals(BluetoothDevice.ACTION_BOND_STATE_CHANGED)){
                BluetoothDevice mDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if(mDevice.getBondState() == BluetoothDevice.BOND_BONDED){
                    Toast.makeText(getContext(), "Successfully paired with " + mDevice.getName(), Toast.LENGTH_SHORT).show();
                    // remove it and send it to the paired recycler
                    mArrayDiscoveredBTDevices.remove(mDevice);
                    mArrayPairedBTDevices.add(mDevice);
                    refreshPairedRecycler(false);
                    refreshPairedRecycler(true);
                }
                if(mDevice.getBondState() == BluetoothDevice.BOND_BONDING){
                    Log.d(TAG, "BOND_BONDING.");
                }
                if(mDevice.getBondState() == BluetoothDevice.BOND_NONE){
                    Log.d(TAG, "BOND_NONE.");
                }
            }
        }
    };

    // check whether it is being discovered or not
    private final BroadcastReceiver mDiscoverabilityBR = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (action.equals(BluetoothAdapter.getDefaultAdapter().ACTION_SCAN_MODE_CHANGED)) {
                final int mode = intent.getIntExtra(BluetoothAdapter.EXTRA_SCAN_MODE, BluetoothAdapter.ERROR);

                switch (mode) {
                    case BluetoothAdapter.SCAN_MODE_CONNECTABLE_DISCOVERABLE:
                        Log.d(TAG, "mBroadcastReceiver2: Discoverability Enabled.");
                        break;
                    case BluetoothAdapter.SCAN_MODE_CONNECTABLE:
                        Log.d(TAG, "mBroadcastReceiver2: Discoverability Disabled. Able to receive connections.");
                        break;
                    case BluetoothAdapter.SCAN_MODE_NONE:
                        Log.d(TAG, "mBroadcastReceiver2: Discoverability Disabled. Not able to receive connections.");
                        break;
                    case BluetoothAdapter.STATE_CONNECTING:
                        Log.d(TAG, "mBroadcastReceiver2: Connecting...");
                        break;
                    case BluetoothAdapter.STATE_CONNECTED:
                        Log.d(TAG, "mBroadcastReceiver2: Connected.");
                        break;
                }
            }
        }
    };


    private BroadcastReceiver mDisconnBR = new BroadcastReceiver() {
        @SuppressLint("MissingPermission")
        @Override
        public void onReceive(Context context, Intent intent) {
            BluetoothDevice mDevice = intent.getParcelableExtra("Device");
            String status = intent.getStringExtra("Status");
            sharedPreferences = getContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
            editor = sharedPreferences.edit();

            if(status.equals("connected")){
                try {
                    mConnectDialog.dismiss();
                } catch(NullPointerException e){
                    e.printStackTrace();
                }

                Log.d(TAG, "mDisconnBR: Device now connected to " + mDevice.getName());
                Toast.makeText(getContext(), "Device now connected to "+mDevice.getName(), Toast.LENGTH_LONG).show();
                editor.putString("connStatus", "Connected to " + mDevice.getName());
                //connStatusTextView.setText("Connected to " + mDevice.getName());
            }
            else if(status.equals("disconnected") && !retryConnection){
                Log.d(TAG, "mDisconnBR: Disconnected from "+mDevice.getName());
                Toast.makeText(getContext(), "Disconnected from "+mDevice.getName(), Toast.LENGTH_LONG).show();


                sharedPreferences = getContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
                editor = sharedPreferences.edit();
                editor.putString("connStatus", "Disconnected");
                editor.commit();

                try {
                    mConnectDialog.show();
                }catch (Exception e){
                    Log.d(TAG, "BluetoothPopUp: mBroadcastReceiver5 Dialog show failure");
                }
                retryConnection = true;
                reconnectionHandler.postDelayed(mReconnectionRunnable, 5000);
            }
            editor.commit();
        }
    };

}