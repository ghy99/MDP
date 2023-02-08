package com.example.mdp;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.SystemClock;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.Chronometer;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.animation.ObjectAnimator;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.RecyclerView;

import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class Arena extends AppCompatActivity {
    public static final String SHARED_PREFS = "sharedPrefs";
    private static final String TAG = "Arena->DEBUG";
    public static boolean firstStart = true;

    public void saveData() {
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREFS, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        editor.putFloat("obs1X", findViewById(R.id.obstacle1).getTranslationX());
        editor.putFloat("obs1Y", findViewById(R.id.obstacle1).getTranslationY());
        editor.putFloat("obs1Rotation", findViewById(R.id.obstacle1).getRotation());

        editor.putFloat("obs2X", findViewById(R.id.obstacle2).getTranslationX());
        editor.putFloat("obs2Y", findViewById(R.id.obstacle2).getTranslationY());
        editor.putFloat("obs2Rotation", findViewById(R.id.obstacle2).getRotation());

        editor.putFloat("obs3X", findViewById(R.id.obstacle3).getTranslationX());
        editor.putFloat("obs3Y", findViewById(R.id.obstacle3).getTranslationY());
        editor.putFloat("obs3Rotation", findViewById(R.id.obstacle3).getRotation());

        editor.putFloat("obs4X", findViewById(R.id.obstacle4).getTranslationX());
        editor.putFloat("obs4Y", findViewById(R.id.obstacle4).getTranslationY());
        editor.putFloat("obs4Rotation", findViewById(R.id.obstacle4).getRotation());

        editor.putFloat("obs5X", findViewById(R.id.obstacle5).getTranslationX());
        editor.putFloat("obs5Y", findViewById(R.id.obstacle5).getTranslationY());
        editor.putFloat("obs5Rotation", findViewById(R.id.obstacle5).getRotation());

        editor.putFloat("obs6X", findViewById(R.id.obstacle6).getTranslationX());
        editor.putFloat("obs6Y", findViewById(R.id.obstacle6).getTranslationY());
        editor.putFloat("obs6Rotation", findViewById(R.id.obstacle6).getRotation());

        editor.putFloat("obs7X", findViewById(R.id.obstacle7).getTranslationX());
        editor.putFloat("obs7Y", findViewById(R.id.obstacle7).getTranslationY());
        editor.putFloat("obs7Rotation", findViewById(R.id.obstacle7).getRotation());

        editor.putFloat("obs8X", findViewById(R.id.obstacle8).getTranslationX());
        editor.putFloat("obs8Y", findViewById(R.id.obstacle8).getTranslationY());
        editor.putFloat("obs8Rotation", findViewById(R.id.obstacle8).getRotation());

        editor.putFloat("carX", findViewById(R.id.car).getTranslationX());
        editor.putFloat("carY", findViewById(R.id.car).getTranslationY());
        editor.putFloat("carRotation", findViewById(R.id.car).getRotation());

        int x = (int) (car.getX() + SNAP_GRID_INTERVAL) / SNAP_GRID_INTERVAL;
        int y = (int) (car.getY() + SNAP_GRID_INTERVAL) / SNAP_GRID_INTERVAL;

        editor.putString("x_tv", String.valueOf(car_x.getText()));
        editor.putString("y_tv", String.valueOf(car_y.getText()));
        editor.putString("car_dir", String.valueOf(car_dir.getText()));
        editor.apply();
    }

    public void loadData() {
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREFS, MODE_PRIVATE);
        obstacle1.setX(sharedPreferences.getFloat("obs1X", 0.0f));
        obstacle1.setY(sharedPreferences.getFloat("obs1Y", 0.0f));
        obstacle1.setRotation((sharedPreferences.getFloat("obs1Rotation", 0.0f)));

        obstacle2.setX(sharedPreferences.getFloat("obs2X", 0.0f));
        obstacle2.setY(sharedPreferences.getFloat("obs2Y", 0.0f));
        obstacle2.setRotation((sharedPreferences.getFloat("obs2Rotation", 0.0f)));

        obstacle3.setX(sharedPreferences.getFloat("obs3X", 0.0f));
        obstacle3.setY(sharedPreferences.getFloat("obs3Y", 0.0f));
        obstacle3.setRotation((sharedPreferences.getFloat("obs3Rotation", 0.0f)));

        obstacle4.setX(sharedPreferences.getFloat("obs4X", 0.0f));
        obstacle4.setY(sharedPreferences.getFloat("obs4Y", 0.0f));
        obstacle4.setRotation((sharedPreferences.getFloat("obs4Rotation", 0.0f)));

        obstacle5.setX(sharedPreferences.getFloat("obs5X", 0.0f));
        obstacle5.setY(sharedPreferences.getFloat("obs5Y", 0.0f));
        obstacle5.setRotation((sharedPreferences.getFloat("obs5Rotation", 0.0f)));

        obstacle6.setX(sharedPreferences.getFloat("obs6X", 0.0f));
        obstacle6.setY(sharedPreferences.getFloat("obs6Y", 0.0f));
        obstacle6.setRotation((sharedPreferences.getFloat("obs6Rotation", 0.0f)));

        obstacle7.setX(sharedPreferences.getFloat("obs7X", 0.0f));
        obstacle7.setY(sharedPreferences.getFloat("obs7Y", 0.0f));
        obstacle7.setRotation((sharedPreferences.getFloat("obs7Rotation", 0.0f)));

        obstacle8.setX(sharedPreferences.getFloat("obs8X", 0.0f));
        obstacle8.setY(sharedPreferences.getFloat("obs8Y", 0.0f));
        obstacle8.setRotation((sharedPreferences.getFloat("obs8Rotation", 0.0f)));

        car.setX(sharedPreferences.getFloat("carX", 0.0f));
        car.setY(sharedPreferences.getFloat("carY", 0.0f));
        car.setRotation(sharedPreferences.getFloat("carRotation", 0.0f));

        car_x.setText((sharedPreferences.getString("x_tv", "")));
        car_y.setText((sharedPreferences.getString("y_tv", "")));
        car_dir.setText((sharedPreferences.getString("car_dir", "")));
        Log.d(TAG, "obs1X: " + Float.toString(sharedPreferences.getFloat("obs1X", 0.0f)));
    }

    private static final int SNAP_GRID_INTERVAL = 35;
    private static final int ANIMATOR_DURATION = 1000;

    /*
     * start from (1,1)
     * NOTE: remember to invert y
     */
    private final int INITIAL_X = 1 * SNAP_GRID_INTERVAL - SNAP_GRID_INTERVAL;
    private final int INITIAL_Y = 18 * SNAP_GRID_INTERVAL - SNAP_GRID_INTERVAL;

    private boolean canSetObstacles = false;
    private String curMode = "IDLE";

    Button IRButton, SPButton, resetButton, preset1Button, setButton, timerButton, saveButton;
    ImageView obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6, obstacle7, obstacle8, car;
    TextView statusWindow, car_x, car_y, car_dir;

    Map<Integer, ImageView> obstacles;

    // RecyclerView
    ArrayList<String> s1 = new ArrayList<String>();
    ArrayList<Integer> images = new ArrayList<Integer>();
    RecyclerView recyclerView;

    protected void onPause() {
        super.onPause();
        Log.d("onpause", "OnPause() called");
        saveData();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // Restore saved instance state
        super.onCreate(savedInstanceState);
        Log.d(TAG, "onCreate called");

        setContentView(R.layout.arena);

        // start listening for incoming messages
        LocalBroadcastManager.getInstance(this).registerReceiver(myReceiver, new IntentFilter("incomingMessage"));

        initObstacles();
        initButtons();
        initMovementButtons();

        if (!firstStart) {
            loadData();
        } else {
            firstStart = false;
            saveData();
        }
    }

    /**
     * Initializes obstacles and setup listeners
     */
    private void initObstacles() {
        obstacle1 = findViewById(R.id.obstacle1);
        obstacle2 = findViewById(R.id.obstacle2);
        obstacle3 = findViewById(R.id.obstacle3);
        obstacle4 = findViewById(R.id.obstacle4);
        obstacle5 = findViewById(R.id.obstacle5);
        obstacle6 = findViewById(R.id.obstacle6);
        obstacle7 = findViewById(R.id.obstacle7);
        obstacle8 = findViewById(R.id.obstacle8);

        obstacles = new HashMap<Integer, ImageView>() {
            {
                put(1, obstacle1);
                put(2, obstacle2);
                put(3, obstacle3);
                put(4, obstacle4);
                put(5, obstacle5);
                put(6, obstacle6);
                put(7, obstacle7);
                put(8, obstacle8);
            }
        };

        obstacle1.setOnClickListener(view -> {
            obstacle1.setRotation((obstacle1.getRotation() + 90) % 360);
            int orientation = (int) obstacle1.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle1.setImageResource(Helper.resources.get("o1n"));
                    break;
                case 1:
                    obstacle1.setImageResource(Helper.resources.get("o1e"));
                    break;
                case 2:
                    obstacle1.setImageResource(Helper.resources.get("o1s"));
                    break;
                case 3:
                    obstacle1.setImageResource(Helper.resources.get("o1w"));
                    break;
            }
        });

        obstacle2.setOnClickListener(view -> {
            obstacle2.setRotation((obstacle2.getRotation() + 90) % 360);
            int orientation = (int) obstacle2.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle2.setImageResource(Helper.resources.get("o2n"));
                    break;
                case 1:
                    obstacle2.setImageResource(Helper.resources.get("o2e"));
                    break;
                case 2:
                    obstacle2.setImageResource(Helper.resources.get("o2s"));
                    break;
                case 3:
                    obstacle2.setImageResource(Helper.resources.get("o2w"));
                    break;
            }
        });

        obstacle3.setOnClickListener(view -> {
            obstacle3.setRotation((obstacle3.getRotation() + 90) % 360);
            int orientation = (int) obstacle3.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle3.setImageResource(Helper.resources.get("o3n"));
                    break;
                case 1:
                    obstacle3.setImageResource(Helper.resources.get("o3e"));
                    break;
                case 2:
                    obstacle3.setImageResource(Helper.resources.get("o3s"));
                    break;
                case 3:
                    obstacle3.setImageResource(Helper.resources.get("o3w"));
                    break;
            }
        });

        obstacle4.setOnClickListener(view -> {
            obstacle4.setRotation((obstacle4.getRotation() + 90) % 360);
            int orientation = (int) obstacle4.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle4.setImageResource(Helper.resources.get("o4n"));
                    break;
                case 1:
                    obstacle4.setImageResource(Helper.resources.get("o4e"));
                    break;
                case 2:
                    obstacle4.setImageResource(Helper.resources.get("o4s"));
                    break;
                case 3:
                    obstacle4.setImageResource(Helper.resources.get("o4w"));
                    break;
            }
        });

        obstacle5.setOnClickListener(view -> {
            obstacle5.setRotation((obstacle5.getRotation() + 90) % 360);
            int orientation = (int) obstacle5.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle5.setImageResource(Helper.resources.get("o5n"));
                    break;
                case 1:
                    obstacle5.setImageResource(Helper.resources.get("o5e"));
                    break;
                case 2:
                    obstacle5.setImageResource(Helper.resources.get("o5s"));
                    break;
                case 3:
                    obstacle5.setImageResource(Helper.resources.get("o5w"));
                    break;
            }
        });

        obstacle6.setOnClickListener(view -> {
            obstacle6.setRotation((obstacle6.getRotation() + 90) % 360);
            int orientation = (int) obstacle6.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle6.setImageResource(Helper.resources.get("o6n"));
                    break;
                case 1:
                    obstacle6.setImageResource(Helper.resources.get("o6e"));
                    break;
                case 2:
                    obstacle6.setImageResource(Helper.resources.get("o6s"));
                    break;
                case 3:
                    obstacle6.setImageResource(Helper.resources.get("o6w"));
                    break;
            }
        });

        obstacle7.setOnClickListener(view -> {
            obstacle7.setRotation((obstacle7.getRotation() + 90) % 360);
            int orientation = (int) obstacle7.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle7.setImageResource(Helper.resources.get("o7n"));
                    break;
                case 1:
                    obstacle7.setImageResource(Helper.resources.get("o7e"));
                    break;
                case 2:
                    obstacle7.setImageResource(Helper.resources.get("o7s"));
                    break;
                case 3:
                    obstacle7.setImageResource(Helper.resources.get("o7w"));
                    break;
            }
        });

        obstacle8.setOnClickListener(view -> {
            obstacle8.setRotation((obstacle8.getRotation() + 90) % 360);
            int orientation = (int) obstacle8.getRotation();
            switch (((orientation / 90) % 4 + 4) % 4) {
                case 0:
                    obstacle8.setImageResource(Helper.resources.get("o8n"));
                    break;
                case 1:
                    obstacle8.setImageResource(Helper.resources.get("o8e"));
                    break;
                case 2:
                    obstacle8.setImageResource(Helper.resources.get("o8s"));
                    break;
                case 3:
                    obstacle8.setImageResource(Helper.resources.get("o8w"));
                    break;
            }
        });

        obstacle1.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle1.setX(obstacle1.getX() + dx);
                        obstacle1.setY(obstacle1.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle1.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle1.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle1 is at " + snapToX + "," + snapToY);
                        obstacle1.setX(snapToX);
                        obstacle1.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle2.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle2.setX(obstacle2.getX() + dx);
                        obstacle2.setY(obstacle2.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle2.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle2.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle2 is at " + snapToX + "," + snapToY);
                        obstacle2.setX(snapToX);
                        obstacle2.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle3.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle3.setX(obstacle3.getX() + dx);
                        obstacle3.setY(obstacle3.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle3.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle3.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle3 is at " + snapToX + "," + snapToY);
                        obstacle3.setX(snapToX);
                        obstacle3.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle4.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle4.setX(obstacle4.getX() + dx);
                        obstacle4.setY(obstacle4.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle4.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle4.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle4 is at " + snapToX + "," + snapToY);
                        obstacle4.setX(snapToX);
                        obstacle4.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle5.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle5.setX(obstacle5.getX() + dx);
                        obstacle5.setY(obstacle5.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle5.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle5.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle5 is at " + snapToX + "," + snapToY);
                        obstacle5.setX(snapToX);
                        obstacle5.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle6.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle6.setX(obstacle6.getX() + dx);
                        obstacle6.setY(obstacle6.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle6.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle6.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle6 is at " + snapToX + "," + snapToY);
                        obstacle6.setX(snapToX);
                        obstacle6.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle7.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle7.setX(obstacle7.getX() + dx);
                        obstacle7.setY(obstacle7.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle7.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle7.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle7 is at " + snapToX + "," + snapToY);
                        obstacle7.setX(snapToX);
                        obstacle7.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });

        obstacle8.setOnTouchListener(new View.OnTouchListener() {
            int x = 0;
            int y = 0;
            int dx = 0;
            int dy = 0;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (!canSetObstacles) {
                    return false;
                }
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        x = (int) event.getX();
                        y = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        dx = (int) event.getX() - x;
                        dy = (int) event.getY() - y;

                        obstacle8.setX(obstacle8.getX() + dx);
                        obstacle8.setY(obstacle8.getY() + dy);
                        break;
                    case MotionEvent.ACTION_UP:
                        int snapToX = ((int) ((obstacle8.getX() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        int snapToY = ((int) ((obstacle8.getY() + SNAP_GRID_INTERVAL / 2) / SNAP_GRID_INTERVAL))
                                * SNAP_GRID_INTERVAL;
                        Log.d(TAG, "obstacle8 is at " + snapToX + "," + snapToY);
                        obstacle8.setX(snapToX);
                        obstacle8.setY(snapToY);
                        break;
                    default:
                        break;
                }
                return true;
            }
        });
    }

    /*
     * Set obstacle ID images
     */
    private void setObstacleImage(int obstacleNumber, String image) {
        int orientation = (int) obstacles.get(obstacleNumber).getRotation();

        if (orientation == 0) {
            obstacles.get(obstacleNumber).setImageResource(Helper.resources.get(image + "n"));
        } else if (orientation == 90) {
            obstacles.get(obstacleNumber).setImageResource(Helper.resources.get(image + "e"));
        } else if (orientation == 180) {
            obstacles.get(obstacleNumber).setImageResource(Helper.resources.get(image + "s"));
        } else if (orientation == 270) {
            obstacles.get(obstacleNumber).setImageResource(Helper.resources.get(image + "w"));
        } else {
            obstacles.get(obstacleNumber).setImageResource(Helper.resources.get(image));
            obstacles.get(obstacleNumber).setRotation(0);
        }
    }

    /*
     * Initializes the arrow buttons
     */
    private void initMovementButtons() {
        ImageButton forwardButton = (ImageButton) findViewById(R.id.forwardButton);
        forwardButton.setOnClickListener(v -> {
            Log.d(TAG, "forward");

            // Bluetooth message
            // TODO: Check why w
            if (BluetoothService.BluetoothConnectionStatus) {
                byte[] bytes = "STM:w100n".getBytes(Charset.defaultCharset());
                BluetoothService.write(bytes);
            }

            // Animation
            forwardButtonCommand();
        });

        ImageButton reverseButton = (ImageButton) findViewById(R.id.reverseButton);
        reverseButton.setOnClickListener(v -> {
            Log.d(TAG, "reverse");

            // Bluetooth message
            if (BluetoothService.BluetoothConnectionStatus) {
                byte[] bytes = "STM:s100n".getBytes(Charset.defaultCharset());
                BluetoothService.write(bytes);
            }

            // Animation
            reverseButtonCommand();
        });

        ImageButton leftButton = (ImageButton) findViewById(R.id.leftButton);
        leftButton.setOnClickListener(v -> {
            Log.d(TAG, "left");
            if (BluetoothService.BluetoothConnectionStatus) {
                byte[] bytes = "STM:ln".getBytes(Charset.defaultCharset());
                BluetoothService.write(bytes);
            }

            leftButtonCommand();
        });

        ImageButton rightButton = (ImageButton) findViewById(R.id.rightButton);
        rightButton.setOnClickListener(v -> {
            Log.d(TAG, "right");
            if (BluetoothService.BluetoothConnectionStatus) {
                byte[] bytes = "STM:rn".getBytes(Charset.defaultCharset());
                BluetoothService.write(bytes);
            }

            rightButtonCommand();
        });
    }

    /**
     * Initalizes buttons, car and setup listeners
     */
    private void initButtons() {
        // Declarations
        car = findViewById(R.id.car);
        car_x = findViewById(R.id.x_tv);
        car_y = findViewById(R.id.y_tv);
        car_dir = findViewById(R.id.dir_tv);
        IRButton = findViewById(R.id.IRButton);
        SPButton = findViewById(R.id.SPBtn);
        resetButton = findViewById(R.id.resetButton);
        preset1Button = findViewById(R.id.preset1Button);
        setButton = findViewById(R.id.setButton);
        saveButton = findViewById(R.id.saveButton);
        timerButton = findViewById(R.id.timerButton);
        statusWindow = findViewById(R.id.statusWindowText);

        // Events
        IRButton.setOnClickListener(view -> sendObstaclesEvent());
        SPButton.setOnClickListener(view -> beginSPTask());
        resetButton.setOnClickListener(view -> setResetButton());
        preset1Button.setOnClickListener(view -> setPreset1Button());
        setButton.setOnClickListener(view -> toggleSetMode());
        saveButton.setOnClickListener(view -> setSaveButton());
        timerButton.setOnClickListener(view -> stopTimerButton());

        // Initialize car to bottom left
        car.setX(INITIAL_X);
        car.setY(INITIAL_Y);
        updateXYDirText();
    }

    /*
     * Function to wait for certain amount of time
     */
    private void sleepFor(int time) {
        try {
            TimeUnit.MILLISECONDS.sleep(time);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void forwardButtonCommand() {
        int orientation = (int) car.getRotation();
        int new_x, new_y;
        ObjectAnimator animator;
        switch (((orientation / 90) % 4 + 4) % 4) {
            case 0: // North
                new_y = (int) car.getY() - SNAP_GRID_INTERVAL;
                car.setY(new_y);
                animator = ObjectAnimator.ofFloat(car, "y", new_y);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            case 1:
                new_x = (int) car.getX() + SNAP_GRID_INTERVAL;
                car.setX(new_x);
                animator = ObjectAnimator.ofFloat(car, "x", new_x);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            case 2:
                new_y = (int) car.getY() + SNAP_GRID_INTERVAL;
                car.setY(new_y);
                animator = ObjectAnimator.ofFloat(car, "y", new_y);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            case 3:
                new_x = (int) car.getX() - SNAP_GRID_INTERVAL;
                car.setX(new_x);
                animator = ObjectAnimator.ofFloat(car, "x", new_x);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            default:
                // Shouldn't reach this case
                break;
        }
    }

    private void reverseButtonCommand() {
        int orientation = (int) car.getRotation();
        int new_x, new_y;
        ObjectAnimator animator;
        switch (((orientation / 90) % 4 + 4) % 4) {
            case 0:
                new_y = (int) car.getY() + SNAP_GRID_INTERVAL;
                car.setY(new_y);
                animator = ObjectAnimator.ofFloat(car, "y", new_y);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            case 1:
                new_x = (int) car.getX() - SNAP_GRID_INTERVAL;
                car.setX(new_x);
                animator = ObjectAnimator.ofFloat(car, "x", new_x);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            case 2:
                new_y = (int) car.getY() - SNAP_GRID_INTERVAL;
                car.setY(new_y);
                animator = ObjectAnimator.ofFloat(car, "y", new_y);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            case 3:
                new_x = (int) car.getX() + SNAP_GRID_INTERVAL;
                car.setX(new_x);
                animator = ObjectAnimator.ofFloat(car, "x", new_x);
                animator.setDuration(ANIMATOR_DURATION);
                animator.start();
                updateXYDirText();
                break;
            default:
                // Shouldn't reach this case
                break;
        }
    }

    public void leftButtonCommand() {
        int orientation = (int) car.getRotation();
        switch (((orientation / 90) % 4 + 4) % 4) {
            case 0:
                car.setRotation(270);
                break;
            case 1:
                car.setRotation(0);
                break;
            case 2:
                car.setRotation(90);
                break;
            case 3:
                car.setRotation(180);
                break;
            default:
                // Shouldn't reach this case
                break;
        }

        updateXYDirText();
    }

    private void rightButtonCommand() {
        int orientation = (int) car.getRotation();
        switch (((orientation / 90) % 4 + 4) % 4) {
            case 0:
                car.setRotation(90);
                break;
            case 1:
                car.setRotation(180);
                break;
            case 2:
                car.setRotation(270);
                break;
            case 3:
                car.setRotation(0);
                break;
            default:
                // Shouldn't reach this case
                break;
        }

        updateXYDirText();
    }

    private void stopTimerButton() {
        Chronometer IRTimer = (Chronometer) findViewById(R.id.IRTimer);
        IRTimer.stop();
        updateStatusWindow("Ready");
    }

    private void sendObstaclesEvent() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder
                .append("ALG:")
                .append(getObstacleString(obstacle1) + "0;")
                .append(getObstacleString(obstacle2) + "1;")
                .append(getObstacleString(obstacle3) + "2;")
                .append(getObstacleString(obstacle4) + "3;")
                .append(getObstacleString(obstacle5) + "4;")
                .append(getObstacleString(obstacle6) + "5;")
                .append(getObstacleString(obstacle7) + "6;")
                .append(getObstacleString(obstacle8) + "7;");
        String IRstart = "ALG:START";

        if (BluetoothService.BluetoothConnectionStatus) {
            // Toast.makeText(this, stringBuilder.toString(), Toast.LENGTH_LONG).show();
            byte[] bytes = IRstart.getBytes(Charset.defaultCharset());
            BluetoothService.write(bytes);
            Toast.makeText(Arena.this, "Obstacles sent", Toast.LENGTH_LONG).show();
            updateStatusWindow("IR Started");
        } else {
            Toast.makeText(Arena.this, "Please connect to Bluetooth.", Toast.LENGTH_LONG).show();
        }

        Chronometer IRTimer = (Chronometer) findViewById(R.id.IRTimer);
        long elapsedRealtime = SystemClock.elapsedRealtime();
        IRTimer.setBase(elapsedRealtime);
        IRTimer.start();
    }

    private void beginSPTask() {
        if (BluetoothService.BluetoothConnectionStatus) {
            byte[] bytes = "STM:sp".getBytes(Charset.defaultCharset());
            BluetoothService.write(bytes);
            Toast.makeText(Arena.this, "Shortest Path Started.", Toast.LENGTH_LONG).show();
            updateStatusWindow("SP Started");
        } else {
            Toast.makeText(Arena.this, "Please connect to Bluetooth.", Toast.LENGTH_LONG).show();
        }
        Chronometer IRTimer = (Chronometer) findViewById(R.id.IRTimer);
        long elapsedRealtime = SystemClock.elapsedRealtime();
        IRTimer.setBase(elapsedRealtime);
        IRTimer.start();
    }

    private void setResetButton() {
        // Reset Timer
        Chronometer IRTimer = (Chronometer) findViewById(R.id.IRTimer);
        IRTimer.setBase(SystemClock.elapsedRealtime());
        IRTimer.stop();
        updateStatusWindow("Ready");

        // Hard coded
        obstacle1.setTranslationX(0);
        obstacle1.setTranslationY(0);

        obstacle2.setTranslationX(0);
        obstacle2.setTranslationY(0);

        obstacle3.setTranslationX(0);
        obstacle3.setTranslationY(0);

        obstacle4.setTranslationX(0);
        obstacle4.setTranslationY(0);

        obstacle5.setTranslationX(0);
        obstacle5.setTranslationY(0);

        obstacle6.setTranslationX(0);
        obstacle6.setTranslationY(0);

        obstacle7.setTranslationX(0);
        obstacle7.setTranslationY(0);

        obstacle8.setTranslationX(0);
        obstacle8.setTranslationY(0);

        car.setX(INITIAL_X);
        car.setY(INITIAL_Y);
        car.setRotation(0);
        updateXYDirText();

        obstacle1.setImageResource(Helper.resources.get("o1n"));
        obstacle1.setTag(Helper.resources.get("o1n"));
        obstacle2.setImageResource(Helper.resources.get("o2n"));
        obstacle2.setTag(Helper.resources.get("o2n"));
        obstacle3.setImageResource(Helper.resources.get("o3n"));
        obstacle3.setTag(Helper.resources.get("o3n"));
        obstacle4.setImageResource(Helper.resources.get("o4n"));
        obstacle4.setTag(Helper.resources.get("o4n"));
        obstacle5.setImageResource(Helper.resources.get("o5n"));
        obstacle5.setTag(Helper.resources.get("o5n"));
        obstacle6.setImageResource(Helper.resources.get("o6n"));
        obstacle6.setTag(Helper.resources.get("o6n"));
        obstacle7.setImageResource(Helper.resources.get("o7n"));
        obstacle7.setTag(Helper.resources.get("o7n"));
        obstacle8.setImageResource(Helper.resources.get("o8n"));
        obstacle1.setTag(Helper.resources.get("o8n"));

        obstacle1.setRotation(0);
        obstacle2.setRotation(0);
        obstacle3.setRotation(0);
        obstacle4.setRotation(0);
        obstacle5.setRotation(0);
        obstacle6.setRotation(0);
        obstacle7.setRotation(0);
        obstacle8.setRotation(0);

        Toast.makeText(this, "Map Reset", Toast.LENGTH_LONG).show();
    }

    private void setPreset1Button() {
        updateStatusWindow("Ready");

        obstacle1.setX(350);
        obstacle1.setY(70);
        obstacle1.setRotation(180);
        obstacle1.setImageResource(Helper.resources.get("o1s"));

        obstacle2.setX(595);
        obstacle2.setY(70);
        obstacle2.setRotation(270);
        obstacle2.setImageResource(Helper.resources.get("o2w"));

        obstacle3.setX(70);
        obstacle3.setY(105);
        obstacle3.setRotation(180);
        obstacle3.setImageResource(Helper.resources.get("o3s"));

        obstacle4.setX(560);
        obstacle4.setY(525);
        obstacle4.setRotation(180);
        obstacle4.setImageResource(Helper.resources.get("o4s"));

        obstacle5.setX(455);
        obstacle5.setY(630);
        obstacle5.setRotation(270);
        obstacle5.setImageResource(Helper.resources.get("o5w"));

        obstacle6.setX(210);
        obstacle6.setY(455);
        obstacle6.setRotation(0);
        obstacle6.setImageResource(Helper.resources.get("o6n"));

        obstacle7.setX(315);
        obstacle7.setY(280);
        obstacle7.setRotation(270);
        obstacle7.setImageResource(Helper.resources.get("o7w"));

        obstacle8.setX(105);
        obstacle8.setY(560);
        obstacle8.setRotation(90);
        obstacle8.setImageResource(Helper.resources.get("o8e"));

        Toast.makeText(Arena.this, "Preset 1 Applied", Toast.LENGTH_SHORT).show();
    }

    public String[][] savedPreset = {};

    private void setPreset2Button() {
        if (savedPreset.length == 0) {
            Toast.makeText(this, "No saved preset found", Toast.LENGTH_SHORT).show();
        } else {
            String[] obstacle1data = savedPreset[0];
            obstacle1.setX(Integer.parseInt(obstacle1data[0]));
            obstacle1.setY(Integer.parseInt(obstacle1data[1]));
            Log.d(TAG, "obstacle1 should be at " + obstacle1data[0] + "," + obstacle1data[1]);
            switch (obstacle1data[2]) {
                case ("N"):
                    obstacle1.setRotation(0);
                    obstacle1.setImageResource(Helper.resources.get("o1n"));
                    break;
                case ("E"):
                    obstacle1.setRotation(90);
                    obstacle1.setImageResource(Helper.resources.get("o1e"));
                    break;
                case ("S"):
                    obstacle1.setRotation(180);
                    obstacle1.setImageResource(Helper.resources.get("o1s"));
                    break;
                case ("W"):
                    obstacle1.setRotation(270);
                    obstacle1.setImageResource(Helper.resources.get("o1w"));
                    break;
                default:
                    break;
            }
            String[] obstacle2data = savedPreset[1];
            obstacle2.setX(Integer.parseInt(obstacle2data[0]));
            obstacle2.setY(Integer.parseInt(obstacle2data[1]));
            Log.d(TAG, "obstacle2 should be at " + obstacle2data[0] + "," + obstacle2data[1]);
            switch (obstacle2data[2]) {
                case ("N"):
                    obstacle2.setRotation(0);
                    obstacle2.setImageResource(Helper.resources.get("o2n"));
                    break;
                case ("E"):
                    obstacle2.setRotation(90);
                    obstacle2.setImageResource(Helper.resources.get("o2e"));
                    break;
                case ("S"):
                    obstacle2.setRotation(180);
                    obstacle2.setImageResource(Helper.resources.get("o2s"));
                    break;
                case ("W"):
                    obstacle2.setRotation(270);
                    obstacle2.setImageResource(Helper.resources.get("o2w"));
                    break;
                default:
                    break;
            }
            String[] obstacle3data = savedPreset[2];
            obstacle3.setX(Integer.parseInt(obstacle3data[0]));
            obstacle3.setY(Integer.parseInt(obstacle3data[1]));
            Log.d(TAG, "obstacle3 should be at " + obstacle3data[0] + "," + obstacle3data[1]);
            switch (obstacle3data[2]) {
                case ("N"):
                    obstacle3.setRotation(0);
                    obstacle3.setImageResource(Helper.resources.get("o3n"));
                    break;
                case ("E"):
                    obstacle3.setRotation(90);
                    obstacle3.setImageResource(Helper.resources.get("o3e"));
                    break;
                case ("S"):
                    obstacle3.setRotation(180);
                    obstacle3.setImageResource(Helper.resources.get("o3s"));
                    break;
                case ("W"):
                    obstacle3.setRotation(270);
                    obstacle3.setImageResource(Helper.resources.get("o3w"));
                    break;
                default:
                    break;
            }
            String[] obstacle4data = savedPreset[3];
            obstacle4.setX(Integer.parseInt(obstacle4data[0]));
            obstacle4.setY(Integer.parseInt(obstacle4data[1]));
            Log.d(TAG, "obstacle4 should be at " + obstacle4data[0] + "," + obstacle4data[1]);
            switch (obstacle4data[2]) {
                case ("N"):
                    obstacle4.setRotation(0);
                    obstacle4.setImageResource(Helper.resources.get("o4n"));
                    break;
                case ("E"):
                    obstacle4.setRotation(90);
                    obstacle4.setImageResource(Helper.resources.get("o4e"));
                    break;
                case ("S"):
                    obstacle4.setRotation(180);
                    obstacle4.setImageResource(Helper.resources.get("o4s"));
                    break;
                case ("W"):
                    obstacle4.setRotation(270);
                    obstacle4.setImageResource(Helper.resources.get("o4w"));
                    break;
                default:
                    break;
            }
            String[] obstacle5data = savedPreset[4];
            obstacle5.setX(Integer.parseInt(obstacle5data[0]));
            obstacle5.setY(Integer.parseInt(obstacle5data[1]));
            Log.d(TAG, "obstacle5 should be at " + obstacle5data[0] + "," + obstacle5data[1]);
            switch (obstacle5data[2]) {
                case ("N"):
                    obstacle5.setRotation(0);
                    obstacle5.setImageResource(Helper.resources.get("o5n"));
                    break;
                case ("E"):
                    obstacle5.setRotation(90);
                    obstacle5.setImageResource(Helper.resources.get("o5e"));
                    break;
                case ("S"):
                    obstacle5.setRotation(180);
                    obstacle5.setImageResource(Helper.resources.get("o5s"));
                    break;
                case ("W"):
                    obstacle5.setRotation(270);
                    obstacle5.setImageResource(Helper.resources.get("o5w"));
                    break;
                default:
                    break;
            }
            String[] obstacle6data = savedPreset[5];
            obstacle6.setX(Integer.parseInt(obstacle6data[0]));
            obstacle6.setY(Integer.parseInt(obstacle6data[1]));
            Log.d(TAG, "obstacle6 should be at " + obstacle6data[0] + "," + obstacle6data[1]);
            switch (obstacle6data[2]) {
                case ("N"):
                    obstacle6.setRotation(0);
                    obstacle6.setImageResource(Helper.resources.get("o6n"));
                    break;
                case ("E"):
                    obstacle6.setRotation(90);
                    obstacle6.setImageResource(Helper.resources.get("o6e"));
                    break;
                case ("S"):
                    obstacle6.setRotation(180);
                    obstacle6.setImageResource(Helper.resources.get("o6s"));
                    break;
                case ("W"):
                    obstacle6.setRotation(270);
                    obstacle6.setImageResource(Helper.resources.get("o6w"));
                    break;
                default:
                    break;
            }
            String[] obstacle7data = savedPreset[6];
            obstacle7.setX(Integer.parseInt(obstacle7data[0]));
            obstacle7.setY(Integer.parseInt(obstacle7data[1]));
            Log.d(TAG, "obstacle7 should be at " + obstacle7data[0] + "," + obstacle7data[1]);
            switch (obstacle7data[2]) {
                case ("N"):
                    obstacle7.setRotation(0);
                    obstacle7.setImageResource(Helper.resources.get("o7n"));
                    break;
                case ("E"):
                    obstacle7.setRotation(90);
                    obstacle7.setImageResource(Helper.resources.get("o7e"));
                    break;
                case ("S"):
                    obstacle7.setRotation(180);
                    obstacle7.setImageResource(Helper.resources.get("o7s"));
                    break;
                case ("W"):
                    obstacle7.setRotation(270);
                    obstacle7.setImageResource(Helper.resources.get("o7w"));
                    break;
                default:
                    break;
            }
            String[] obstacle8data = savedPreset[7];
            obstacle8.setX(Integer.parseInt(obstacle8data[0]));
            obstacle8.setY(Integer.parseInt(obstacle8data[1]));
            Log.d(TAG, "obstacle8 should be at " + obstacle8data[0] + "," + obstacle8data[1]);
            switch (obstacle8data[2]) {
                case ("N"):
                    obstacle8.setRotation(0);
                    obstacle8.setImageResource(Helper.resources.get("o8n"));
                    break;
                case ("E"):
                    obstacle8.setRotation(90);
                    obstacle8.setImageResource(Helper.resources.get("o8e"));
                    break;
                case ("S"):
                    obstacle8.setRotation(180);
                    obstacle8.setImageResource(Helper.resources.get("o8s"));
                    break;
                case ("W"):
                    obstacle8.setRotation(270);
                    obstacle8.setImageResource(Helper.resources.get("o8w"));
                    break;
                default:
                    break;
            }

            Toast.makeText(this, "Preset 2 Applied", Toast.LENGTH_SHORT).show();
        }
    }

    private void toggleSetMode() {
        canSetObstacles = !canSetObstacles;
        if (curMode.equals("IDLE")) {
            curMode = "SET";
            setButton.setText("Done");
            Toast.makeText(this, "In set mode", Toast.LENGTH_SHORT).show();
        } else if (curMode.equals("SET")) {
            curMode = "IDLE";
            setButton.setText("Set");
            Toast.makeText(this, "Obstacles set", Toast.LENGTH_SHORT).show();
        }
    }

    private void setObstacles(String[] obstaclesPreset) {
        if (obstaclesPreset.length == 0) {
            Toast.makeText(this, "No saved preset found", Toast.LENGTH_SHORT).show();
        } else {
            for (int i = 0; i < obstaclesPreset.length; i++) {
                int obstaclenum = i + 1;
                String[] obsdata = obstaclesPreset[i].split(",");
                Log.d(TAG, "Obstacle preset length is " + obstaclesPreset.length);
                Log.d(TAG, "obstacle " + obstaclenum + " data is " + Arrays.toString(obsdata));

                obstacles.get(obstaclenum).setX(Integer.parseInt(obsdata[0]) * 40);
                obstacles.get(obstaclenum).setY(Integer.parseInt(obsdata[1]) * 40);
                switch (obsdata[2]) {
                    case ("N"):
                        obstacles.get(obstaclenum).setRotation(0);
                        obstacles.get(obstaclenum).setImageResource(Helper.resources.get("o" + obstaclenum + "n"));
                        break;
                    case ("E"):
                        obstacles.get(obstaclenum).setRotation(90);
                        obstacles.get(obstaclenum).setImageResource(Helper.resources.get("o" + obstaclenum + "e"));
                        break;
                    case ("S"):
                        obstacles.get(obstaclenum).setRotation(180);
                        obstacles.get(obstaclenum).setImageResource(Helper.resources.get("o" + obstaclenum + "s"));
                        break;
                    case ("W"):
                        obstacles.get(obstaclenum).setRotation(270);
                        obstacles.get(obstaclenum).setImageResource(Helper.resources.get("o" + obstaclenum + "w"));
                        break;
                    default:
                        break;
                }
            }
        }
    }

    private void setSaveButton() {
        savedPreset = savedObstacles();
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder
                .append("ALG:")
                .append(getObstacleString(obstacle1) + "0;")
                .append(getObstacleString(obstacle2) + "1;")
                .append(getObstacleString(obstacle3) + "2;")
                .append(getObstacleString(obstacle4) + "3;")
                .append(getObstacleString(obstacle5) + "4;")
                .append(getObstacleString(obstacle6) + "5;")
                .append(getObstacleString(obstacle7) + "6;")
                .append(getObstacleString(obstacle8) + "7;");
        Log.d(TAG, stringBuilder.toString());

        if (BluetoothService.BluetoothConnectionStatus) {
            // Toast.makeText(this, stringBuilder.toString(), Toast.LENGTH_LONG).show();
            byte[] bytes = stringBuilder.toString().getBytes(Charset.defaultCharset());
            BluetoothService.write(bytes);
            Toast.makeText(Arena.this, "Obstacles sent", Toast.LENGTH_LONG).show();
        }
    }

    /*
     * Returns 2-D array of obstacles in [x, y, direction] format
     */
    private String[][] savedObstacles() {
        String[][] savedPreset = { getObstacleLocation(obstacle1).split(","), getObstacleLocation(obstacle2).split(","),
                getObstacleLocation(obstacle3).split(","),
                getObstacleLocation(obstacle4).split(","), getObstacleLocation(obstacle5).split(","),
                getObstacleLocation(obstacle6).split(","),
                getObstacleLocation(obstacle7).split(","), getObstacleLocation(obstacle8).split(",") };
        // {1,2,N,2,3,E}
        Log.d(TAG, "Saved obstacle data: " + savedPreset);
        return savedPreset;
    }

    /*
     * Get obstacle location in <x, y, direction> format
     */
    private String getObstacleLocation(ImageView obstacle) {
        return (int) obstacle.getX() + "," + (int) obstacle.getY() + "," + getImageOrientation(obstacle);
    }

    /*
     * Get obstacle location in <x, y, direction> format
     * NOTE: 19 because grid is only 20 x 20
     */
    private String getObstacleString(ImageView obstacle) {
        if ((int) (obstacle.getX() / 40) > 19 || ((int) obstacle.getY() / 40) > 19) {
            return "";
        } else {
            return ((int) obstacle.getX() / 40) + "," + ((int) obstacle.getY() / 40) + ","
                    + getImageOrientation(obstacle) + ",";
        }
    }

    private String getImageOrientation(ImageView obstacle) {
        switch (((int) ((obstacle.getRotation() / 90) % 4 + 4) % 4)) {
            case 0:
                return "N";
            case 1:
                return "E";
            case 2:
                return "S";
            case 3:
                return "W";
            default:
                return "X";
        }
    }

    private void updateStatusWindow(String msg) {
        statusWindow.setText(msg);
        Log.d(TAG, "Status window: " + msg);
    }

    private void updateRobotPosition(int x, int y, int direction) {
        car.setX(x * SNAP_GRID_INTERVAL - SNAP_GRID_INTERVAL);
        car.setY(y * SNAP_GRID_INTERVAL - SNAP_GRID_INTERVAL);
        switch (direction) {
            case 7: // North-west
                car.setRotation(315);
                break;
            case 0: // North
                car.setRotation(0);
                break;
            case 1: // North-east
                car.setRotation(45);
                break;
            case 2: // East
                car.setRotation(90);
                break;
            case 3: // South-east
                car.setRotation(135);
                break;
            case 4: // South
                car.setRotation(180);
                break;
            case 5: // South-west
                car.setRotation(225);
                break;
            case 6: // West
                car.setRotation(270);
                break;
            default:
                // Shouldn't reach this case
                break;
        }

        updateXYDirText();
    }

    private void updateXYDirText() {
        int x = (int) (car.getX() + SNAP_GRID_INTERVAL) / SNAP_GRID_INTERVAL;
        int y = (int) (car.getY() + SNAP_GRID_INTERVAL) / SNAP_GRID_INTERVAL;
        // (0,0) starts from top left hence invert y
        int new_y = 20 - y - 1;
        car_x.setText(String.valueOf(x));
        car_y.setText(String.valueOf(new_y));

        int direction = (int) car.getRotation();

        if (direction == 315)
            car_dir.setText("North-West");
        else if (direction == 0)
            car_dir.setText("North");
        else if (direction == 45)
            car_dir.setText("North-East");
        else if (direction == 90)
            car_dir.setText("East");
        else if (direction == 135)
            car_dir.setText("South-East");
        else if (direction == 180)
            car_dir.setText("South");
        else if (direction == 225)
            car_dir.setText("South-West");
        else if (direction == 270)
            car_dir.setText("West");
        else
            car_dir.setText("None");
    }

    // Broadcast Receiver for incoming messages
    BroadcastReceiver myReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String message = intent.getStringExtra("receivedMessage");
            String command;
            Log.d(TAG, "Received message: " + message);

            try {
                command = message.substring(0, message.indexOf(','));
            } catch (IndexOutOfBoundsException e) {
                Toast.makeText(Arena.this, "Invalid message format!", Toast.LENGTH_SHORT).show();
                return;
            }

            switch (command) {
                // move robot
                case Helper.ROBOT:
                    int startingIndex = message.indexOf("<");
                    int endingIndex = message.indexOf(">");
                    String x = message.substring(startingIndex + 1, endingIndex);

                    startingIndex = message.indexOf("<", endingIndex + 1);
                    endingIndex = message.indexOf(">", endingIndex + 1);
                    String y = message.substring(startingIndex + 1, endingIndex);
                    int adjusted_y = 19 - Integer.parseInt(y);

                    startingIndex = message.indexOf("<", endingIndex + 1);
                    endingIndex = message.indexOf(">", endingIndex + 1);
                    String direction = message.substring(startingIndex + 1, endingIndex);

                    Log.d("ROBOT", "(x: " + x + ") (y: " + adjusted_y + ") (direction: " + direction + ")");

                    int direction_int = 0;
                    switch (direction) {
                        case "N":
                            direction_int = 0;
                            break;
                        case "NE":
                            direction_int = 1;
                            break;
                        case "E":
                            direction_int = 2;
                            break;
                        case "SE":
                            direction_int = 3;
                            break;
                        case "S":
                            direction_int = 4;
                            break;
                        case "SW":
                            direction_int = 5;
                            break;
                        case "W":
                            direction_int = 6;
                            break;
                        case "NW":
                            direction_int = 7;
                            break;
                        default:
                            break;
                    }

                    // updateRobotPosition(Integer.parseInt(x), Integer.parseInt(y), direction_int);
                    updateRobotPosition(Integer.parseInt(x), adjusted_y, direction_int);
                    break;
                // update obstacle ID (format - TARGET, obstacle_number, target_ID)
                case Helper.TARGET:
                    int obstacleNumber = Character.getNumericValue(message.charAt(7));
                    String solution = message.substring(9);
                    Log.d(TAG, "Solution value" + solution);
                    if (Integer.parseInt(solution) == -1) {
                        Toast.makeText(Arena.this, "Image not recognized, trying again", Toast.LENGTH_SHORT).show();
                    } else {
                        setObstacleImage(obstacleNumber, solution);
                        Toast.makeText(Arena.this, "Obstacle " + obstacleNumber + " changed to Target ID: " + solution,
                                Toast.LENGTH_SHORT).show();
                    }
                    break;
                // update status window
                case Helper.STATUS:
                    String msg;
                    if (message.contains("\n")) {
                        msg = message.substring(message.indexOf(',') + 1, message.indexOf('\n'));
                    } else {
                        msg = message.substring(message.indexOf(',') + 1);
                    }
                    if (message.contains("STOPPED")) {
                        Chronometer IRTimer = (Chronometer) findViewById(R.id.IRTimer);
                        IRTimer.stop();
                        updateStatusWindow("IR Completed");
                    } else {
                        updateStatusWindow(msg);
                    }
                    break;
                // plot obstacles
                case Helper.PLOT:
                    String receivedmsg = message.substring(message.indexOf(",") + 1); // string after PLOT,
                    String[] obstaclesPreset = receivedmsg.split(";"); // create 2d array for obstacle data\
                    Log.d(TAG, "Obstacle data is " + Arrays.toString(obstaclesPreset));
                    setObstacles(obstaclesPreset);
                    break;
                case Helper.MOVE:
                    String moveCommand = message.substring(message.indexOf(',') + 1); // substring after MOVE (w10n)
                    // Forward and Reverse commands
                    if (moveCommand.length() > 2) {
                        // Split moveCommand (eg w10n) into direction (w) + interval (how many 10s) +
                        // 'n'
                        String moveDirection = moveCommand.substring(0, 1); // w
                        Log.d("this", moveDirection);
                        String moveInterval = moveCommand.substring(1, moveCommand.length() - 1); // doesn't take n, we
                                                                                                  // can leave that out
                                                                                                  // of any
                                                                                                  // consideration
                        int intervals = Integer.parseInt(moveInterval) / 10; // intervals = how many units of 10s we
                                                                             // have to move (10 = 1 grid block)
                        switch (moveDirection) {
                            case "w":
                                for (int i = 0; i < intervals; i++) {
                                    forwardButtonCommand();
                                    // sleepFor(500);
                                }
                                break;
                            case "s":
                                for (int i = 0; i < intervals; i++) {
                                    reverseButtonCommand();
                                    // sleepFor(500);
                                }
                                break;
                            default:
                                Log.d("Move command", "Direction is not valid");
                                break;
                        }
                    }

                    else {
                        switch (moveCommand) { // Turn commands
                            case "ln": // forward left (w, w,w, a, w, w, w)
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                leftButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                break;
                            case "rn": // forward right (w,w, w, d, w, w,w)
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                rightButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                forwardButtonCommand();
                                // sleepFor(500);
                                break;
                            case "Ln": // reverse left (s, s, s, d, s, s, s)
                                reverseButtonCommand();
                                reverseButtonCommand();
                                reverseButtonCommand();
                                rightButtonCommand();
                                reverseButtonCommand();
                                reverseButtonCommand();
                                reverseButtonCommand();
                                break;
                            case "Rn": // reverse right (s, s, s, a, s, s, s)
                                reverseButtonCommand();
                                reverseButtonCommand();
                                reverseButtonCommand();
                                leftButtonCommand();
                                reverseButtonCommand();
                                reverseButtonCommand();
                                reverseButtonCommand();
                                break;
                            case "xn": // spot turn left
                                leftButtonCommand();
                                break;
                            case "Xn":// spot turn right
                                rightButtonCommand();
                                break;
                            default:
                                Log.d("Move command", "Command is not a valid turn");
                                Log.d("this", moveCommand); // checking value of moveCommand
                                break;
                        }
                    }
                default:
                    // for outer "ROBOT/TARGET/STATUS/MOVE cases
                    break;
            }

        }
    };
}
