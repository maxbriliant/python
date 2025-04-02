import win32file
def locate_usb():

	drive_list = []
	drivebits=win32file.GetLogicalDrives()
	for d in range(1,26):
	    mask=1 << d
	    if drivebits & mask:
	        # here if the drive is at least there
	        drname='%c:\\' % chr(ord('A')+d)
	        t=win32file.GetDriveType(drname)
	        if t == win32file.DRIVE_REMOVABLE:
	            drive_list.append(drname)
	return drive_list