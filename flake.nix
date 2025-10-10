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
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            # Python environment
            pkgs.python3
            pkgs.python3Packages.pip
            pkgs.python3Packages.venv

            # Google Cloud SDK for authentication
            pkgs.google-cloud-sdk

            # General tools
            pkgs.bashInteractive
          ];

          shellHook = ''
            echo "Barsoom MUD development environment loaded."
            echo "-------------------------------------------"

            # Set up a virtual environment
            if [ ! -d ".venv" ]; then
              echo "Creating Python virtual environment..."
              python -m venv .venv
            fi

            source .venv/bin/activate

            # Install dependencies if they haven't been installed yet
            if [ ! -f ".venv/installed-requirements" ] || [ "requirements.txt" -nt ".venv/installed-requirements" ]; then
              echo "Installing Python dependencies from requirements.txt..."
              pip install -r requirements.txt
              touch .venv/installed-requirements
            fi

            echo ""
            echo "Virtual environment activated."
            echo "Available tools: python, pip, gcloud"
            echo ""
            echo "To generate images, first configure your PROJECT_ID in tools/image_generator.py"
            echo "Then run: gcloud auth application-default login"
            echo "Finally, run: python tools/image_generator.py"
          '';
        };
      });
}