import threading
import sqlite3 as sql
import subprocess
import time
import csv
import shutil
from powerboard import summary_v2
import tensorflow as tf
import os

time_start = 0
glob_var = True
thread_list = []

# Stop the data reading using a global variable
def stop():
    global glob_var
    glob_var = False

# Function for threading the data saving on the Database
def saveDB(single_buffer, threadID):
    print("\n" + "ThreadID:" + str(threadID) + "\n")
    conn = sql.connect('ipmi_data.db')
    c = conn.cursor()
    for inst in single_buffer:
        newRow = " " + "(" + "\'" + str(inst[0].replace('\n', '\\n')) + "\'" + "," + str(inst[1]) + ")"
        newRow = "INSERT INTO SensorData VALUES" + newRow
        c.execute(newRow)
    conn.commit()
    conn.close()

# The function in which runs the loop that collects the data
def mainThread():
    global glob_var
    global thread_list

    # Delete current database file
    try:
      os.remove("ipmi_data.db")
    except OSError:
      pass

    # Create database
    conn = sql.connect('ipmi_data.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS SensorData")
    c.execute("CREATE TABLE SensorData (sensorRead TEXT, dataTime FLOAT)")
    conn.commit()

    # Create buffers
    buffers = []
    buffers.append([])
    buffers.append([])

    # Create thread
    #thread = saveDB()

    # Complete buffer, after buffer is completed, use the other one while
    # the first one is being saved on the database
    bufferNumber = 0
    i = 0
    while (glob_var):
      # Get sensor value from ipmi
      sens = 'Total Power'
      command = ['sudo', 'ipmitool', 'sensor', 'get', sens]
      process = subprocess.run(
              command,
              stdout=subprocess.PIPE,
              universal_newlines=True)
      output = process.stdout
      output = output.replace('\n', '\\n')

      # Append on buffer
      buffers[bufferNumber].append([output, time.time() - time_start])

      # Checks if the current buffer is full
      if len(buffers[bufferNumber]) > 10:
        #thread.start(buffers[bufferNumber], bufferNumber)
        #thread.run(buffers[bufferNumber], bufferNumber)
        #buffers[bufferNumber] = []
        thread = threading.Thread(target=saveDB, args=(buffers[bufferNumber], bufferNumber,))
        thread_list.append(thread)
        thread.start()
        if bufferNumber == 0:
          bufferNumber = 1
        else:
          bufferNumber = 0
        buffers[bufferNumber] = []
      i += 1

    # At the end of process, saves the buffer data remaining in the database.
    if len(buffers[0]) > 0:
      conn = sql.connect('ipmi_data.db')
      c = conn.cursor()
      for inst in buffers[0]:
        newRow = " " + "(" + "\'" + str(inst[0].replace('\n', '\\n')) + "\'" + "," + str(inst[1]) + ")"
        newRow = "INSERT INTO SensorData VALUES" + newRow
        c.execute(newRow)
      conn.commit()
      conn.close()
    elif len(buffers[1]) > 0:
      conn = sql.connect('ipmi_data.db')
      c = conn.cursor()
      for inst in buffers[1]:
        newRow = " " + "(" + "\'" + str(inst[0].replace('\n', '\\n')) + "\'" + "," + str(inst[1]) + ")"
        newRow = "INSERT INTO SensorData VALUES" + newRow
        c.execute(newRow)
      conn.commit()
      conn.close()

# Starts the main thread and sets the timestamp
def start():
    command = ['sudo', 'echo']
    process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            universal_newlines=True)

    global time_start
    time_start = time.time()

    main_thread = threading.Thread(target=mainThread)
    main_thread.start()

# Saves the raw database data on a nice CSV file
def dbToCSV(path):
    try:
        os.mkdir(path)
    except:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    writer = tf.summary.create_file_writer("demo_logs")
    with writer.as_default():
         summary_v2.greeting("ipmi_data.csv",path, step=0)
    conn = sql.connect('ipmi_data.db')
    c = conn.cursor()
    sens = 'Total Power'
    with open('ipmi_data' + '.csv', 'w') as file_out:
        write = csv.writer(file_out)
        first_row = ['Sensor_ID', 'Entity_ID', 'Sensor_Type_Threshold_',
                     'Sensor_Reading', 'Status',
                     'Lower_Non_Recoverable', 'Lower_Critical',
                     'Lower_Non_Critical', 'Upper_Non_Critical', 'Upper_Critical',
                     'Upper_Non_Recoverable', 'Positive_Hysteresis',
                     'Negative_Hysteresis', 'Assertion_Events',
                     'Assertions_Enabled', 'Time_elapsed']
        write.writerow(first_row)
        for db_row in c.execute("SELECT * FROM SensorData"):
            output = str(db_row[0])
            read_time_value = float(db_row[1])
            output = output.replace('\\n', '\n')
            output = output.split('\n')[2:-2]
            current_row = []
            current_row.append(sens)
            for i in range(len(output)):
                output[i] = output[i].split(':')
                output[i][0] = output[i][0].replace(' ', '')
                for j in range(1,len(output[i])):
                    output[i][j] = output[i][j].split()
                    if len(output[i][j]) > 0:
                        current_row.append(output[i][j][0])
                    else:
                        current_row.append('Empty_string')
            current_row.append("{:.5f}".format(read_time_value))
            #print(current_row)
            #print(current_row)
            write.writerow(current_row)
    #add the CSV file in a path passed in argument
    shutil.copy("ipmi_data.csv",path)
