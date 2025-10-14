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
            echo "--- Image Generation Setup ---"
            echo "1. Configure your PROJECT_ID in tools/image_generator.py"
            echo "2. Authenticate with Google Cloud: gcloud auth application-default login"
            echo "3. Set the quota project: gcloud auth application-default set-quota-project YOUR_PROJECT_ID"
            echo "4. Run the script: python tools/image_generator.py"
            echo ""
            echo "NOTE: Replace YOUR_PROJECT_ID in step 3 with the same project ID from step 1."
          '';
        };
      });
}