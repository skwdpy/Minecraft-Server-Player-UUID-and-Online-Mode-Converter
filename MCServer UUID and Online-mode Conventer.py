import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


class MinecraftUUIDConverter:
    def __init__(self, config_path: str = 'Info.json'):
        self.config = self._load_config(config_path)
        self.players = self._prepare_players()
        self.dirs = self._prepare_directories()
        self.mode_id = 0
        
        # Get Python script directory for log file location
        self.script_dir = Path(__file__).parent
        self.log_file = self.script_dir / "log.txt"
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging to file"""
        # Clear or create log file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"Minecraft Online/Offline UUID Converter (with online-mode switching)Log\n")
            f.write(f"============================\n")
            f.write(f"Log file location: {self.log_file}\n")
            f.write(f"Run time: {self._get_current_time()}\n\n")
        
        # Redirect stdout to file and console
        self.original_stdout = sys.stdout
        sys.stdout = self

    def _get_current_time(self):
        """Get current time string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def write(self, text):
        """Override write method to output to both file and console"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(text)
        self.original_stdout.write(text)

    def flush(self):
        """Override flush method"""
        self.original_stdout.flush()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.flush()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration file"""
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _prepare_players(self) -> List[Dict[str, str]]:
        """Prepare player information"""
        return [
            {
                'name': player['name'],
                'online_uuid': player['Online_UUID'],
                'offline_uuid': player['Offline_UUID']
            }
            for player in self.config['player']
        ]

    def _prepare_directories(self) -> List[Tuple[Path, bool]]:
        """Prepare directory information"""
        return [
            (Path(self.config['root_dir']) / folder['name'], folder['change_content'])
            for folder in self.config['changeUUID_folder_name']
        ]

    def _determine_mode_from_server_properties(self) -> int:
        """Determine current mode from server.properties file"""
        server_properties_path = Path(self.config['root_dir']) / "server.properties"
        
        if not server_properties_path.exists():
            raise FileNotFoundError(f"server.properties file not found: {server_properties_path}")
        
        with open(server_properties_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        online_mode_line = None
        for line in lines:
            if line.strip().startswith('online-mode='):
                online_mode_line = line.strip()
                break
        
        if online_mode_line is None:
            raise ValueError("online-mode setting not found in server.properties")
        
        # Parse online-mode value
        if '=' in online_mode_line:
            value = online_mode_line.split('=', 1)[1].strip().lower()
            if value == 'true':
                print("Current mode: Online (online-mode=true)")
                return 1  # Online -> Offline
            elif value == 'false':
                print("Current mode: Offline (online-mode=false)")
                return 2  # Offline -> Online
            else:
                raise ValueError(f"Invalid online-mode value: {value}")
        else:
            raise ValueError("Invalid online-mode line format")

    def _update_server_properties(self):
        """Update online-mode setting in server.properties"""
        server_properties_path = Path(self.config['root_dir']) / "server.properties"
        
        if not server_properties_path.exists():
            print(f"Warning: server.properties file not found: {server_properties_path}")
            return
        
        with open(server_properties_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('online-mode='):
                if self.mode_id == 1:  # Online -> Offline, need to change to false
                    new_value = 'false'
                    print("Changing online-mode to: false")
                else:  # Offline -> Online, need to change to true
                    new_value = 'true'
                    print("Changing online-mode to: true")
                
                lines[i] = f"online-mode={new_value}\n"
                updated = True
                break
        
        if updated:
            with open(server_properties_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            print("Updated server.properties file")
        else:
            print("Warning: online-mode setting not found, server.properties not updated")

    def _update_json_file(self, file_path: Path, update_callback: callable):
        """Generic JSON file update method"""
        if not file_path.exists():
            print(f"Warning: File {file_path} does not exist")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        update_callback(data)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _update_uuid_in_list(self, data: List[Dict]):
        """Update UUIDs in list data"""
        for item in data:
            for player in self.players:
                if item.get('name') == player['name']:
                    item['uuid'] = (
                        player['offline_uuid'] if self.mode_id == 1 
                        else player['online_uuid']
                    )
                    break

    def _update_usercache(self):
        """Update usercache.json"""
        usercache_path = Path(self.config['root_dir']) / "usercache.json"
        
        def update_data(data):
            self._update_uuid_in_list(data)
        
        self._update_json_file(usercache_path, update_data)

    def _update_ops(self):
        """Update ops.json"""
        ops_path = Path(self.config['root_dir']) / "ops.json"
        self._update_json_file(ops_path, self._update_uuid_in_list)

    def _update_usernamecache(self):
        """Update usernamecache.json"""
        usernamecache_path = Path(self.config['root_dir']) / "usernamecache.json"
        
        def update_data(data: Dict):
            for old_uuid, username in list(data.items()):
                for player in self.players:
                    if username == player['name']:
                        new_uuid = (
                            player['offline_uuid'] if self.mode_id == 1 
                            else player['online_uuid']
                        )
                        if old_uuid != new_uuid:
                            data[new_uuid] = data.pop(old_uuid)
                        break
        
        self._update_json_file(usernamecache_path, update_data)

    def _remove_hyphens(self, uuid: str) -> str:
        """Remove hyphens from UUID"""
        return uuid.replace('-', '')

    def _update_file_content(self, file_path: Path):
        """Update UUIDs in file content"""
        if not file_path.exists():
            return
        
        file_extension = file_path.suffix.lower()
        
        if file_extension == '.json':
            self._update_json_file_content(file_path)
        elif file_extension == '.snbt':
            self._update_snbt_file_content(file_path)
        else:
            self._update_binary_file_content(file_path)

    def _update_json_file_content(self, file_path: Path):
        """Update UUIDs in JSON file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            for player in self.players:
                # Get current UUID and target UUID
                current_uuid = (
                    player['online_uuid'] if self.mode_id == 1 
                    else player['offline_uuid']
                )
                target_uuid = (
                    player['offline_uuid'] if self.mode_id == 1 
                    else player['online_uuid']
                )
                
                # Replace UUID with hyphens
                content = content.replace(current_uuid, target_uuid)
                
                # Replace UUID without hyphens
                current_uuid_no_hyphen = self._remove_hyphens(current_uuid)
                target_uuid_no_hyphen = self._remove_hyphens(target_uuid)
                content = content.replace(current_uuid_no_hyphen, target_uuid_no_hyphen)
            
            # Write file if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated JSON file content: {file_path.name}")
                
        except Exception as e:
            print(f"Error updating JSON file content {file_path}: {e}")

    def _update_snbt_file_content(self, file_path: Path):
        """Update UUIDs in SNBT file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            for player in self.players:
                # Get current UUID and target UUID
                current_uuid = (
                    player['online_uuid'] if self.mode_id == 1 
                    else player['offline_uuid']
                )
                target_uuid = (
                    player['offline_uuid'] if self.mode_id == 1 
                    else player['online_uuid']
                )
                
                # UUID in SNBT files may exist in various forms:
                # 1. String with hyphens
                # 2. String without hyphens
                # 3. Possibly quoted
                
                # Replace UUID with hyphens (handle quoted cases)
                content = content.replace(f'"{current_uuid}"', f'"{target_uuid}"')
                content = content.replace(f"'{current_uuid}'", f"'{target_uuid}'")
                content = content.replace(current_uuid, target_uuid)
                
                # Replace UUID without hyphens
                current_uuid_no_hyphen = self._remove_hyphens(current_uuid)
                target_uuid_no_hyphen = self._remove_hyphens(target_uuid)
                content = content.replace(f'"{current_uuid_no_hyphen}"', f'"{target_uuid_no_hyphen}"')
                content = content.replace(f"'{current_uuid_no_hyphen}'", f"'{target_uuid_no_hyphen}'")
                content = content.replace(current_uuid_no_hyphen, target_uuid_no_hyphen)
            
            # Write file if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated SNBT file content: {file_path.name}")
                
        except Exception as e:
            print(f"Error updating SNBT file content {file_path}: {e}")

    def _update_binary_file_content(self, file_path: Path):
        """Update UUIDs in binary file content (like .dat files)"""
        try:
            with open(file_path, 'rb') as file:
                content_bytes = file.read()
            
            original_content_bytes = content_bytes
            
            for player in self.players:
                # Get current UUID and target UUID
                current_uuid = (
                    player['online_uuid'] if self.mode_id == 1 
                    else player['offline_uuid']
                )
                target_uuid = (
                    player['offline_uuid'] if self.mode_id == 1 
                    else player['online_uuid']
                )
                
                # Replace UUID with hyphens (convert to bytes)
                current_uuid_bytes = current_uuid.encode('utf-8')
                target_uuid_bytes = target_uuid.encode('utf-8')
                content_bytes = content_bytes.replace(current_uuid_bytes, target_uuid_bytes)
                
                # Replace UUID without hyphens
                current_uuid_no_hyphen = self._remove_hyphens(current_uuid)
                target_uuid_no_hyphen = self._remove_hyphens(target_uuid)
                current_uuid_no_hyphen_bytes = current_uuid_no_hyphen.encode('utf-8')
                target_uuid_no_hyphen_bytes = target_uuid_no_hyphen.encode('utf-8')
                content_bytes = content_bytes.replace(current_uuid_no_hyphen_bytes, target_uuid_no_hyphen_bytes)
            
            # Write file if content changed
            if content_bytes != original_content_bytes:
                with open(file_path, 'wb') as file:
                    file.write(content_bytes)
                print(f"Updated binary file content: {file_path.name}")
                
        except Exception as e:
            print(f"Error updating binary file content {file_path}: {e}")

    def _rename_player_files(self, dir_path: Path, change_content: bool):
        """Rename player data files and update file content if needed"""
        # Define file extension patterns to process
        file_patterns = [
            ('_cyclic.dat', ''),     # uuid_cyclic.dat - put this first!
            ('.json', ''),           # uuid.json
            ('.dat_old', ''),        # uuid.dat_old
            ('.dat', ''),            # uuid.dat
            ('.snbt', ''),           # uuid.snbt
        ]
        
        for file_path in dir_path.iterdir():
            if not file_path.is_file():
                continue
                
            for pattern_suffix, special_handler in file_patterns:
                if file_path.name.endswith(pattern_suffix):
                    # First rename the file
                    renamed = self._process_single_file(file_path, pattern_suffix)
                    
                    # If content update is needed, update file content
                    if change_content and renamed:
                        self._update_file_content(renamed)
                    break

    def _process_single_file(self, file_path: Path, pattern_suffix: str) -> Path:
        """Process single file rename, return renamed file path"""
        filename = file_path.name
        
        # Extract UUID part based on different file suffixes
        if pattern_suffix == '_cyclic.dat':
            # For _cyclic.dat files, remove _cyclic.dat suffix to get UUID
            stem = filename[:-11]  # _cyclic.dat is 11 characters
        elif pattern_suffix == '.json':
            stem = file_path.stem  # Direct filename without .json
        elif pattern_suffix == '.dat_old':
            stem = filename[:-8]   # Remove .dat_old (8 characters)
        elif pattern_suffix == '.dat':
            stem = file_path.stem  # Direct filename without .dat
        elif pattern_suffix == '.snbt':
            stem = file_path.stem  # Direct filename without .snbt
        else:
            return file_path
        
        # Find matching player and rename
        for player in self.players:
            # Determine current UUID based on current mode
            if self.mode_id == 1:  # Online -> Offline
                current_uuid = player['online_uuid']
                target_uuid = player['offline_uuid']
            else:  # Offline -> Online
                current_uuid = player['offline_uuid']
                target_uuid = player['online_uuid']
            
            if stem == current_uuid:
                # Build new filename
                if pattern_suffix == '_cyclic.dat':
                    new_filename = f"{target_uuid}_cyclic.dat"
                elif pattern_suffix == '.json':
                    new_filename = f"{target_uuid}.json"
                elif pattern_suffix == '.dat_old':
                    new_filename = f"{target_uuid}.dat_old"
                elif pattern_suffix == '.dat':
                    new_filename = f"{target_uuid}.dat"
                elif pattern_suffix == '.snbt':
                    new_filename = f"{target_uuid}.snbt"
                
                new_path = file_path.parent / new_filename
                
                # Only rename if new filename is different from original
                if new_path != file_path:
                    file_path.rename(new_path)
                    print(f"Renamed: {file_path.name} -> {new_path.name}")
                    return new_path
                else:
                    print(f"No rename needed: {file_path.name} (same filename)")
                    return file_path
        
        return file_path

    def convert(self):
        """Main conversion method"""
        try:
            # Determine current mode from server.properties
            self.mode_id = self._determine_mode_from_server_properties()
            
            if self.mode_id == 1:
                print("Mode Change: Online -> Offline")
            else:
                print("Mode Change: Offline -> Online")

            # Update UUID configuration files
            self._update_usercache()
            self._update_ops()
            self._update_usernamecache()

            # Process all directories
            for dir_path, change_content in self.dirs:
                print(f"Processing directory: {dir_path} (update content: {change_content})")
                self._rename_player_files(dir_path, change_content)

            # Finally update server.properties
            self._update_server_properties()

            print("Conversion completed!")
            print(f"Detailed log saved to: {self.log_file}")

        except Exception as e:
            print(f"Error during conversion: {e}")
            raise
        finally:
            # Restore stdout
            sys.stdout = self.original_stdout


def main():
    """Main function"""
    try:
        converter = MinecraftUUIDConverter()
        converter.convert()
    except FileNotFoundError:
        print("Error: Configuration file Info.json not found")
    except json.JSONDecodeError:
        print("Error: Configuration file format is incorrect")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()