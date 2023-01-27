package com.example.mdp;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.util.Log;
import android.widget.Toast;

import androidx.core.app.ActivityCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.UUID;

public class BluetoothService {
    private static final String TAG = "BluetoothServ->Debug";
    public static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    public static boolean BluetoothConnectionStatus = false;
    private static ConnectedThread myConnectedThread;
    public static BluetoothDevice myBluetoothDevice;
    private final BluetoothAdapter myBluetoothAdapter;
    private BluetoothDevice myDevice;
    private ConnectThread myConnectThread;
    private UUID deviceUUid;

    Context myContext;
    ProgressDialog myProgressDialog;
    Intent connStatus;

    public BluetoothService(Context context) {
        this.myBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        this.myContext = context;
    }

    private class ConnectThread extends Thread {
        private BluetoothSocket mySocket;

        public ConnectThread(BluetoothDevice device, UUID uuid) {
            myDevice = device;
            deviceUUid = uuid;
        }

        public void run() {
            BluetoothSocket tmpSocket = null;

            // create socket to initiate communication
            try {
                if (ActivityCompat.checkSelfPermission(myContext, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                    // TODO: Consider calling
                    //    ActivityCompat#requestPermissions
                    // here to request the missing permissions, and then overriding
                    //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                    //                                          int[] grantResults)
                    // to handle the case where the user grants the permission. See the documentation
                    // for ActivityCompat#requestPermissions for more details.
                    return;
                }
                tmpSocket = myDevice.createRfcommSocketToServiceRecord(deviceUUid);
            } catch (IOException e) {
                e.printStackTrace();
            }

            mySocket = tmpSocket;
            myBluetoothAdapter.cancelDiscovery();

            try {
                mySocket.connect();
                connected(mySocket);
            } catch (IOException e) {
                try {
                    mySocket.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }

                try {
                    Bluetooth myBluetoothAct = (Bluetooth) myContext;
                    myBluetoothAct.runOnUiThread(() -> Toast.makeText(myContext, "Failed to connect to the device", Toast.LENGTH_LONG).show());
                } catch (Exception z) {
                    z.printStackTrace();
                }
            }

            try {
                myProgressDialog.dismiss();
            } catch (NullPointerException e) {
                e.printStackTrace();
            }
        }

        public void cancel() {
            try {
                mySocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private class ConnectedThread extends Thread {
        private final InputStream streamIn;
        private final OutputStream streamOut;

        public ConnectedThread(BluetoothSocket socket) {
            connStatus = new Intent("ConnStatus");
            connStatus.putExtra("Status", "connected");
            connStatus.putExtra("Device", myDevice);
            LocalBroadcastManager.getInstance(myContext).sendBroadcast(connStatus);
            BluetoothConnectionStatus = true;

            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            try {
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            } catch (IOException e) {
                e.printStackTrace();
            }

            streamIn = tmpIn;
            streamOut = tmpOut;
        }

        public void run() {
            byte[] buffer = new byte[1024];
            int bytes;

            // read incoming data
            while (true) {
                try  {
                    bytes = streamIn.read(buffer);
                    String incomingMsg = new String(buffer, 0, bytes);

                    Intent incomingMsgIntent = new Intent("incomingMessage");
                    incomingMsgIntent.putExtra("receivedMessage", incomingMsg);
                    LocalBroadcastManager.getInstance(myContext).sendBroadcast(incomingMsgIntent);
                } catch (IOException e) {
                    connStatus = new Intent("ConnStatus");
                    connStatus.putExtra("Status", "disconnected");
                    connStatus.putExtra("Device", myDevice);
                    LocalBroadcastManager.getInstance(myContext).sendBroadcast(connStatus);
                    BluetoothConnectionStatus = false;
                    break;
                }
            }
        }

        public void write(byte[] bytes) {
            try {
                streamOut.write(bytes);
                Log.d(TAG, "Sending out messages...");
            } catch (IOException e) {}
        }
    }

    public void startClientThread(BluetoothDevice device, UUID uuid) {
        try {
            myBluetoothDevice = device;
            myProgressDialog = ProgressDialog.show(myContext, "Connecting Bluetooth...", "Please wait for a moment...", true);
        } catch (Exception ignored) {}

        myConnectThread = new ConnectThread(device, uuid);
        myConnectThread.start();
    }

    private void connected(BluetoothSocket socket) {
        myConnectedThread = new ConnectedThread(socket);
        myConnectedThread.start();
    }

    // wrapper function to call write method of ConnectedThread
    public static void write(byte[] out) {
        myConnectedThread.write(out);
    }
}
