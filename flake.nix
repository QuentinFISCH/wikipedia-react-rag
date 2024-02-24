{
  description = "A flake for Rele";

  inputs = {
    nixpkgs = {
      type = "github";
      owner = "NixOS";
      repo = "nixpkgs";
      ref = "nixos-23.05";
    };
    flake-utils = {
      type = "github";
      owner = "numtide";
      repo = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem [ "x86_64-linux" ] (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      rec {
        devShells.default = pkgs.mkShell
          {
            packages = with pkgs; [
              python311
              stdenv.cc.cc.lib
              xorg.libXrender
              xorg.libX11
              xorg.libXext
            ];
            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc
                pkgs.xorg.libXrender
                pkgs.xorg.libX11
                pkgs.xorg.libXext
              ]}
            '';
          };
      });
}
