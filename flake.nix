{
  description = "University: Introduction to IoT: Project (2024/11/05--2024/12/18)";
  inputs.asciidoctor-nix.url = "github:trueNAHO/asciidoctor.nix";

  outputs = inputs:
    inputs.asciidoctor-nix.mkOutputs (
      outputs: {
        packages = outputs.packages {
          inherit (inputs.self) lastModified;

          commandOptions.doctype = "book";
          inputFile = "pages/index.adoc";
          src = ./src/report;
        };
      }
    );
}
