Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "512"
    vb.cpus = "1"
  end

  config.vm.define "nodeA" do |machine|
    machine.vm.hostname = "NodeA"
    machine.vm.network "private_network", ip: "192.168.11.2"
    machine.vm.provision "shell", inline: "git clone https://github.com/Vearol/TalTech-Network-Protocol.git /home/vagrant/Network-Protocol"
  end

  config.vm.define "nodeB" do |machine|
    machine.vm.hostname = "NodeB"
    machine.vm.network "private_network", ip: "192.168.11.3"
    machine.vm.provision "shell", inline: "git clone https://github.com/Vearol/TalTech-Network-Protocol.git /home/vagrant/Network-Protocol"
  end

  config.vm.define "nodeC" do |machine|
    machine.vm.hostname = "NodeC"
    machine.vm.network "private_network", ip: "192.168.11.4"
    machine.vm.provision "shell", inline: "git clone https://github.com/Vearol/TalTech-Network-Protocol.git /home/vagrant/Network-Protocol"
  end

  config.vm.define "nodeD" do |machine|
    machine.vm.hostname = "NodeD"
    machine.vm.network "private_network", ip: "192.168.11.5"
    machine.vm.provision "shell", inline: "git clone https://github.com/Vearol/TalTech-Network-Protocol.git /home/vagrant/Network-Protocol"
  end
end
