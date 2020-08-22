# Available on GitHub!
# This program will gather data from raspberry pi sensors and store the data to make calculations later
# It must be compatible with raspbian and windows
# I would like to rely on as few modules as possible

# This program is intended for use with a raspberry 3 B+, BMP388 board, and ICM20629 board running with i2c


import time
# board is from adafruit-cyrcuitpython and will work on a rasp pi, I cant find how to make it work for windows
# without breaking something else
import board
import busio
import adafruit_bmp3xx
import adafruit_icm20x
import pandas as pd
import pathlib as pl
import datetime as dt
import logging

# Gotta learn logging

i2c = busio.I2C(board.SCL, board.SDA)
bmp388 = adafruit_bmp3xx.BMP3XX_I2C(i2c)
icm20649 = adafruit_icm20x.ICM20649(i2c)

def main():

    print('Program start!')

    setup_boards()

    gather_store_data()

    # while not determine_landed():
    # figure out how to keep only data from 3 seconds before launch
    # perhaps log data from when program starts and determine time of launch, then sort the big csv and remove data
    # from before the launch

    print('Program end!')

    return None

def setup_boards():

    global bmp388
    global icm20649

    # Ask for pressure at sea level or use gps to find it

    bmp388.reset()
    bmp388.sea_level_pressure = 1014.9

    icm20649.reset()
    icm20649.initialize()
    print('Initializing, please wait...')
    time.sleep(5)

    print('Begin test!')

def determine_launch():
    """
    Will find the time of launch to be used in sorting data
    """
    return None

def determine_landed():
    """
    Will find the time of landing to be used in ending recording
    """
    return None

def get_data():
    """
    This function will interact with bmp388 and return the barometric pressure and temperature detected by the
    sensor. It will also return the current altitude calculated by its built in altitude function

    This function will interact with icm20649 and return the accelerometer and gyro data detected by the
    sensor
    """

    # b =  speak to bmp388 to get current data point
    # t =  speak to bmp388 to get current data point
    # a =  speak to bmp388 to get current data point
    # a_x =  speak to icm20649 to get current data point
    # a_y =  speak to icm20649 to get current data point
    # a_z =  speak to icm20649 to get current data point
    # g_x =  speak to icm20649 to get current data point
    # g_y =  speak to icm20649 to get current data point
    # g_z =  speak to icm20649 to get current data point

    b = []
    t = []
    a = []
    a_x = []
    a_y = []
    a_z = []
    g_x = []
    g_y = []
    g_z = []

    # test
    start = time.time()
    for _ in range(1000):
        a_x.append(icm20649.acceleration[0])
        a_y.append(icm20649.acceleration[1])
        a_z.append(icm20649.acceleration[2])
        g_x.append(icm20649.gyro[0])
        g_y.append(icm20649.gyro[1])
        g_z.append(icm20649.gyro[2])
        b.append(bmp388.pressure)
        t.append(bmp388.temperature)
        a.append(bmp388.altitude)
        print(_)

    print('End test!')
    end = time.time()
    duration = end - start
    print(f'test took {duration} seconds to complete.')

    return b, t, a, a_x, a_y, a_z, g_x, g_y, g_z

    # end test

def mk_run_dir():
    """
    This function will find the current path to the Flight-Recorder program and make a new directory named "Date-Run-#".
    It will also create all sub directories needed to store all flight data for further calculations
    if the same date and # exist it will add 1 to the greatest number file found
    """

    file_num = 1

    while True:
        try:
            folder_name = f'{dt.date.today()}-Run-{file_num}'
            run_path = pl.Path.cwd() / folder_name
            run_path.mkdir(exist_ok = False)
            break
        except FileExistsError:
            file_num += 1
    # log print(f'Folder Created, {folder_name} @ {run_path}')
    return run_path

def gather_store_data():
    """
    This function will gather the data and create a .csv file to save all the data into, each data type will have its own
    and column. Each consecutive data point will be stored in rows under their respective columns
    """

    run_path = mk_run_dir()

    b, t, a, a_x, a_y, a_z, g_x, g_y, g_z = get_data()

    data_dict = {
            "Barometric Pressure":b,
            "Temperature":t,
            "Altitude_B":a,
            "Accelerometer_x":a_x,
            "Accelerometer_y":a_y,
            "Accelerometer_z":a_z,
            "Gyroscope_x":g_x,
            "Gyroscope_y":g_y,
            "Gyroscope_z":g_z,
        }
    data = pd.DataFrame.from_dict(data_dict)

    pd.DataFrame.to_csv(data,
                        path_or_buf = run_path / 'Run-Data',
                        mode = 'w'
                        )

    return None

# Optional things
# def get_gps, will determine devices location
# def determine_b_sea, will gather local barometric pressure at sea level from internet, will call get_gps

if __name__ == '__main__':
    main()