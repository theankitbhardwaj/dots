#!/usr/bin/env python3
"""
OpenRGB Profile Changer Script
Connects to OpenRGB server and changes lighting profiles
"""

import sys
import argparse
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

def connect_to_server(host="127.0.0.1", port=6742):
    """
    Connect to OpenRGB server
    
    Args:
        host (str): Server hostname or IP address
        port (int): Server port number
    
    Returns:
        OpenRGBClient: Connected client instance or None if failed
    """
    try:
        print(f"Connecting to OpenRGB server at {host}:{port}...")
        client = OpenRGBClient(host, port, "ProfileChanger")
        print("Successfully connected to OpenRGB server")
        return client
    except Exception as e:
        print(f"Failed to connect to OpenRGB server: {e}")
        return None

def list_profiles(client):
    """
    List available profiles
    
    Args:
        client (OpenRGBClient): Connected OpenRGB client
    """
    try:
        profiles = client.get_profiles()
        if not profiles:
            print("No profiles found")
            return
        
        print("\nAvailable profiles:")
        for i, profile in enumerate(profiles):
            print(f"  {i}: {profile}")
    except Exception as e:
        print(f"Error listing profiles: {e}")

def load_profile(client, profile_name):
    """
    Load a specific profile
    
    Args:
        client (OpenRGBClient): Connected OpenRGB client
        profile_name (str): Name of the profile to load
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Loading profile: {profile_name}")
        client.load_profile(profile_name)
        print(f"Successfully loaded profile: {profile_name}")
        return True
    except Exception as e:
        print(f"Error loading profile '{profile_name}': {e}")
        return False

def save_current_as_profile(client, profile_name):
    """
    Save current RGB state as a new profile
    
    Args:
        client (OpenRGBClient): Connected OpenRGB client
        profile_name (str): Name for the new profile
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Saving current state as profile: {profile_name}")
        client.save_profile(profile_name)
        print(f"Successfully saved profile: {profile_name}")
        return True
    except Exception as e:
        print(f"Error saving profile '{profile_name}': {e}")
        return False

def delete_profile(client, profile_name):
    """
    Delete a profile
    
    Args:
        client (OpenRGBClient): Connected OpenRGB client
        profile_name (str): Name of the profile to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Deleting profile: {profile_name}")
        client.delete_profile(profile_name)
        print(f"Successfully deleted profile: {profile_name}")
        return True
    except Exception as e:
        print(f"Error deleting profile '{profile_name}': {e}")
        return False

def list_devices(client):
    """
    List connected RGB devices
    
    Args:
        client (OpenRGBClient): Connected OpenRGB client
    """
    try:
        devices = client.get_devices_by_type(DeviceType.DRAM)
        if not devices:
            print("No RGB devices found")
            return
        
        print(f"\nFound {len(devices)} RGB device(s):")
        for i, device in enumerate(devices):
            print(f"  {i}: {device.name} ({device.type})")
            print(f"     Modes: {len(device.modes)}, LEDs: {len(device.leds)}")
    except Exception as e:
        print(f"Error listing devices: {e}")

def main():
    parser = argparse.ArgumentParser(description="OpenRGB Profile Manager")
    parser.add_argument("--host", default="127.0.0.1", help="OpenRGB server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=6742, help="OpenRGB server port (default: 6742)")
    
    # Action group - only one action at a time
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--load", metavar="PROFILE_NAME", help="Load a profile")
    action_group.add_argument("--save", metavar="PROFILE_NAME", help="Save current state as profile")
    action_group.add_argument("--delete", metavar="PROFILE_NAME", help="Delete a profile")
    action_group.add_argument("--list-profiles", action="store_true", help="List available profiles")
    action_group.add_argument("--list-devices", action="store_true", help="List connected RGB devices")
    
    args = parser.parse_args()
    
    # Connect to OpenRGB server
    client = connect_to_server(args.host, args.port)
    if not client:
        sys.exit(1)
    
    try:
        # Execute the requested action
        if args.load:
            success = load_profile(client, args.load)
        elif args.save:
            success = save_current_as_profile(client, args.save)
        elif args.delete:
            success = delete_profile(client, args.delete)
        elif args.list_profiles:
            list_profiles(client)
            success = True
        elif args.list_devices:
            list_devices(client)
            success = True
        else:
            success = False
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    finally:
        # Clean up connection
        try:
            client.disconnect()
        except:
            pass

if __name__ == "__main__":
    main()
