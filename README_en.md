 [中文](README.md)| **English** <!-- lang -->

# Minecraft Server Player UUID and Online Mode Converter

## 📖 Introduction
When we run our own JAVA Minecraft server, we sometimes encounter this problem: All players are using official Minecraft accounts, and the server has `online-mode` set to `true` by default. A player without an official account becomes very interested in the server and wants to join. To allow this player to join, `online-mode` must be set to `false`. This creates a new issue: the original players will lose their inventory items, advancements, and FTB quests, team data, etc.(if FTB-related mods are present), forcing them to start over.

The solution to this problem is to modify all files within the server that contain player UUIDs, changing the players' online UUIDs to their corresponding offline UUIDs.

This converter serves exactly that purpose! It can modify player UUIDs in relevant files according to your configuration while you switch the `online-mode` setting.

## 🔩 File Description

There are three files in the directory:

1.  `Info.json`
    *   **Required**. This is the file you need to configure. You must add the UUIDs for each server player, specify the files/folders where player UUIDs need to be changed, and indicate whether the UUIDs *inside* those files also need modification.

2.  `MCServer UUID and Online-mode Conventer_vanilla.py`
    *   **Optional**. This is the code I wrote myself (hence the comments are in Chinese). It can be used for switching UUIDs and Online-Mode on a vanilla server. However, the code is not very elegant, uses many if-elif statements, and lacks error detection. You can use it to learn the algorithmic approach, but it's not recommended for beginners.

3.  `MCServer UUID and Online-mode Conventer.py`
    *   **Required and Recommended**. This file is modified from `MCServer UUID and Online-mode Conventer_vanilla.py`, with enhanced requirements and improved using DeepSeek (comments are in English). It features output logs and error detection, and can perform the switch for both vanilla and modded servers based on your needs.

## 🔑 How to Use

1.  **Shut down and BACK UP your entire server and its world save folder!!!** (If your save or server gets corrupted due to using this tool without a backup, you must bear the consequences!!!)
  
2.  Install the latest version of Python.
   
3.  Clone this repository or download the ZIP file. Place both `Info.json` and `MCServer UUID and Online-mode Conventer.py` in the same directory.

4.  Open `Info.json` and configure it based on your server players' UUIDs and the files that need modification.

    * Please refer to the wiki for a detailed explanation of `Info.json` configuration.

      * `root_dir` is your server's root directory, e.g., `D:/MC Server`.

      * `changeUUID_folder_name` lists the names of folders where player UUIDs need modification. Configure this based on your actual situation and whether the file *contents* also need changes.

          For example: A vanilla world typically only requires changing the player UUID *within the filenames* inside the `advancements`, `playerdata`, and `stats` folders. A modded world, e.g., with FTB mods installed, might require changing both the UUIDs *in the filenames* and *replacing the UUIDs inside the file contents* of certain files.

      * `player` contains player information. Here you need to fill in the player's nickname (`name`), their UUID when `online-mode=true` (`Online_uuid`), and their UUID when `online-mode=false` (`Offline_uuid`).
  
          
5.  Run `MCServer UUID and Online-mode Conventer.py` with Python.

## 📄 Documentation
  * [wiki](https://github.com/skwdpy/Minecraft-Server-Player-UUID-and-Online-Mode-Converter/wiki) - Detailed instructions for configuring `Info.json`.
