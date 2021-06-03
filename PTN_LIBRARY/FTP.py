import os, sys, paramiko, threading
import time 

logger = None 
_loggerflag = False 

# if logger is None: 
#     from applogger import Logger 
#     _loggerflag = True 
#     logger = Logger(logtype='STREAM', loglevel='DEBUG').UseLogger()

'''
사용자 정보 dirctionary
'''
info ={
    0: {
        'hostname': '10.82.66.65', 
        'port': 22, 
        'username': 'h20200155', 
        'password': 'h20200155', 
        'src': [''], 
        'dst': ['']
    }
}

class UseSFTP(threading.Thread): 
    def __init__(self, hostname, port, username, password, src, dst): 
        threading.Thread.__init__(self)
        self.hostname = hostname 
        self.port = port
        self.username = username
        self.password = password
        self.src = src 
        self.dst = dst 

    def ConnectSFTP(self): 

        ssh = None 
        sftp = None 

        try: 
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
            sftp = ssh.open_sftp()
            print ("Success to connect : %s"%(self.hostname))
        except: 
        #     # except Exception as e: 
        #     #     if _loggerflag is True : 
        #     #         logger.warning('{}'.format(e)) 

        #     #     else: 
        #     #         print (e)
        #     print(e)
            print ("Fail to connect : %s"%(self.hostname))
            ssh = None 
            sftp = None 
        return ssh, sftp 

    def CloseSFTP(self, sftp, ssh): 
        sftp.close()
        ssh.close()
        
    def GetFileList(self, ssh, sftp, wdir): 
        dirList =sftp.listdir(wdir)

        


        return dirList 

    def GetFileSize(self,file):
        '''
        파일 사이즈 출력해주는 함수
        '''
        if file < 1024:
            return str(file) + "byte"
        elif file < 1024*1024:
            return str(file/1024) + "kbyte"
        elif file < 1024*1024*1024:
            return str(file/1024/1024) + "mbyte"
        

    def PrintSummury(self,hostname,totaltime,filesize,filename):
        '''
        전송 정보 요약해서 출력해주는 함수, _loggerflag가 True일 경우에만 사용됩니다.
        '''
        # if len(filename) > 1:
        #     for i in range(len(filename)):
        #         logger.info('{} Transmission file: {}'.format(hostname,filename[i]))
        # else:
        #     logger.info('{} Transmission file: {}'.format(hostname,filename))
        # logger.info('{} Transmission size: {}'.format(hostname,filesize))
        # logger.info('{} Transmission time: {} seconds'.format(hostname,totaltime))
        # logger.info('{} Transmission Complete'.format(hostname))

        if len(filename) > 1:
            print ("%s Transmission file: %s"%(hostname, filename[i]))
        


    def TransferDir(self):
        '''
        로컬에서 원격지로 디렉토리 전송을 담당하는 함수
        '''
        try:
            error = ''
            flag = True
            # 소스경로
            self.src[0] = os.path.abspath(self.src[0]) + '/'
            parent = os.path.expanduser(self.src[0])
            ssh, sftp = self.ConnectSFTP()
            totaltime = ''
            filesize = 0
            totalsize = 0
            fileindex = self.src[0][:self.src[0].rfind('/')].rfind('/')
            srcdir = self.src[0][fileindex:self.src[0].rfind('/')]
            # 배포경로 
            self.dst[0] = os.path.abspath(self.dst[0]) + srcdir
            # 배포경로 생성 
            stdin, stdout, stderr = ssh.exec_command('mkdir -p %s' % self.dst[0])
            # exec_command가 non-blocking이라 blocking으로 ssh.exec_command의 결과를 대기
            exit_status = stderr.channel.recv_exit_status()
            
            # ssh.exec_command명령에서 에러가 발생한 경우에 진입
            if exit_status != 0:
                flag = False
                error = 'exit_status is 1'
                return flag, error
            
            # ssh와 sftp가 이상없이 연결되었을 경우에 진입
            if ssh is not None and sftp is not None:
                starttime = time.time()
                for dirpath, dirnames, filenames in os.walk(parent):
                    remote_path = os.path.join(self.dst[0], dirpath[len(parent):])
                    try:
                        sftp.listdir(remote_path)
                    except IOError:
                        sftp.mkdir(remote_path)
                    except Exception as e:
                        # if _loggerflag is True:
                        #     logger.warning('{}'.format(e))
                        # else:
                        #     print(e)

                        print(e)

                    for i in range(len(filenames)):
                        filesize = filesize + os.path.getsize(dirpath+'/'+filenames[i])
                        sftp.put(os.path.join(dirpath, filenames[i]), os.path.join(remote_path, filenames[i]))

                endtime = time.time()
                totaltime = '%.02f' % (endtime - starttime)
                # if _loggerflag is True:
                #     self.PrintSummury(self.hostname,totaltime,self.GetFileSize(filesize),self.src)
                # else:
                #     pass

            else:
                flag = False
                error = 'SSH & SFTP CONNECTION is FAIL'
                return flag, error

        except Exception as e:
            flag = False
            error = e
            return flag, error


    def TrasferFiles(self):
        '''
        로컬에서 원격지로 파일 전송을 담당하는 함수
        '''
        error = ''
        flag = True
        # 소스경로
        self.dst[0] = os.path.abspath(self.dst[0]) + '/'   
        # ssh & sftp 클라이언트 연결     
        ssh, sftp = self.ConnectSFTP()
        totaltime = ''
        filesize = 0
        totalsize = 0
        try:
            # 배포경로 생성 
            stdin, stdout, stderr = ssh.exec_command('mkdir -p %s' % self.dst[0])
            # exec_command가 non-blocking이라 blocking으로 ssh.exec_command의 결과를 대기
            exit_status = stderr.channel.recv_exit_status()

            # ssh.exec_command명령에서 에러가 발생한 경우에 진입
            if exit_status != 0:
                flag = False
                error = 'exit_status is 1'
                return flag, error

            # ssh와 sftp가 이상없이 연결되었을 경우에 진입
            if ssh is not None and sftp is not None:
                starttime = time.time()
                # src 개수만큼 반복하면서 원격지에 파일 전송                
                for i in range(len(self.src)):
                    filesize = filesize + os.path.getsize(self.src[i])
                    if not os.path.isfile(self.src[i]):
                        # if _loggerflag is True:
                        #     logger.info('No Such File...')
                        # else:
                        #     print('No Such File...')
                        print('No Such File...')
                        return
                    elif len(stderr.readlines()) == 1:
                        # if _loggerflag is True:
                        #     logger.warning('No Such Directory...')
                        # else:
                        print('No Such Directory...')
                        sftp.mkdir(self.dst[0], mode=511)
                    else:
                        filename_index = self.src[i].rfind('/')
                        filename = self.src[i][filename_index+1:]
                        sftp.put(self.src[i], self.dst[0]+filename)

            else:
                flag = False
                error = 'SSH & SFTP CONNECTION is FAIL'
                return flag, error

            endtime = time.time()
            totaltime = '%.02f' % (endtime - starttime)

            # if _loggerflag is True:
            #     self.PrintSummury(self.hostname,totaltime,self.GetFileSize(filesize),self.src)
            # else:
            #     pass

        except IOError as e:
            flag = False
            error = e
            return flag, error

        except Exception as e:
            flag = False
            error = e
            return flag, error


    def SendToRemote(self):
        '''
        파일전송인지 폴더전송인지 구분한 후 전송함수 호출을 담당하는 함수
        '''
        # 소스가 파일 전송일 경우
        if os.path.isfile(self.src[0]) or len(self.src) > 1:
            self.TrasferFiles()
        
        # 소스가 폴더 전송일 경우
        elif not os.path.isfile(self.src[0]) and len(self.src) < 2:
            self.TransferDir()


    def run(self):
        '''
        스레드 Run 담당하는 함수
        '''
        try:
            self.SendToRemote()

        except Exception as e:
            logger.warning('{}'.format(e))


def GetInformation(info):
    '''
    SFTP 전송관련 정보들을 담은 dict를 반환하는 함수
    '''
    infolist = []
    idx = len(info)
    for i in range(idx):
        infolist.append(info[i])
    
    return infolist


def Validation():

    flag = True
    data = GetInformation(info)
    
    for i in range(len(data)):
        if len(data[i]['hostname']) < 1:
            # logger.critical('%d hostname 입력되지 않았습니다' % i)
            print('%d hostname 입력되지 않았습니다' % i)
            flag = False
        if data[i]['port'] is None:
            # logger.critical('%d port 입력되지 않았습니다' % i)
            print ('%d port 입력되지 않았습니다' % i)
            flag = False
        if len(data[i]['username']) < 1:
            # logger.critical('%d username 입력되지 않았습니다' % i)
            print('%d username 입력되지 않았습니다' % i)
            flag = False
        if len(data[i]['password']) < 1:
            # logger.critical('%d password 입력되지 않았습니다' % i)
            print(logger.critical('%d password 입력되지 않았습니다' % i))
            flag = False
        if len(data[i]['src']) < 1:
            # logger.critical('%d src 입력되지 않았습니다' % i)
            print(logger.critical('%d src 입력되지 않았습니다' % i))
            flag = False
        if len(data[i]['dst']) < 1:
            # logger.critical('%d dst 입력되지 않았습니다' % i)
            print(logger.critical('%d dst 입력되지 않았습니다' % i))
            flag = False
            
    return flag, data
    
def main():
    '''
    배포대상 서버의 수만큼 스레드가 생성되며 스레드를 시작시키는 메인함수
    self, hostname, port, username, src, dst)
    '''
    flag, data = Validation()


    if flag is True:
        for i in range(len(data)):
            clss = UseSFTP(data[i]['hostname'],
                            data[i]['port'],
                            data[i]['username'],
                            data[i]['password'],
                            data[i]['src'],
                            data[i]['dst'])

            # clss.start()
        wdir =  "/home/users/h20200155/2020"
        ssh, sftp = clss.ConnectSFTP()
        fileList = clss.GetFileList(ssh, sftp, wdir)
        for f in dirList: 
            if os.path.isfile(wdir+"/"+f): 
                print (os.path.isfile(wdir+"/"+f), "DIR  : %s"%(wdir+"/"+f))
            else: 
                print (os.path.isfile(wdir+"/"+f), "FILE : %s"%(wdir+"/"+f))

        clss.CloseSFTP(sftp, ssh)

if __name__ == "__main__":
    '''
    아래와 같이 메인함수를 호출하여 테스트 하시면 됩니다.
    '''
    if _loggerflag is True:
        logger.info('START SFTP Module :D')
    else:
        print('START SFTP Module :D')
    main()
    if _loggerflag is True:
        logger.info('END SFTP Module!!')
    else:
        print('END SFTP Module!!') 