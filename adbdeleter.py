from adbutils import AdbClient
import sys
import tqdm

client = AdbClient(host="127.0.0.1",port=5037)

#判断参数是否输入 Determine If The Parameter Is Input
if len(sys.argv) != 3:
    if len(sys.argv) != 2:
        print("Parameters incorrect!")
        sys.exit()
#显示帮助手册 Show Help Manual
    elif len(sys.argv) == 2:
        print("AdbDeleter v1.0")
        print("Syntax: adbdeleter [filepath] [mode]")
        print("Options:")
        print("fast (and insecure mode):3 write zeros and 1 android rm command")
        print("safe (slow but secure mode):37 write randoms 1 write zeros and 1 android rm command")
        sys.exit()
target = sys.argv[1]
mode = sys.argv[2]

#获取设备 Get Device
devices = client.device_list()
if len(devices) == 0:
    print("Device not connected!")
    sys.exit()
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

try:
#弹出警告并根据选择擦除数据 A Warning Pops Up And Erases Data Based On The Selection
    print("Erase data in "+target+" by "+mode+" mode")
    answer = input("Do you want do to it?This deletes your data and files may not be recoverable(Y,n)?")
    if answer == "Y":
#以37次写随机数,1次写零和1次安卓rm命令擦除目标文件 Erase Target File With 37 Write Randoms,1 Write Zeros And 1 Android rm Command
        if mode == "safe":
            print("Getting target file size")
            targetfilesize = device.shell("wc "+target).split(" ")[2]
            print("Target file size:"+targetfilesize+" Bytes")
            print("Starting random erasing")
            for i in tqdm.tqdm(range(37),unit="Times"):
                device.shell("dd if=/dev/urandom of="+target+" bs=1 count="+targetfilesize)
            print("Complete")
            print("Starting zero erasing")
            device.shell("dd if=/dev/zero of="+target+" bs=1 count="+targetfilesize)
            print("Complete")
            print("Starting android rm command")
            device.shell("rm "+target)
            print("Complete")
            print("Secure erase completed")
#以3次写零和1次安卓rm命令擦除目标文件 Erase Target File With 1 Write Zeros And 1 Android rm Command
        elif mode == "fast":
            print("Getting target file size")
            targetfilesize = device.shell("wc "+target).split(" ")[2]
            print("Target file size:"+targetfilesize+" Bytes")
            print("Starting zero erasing")
            device.shell("dd if=/dev/zero of="+target+" bs=1 count="+targetfilesize)
            print("Complete")
            print("Starting android rm commnad")
            device.shell("rm "+target)
            print("Complete")
            print("Insecure erase completed")
    elif answer == "n":
        print("Stop erasing")
    else:
        print("Answer incorrect!")
except KeyboardInterrupt:
    sys.exit()