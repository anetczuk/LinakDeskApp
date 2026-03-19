{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };
  outputs =
    {
      self,
      nixpkgs,
      utils,
    }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            gcc
            gnumake
            pkg-config
          ];

          buildInputs = with pkgs; [
            bluez
            dbus
            fontconfig
            freetype
            git
            glib
            libglvnd
            libx11
            libxcb
            libxext
            libxrender
            libxkbcommon
            python312
            stdenv.cc.cc.lib
            uv
            wayland
            xcbutil
            xcbutilimage
            xcbutilkeysyms
            xcbutilrenderutil
            xcbutilwm
            zlib
          ];

          LD_LIBRARY_PATH = "${
            pkgs.lib.makeLibraryPath (
              with pkgs;
              [
                bluez
                dbus
                fontconfig
                freetype
                glib
                libglvnd
                libx11
                libxcb
                libxext
                libxrender
                libxkbcommon
                stdenv.cc.cc.lib
                wayland
                xcbutil
                xcbutilimage
                xcbutilkeysyms
                xcbutilrenderutil
                xcbutilwm
                zlib
              ]
            )
          }:$LD_LIBRARY_PATH";

          shellHook = "";
        };
      }
    );

}
