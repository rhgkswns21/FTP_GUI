import ftplib
import socket
import csv
import datetime
import threading

ftp = ftplib.FTP()

th_list = []
file_alive_state = []
th_time_out = None

# dir_name = '/local/inspection/' + str(ftp_info[4]) + '/data/' + str(ftp_info[5])
# log_dir_name = '/local/inspection/' + str(ftp_info[4]) + '/log/' + str(ftp_info[5])[:-2]
# command_dir_name = '/local/inspection/' + str(ftp_info[4]) + '/command'
# master_log_name = ''

def ftp_connect(server_url, port, id, pw) -> bool:
    print('ftp_connect')
    try:
        print(ftp.connect(server_url, port, timeout=5))
        print(ftp.login(id, pw))
        return True

    except(ftplib.error_perm, socket.gaierror):
        print('connect error')
        return False

def make_csv_file(panid, date) -> bool:
    dir_raw_data = []
    dir_raw_data_split = []
    dir_file_name = []
    dir_file_size = []
    data_check = []
    size_check = []
    device_num = []
    csv_header = ['date', 'No.']
    write_list = []
    print('get_data_file_list')
    try:
        dir_name = '/local/inspection/' + panid + '/data/' + date
        ftp.cwd(dir_name)
        ftp.dir(dir_raw_data.append)
        for i in dir_raw_data:
            dir_raw_data_split.append(list(filter(None, i.split(' '))))

        for i in dir_raw_data_split:
            dir_file_name.append(i[8])
            dir_file_size.append(i[4])

        for num in range(1, 50):
            check_str = '_' + str(num) + '.csv'
            check_list = []
            check_size_list = []
            for index, i in enumerate(dir_file_name):
                if check_str in i:
                    check_list.append(i.split('_')[2])
                    check_size_list.append(dir_file_size[index])
                    if num in device_num:
                        pass
                    else:
                        device_num.append(num)
            data_check.append(check_list)
            size_check.append(check_size_list)

        ## data min & max number check
        min_num = 999
        max_num = 0
        data_check = list(filter(None, data_check))
        size_check = list(filter(None, size_check))
        for i in data_check:
            if int(min(i)) < min_num:
                min_num = int(min(i))
            if int(max(i)) > max_num:
                max_num = int(max(i))

        ## make write Data / time & data number
        for j in range(min_num, max_num + 1):
            for i in dir_file_name:
                if '_' + str(j).zfill(3) + '_' in i:
                    write_list.append([datetime.datetime.strptime(i.split('_')[1], '%Y%m%d%H%M%S'), i.split('_')[2]])
                    break

        ## Check data availability
        for i_index, i in enumerate(data_check):
            check_count = min_num
            for j_index, j in enumerate(i):
                while (check_count != int(j)):
                    write_list[check_count - min_num].append('0')
                    check_count = check_count + 1
                if size_check[i_index][j_index] > '144000':
                    write_list[check_count - min_num].append('1')
                else:
                    write_list[check_count - min_num].append('!')
                check_count = check_count + 1

        ## .csv Save
        save_file_name = date + '_' + panid
        for i in device_num:
            if i == 1:
                csv_header.append('M')
            else:
                csv_header.append('S' + str(i-1))
        f = open(save_file_name + '.csv', 'w', newline='')
        csvwr = csv.writer(f)
        csvwr.writerow(csv_header)
        for i in write_list:
            csvwr.writerow(i)
        f.close()

        return True
    except:
        print('error')
        return False

def ftp_disconnect() -> bool:
    print('ftp_disconnect')
    try:
        ftp.quit()
        return True
    except:
        return False

def ftp_file_alive_check_timeout():
    print('ftp_file_alive_check_timeout')


def ftp_file_alive_check(ftp_path, file_list, event_func = None):
    print('ftp_file_alive_check')
    try:
        ftp.cwd(ftp_path)
        now_ftp_file_list = ftp.nlst()
        for index, i in enumerate(file_list):
            if i in now_ftp_file_list:
                pass
            else:
                file_alive_state[index] = 'Remove'
        print(file_alive_state)
        event_func(file_alive_state)

        if file_alive_state.count('Remove') == len(file_alive_state):
            print('Removed all file')
            th_time_out.cancel()
        elif th_time_out.isAlive() == False:
            print('ftp_file_alive_check_time_out')
            pass
        else:
            th = threading.Timer(10, ftp_file_alive_check, args=(ftp_path, file_list, event_func))
            th_list.append(th)
            th.start()
    except:
        print('error')

def ftp_file_upload(local_path, ftp_path, file_list, time_out_state = False, time_out_time = 60, evenc_func = None) -> bool:
    global th_time_out
    print('ftp_file_upload')
    try:
        ftp.cwd(ftp_path)
        for i in file_list:
            f = open(local_path + '/' + i, 'rb')
            ftp.storbinary('STOR ' + i, f)
            f.close()

        if time_out_state == True:
            file_alive_state.clear()
            for i in file_list:
                file_alive_state.append(i)
            th = threading.Timer(10, ftp_file_alive_check, args=(ftp_path, file_list, evenc_func))
            th_list.append(th)
            th.start()
            th_time_out = threading.Timer(int(time_out_time), ftp_file_alive_check_timeout)
            th_time_out.start()
        return True
    except:
        return False



# import time
# ftp_connect('mnn001.com', 21, 'uploader002@mnn001.com', 'Yamorin1717')
# make_csv_file('000a', '20200129')
# time.sleep(10)
# make_csv_file('000a', '20200129')
#
# ftp.quit()