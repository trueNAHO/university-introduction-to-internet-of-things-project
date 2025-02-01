{
  description = "University: Introduction to IoT: Project (2024/11/05--2024/12/18)";

  inputs = {
    asciidoctor-nix.url = "github:trueNAHO/asciidoctor.nix";
    flake-utils.follows = "asciidoctor-nix/flake-utils";
    nixpkgs.follows = "asciidoctor-nix/nixpkgs";
  };

  outputs = inputs:
    inputs.flake-utils.lib.eachDefaultSystemPassThrough (
      system: let
        lib = inputs.asciidoctor-nix.mkLib pkgs.lib;

        mkOutputs = name:
          inputs.asciidoctor-nix.mkOutputs {
            checks.hooks = {
              autoflake.enable = true;
              isort.enable = true;
              mypy.enable = true;
              pyright.enable = true;
              ruff-format.enable = true;
              ruff.enable = true;
            };

            devShells.packages = lib.singleton (
              pkgs.python3.withPackages (_: [])
            );

            packages = {
              inherit (inputs.self) lastModified;
              inherit name;

              commandOptions.doctype = "book";
              inputFile = "pages/index.adoc";
              src = ./src + "/${name}";
            };
          };

        pkgs = inputs.nixpkgs.legacyPackages.${system};
      in
        lib.asciidoctor.mergeAttrsMkMerge [
          (
            inputs.flake-utils.lib.eachDefaultSystem (
              _: {
                packages = lib.fix (
                  self: {
                    application-default = pkgs.stdenvNoCC.mkDerivation {
                      buildPhase = let
                        out = "${builtins.placeholder "out"}/share/src";
                      in ''
                        mkdir --parents ${out}
                        zip --recurse-paths ${out}/application.zip .
                      '';

                      name = "application-default";
                      nativeBuildInputs = [pkgs.zip];
                      postPatch = "cp ${./LICENSE} LICENSE";
                      src = src/application;
                    };

                    application-default-external = self.application-default;
                    application-default-local = self.application-default;

                    application-mongo-external = self.application-mongo-local;

                    application-mongo-local = pkgs.dockerTools.buildImage {
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
                    };

                    default = pkgs.buildEnv {
                      name = "default";

                      paths = lib.attrsets.attrValues (
                        lib.filterAttrs
                        (name: _: lib.hasSuffix "-default" name)
                        inputs.self.packages.${system}
                      );
                    };

                    default-external = pkgs.buildEnv {
                      name = "default-external";

                      paths = lib.attrsets.attrValues (
                        lib.filterAttrs
                        (name: _: lib.hasSuffix "-default-external" name)
                        inputs.self.packages.${system}
                      );
                    };

                    default-local = pkgs.buildEnv {
                      name = "default-local";

                      paths = lib.attrsets.attrValues (
                        lib.filterAttrs
                        (name: _: lib.hasSuffix "-default-local" name)
                        inputs.self.packages.${system}
                      );
                    };
                  }
                );
              }
            )
          )

          (mkOutputs "presentation")
          (mkOutputs "report")
        ]
    );
}
