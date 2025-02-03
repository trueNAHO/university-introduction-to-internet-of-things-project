pkgs.dockerTools.buildImage {
  config.Cmd = ["mongod" "--bind_ip_all"];

  fromImage = pkgs.dockerTools.pullImage {
    finalImageName = "mongo";
    finalImageTag = "5.0.31-focal";
    hash = "sha256-pnc6tcxAArXZVSbAyLb5RILrpSy/HmUAT+32sA9LGTg=";
    imageDigest = "sha256:f7a950ee4a1cc048300cd3b3da3e939974eb8278525101ac917dbed1a3ce3d51";
    imageName = "mongo";
  };

  name = "mongo";
  tag = "latest";
}
