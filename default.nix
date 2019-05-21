with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    python27
    python27Packages.virtualenv
    python27Packages.recursivePthLoader
    python27Packages.pip
    libxml2
    libxslt
    python27Packages.pillow
    python27Packages.isort
    python27Packages.flake8
    gitAndTools.pre-commit
    zlib
    zsh
  ];
}
