from adbutils import AdbClient
import sys
import tqdm

client = AdbClient(host="127.0.0.1",port=5037)

#判断参数是否输入 Determine If The Parameter Is Input
if len(sys.argv) != 4 and len(sys.argv) != 3 and len(sys.argv) != 2:
    print("Parameters incorrect!")
    sys.exit()
#显示帮助手册 Show Help Manual
elif len(sys.argv) == 2 and sys.argv[1] == "help":
    print("AdbDeleter v1.0")
    print("Syntax: adbdeleter [options] [filepath] [mode]")
    print("Options:")
    print("-f(Force but dangerous and need device rooted):Delete file in root mode")
    print("Modes:")
    print("fast (and insecure mode):1 write zeros and 1 android rm command")
    print("safe (slow but secure mode):37 write randoms 1 write zeros and 1 android rm command")
    sys.exit()

if len(sys.argv) == 4:
    parameters = sys.argv[1].strip("-")
    target = sys.argv[2]
    mode = sys.argv[3]
else:
    target = sys.argv[1]
    mode = sys.argv[2]

#获取设备 Get Device
devices = client.device_list()
if len(devices) == 0:
    print("Device not connected!")
    sys.exit()
#如果设备数大于1,让用户选择设备 If The Number Of Devices Is Greater Than 1, Let The User Select The Device.
if len(devices) != 1:
    print("Connected "+str(len(devices))+" devices")
    print("Which device do you want to choose?")
    for i in devices:
        print("Device"+str((devices.index(i)+1))+" Serial Number:"+i.serial)
        device_number = input("Input the device number of the device you want to choose:")
    #检查设备序列号是否正确 Check That The Device Number Is Correct
    if device_number > len(devices):
        print("Device number incorrect!")
        sys.exit()
    device = devices[device_number - 1]
    print("Connected to device:"+device.serial)
else:
    device = devices[0]
    print("Connected to device:"+device.serial)

#检查文件是否存在 Check If The File Exists
try:
    if device.shell("ls "+target).split(":")[2] == " No such file or directory":
        print("Target not find")
        sys.exit()
except:
    pass
#判断模式是否正确 Determine If The Mode Is Correct
if mode != "safe":
    if mode != "fast":
        print("Mode incorrect!")
        sys.exit()

#检查参数
if "f" in parameters:
    try:
        if device.shell("ls /system/bin/su").split[2] == " No such file or directory":
            print("Your device is not rooted or you have not given adb root permissions")       
            sys.exit()
    except TypeError:
        root_permission = True

#擦除函数 Erase Function
def erase(target,randomerasetimes):
        print("Getting target file size")
        targetfilesize = device.shell("wc "+target).split(" ")[2]
        print("Target file size:"+targetfilesize+" Bytes")
        if randomerasetimes != 0:
            print("Starting random erasing")
            if root_permission:
            #Root模式随机擦除 Random Erase In Root Mode
                for i in tqdm.tqdm(range(randomerasetimes),unit="Times"):
                    device.shell("su -c dd if=/dev/urandom of="+target+" bs=1 count="+targetfilesize)
            else:
                    for i in tqdm.tqdm(range(randomerasetimes),unit="Times"):
                        device.shell("dd if=/dev/urandom of="+target+" bs=1 count="+targetfilesize)
            print("Complete")
        print("Starting zero erasing")
        #Root模式写零 Zero Erase In Root Mode
        if root_permission:
            device.shell("su -c dd if=/dev/zero of="+target+" bs=1 count="+targetfilesize)
        else:
            device.shell("su -c dd if=/dev/zero of="+target+" bs=1 count="+targetfilesize)
        print("Complete")
        print("Starting android rm command")
        device.shell("rm "+target)
        print("Complete")

try:
    #弹出警告并根据选择擦除数据 A Warning Pops Up And Erases Data Based On The Selection
    if root_permission:
        print("Erase data in "+target+" by "+mode+" mode with root permission")
    else:
        print("Erase data in "+target+" by "+mode+" mode with normal permission")
    if root_permission:
        print("You are using root permission,it means your may be deleteing system files,it will breaks your android system,please be careful")
    answer = input("Do you want do to it?This deletes your data and files may not be recoverable(Y,n)?")
    if answer == "Y":
    #以37次写随机数,1次写零和1次安卓rm命令擦除目标文件 Erase Target File With 37 Write Randoms,1 Write Zeros And 1 Android rm Command
        if mode == "safe":
            erase(target,37)
            print("Secure erase completed")
        #以1次写零和1次安卓rm命令擦除目标文件 Erase Target File With 1 Write Zeros And 1 Android rm Command
        elif mode == "fast":
            erase(target,0)
            print("Fast erase completed")
    elif answer == "n":
        print("Stop erasing")
    else:
        print("Answer incorrect!")
        sys.exit()
except KeyboardInterrupt:
    sys.exit()