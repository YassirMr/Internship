#!/bin/bash


function init-ad-hoc-network (){
    driver=$1; shift
    netname=$1; shift
    freq=$1;   shift
    phyrate=$1; shift
    antmask=$1; shift
    txpower=$1; shift
  #  ipipaddr_mask=$1; shift  

    # load the r2lab utilities - code can be found here:
    # https://github.com/parmentelat/r2lab/blob/master/infra/user-env/nodes.sh
    source /root/r2lab/infra/user-env/nodes.sh

    # make sure to use the latest code on the node
    git-pull-r2lab
    iw reg set AW
   # turn-off-wireless  
    
    ipaddr_mask=10.0.0.$(r2lab-ip)/24

    echo loading module $driver
    
 
  
  #  modprobe $driver 
  #  iw reg set AW
    iw dev moni0 del
    
    # some time for udev to trigger its rules
    sleep 1

    # install tshark on the node for the post-processing step
    apt-get install tshark
    ifname=atheros #$(wait-for-interface-on-driver $driver)  
    phyname=`iw $ifname info|grep wiphy |awk '{print "phy"$2}'`  

    echo configuring interface $ifname
    # make sure to wipe down everything first so we can run again and again
    ip address flush dev $ifname
    echo "ip link set $ifname down"
    ip link set $ifname down 
    # configure wireless
    echo "iw phy $phyname set antenna $antmask"
    iw phy $phyname set antenna $antmask    # phy1 <> phy0
    iw dev $ifname set type ibss
    # set the Tx power Atheros'range is between 5dbm (500) and 14dBm (1400)
    sleep 1
    ip link set $ifname up
    # set to ad-hoc mode and set the right PHY rate 
    echo "iw dev $ifname ibss join $netname $freq"
    iw dev $ifname ibss join $netname $freq 
    sleep 1
    echo "iw dev $ifname set txpower fixed $txpower"
    iw dev $ifname set txpower fixed $txpower
    echo "POWER!!"
    iwconfig atheros | grep Tx-Power
    ip address add $ipaddr_mask dev $ifname
    if test $freq -eq 2412
    then
 	iw dev $ifname set bitrates legacy-2.4 $phyrate
    else
 	iw dev $ifname set bitrates legacy-5 $phyrate
    fi
    echo "iw dev $ifname set bitrates legacy-2.4 $phyrate"

    # set the wireless interface in monitor mode                                                                   
    iw phy $phyname interface add moni0 type monitor
    ip link set moni0 up
    
    # then, run tcpdump with the right parameters 
    
#    tcpdump -U -W 2 -i moni0 -y ieee802_11_radio -w "/tmp/"$(hostname)".pcap"


    ### addition - would be cool to come up with something along these lines that
    # works on both cards
    # a recipe from Naoufal for Intel
    # modprobe iwlwifi
    # iwconfig wlan2 mode ad-hoc
    # ip addr add 10.0.0.41/16 dev wlan2
    # ip link set wlan2 up
    # iwconfig wlan2 essid mesh channel 1
    
}

function my-ping (){
    dest=$1; shift
    ptimeout=$1; shift
    pint=$1; shift
    psize=$1; shift
    pnumber=$1; shift
    
    echo "ping -W $ptimeout -c $pnumber -i $pint -s $psize -q $dest >& /tmp/ping.txt"
    ping -w $ptimeout -c $pnumber -i $pint -s $psize -q $dest >& /tmp/ping.txt
    result=$(grep "%" /tmp/ping.txt)
    echo "$(hostname) -> $dest: ${result}"
    return 0
}


function process-pcap (){
    i=$1; shift
    array="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37" 
    for j in `echo ${array[@]/$i}` 
    do
     tshark -r /tmp/fit"$i".pcap  -Y "ip.src==10.0.0.$j && icmp"  -Tfields -e "ip.src" -e "ip.dst" -e "radiotap.dbm_antsignal" >> /tmp/result"-$i".txt
    done
    echo "Run tshark post-processing on node fit$node"
    return 0
}



########################################
# just a wrapper so we can call the individual functions. so e.g.
# node-utilities.sh tracable-ping 10.0.0.2 20
# results in calling tracable-ping 10.0.0.2 20

"$@"
