Vagrant.configure(2) do |config|

  config.dns.tld = "dev"
  config.dns.patterns = [/^.*vagrant.dev$/]

  config.vm.define :gitlab do |cos6|
    cos6.vm.box = "geerlingguy/centos6"
    cos6.vm.provider :virtualbox do |p|
      p.memory = 2048
      p.customize ["modifyvm", :id, "--paravirtprovider", "kvm"]
    end

    cos6.vm.network "private_network", ip: "55.55.55.17"
    cos6.vm.hostname = "gitlab.vagrant.dev"
  end

  config.vm.provision "ansible" do |a|
    a.playbook = "tests/vagrant.yml"
  end

end
