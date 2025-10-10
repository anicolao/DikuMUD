{
  description = "A development environment for the Barsoom MUD website";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        # Python dependencies
        python-packages = ps: with ps; [
          google-cloud-aiplatform
        ];

        python-with-packages = pkgs.python3.withPackages python-packages;

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            # Python environment
            python-with-packages

            # Google Cloud SDK for authentication
            pkgs.google-cloud-sdk

            # General tools
            pkgs.bashInteractive
          ];

          shellHook = ''
            echo "Barsoom MUD development environment loaded."
            echo "-------------------------------------------"
            echo "Available tools: python, gcloud"
            echo ""
            echo "To generate images, first configure your PROJECT_ID in tools/image_generator.py"
            echo "Then run: gcloud auth application-default login"
            echo "Finally, run: python tools/image_generator.py"
          '';
        };
      });
}