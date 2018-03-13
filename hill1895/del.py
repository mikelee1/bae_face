#!/usr/bin/env python
# encoding=utf-8

import urllib, urllib2, cookielib, re, sys, threading,time

myemail = '1430086923@qq.com'
mypassword = 'renren1212'


class Renren(threading.Thread):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.origURL = 'http://www.renren.com/Home.do'
        self.domain = 'renren.com'
        self.cj = cookielib.LWPCookieJar()

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def login(self):
        params = {'email': self.email, 'password': self.password, 'origURL': self.origURL, 'domain': self.domain}
        req = urllib2.Request(
            'http://www.renren.com/PLogin.do',
            urllib.urlencode(params)
        )
        r = self.opener.open(req)
        tmp = r.read()
        self.myid = re.search(r'http://www.renren.com/(\d+)', tmp).group(1)
        self.myid = '332098384'
        print(self.myid)

    def friends(self):
        print ("Get my friends")
        f,imgs,names = self.getmyfriends()
        print ("friends list")
        print (f, len(f))

        # todo
        self.todolist = f
        self.donelist = []

        # write data
        fdata = open('data00.txt', 'w')
        for item in f:
            fdata.write(item + ' ')
        fdata.close()

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}


        for i in range(len(imgs)):
            with open('pachongimgs/'+f[i]+'.jpg','w') as f_file:
                request = urllib2.Request(imgs[i], headers=headers)
                page = urllib2.urlopen(request)
                tmpdat = page.read()
                f_file.write(tmpdat)
            # urllib.urlretrieve(imgs[i],'pachongimgs/'+names[i]+'.png')
            # time.sleep(1)





    def realfun(self, x):

        for i in range(10):
            rrid = self.getone()
            if rrid == 1:
                break
            print (rrid)
            f,imgs,names = self.getfriends(rrid)
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}


            for i in range(len(imgs)):
                with open('pachongimgs/'+f[i]+'.jpg','w') as f_file:
                    request = urllib2.Request(imgs[i], headers=headers)
                    page = urllib2.urlopen(request)
                    tmpdat = page.read()
                    f_file.write(tmpdat)



    def realrun(self):
        th1 = threading.Thread(target=self.realfun, args=('1'))
        th2 = threading.Thread(target=self.realfun, args=('2'))
        th3 = threading.Thread(target=self.realfun, args=('3'))
        # # th4 = threading.Thread(target=self.realfun, args=('4'))
        # # th5 = threading.Thread(target=self.realfun, args=('5'))
        # # th6 = threading.Thread(target=self.realfun, args=('6'))
        # # th7 = threading.Thread(target=self.realfun, args=('7'))
        # # th8 = threading.Thread(target=self.realfun, args=('8'))
        # # th9 = threading.Thread(target=self.realfun, args=('9'))
        th1.start()
        th2.start()
        th3.start()
        # # th4.start()
        # # th5.start()
        # # th6.start()
        # # th7.start()
        # # th8.start()
        # # th9.start()
        # pass

    # def getfriends(self, rrid):
    #     friends = []
    #     count = 0
    #
    #     while True:
    #         count1 = str(count)
    #         req = "http://friend.renren.com/GetFriendList.do?curpage=" + count1 + '&id=' + str(rrid)
    #         print ('Get', req)
    #         r = self.opener.open(req)
    #         data = r.read()
    #         f = re.findall('<a id="addFriend(\d{5,15})"', data)
    #         friends = friends + f
    #         count = count + 1
    #         if f == [] or count>0:
    #             return friends
    def getfriends(self,rrid):
        friends = []
        imgs = []
        names = []
        count = 0
        try:
            with open('havedown.txt','r') as f:
                havedown = f.read().strip().split(' ')
        except:
            havedown = []

        while True:
            print(count)
            img = []
            count1 = str(count)
            req = "http://friend.renren.com/GetFriendList.do?curpage=" + count1 + '&id=' + str(rrid)
            print ('Get', req)
            r = self.opener.open(req)
            data = r.read()
            # data = str(data,'utf-8')
            f = re.findall('Poke.do\?id=(\d{5,15})" oncl', data)

            friendprofile = re.findall('<a href="(http://www.renren.com/profile.do\?id=.*?)">',data)
            for i in range(len(friendprofile)):
                if friendprofile[i] in havedown:
                    continue
                tmpdata = urllib2.urlopen(friendprofile[i]).read()
                friendimg = re.findall('<img.*src="(.*?)".*userpic',tmpdata)
                print(friendimg)
                try:

                    img.append(friendimg[0])
                except:
                    print('break')

                    break
                havedown.append(friendprofile[i])

                # time.sleep(1)

            print(img)

            # img = re.findall('src="(http://hdn.*?jpg)', data)
            b = re.findall('src="http://hdn.*?jpg.*\((.*?)\)', data)

            names = names + b
            friends = friends + f
            imgs.extend(img)
            count = count + 1
            if f == [] :
                with open('havedown.txt', 'w') as f:
                    f.write(' '.join(havedown))
                return friends,imgs,names



    def getmyfriends(self):
        friends = []
        imgs = []
        names = []
        count = 0
        try:
            with open('havedown.txt','r') as f:
                havedown = f.read().strip().split(' ')
        except:
            havedown = []

        while True:
            print(count)
            img = []
            count1 = str(count)
            req = "http://friend.renren.com/GetFriendList.do?curpage=" + count1 + '&id=' + str(self.myid)
            print ('Get', req)
            r = self.opener.open(req)
            data = r.read()
            # data = str(data,'utf-8')
            f = re.findall('Poke.do\?id=(\d{5,15})" oncl', data)

            friendprofile = re.findall('<a href="(http://www.renren.com/profile.do\?id=.*?)">',data)
            for i in range(len(friendprofile)):
                if friendprofile[i] in havedown:
                    continue
                tmpdata = urllib2.urlopen(friendprofile[i]).read()
                friendimg = re.findall('<img.*src="(.*?)".*userpic',tmpdata)
                print(friendimg)
                try:

                    img.append(friendimg[0])
                except:
                    print('break')
                    break
                havedown.append(friendprofile[i])

                # time.sleep(1)


            # img.pop(0)
            print(img)

            # img = re.findall('src="(http://hdn.*?jpg)', data)
            b = re.findall('src="http://hdn.*?jpg.*\((.*?)\)', data)

            names = names + b
            friends = friends + f
            imgs.extend(img)
            count = count + 1
            if f == [] or count>0:
                with open('havedown.txt', 'w') as f:
                    f.write(' '.join(havedown))
                return friends,imgs,names

    def getone(self):
        if self.todolist == []:
            print ("Empty todo list")
            return 1
        popup = self.todolist[0]
        self.donelist.append(popup)
        del self.todolist[0]
        return popup


def down():
    f= ['223438632', '243793087', '244862622', '244294110', '232244690', '200760107', '244995083', '223668788', '231006189', '244279311', '239325029', '227628635', '239147872', '240158483', '239980246', '243092645', '244432629', '223610984', '229556679', '230132728', '249348011', '247464868', '249762381', '253867986', '252168926', '250357425', '251716817', '249111940', '253757544', '250268562', '248501017', '249659970', '254877953', '253399999', '249030251', '250406257', '248323420', '252318998', '248110938', '250599155', '257432006', '264985021', '261090576', '255121268', '256543272', '263166303', '265077688', '259574824', '265129728', '263407620', '264057281', '264797566', '264407547', '265067566', '264464006', '264627986', '263402519', '263619663', '264633077', '261898614', '278332513', '278065110', '279578548', '266091072', '278154590', '265794627', '275460015', '277739491', '273872075', '276627635', '266552741', '265840443', '276039423', '268364554', '275766409', '279333366', '277181613', '266475461', '272370519', '278001895', '282283761', '287158026', '281277760', '290604755', '281386658', '282260042', '289218326', '287395693', '280011540', '282251011', '290372477', '285710101', '288516758', '282516510', '282915011', '291975683', '281981893', '282658987', '288331741', '281117083', '302622736', '303887586', '303841167', '299229549', '302363647', '304815857', '301150451', '293985044', '301473286', '302100474', '301252877', '299938257', '300203976', '304984419', '299253648', '293868373', '300389556', '298443325', '304011972', '302478068']
    imgs= ['http://hdn.xnimg.cn/photos/hdn421/20150726/2330/h_main_ykoi_c3110000647c1986.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20150204/1945/h_main_IZse_4f8c00001d251986.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20121218/2310/h_main_OrSl_4e25000003891375.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20121112/1000/h_main_UTI7_7a780000470d1375.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20120815/2145/h_main_2C4o_0f3600008e281375.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20130509/1530/h_main_yA9j_c2b70000040e113e.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20160107/1035/main_UZxT_725c00008b77195a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20140526/1900/h_main_HtCU_27f500017f891986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20131011/0740/h_main_nNlT_516b00000375113e.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20131203/0925/h_main_HoyY_529200008e05113e.jpg', 'http://hd53.xiaonei.com/photos/hd53/20080904/16/00/main_0RnX_5060o200150.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20150904/1415/h_main_XCF5_faa600023bc4195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20110709/1150/h_main_Ue5d_1fb50000d0762f76.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20120925/2155/h_main_yPIa_5a39000024091375.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20150816/1440/h_main_8t19_48590001fd48195a.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20151122/0905/h_main_9mb1_b0dc0001e5c8195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20150522/0155/h_main_rZuu_6a0d0000a3b81986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20130407/0655/h_main_KYz5_11cf0000002c111a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20130922/1430/h_main_kMlG_d9530000007b111a.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20140729/2215/h_main_WGmz_a050000236361986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20110624/2310/h_main_ng0Q_635c000355652f75.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20111023/0900/main_hkvs_82811i019117.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20140420/1845/h_main_ordW_107000015363113e.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20130521/1110/h_main_iyCA_527d00000180113e.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20140823/0805/h_main_gLzj_8d97000394061986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20130405/2355/h_main_aTaU_ec49000001c2113e.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20150519/2250/h_main_mZzr_48590000ee30195a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20141108/0030/h_main_aviu_e0f900046498195a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20140822/1020/h_main_ICXN_27dd0004c2ea1986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20160602/1030/h_main_BfrV_1a170003813d1986.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130128/0445/h_main_oEri_cf66000003a9111a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20150129/0100/h_main_8OK8_954b00009a53195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20101015/0425/h_main_1zXg_407500015eee2f74.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20110613/1020/main_bjOa_186515b019118.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20130813/1015/h_main_3duo_95af00000112113e.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20120508/1555/h_main_0LmZ_25a0000051ad2f76.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20140712/2105/h_main_MMa3_27bd0003756a1986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20140415/1405/h_main_ptFw_328700010a2d111a.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130415/1455/h_main_eaEB_326d0000043d113e.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20130803/1040/h_main_of48_a3a800000217111a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20130128/1230/h_main_qerK_79490000022c113e.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20100509/1325/main_4wjV_12754j019118.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20130518/0615/h_main_5fPA_7b4100000e98113e.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20100824/0735/h_main_QUtO_02d60001afa82f74.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20140913/2355/h_main_gufE_e0f90002d107195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20121013/1050/h_main_NFzP_46c0000092a61375.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20110814/1320/h_main_MiAn_68e500036d802f75.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20140815/0755/h_main_QvmL_27bd00048dbe1986.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20121104/0155/h_main_gaQ7_348f000010881376.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130730/2000/h_main_rcbq_a5f200000175113e.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20150128/1405/h_main_vWup_ae990005f4181986.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20141103/1740/h_main_DuD5_e14100044160195a.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20100304/0930/h_main_dHwV_507c0006059d2f76.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20140607/2335/h_main_1OXJ_0eac000123e3195a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20160307/0035/h_main_Z2uN_b11500014b9c195a.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20150619/0130/h_main_Czwl_781200014c021986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20140801/0240/h_main_ygWJ_e1230001812f195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20130428/0955/h_main_gltL_1ae300000364111a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20131003/1440/h_main_K9Ea_943f0000059d111a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20130605/2345/main_KGiU_f93b00040e89111a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20131105/0100/h_main_WfCg_8a2800000b85113e.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20110411/2350/h_main_3af6_101600016cae2f74.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20150610/1920/h_main_UDmn_774800006c37195a.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20151231/0940/h_main_NxCr_4e920000c8971986.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20120620/2155/h_main_yiki_1830000003b21376.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20100503/1545/h_main_lHsZ_6afb000203322f74.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20120522/2320/h_main_YGKa_6a8b000004331375.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20141113/0420/h_main_Ia8g_e1350004878a195a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20110821/0240/h_main_R1k4_692c0003f3022f75.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130923/0050/h_main_33Wt_d953000009db111a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20141117/0130/h_main_O6BM_8d970005ff881986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20131231/1525/h_main_Rxk7_5fa50001e6e9111a.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20140714/1350/h_main_UEwk_27f50003840c1986.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130424/1530/h_main_dyuk_974f00000069111a.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20120329/0115/h_main_ltUz_5f430002f5512f75.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20160817/2055/h_main_zkLw_faa6000531c9195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20141031/1235/main_nYcT_53f80001f9581986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20140608/1030/h_main_Cx05_8d970000f8f91986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20150118/0110/h_main_vRs8_8d64000134b11986.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20110923/2220/h_main_Ivhi_615c000028272f76.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20140620/0300/h_main_VmgM_e12f0000167f195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20140418/1700/h_main_sgG1_17dc0002f7be111a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20120523/2210/h_main_Vo9a_37800000009c1376.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20170412/1225/h_main_bvNv_b11500062ed1195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20130102/0200/h_main_l6vH_6af2000004a51376.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130904/0630/h_main_TfLd_8e6100000241113e.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20140927/0105/h_main_UEwV_d68f000320e4195a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20140629/2145/main_ptGa_5418000037bf1986.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20141130/1710/h_main_SOQB_e1230004f28b195a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20140801/2215/h_main_FiHE_e13b00018928195a.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20130313/1505/h_main_bBNt_d10900001131111a.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20140504/2130/h_main_vWGY_27d700004a9b1986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20130626/1340/h_main_at9w_a4c4000004e0113e.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20130611/1055/h_main_jnXH_910700001de4111a.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20150721/1240/main_l0zi_747d00040e0a195a.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20121002/2330/h_main_jzij_2bca000075cd1376.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20151207/1330/h_main_ag48_c3110001ecda1986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20141103/2030/h_main_CKzB_e0f900044268195a.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20121021/2155/h_main_SIki_16e6000015f31376.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20110304/1330/main_UNtK_250246i019118.jpg', 'http://hdn.xnimg.cn/photos/hdn421/20130605/1315/h_main_By69_c457000001e6113e.jpg', 'http://hdn.xnimg.cn/photos/hdn221/20121012/1150/main_T3kn_73e30002d4091375.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20131209/1440/h_main_lo8K_24490000ce32113e.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20160127/0640/h_main_d3Ta_bc2300004dea195a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20121020/1550/h_main_yoRJ_3589000066261375.jpg', 'http://hdn.xnimg.cn/photos/hdn121/20130531/2100/h_main_HQQS_353e000007d8111a.jpg', 'http://hdn.xnimg.cn/photos/hdn321/20140508/2240/h_main_s2GP_27ef0000820b1986.jpg', 'http://hdn.xnimg.cn/photos/hdn521/20140516/2010/h_main_Dnja_8fd600006b261986.jpg']
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}

    for i in range(len(imgs)):
        try:
            with open('pachongimgs/' + f[i] + '.jpg', 'w') as f_file:
                request = urllib2.Request(imgs[i], headers=headers)
                page = urllib2.urlopen(request)
                tmpdat = page.read()
                f_file.write(tmpdat)
        except:
            print('what')

if __name__ == "__main__":
    # a = Renren(myemail, mypassword)
    # print ("your account and password are %s %s" % (myemail, mypassword))
    # a.login()
    # with open('data00.txt','r') as con:
    #     tmpda = con.read()
    #     f = tmpda.strip().split(' ')
    #
    # a.todolist = f
    # a.donelist = []
    # a.friends()
    # a.realrun()
    down()
