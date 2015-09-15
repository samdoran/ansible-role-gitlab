Vagrant.configure(2) do |config|

  config.vm.define :gitlab do |cos6|
    cos6.vm.box = "geerlingguy/centos6"
    cos6.vm.provider :virtualbox do |p|
      p.memory = 2048
      p.customize ["modifyvm", :id, "--paravirtprovider", "kvm"]
    end

    cos6.vm.network "private_network", type: "dhcp"
    cos6.vm.network "forwarded_port", guest: 80, host: 8080
    cos6.vm.network "forwarded_port", guest: 443, host: 8443


    cos6.vm.hostname = "gitlabcos6.acme.com"
  end

  config.vm.provision "ansible" do |a|
    a.playbook = "tests/vagrant.yml"
  end

end
