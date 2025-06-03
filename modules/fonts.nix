# modules/fonts.nix
{ config, pkgs, ... }:

{
  fonts = {
    enableDefaultPackages = true;

    fontconfig = {
      enable = true;

      defaultFonts = {
        monospace = [ "JetBrainsMono Nerd Font" ];
        sansSerif = [ "Inter" "Noto Sans" ];
        serif = [ "Noto Serif" ];
      };
    };
  };

  environment.systemPackages = with pkgs; [
    (pkgs.nerdfonts.override { fonts = [ "JetBrainsMono" ]; })
    pkgs.inter
    pkgs.noto-fonts
  ];
}
