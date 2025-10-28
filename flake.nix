{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    };

    outputs = { nixpkgs, ... } @inputs:
        let
            forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ];
        in {
            devShells = forAllSystems (system: 
                let
                    pkgs = import nixpkgs { inherit system; };
                in {
                    default = pkgs.mkShell {
                        packages = with pkgs; [
                            uv
                            python313
                        ];

                        shellHook = ''
                            exec zsh
                        '';
                    };
                }
            );
    };
}
