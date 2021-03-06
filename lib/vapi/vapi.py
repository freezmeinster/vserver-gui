# -*- coding: iso-8859-1 -*-
#  Vapi adalah API tidak resmi untuk Vserver .Dibuat menggunakan bahasa pemrograman Python. 
#  
#  Vapi Didistribusikan dibawah Lisensi BSD
#   
#  Untuk info lebih lanjut silahkan kunjungi http://bramandityo.com
import os,socket,shutil,hmac,ConfigParser
from config_changer import change_sshd_config

V_PREFIX = os.popen("vserver-info APPDIR SYSINFO | grep \"prefix:\" | cut -d \":\" -f2").read().strip()
V_ROOTDIR = os.popen("vserver-info APPDIR SYSINFO | grep \"Rootdir:\" | cut -d \":\" -f2").read().strip()
V_CONFDIR = os.path.join(V_PREFIX,'etc/vservers')
API_DIR = os.path.realpath( os.path.dirname( __file__ ) )
config= ConfigParser.ConfigParser()
config.readfp(open('vapi.conf'))
HOSTNAME = socket.gethostname()

V_IP = config.get('apps','ip')
V_PORT = int(config.get('apps','port'))
V_SNAPSHOT = config.get('snapshot','store')
V_BASEPKG = config.get('vserver','v_basepkg')
V_IPPREFIX = config.get('vserver','v_ipprefix')
ALL_IP = [ V_IPPREFIX+str(x) for x in range(2,254)]
V_KEY = config.get('apps','key')

class Vps(object):
    
    on_server = False
    
    # fungsi untuk menginisasi virtual private server. Apabila VPS yang dimaksud tidak ada
    # di dalam Host server, maka attribut on_server akan bernilai False.
    
    def get(self,nama):
	#scan Vserver-Rootdir untuk mengetahui semua Vps yang ada
	vps_list = os.listdir(V_ROOTDIR)
	vps_list.remove('.pkg')
	#membandingkan apakah nama VPS yang akan1; en-us; GT-S5660 Build/FROYO) AppleWeb dibuat sudah ada atau belum 
	if nama in vps_list :
	    self.on_server = True
	    self.nama = nama
	else :
	    self.on_server = False
	    self.nama = nama
	    
	    
    # Fungsi untuk parser config dari setiap vps
    def get_conf(self):
        if self.on_server == True :
            self.vdir = os.path.join(V_CONFDIR,self.nama)      
            self.ip = open(self.vdir+'/interfaces/0/ip','r').read().strip().replace('\n','')
	    self.context = open(self.vdir+'/context','r').read().strip().replace('\n','')
            self.memory = open(self.vdir+'/cgroup/memory.limit_in_bytes','r').read().strip().replace('\n','')
        elif self.on_server == False :
            return "VPS %s not available" % self.nama 
	    
	    
    def commit_conf(self):
        if self.on_server == True :
            ip = self.ip 
            mem = str(int(self.memory)*250)
            ip_hendler = open(self.vdir+'/interfaces/0/ip','w')
            ip_hendler.write(ip)
            ip_hendler.close()
                    
            mem_hendler = open(self.vdir+'/cgroup/memory.limit_in_bytes','w')
            mem_hendler.write(mem)
            mem_hendler.close()
        elif self.on_server == False :
            return "VPS %s tidak ada" % self.nama
	
	
    def destroy(self):
        if self.on_server == True :
            shutil.rmtree(os.path.join(V_CONFDIR,self.nama))
            shutil.rmtree(os.path.join(V_ROOTDIR,self.nama))
            #print "VPS with name %s deleted" % self.nama
	elif self.on_server == False :
            return "Vps %s not Available" % self.nama
	
    def get_stat(self):
	run = os.path.exists(self.vdir+'/run')
	if run == True :
	    return "Running"
	elif run == False :
	    return "Sleep"

class VpsServer(object):
    vps_obj= list()
    vps_list = os.listdir(V_ROOTDIR)
    vps_list.remove('.pkg')
    for vps in vps_list :
	if vps != 'lost+found' :
	    VPS = Vps()
	    VPS.get(vps)
	    VPS.get_conf()
	    VPS.get_stat()
	    vps_obj.append(VPS)

    def get_registered_vps(self):
        return self.vps_obj
    
    def get_available_ip(self):
	vps_list = os.listdir(V_ROOTDIR)
	vps_list.remove('.pkg')
	for vps in vps_list :
	    if vps != 'lost+found':
		VPS = Vps()
		VPS.get(vps)
		if VPS.on_server :
		    VPS.get_conf()
		    ip = VPS.ip
		    ALL_IP.remove(ip)

	return ALL_IP
    
			

class VpsFactory(object):
    vps_server = VpsServer()
    ip = None
    ip_list = vps_server.get_available_ip()
    memory = None
    nama = None
    password = None

    def __init__(self,**kwargs):
        self.nama = kwargs['nama']
        self.memory = kwargs['memory']
        self.ip = kwargs['ip']
        self.password = kwargs['password']
    
    def valid_ip(self,ip):
	if ip in self.ip_list :
	    return True
	else : 
	    return False
	    
    def create_vps(self,ip,name,memory):
	vps_hostname = HOSTNAME.__add__("."+name+"")
	interface = "eth0:"+ip+"/24"
	home = os.path.join(V_ROOTDIR,name)
	conf = os.path.join(V_CONFDIR,name)
	base = V_BASEPKG.__add__("/*.t?z") 
	command = """
		   vserver %s build -m skeleton \
		   --hostname %s \
		   --interface %s \
		   --flags lock,virt_mem,virt_uptime,virt_cpu,virt_load,hide_netif\
		   --initstyle sysv
		  """ % (name,vps_hostname,interface)
	initcontent = """
		      #!/bin/bash
                      if [ "$1" == "3" ]; then
                         /etc/rc.d/rc.M
                      elif [ "$1" == "6" ]; then
                         /etc/rc.d/rc.6
                      else
                         echo "Invalid level."
                         exit 1
                      fi
		      """
	
	os.popen(command)
	
	os.mkdir(os.path.join(conf,'cgroup'))
	mem = open(os.path.join(conf,'cgroup/memory.limit_in_bytes'),'w')
	mem.write(""+str(memory)+"M\n")
	mem.close()
	
	swap = open(os.path.join(conf,'cgroup/memory.memsw.limit_in_bytes'),'w')
        swap.write(""+str(int(memory)+2*int(memory))+"M\n")
        swap.close()
	
	os.system("/sbin/installpkg -root "+home+" "+base+"") 
	
	shutil.copy('/etc/localtime',os.path.join(home,'etc/localtime'))
	
	hname = open(os.path.join(home,'etc/HOSTNAME'),'w')
	hname.write(vps_hostname)
	hname.close()
	
	open(os.path.join(home,'etc/fstab'),'w').close()
	open(os.path.join(home,'etc/mtab'),'w').close()
	
	hosts = open(os.path.join(home,'etc/hosts'),'a')
	hosts.write(""+ip+" "+vps_hostname+" "+name+" ")
	hosts.close()

	init = open(os.path.join(home,'etc/init.d/rc'),'w')
	init.write(initcontent)
	init.close()
	init_file = os.path.join(home,'etc/init.d/rc')
	os.system("chmod +x "+init_file+"")
	
	change_sshd_config(home,ip)
	
	os.chdir(os.path.join(home,'etc/rc.d'))
	os.system("patch -p 1 < "+os.path.join(API_DIR,'slackware.patch')+"")
	old_password = os.popen("openssl passwd "+self.password+"").read().strip()
	os.popen("chroot "+home+" /usr/sbin/usermod -p \""+old_password+"\" root") 
	

    def init_snapshot(self):
        home = os.path.join(V_ROOTDIR,self.nama)
        snap_home = os.path.join(V_SNAPSHOT,self.nama)
        os.mkdir(snap_home)
        os.popen("rsync -a --delete "+home+"/ "+snap_home+"/base/")
        #print "Snapshot directory was created"
        
    def save(self):
	if self.valid_ip(self.ip):
	    self.create_vps(self.ip,self.nama,self.memory)
	    self.init_snapshot()
	else :
	    pass
	    #print "may be you must change name or ip of new VPS , couse your desire name for vps already taken !"