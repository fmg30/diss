package com.example.logging;

import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.wearable.activity.WearableActivity;
import android.util.Log;
import android.view.View;

import androidx.fragment.app.FragmentActivity;

import java.util.List;

public class MainActivity extends FragmentActivity {
    private static final String TAG = "MainActivity";



    public void onCreate(Bundle savedInstanceState) {
        Log.d(TAG, "onCreate()");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        // Enables Always-on
//        setAmbientEnabled();
    }

    public final void pressButton(View view){
        Intent myIntent = new Intent(MainActivity.this, LoggingSensor.class);
        myIntent.putExtra("hi", 1);
        this.startActivity(myIntent);
    }
}
