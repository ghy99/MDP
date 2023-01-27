package com.example.mdp;

import android.annotation.SuppressLint;
import android.Manifest;
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
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ListView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

public class Bluetooth extends AppCompatActivity {
    private static final String TAG = "Bluetooth->Debug";
    public static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    public static BluetoothDevice myBluetoothDevice;
    public ArrayList<BluetoothDevice> myNewBTDevices;
    public ArrayList<BluetoothDevice> myPairedBTDevices;
    public DeviceListAdapter myNewDeviceListAdapter;
    public DeviceListAdapter myPairedDeviceListAdapter;
    private String connStatus;

    boolean retryConn = false;
    Button connectBtn;
    ProgressDialog myDialog;
    TextView connStatusTextView;
    ListView otherDevicesListView;
    ListView pairedDevicesListView;
    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;
    BluetoothAdapter myBluetoothAdapter;
    BluetoothService myBluetoothConnection;
    Handler reconnHandler = new Handler();
    Runnable reconnRunnable = new Runnable() {
        @Override
        public void run() {
            try {
                if (!BluetoothService.BluetoothConnectionStatus) {
                    Log.d(TAG, "Reconnecting...");
                    startBluetoothConnection(myBluetoothDevice, myUUID);
                    Toast.makeText(Bluetooth.this, "Reconnection Success", Toast.LENGTH_SHORT).show();
                }
                reconnHandler.removeCallbacks(reconnRunnable);
                retryConn = false;
            } catch (Exception e) {
                Log.d(TAG, " Reconnection failed!");
                e.printStackTrace();
                Toast.makeText(Bluetooth.this, "Failed to reconnect.", Toast.LENGTH_SHORT).show();
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bluetooth);
        Log.d(TAG, "Bluetooth created!");

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);

        // device dimensions
        int width = dm.widthPixels;
        int height = dm.heightPixels;

        myBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        Switch bluetoothSwitch = (Switch) findViewById(R.id.bluetoothSwitch);
        if (myBluetoothAdapter.isEnabled()) {
            bluetoothSwitch.setChecked(true);
            bluetoothSwitch.setText("ON");
        }

        otherDevicesListView = (ListView) findViewById(R.id.otherDevicesListView);
        pairedDevicesListView = (ListView) findViewById(R.id.pairedDevicesListView);
        myNewBTDevices = new ArrayList<>();
        myPairedBTDevices = new ArrayList<>();
        connectBtn = (Button) findViewById(R.id.connectBtn);
        Button scanButton = (Button) findViewById(R.id.scanButton);

        IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
        registerReceiver(onAndOffWatcher, BTIntent);

        IntentFilter discoverIntent = new IntentFilter(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED);
        registerReceiver(scannerModeWatcher, discoverIntent);

        IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        registerReceiver(scannerWatcher, discoverDevicesIntent);

        IntentFilter pairingIntent = new IntentFilter(BluetoothDevice.ACTION_BOND_STATE_CHANGED);
        registerReceiver(pairingWatcher, pairingIntent);

        IntentFilter connStatusIntent = new IntentFilter("ConnStatus");
        LocalBroadcastManager.getInstance(this).registerReceiver(connectionWatcher, connStatusIntent);

        scanButton.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.M)
            @Override
            public void onClick(View v) {
                toggleScanButton(v);
            }
        });

        otherDevicesListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//                if (ActivityCompat.checkSelfPermission(Bluetooth.this, android.Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
//                    // TODO: Consider calling
//                    //    ActivityCompat#requestPermissions
//                    // here to request the missing permissions, and then overriding
//                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
//                    //                                          int[] grantResults)
//                    // to handle the case where the user grants the permission. See the documentation
//                    // for ActivityCompat#requestPermissions for more details.
//                    return;
//                }
                myBluetoothAdapter.cancelDiscovery();
                String deviceName = myNewBTDevices.get(position).getName();
                String deviceAddress = myNewBTDevices.get(position).getAddress();
                Log.d(TAG, "onItemClick: A device is selected.");
                Log.d(TAG, "onItemClick - DEVICE NAME: " + deviceName);
                Log.d(TAG, "onItemClick - DEVICE ADDRESS: " + deviceAddress);

                if (Build.VERSION.SDK_INT > Build.VERSION_CODES.JELLY_BEAN_MR2) {
                    Log.d(TAG, "onItemClick - Initiating pairing with " + deviceName);
                    boolean success = myNewBTDevices.get(position).createBond();
                    myBluetoothConnection = new BluetoothService(Bluetooth.this);
                    myBluetoothDevice = myNewBTDevices.get(position);
                }
            }
        });

        pairedDevicesListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                if (ActivityCompat.checkSelfPermission(Bluetooth.this, android.Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
                    return;
                }
                myBluetoothAdapter.cancelDiscovery();
                otherDevicesListView.setAdapter(myNewDeviceListAdapter);

                String deviceName = myPairedBTDevices.get(i).getName();
                String deviceAddress = myPairedBTDevices.get(i).getAddress();
                Log.d(TAG, "onItemClick: A device is selected.");
                Log.d(TAG, "onItemClick - DEVICE NAME: " + deviceName);
                Log.d(TAG, "onItemClick - DEVICE ADDRESS: " + deviceAddress);
                BluetoothService.myBluetoothDevice = myPairedBTDevices.get(i);
                Toast.makeText(Bluetooth.this, deviceName, Toast.LENGTH_SHORT).show();
                myBluetoothConnection = new BluetoothService(Bluetooth.this);
                myBluetoothDevice = myPairedBTDevices.get(i);
            }
        });

        // on and off bluetooth switch
        bluetoothSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                Log.d(TAG, "onChecked: Switch button toggled, enabling/disabling Bluetooth...");
                if (isChecked) {
                    compoundButton.setText("ON");
                } else {
                    compoundButton.setText("OFF");
                }

                if (myBluetoothAdapter == null) {
                    Log.d(TAG, "enableDisableBT: Device does not support Bluetooth capabilities!");
                    Toast.makeText(Bluetooth.this, "Device Does Not Support Bluetooth capabilities!", Toast.LENGTH_LONG).show();
                    compoundButton.setChecked(false);
                } else {
                    if (!myBluetoothAdapter.isEnabled()) {
                        Log.d(TAG, "enableDisableBT: Enabling Bluetooth...");
                        Log.d(TAG, "enableDisableBT: Making device discoverable for 600 seconds");

                        if (ActivityCompat.checkSelfPermission(Bluetooth.this, android.Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) {
                            // TODO: Consider calling
                            //    ActivityCompat#requestPermissions
                            // here to request the missing permissions, and then overriding
                            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                            //                                          int[] grantResults)
                            // to handle the case where the user grants the permission. See the documentation
                            // for ActivityCompat#requestPermissions for more details.
                            return;
                        }
                        Intent discoverableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
                        discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 600);
                        startActivity(discoverableIntent);

                        compoundButton.setChecked(true);

                        IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
                        registerReceiver(onAndOffWatcher, BTIntent);

                        IntentFilter discoverIntent = new IntentFilter(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED);
                        registerReceiver(scannerModeWatcher, discoverIntent);
                    } else {
                        Log.d(TAG, "enableDisableBT: Disabling Bluetooth...");
                        myBluetoothAdapter.disable();

                        IntentFilter BTIntent = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
                        registerReceiver(onAndOffWatcher, BTIntent);
                    }
                }
            }
        });

        // connect button
        connectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (myBluetoothDevice == null) {
                    Toast.makeText(Bluetooth.this, "Please select a device before connecting", Toast.LENGTH_LONG).show();
                } else {
                    startBluetoothConnection(myBluetoothDevice, myUUID);
                }
            }
        });

        connStatus = "Disconnected";
        connStatusTextView = (TextView) findViewById(R.id.connStatusTextView);
        connStatusTextView.setText(connStatus);

        myDialog = new ProgressDialog(Bluetooth.this);
        myDialog.setMessage("Waiting for other device to reconnect...");
        myDialog.setCancelable(false);
        myDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });
    }

    //    @SuppressLint("MissingPermission")
    @RequiresApi(api = Build.VERSION_CODES.M)
    public void toggleScanButton(View view) {
        Log.d(TAG, "toggleButton: Scanning for unpaired devices...");

        myNewBTDevices.clear();
        if (myBluetoothAdapter != null) {
            if (!myBluetoothAdapter.isEnabled()) {
                Toast.makeText(Bluetooth.this, "Please turn on Bluetooth first!", Toast.LENGTH_SHORT).show();
            }
            if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    ActivityCompat#requestPermissions
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for ActivityCompat#requestPermissions for more details.
                return;
            }
            if (myBluetoothAdapter.isDiscovering()) {
                myBluetoothAdapter.cancelDiscovery();
                Log.d(TAG, "toggleButton: Cancelling discovery...");

                checkBTPermissions();

                myBluetoothAdapter.startDiscovery();
                IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
                registerReceiver(scannerWatcher, discoverDevicesIntent);
            } else if (!myBluetoothAdapter.isDiscovering()) {
                checkBTPermissions();

                myBluetoothAdapter.startDiscovery();
                IntentFilter discoverDevicesIntent = new IntentFilter(BluetoothDevice.ACTION_FOUND);
                registerReceiver(scannerWatcher, discoverDevicesIntent);
            }

            myPairedBTDevices.clear();
            Set<BluetoothDevice> pairedDevices = myBluetoothAdapter.getBondedDevices();
            Log.d(TAG, "toggleButton: Number of paired devices found: " + pairedDevices.size());
            for (BluetoothDevice d : pairedDevices) {
                Log.d(TAG, "Paired Devices: " + d.getName() + " : " + d.getAddress());
                myPairedBTDevices.add(d);
            }
            myPairedDeviceListAdapter = new DeviceListAdapter(this, R.layout.device_adapter_view, myPairedBTDevices);
            pairedDevicesListView.setAdapter(myPairedDeviceListAdapter);
        }
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    private void checkBTPermissions() {
        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP) {
            int permissionCheck = this.checkSelfPermission("Manifest.permission.ACCESS_FINE_LOCATION");
            permissionCheck += this.checkSelfPermission("Manifest.permission.ACCESS_COARSE_LOCATION");
            if (permissionCheck != 0) {
                this.requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);
            }
        } else {
            Log.d(TAG, "checkBTPermissions: No need to check permissions. SDK version < LOLLIPOP.");
        }
    }

    public void startBluetoothConnection(BluetoothDevice device, UUID uuid) {
        Log.d(TAG, "StartBluetoothConnection: Initializing Bluetooth Connection");
        myBluetoothConnection.startClientThread(device, uuid);
    }

    private final BroadcastReceiver onAndOffWatcher = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            Log.d(TAG, "myBroadcastReceiver1:" + this.getClass().getSimpleName());
            if (action.equals(myBluetoothAdapter.ACTION_STATE_CHANGED)) {
                final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR);

                switch (state) {
                    case BluetoothAdapter.STATE_OFF:
                        Log.d(TAG, "myBroadcastReceiver1: STATE OFF");
                        break;
                    case BluetoothAdapter.STATE_TURNING_OFF:
                        Log.d(TAG, "myBroadcastReceiver1: STATE TURNING OFF");
                        break;
                    case BluetoothAdapter.STATE_ON:
                        Log.d(TAG, "myBroadcastReceiver1: STATE ON");
                        break;
                    case BluetoothAdapter.STATE_TURNING_ON:
                        Log.d(TAG, "myBroadcastReceiver1: STATE TURNING ON");
                        break;
                }
            }
        }
    };

    // handles the scan mode
    private final BroadcastReceiver scannerModeWatcher = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            Log.d(TAG, "myBroadcastReceiver2:" + this.getClass().getSimpleName());
            if (action.equals(myBluetoothAdapter.ACTION_SCAN_MODE_CHANGED)) {
                final int mode = intent.getIntExtra(BluetoothAdapter.EXTRA_SCAN_MODE, BluetoothAdapter.ERROR);

                switch (mode) {
                    case BluetoothAdapter.SCAN_MODE_CONNECTABLE_DISCOVERABLE:
                        Log.d(TAG, "myBroadcastReceiver2: Discoverability Enabled.");
                        break;
                    case BluetoothAdapter.SCAN_MODE_CONNECTABLE:
                        Log.d(TAG, "myBroadcastReceiver2: Discoverability Disabled. Able to receive connections.");
                        break;
                    case BluetoothAdapter.SCAN_MODE_NONE:
                        Log.d(TAG, "myBroadcastReceiver2: Discoverability Disabled. Not able to receive connections.");
                        break;
                    case BluetoothAdapter.STATE_CONNECTING:
                        Log.d(TAG, "myBroadcastReceiver2: Connecting...");
                        break;
                    case BluetoothAdapter.STATE_CONNECTED:
                        Log.d(TAG, "myBroadcastReceiver2: Connected.");
                        break;
                }
            }
        }
    };

    // handles new devices discovered
    private BroadcastReceiver scannerWatcher = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            Log.d(TAG, "myBroadcastReceiver3:" + this.getClass().getSimpleName());
            if (action.equals(BluetoothDevice.ACTION_FOUND)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                myNewBTDevices.add(device);
                if (ActivityCompat.checkSelfPermission(Bluetooth.this, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
                    return;
                }
                Log.d(TAG, "onReceive: " + device.getName() + " : " + device.getAddress());
                myNewDeviceListAdapter = new DeviceListAdapter(context, R.layout.device_adapter_view, myNewBTDevices);
                otherDevicesListView.setAdapter(myNewDeviceListAdapter);
            }
        }
    };

    // handles pairing of devices
    private BroadcastReceiver pairingWatcher = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            Log.d(TAG, "myBroadcastReceiver4:" + this.getClass().getSimpleName());
            if (action.equals(BluetoothDevice.ACTION_BOND_STATE_CHANGED)) {
                BluetoothDevice myDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (ActivityCompat.checkSelfPermission(Bluetooth.this, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
                    return;
                }
                if (myDevice.getBondState() == BluetoothDevice.BOND_BONDED) {
                    Log.d(TAG, "BOND_BONDED.");
                    myPairedBTDevices.clear();
                    Set<BluetoothDevice> pairedDevices = myBluetoothAdapter.getBondedDevices();
                    for (BluetoothDevice d : pairedDevices) {
                        Log.d(TAG, "*********************************************************");
                        Log.d(TAG, "Paired Devices: " + d.getName() + " : " + d.getAddress());
                        myPairedBTDevices.add(d);
                    }
                    myPairedDeviceListAdapter = new DeviceListAdapter(Bluetooth.this, R.layout.device_adapter_view, myPairedBTDevices);
                    pairedDevicesListView.setAdapter(myPairedDeviceListAdapter);
                    Toast.makeText(Bluetooth.this, "Successfully paired with " + myDevice.getName(), Toast.LENGTH_SHORT).show();
                    myBluetoothDevice = myDevice;
                }
                if (myDevice.getBondState() == BluetoothDevice.BOND_BONDING) {
                    Log.d(TAG, "BOND_BONDING.");
                }
                if (myDevice.getBondState() == BluetoothDevice.BOND_NONE) {
                    Log.d(TAG, "BOND_NONE.");
                }
            }
        }
    };

    // handles connection status changes
    private BroadcastReceiver connectionWatcher = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            BluetoothDevice myDevice = intent.getParcelableExtra("Device");
            Log.d(TAG, "I'm in BLUETOOTH POPUP");
            String status = intent.getStringExtra("Status");
            sharedPreferences = getApplicationContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
            editor = sharedPreferences.edit();
            TextView connStatusTextView = findViewById(R.id.connStatusTextView);
            Log.d(TAG, "I'm working");
            Log.d(TAG, status);
            if (status.equals("connected")) {
                try {
                    myDialog.dismiss();
//                    Log.d(TAG, String.valueOf(bluetooth_home.myDialog));
//                    bluetooth_home.myDialog.dismiss();
                } catch (NullPointerException e) {
                    e.printStackTrace();
                }

                if (ActivityCompat.checkSelfPermission(Bluetooth.this, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
                    return;
                }
                Log.d(TAG, "myBroadcastReceiver5: Device now connected to " + myDevice.getName());
                Toast.makeText(Bluetooth.this, "Device now connected to " + myDevice.getName(), Toast.LENGTH_SHORT).show();
                editor.putString("connStatus", "Connected to " + myDevice.getName());
                connStatusTextView.setText("Connected to " + myDevice.getName());
                connStatusTextView.setTextColor(Color.parseColor("#6BDE42"));
            } else if (status.equals("disconnected") && retryConn == false){
                Log.d(TAG, "mBroadcastReceiver5: Disconnected from "+ myDevice.getName());
                Toast.makeText(Bluetooth.this, "Disconnected from " + myDevice.getName(), Toast.LENGTH_SHORT).show();
                myBluetoothConnection = new BluetoothService(Bluetooth.this);
//                mBluetoothConnection.startAcceptThread();
//                sharedPreferences = getApplicationContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
//                editor = sharedPreferences.edit();
                editor.putString("connStatus", "Disconnected");

                connStatusTextView.setText("Disconnected");
                connStatusTextView.setTextColor(Color.parseColor("#b00020"));
                editor.commit();

                try {
                    try {
                        if (myDialog != null) myDialog.show();
                    } catch (Exception e) {
                        Log.d(TAG, "Local dialog failure!");
                    }
//                    Log.d(TAG, String.valueOf(bluetooth_home.myDialog));
//                    bluetooth_home.myDialog.show();
                } catch (Exception e) {
                    Log.d(TAG, "Bluetooth: myBroadcastReceiver5 Dialog show failure!");
                }
                retryConn = true;
                reconnHandler.postDelayed(reconnRunnable, 5000);
            }
            if (status.equals("disconnected")) connStatusTextView.setText("Disconnected");
            editor.commit();
        }
    };

    @Override
    public void finish() {
        Intent data = new Intent();
        data.putExtra("myBTDevice", myBluetoothDevice);
        data.putExtra("myUUID",myUUID);
        setResult(RESULT_OK, data);
        super.finish();
    }
}
