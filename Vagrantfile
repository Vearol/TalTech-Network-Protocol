Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "512"
    vb.cpus = "1"
  end

  config.vm.define "nodeA" do |machine|
    machine.vm.network "private_network", ip: "192.168.11.1"
  end

  config.vm.define "nodeB" do |machine|
    machine.vm.network "private_network", ip: "192.168.11.2"
  end

  config.vm.define "nodeC" do |machine|
    machine.vm.network "private_network", ip: "192.168.11.3"
  end

  config.vm.define "nodeD" do |machine|
    machine.vm.network "private_network", ip: "192.168.11.4"
  end
end
