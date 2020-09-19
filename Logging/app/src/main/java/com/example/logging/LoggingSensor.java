package com.example.logging;

// file path for the logfile:
// /data/data/com.example.logging/files/logfile

// PPG sensor name: D/pah8011_ppg Non-wakeup

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.PowerManager;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;

import java.io.File;
import java.io.FileOutputStream;
import java.util.List;

import static android.webkit.ConsoleMessage.MessageLevel.LOG;

public class LoggingSensor extends Activity implements SensorEventListener {

    private SensorManager mSensorManager;
    private Sensor ppgSensor;
    private Sensor accSensor;
    private FileOutputStream outputStream;

    private PowerManager.WakeLock wakeLock;

    private static final float NS2S = 1.0f / 1000000000.0f;

    public LoggingSensor(){
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // flag that screen should be kept on
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        // use wake lock to support continuous PPG reading
        PowerManager powerManager = (PowerManager) getSystemService(POWER_SERVICE);
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,
                "MyApp::MyWakelockTag");
        wakeLock.acquire();

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logging_sensor);

        File logfile = new File(this.getFilesDir(), "logfile");
        Log.d("CREATED LOG FILE AT:", logfile.getAbsolutePath());

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        ppgSensor = mSensorManager.getDefaultSensor(65572);
        // also get acceleration data for syncing time with ECG ground truth signal
        accSensor = mSensorManager.getDefaultSensor(1);

        mSensorManager.registerListener(this, ppgSensor, SensorManager.SENSOR_DELAY_FASTEST);
        mSensorManager.registerListener(this, accSensor, SensorManager.SENSOR_DELAY_FASTEST);

        try {
            // open logfile and write headers
            outputStream = openFileOutput("logfile", Context.MODE_PRIVATE);
            outputStream.write(("sensor,timestamp,v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11," +
                    "v12,v13,v14,v15,v16,v17\n").getBytes());
        }catch (Exception e){
            e.printStackTrace();
        }




    }

    private void listSensors(){
        // List available sensors in the log list - used for debugging/finding ppg sensor name
        List<Sensor> sensorList = mSensorManager.getSensorList(Sensor.TYPE_ALL);
        for (Sensor currentSensor : sensorList) {
            Log.d("List sensors", "Name: "+currentSensor.getName() + " /Type_String: " +currentSensor.getStringType()+ " /Type_number: "+currentSensor.getType());
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event){
        // get sensor data and timestamp (convert from nanoseconds to seconds)
        String timestamp = String.valueOf(event.timestamp * NS2S);
        String logline = event.sensor.getName() + "," + timestamp + ",";

        for(int i = 0; i < event.values.length; i++){
            // data must be converted from raw bit pattern stored in float
            logline += Float.floatToRawIntBits(event.values[i]) + ",";
        }

        logline += "\n";

        // write to file
        try {
            outputStream.write(logline.getBytes());
        }catch (Exception e){
            e.printStackTrace();
        }

    }

    public void onAccuracyChanged(Sensor sensor, int accuracy){

    }

    public final void stopButton(View view){
        // finish logging and exit
        Intent myIntent = new Intent(LoggingSensor.this, MainActivity.class);
        myIntent.putExtra("hi", 1);
        this.startActivity(myIntent);

        // release wake lock
        wakeLock.release();

        // flag that screen can be turned off
        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    }
}
