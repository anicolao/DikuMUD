#!/usr/bin/env python3
"""
Integration Test Runner for DikuMUD

This module provides automated testing of DikuMUD functionality by:
1. Starting a DikuMUD server
2. Connecting as a virtual player via telnet
3. Executing test commands
4. Validating expected outcomes
5. Reporting results

Usage:
    python3 integration_test_runner.py test_file.yaml
    python3 integration_test_runner.py --all tests/integration/
"""

import sys
import subprocess
import socket
import time
import re
import yaml
import telnetlib
import signal
import os
import struct
from pathlib import Path
from typing import Dict, List, Optional, Any


class ServerManager:
    """
    Manages DikuMUD server lifecycle for testing.
    
    Responsibilities:
    - Start server on random or specified port
    - Wait for server to be ready
    - Stop server gracefully
    - Clean up test artifacts
    """
    
    def __init__(self, server_path: str, lib_path: str, spin_mode: bool = True):
        self.server_path = server_path
        self.lib_path = lib_path
        self.test_lib_path = None  # Will be created as a copy of lib_path
        self.process = None
        self.port = None
        self.spin_mode = spin_mode  # Enable spin mode for faster testing
    
    def _create_test_lib(self):
        """Create a test copy of the lib directory to avoid modifying real game assets."""
        import shutil
        
        # Create test_lib directory
        server_dir = os.path.dirname(self.server_path)
        self.test_lib_path = os.path.join(server_dir, 'test_lib')
        
        # Remove if it already exists
        if os.path.exists(self.test_lib_path):
            shutil.rmtree(self.test_lib_path)
        
        # Copy lib directory to test_lib
        shutil.copytree(self.lib_path, self.test_lib_path)
        
    def start(self, port: Optional[int] = None) -> int:
        """
        Start DikuMUD server.
        
        Args:
            port: Port to use, or None for random port
            
        Returns:
            The port number the server is listening on
            
        Raises:
            RuntimeError: If server fails to start
        """
        if port is None:
            port = self._find_free_port()
        
        # Create test lib directory (if not already created by create_test_player)
        if not self.test_lib_path:
            self._create_test_lib()
        
        # Start server as subprocess with test_lib as the data directory
        server_dir = os.path.dirname(self.server_path)
        cmd = [self.server_path, '-p', str(port), '-d', 'test_lib']
        if self.spin_mode:
            cmd.append('-spin')  # Enable spin mode for maximum speed
        self.process = subprocess.Popen(
            cmd,
            cwd=server_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group for clean shutdown
        )
        
        self.port = port
        
        # Wait for server to be ready
        self._wait_for_startup(timeout=15)
        
        return port
    
    def stop(self):
        """Stop the server gracefully."""
        if self.process:
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if necessary
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                self.process.wait()
            except ProcessLookupError:
                # Process already dead
                pass
            self.process = None
    
    def create_test_player(self, name: str, password: str, start_room: int = 3001, level: int = 1):
        """
        Create a test player file with the specified starting room.
        
        Uses the C helper program to create a properly formatted player file
        that matches the exact struct char_file_u format from structs.h.
        This creates the player in the test_lib directory, not the real lib directory.
        
        Args:
            name: Character name (will be lowercased)
            password: Character password (plaintext, will be encrypted by server)
            start_room: Room vnum where character should start
            level: Character level (default: 1)
        """
        # Create test_lib first if not already created
        if not self.test_lib_path:
            self._create_test_lib()
        
        server_dir = os.path.dirname(self.server_path)
        helper_path = os.path.join(os.path.dirname(__file__), 'create_test_player')
        
        # Check if helper program exists
        if not os.path.exists(helper_path):
            print(f"    ! Warning: Helper program not found at {helper_path}")
            print(f"    ! Build it with: cd dm-dist-alfa && make ../tools/create_test_player")
            return
        
        # Run helper program with -d parameter to write directly to test_lib
        try:
            env = os.environ.copy()
            
            # Build command with optional level parameter
            cmd = [helper_path, '-d', self.test_lib_path]
            if level > 1:
                cmd.extend(['-l', str(level)])
            cmd.extend([name, password, str(start_room)])
            
            result = subprocess.run(
                cmd,
                cwd=server_dir,
                capture_output=True,
                text=True,
                timeout=5,
                env=env
            )
            
            if result.returncode == 0:
                print(f"    {result.stdout.strip()}")
            else:
                print(f"    ! Error creating player file: {result.stderr}")
        except Exception as e:
            print(f"    ! Exception creating player file: {e}")
    
    def cleanup(self):
        """Clean up test artifacts (test_lib directory, etc.)."""
        import shutil
        
        # Remove the entire test_lib directory
        if self.test_lib_path and os.path.exists(self.test_lib_path):
            try:
                shutil.rmtree(self.test_lib_path)
            except Exception as e:
                print(f"    ! Warning: Failed to clean up test_lib: {e}")
        
        self.test_lib_path = None
    
    def _find_free_port(self) -> int:
        """Find an available port for the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def _wait_for_startup(self, timeout: int = 10):
        """Wait for server to be ready to accept connections."""
        start_time = time.time()
        last_error = None
        
        while time.time() - start_time < timeout:
            try:
                # Try to connect to the port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect(('localhost', self.port))
                    # Connection successful, server is ready
                    return
            except (ConnectionRefusedError, socket.timeout, OSError) as e:
                last_error = e
                time.sleep(0.01)  # Minimal wait between retries
        
        # Try to get server output if available
        error_msg = f"Server failed to start within {timeout} seconds"
        if self.process and self.process.poll() is not None:
            stderr = self.process.stderr.read() if self.process.stderr else b""
            if stderr:
                error_msg += f"\nServer error: {stderr.decode('utf-8', errors='ignore')}"
        if last_error:
            error_msg += f"\nLast connection error: {last_error}"
        
        raise RuntimeError(error_msg)


class GameClient:
    """
    Handles telnet communication with DikuMUD server.
    
    Responsibilities:
    - Connect to server
    - Send commands
    - Read responses
    - Handle prompts and output
    """
    
    def __init__(self, host: str = 'localhost', port: int = 4000, spin_mode: bool = True):
        self.host = host
        self.port = port
        self.connection = None
        self.spin_mode = spin_mode
        # Set idle timeout for spin mode - very small for maximum speed
        self.idle_timeout = 0.001
    
    def connect(self, timeout: int = 10, char_name: str = None, char_pass: str = None):
        """
        Connect to game server and optionally login.
        
        Args:
            timeout: Connection timeout in seconds
            char_name: Character name for login (optional)
            char_pass: Character password for login (optional)
            
        Raises:
            ConnectionError: If connection fails
        """
        try:
            self.connection = telnetlib.Telnet(self.host, self.port, timeout)
            
            # If character name provided, handle login
            # We know the exact sequence: username, password, 1 (for PRESS RETURN), 1 (for menu)
            # Send all inputs at once - the first '1' gets consumed by PRESS RETURN prompt,
            # the second '1' triggers menu selection. This avoids the empty line issue where
            # consecutive newlines get skipped by the server's input processing.
            if char_name and char_pass:
                # Send all commands in a single write to test buffering
                login_sequence = (
                    char_name.encode('ascii') + b'\n' +
                    char_pass.encode('ascii') + b'\n' +
                    b'1\n' +  # PRESS RETURN (any input works, server just waits for newline)
                    b'1\n'    # Menu choice
                )
                self.connection.write(login_sequence)
                
                # Now read until we get the game prompt
                # This will consume all the welcome messages, MOTD, and room description
                self._read_until_prompt(timeout=15)
                
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}: {e}")
    
    def disconnect(self):
        """Disconnect from server."""
        if self.connection:
            try:
                self.connection.write(b"quit\n")
                # No sleep needed - close will flush and disconnect
            except Exception:
                pass
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None
    
    def send_command(self, command: str, wait_for_prompt: bool = True) -> str:
        """
        Send command to server (without reading response).
        
        Args:
            command: Command to send
            wait_for_prompt: Ignored (kept for backwards compatibility)
            
        Returns:
            Empty string (use expect_output to read and validate responses)
        """
        if not self.connection:
            raise RuntimeError("Not connected to server")
        
        self.connection.write(command.encode('ascii') + b'\n')
        # Don't read here - let expect_output handle reading
        return ""
    
    def expect_output(self, pattern: str, timeout: int = 30, retries: int = 3) -> bool:
        """
        Wait for output matching pattern (with retries for robustness).
        
        Args:
            pattern: Regular expression pattern to match
            timeout: How long to wait for match
            retries: Number of times to retry reading if pattern not found
            
        Returns:
            True if pattern found, False otherwise
        """
        for attempt in range(retries):
            output = self._read_until_prompt(timeout)
            if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
                return True
            # If not found and retries left, wait a bit and try again
            if attempt < retries - 1:
                time.sleep(0.1)
        return False
    
    def _read_available(self) -> str:
        """Read all currently available data."""
        try:
            data = self.connection.read_very_eager()
            return data.decode('ascii', errors='ignore')
        except Exception:
            return ""
    
    def _read_until_prompt(self, timeout: int = 30) -> str:
        """Read until we get a prompt."""
        output = ""
        start_time = time.time()
        last_read_time = start_time
        
        while time.time() - start_time < timeout:
            try:
                chunk = self.connection.read_very_eager()
                if chunk:
                    decoded = chunk.decode('ascii', errors='ignore')
                    # Debug output for troubleshooting
                    import os
                    if os.getenv('DEBUG_OUTPUT'):
                        print(decoded, end='', flush=True)
                    output += decoded
                    last_read_time = time.time()
                    # Check for prompt patterns (>, ], etc.)
                    if re.search(r'[>]\s*$', output):
                        break
                else:
                    # No data - if we have output with a prompt, we're done
                    if output and re.search(r'[>]\s*$', output):
                        break
                    # If we haven't received data for a bit and have output, check if done
                    if output and (time.time() - last_read_time > 0.5):
                        # Give it one more chance to see if prompt arrives
                        time.sleep(0.1)
                        chunk = self.connection.read_very_eager()
                        if chunk:
                            decoded = chunk.decode('ascii', errors='ignore')
                            output += decoded
                            last_read_time = time.time()
                            if re.search(r'[>]\s*$', output):
                                break
                        else:
                            # Still no data, we're probably done
                            break
                
                # Smaller sleep for faster response
                time.sleep(0.001 if self.spin_mode else 0.01)
            except Exception:
                break
        
        return output


class TestExecutor:
    """
    Executes test steps and validates results.
    
    Responsibilities:
    - Parse YAML test files
    - Execute test actions
    - Validate expectations
    - Report results
    """
    
    def __init__(self, client: GameClient, show_all_output: bool = False):
        self.client = client
        self.results = []
        self.show_all_output = show_all_output
    
    def load_test(self, test_file: Path) -> Dict[str, Any]:
        """
        Load test from YAML file.
        
        Args:
            test_file: Path to YAML test file
            
        Returns:
            Test definition dictionary
        """
        with open(test_file, 'r') as f:
            return yaml.safe_load(f)
    
    def execute_test(self, test_def: Dict[str, Any]) -> bool:
        """
        Execute a complete test.
        
        Args:
            test_def: Test definition from YAML
            
        Returns:
            True if test passed, False otherwise
        """
        print(f"\nRunning test: {test_def['test']['id']}")
        print(f"Description: {test_def['test']['description']}")
        
        # Setup
        if 'setup' in test_def:
            self._execute_setup(test_def['setup'])
        
        # Execute steps
        all_passed = True
        for i, step in enumerate(test_def.get('steps', []), 1):
            print(f"  Step {i}: {step.get('description', step['action'])}")
            if not self._execute_step(step):
                all_passed = False
                break
        
        # Cleanup
        if 'cleanup' in test_def:
            self._execute_cleanup(test_def['cleanup'])
        
        return all_passed
    
    def _execute_setup(self, setup: Dict[str, Any]):
        """Execute test setup."""
        # For now, setup is mostly informational
        # Character creation happens automatically when connecting
        # Starting room and gold would need to be set via game commands
        # which we skip for simplicity in this implementation
        pass
    
    def _execute_step(self, step: Dict[str, Any]) -> bool:
        """
        Execute a single test step.
        
        Args:
            step: Step definition
            
        Returns:
            True if step passed, False otherwise
        """
        action = step['action']
        
        if action == 'move':
            return self._execute_move(step)
        elif action == 'command':
            return self._execute_command(step)
        elif action == 'look':
            return self._execute_look(step)
        elif action == 'inventory':
            return self._execute_inventory(step)
        else:
            print(f"    ! Unknown action: {action}")
            return False
    
    def _execute_move(self, step: Dict[str, Any]) -> bool:
        """Execute movement action."""
        output = ""
        if 'direction' in step:
            # Single direction
            direction = step['direction']
            self.client.send_command(direction)
            output = self.client._read_until_prompt(timeout=30)
        elif 'path' in step:
            # Multiple directions
            for direction in step['path']:
                self.client.send_command(direction)
                output = self.client._read_until_prompt(timeout=30)
        elif 'target_room' in step:
            # Target room specified - for now we just skip
            # In full implementation, would pathfind to target
            print(f"    - Moving to target room {step['target_room']} (skipped - pathfinding not implemented)")
            # Since we can't actually move to target room, skip validation
            return True
        else:
            print("    ✗ Move action requires 'direction', 'path', or 'target_room'")
            return False
        
        # Validate expectations if present (only for actual movement)
        if 'expected' in step and 'target_room' not in step:
            return self._validate_expectations(output, step['expected'])
        return True
    
    def _execute_command(self, step: Dict[str, Any]) -> bool:
        """Execute general command."""
        command = step['command']
        self.client.send_command(command)
        
        # Read the output
        output = self.client._read_until_prompt(timeout=30)
        
        # Show all output if flag is set
        if self.show_all_output:
            print(f"\n    === Command Output ===")
            print(f"    Command: {command}")
            print(f"    Output:\n{output}")
            print(f"    === End Output ===\n")
        
        # Check fail_on conditions first
        if 'fail_on' in step:
            for fail_condition in step['fail_on']:
                pattern = fail_condition['pattern']
                if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
                    print(f"    ✗ FAILED: {fail_condition.get('message', 'Fail condition matched')}")
                    return False
        
        # Validate expectations
        if 'expected' in step:
            return self._validate_expectations(output, step['expected'])
        
        return True
    
    def _execute_look(self, step: Dict[str, Any]) -> bool:
        """Execute look action."""
        target = step.get('target', '')
        if target:
            command = f"look {target}"
        else:
            command = "look"
        
        self.client.send_command(command)
        output = self.client._read_until_prompt(timeout=30)
        
        # Show all output if flag is set
        if self.show_all_output:
            print(f"\n    === Command Output ===")
            print(f"    Command: {command}")
            print(f"    Output:\n{output}")
            print(f"    === End Output ===\n")
        
        # Validate expectations
        if 'expected' in step:
            return self._validate_expectations(output, step['expected'])
        
        return True
    
    def _execute_inventory(self, step: Dict[str, Any]) -> bool:
        """Execute inventory check."""
        self.client.send_command("inventory")
        output = self.client._read_until_prompt(timeout=30)
        
        # Validate expectations
        if 'expected' in step:
            return self._validate_expectations(output, step['expected'])
        
        return True
    
    def _execute_cleanup(self, cleanup: Dict[str, Any]):
        """Execute test cleanup."""
        # Cleanup is minimal - just disconnect
        # Character removal would need admin commands
        pass
    
    def _validate_expectations(self, output: str, expectations: List[Dict]) -> bool:
        """
        Validate output matches expectations.
        
        Args:
            output: Server output to validate
            expectations: List of expectation patterns
            
        Returns:
            True if all expectations met
        """
        all_passed = True
        for expectation in expectations:
            pattern = expectation['pattern']
            optional = expectation.get('optional', False)
            
            if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
                print(f"    ✓ {expectation.get('message', 'Pattern matched')}")
            else:
                if not optional:
                    print(f"    ✗ FAILED: {expectation.get('message', 'Pattern not found')}")
                    # Debug: show first 200 chars of output
                    debug_output = output[:200].replace('\n', '\\n').replace('\r', '\\r')
                    print(f"      Output preview: {debug_output}...")
                    all_passed = False
                else:
                    print(f"    - {expectation.get('message', 'Optional pattern not found')} (optional)")
        
        return all_passed


class TestRunner:
    """
    Main test runner that coordinates all components.
    
    Responsibilities:
    - Discover tests
    - Manage server lifecycle
    - Execute tests
    - Generate reports
    """
    
    def __init__(self, server_path: str, lib_path: str, show_all_output: bool = False, spin_mode: bool = True):
        self.server_manager = ServerManager(server_path, lib_path, spin_mode=spin_mode)
        self.results = []
        self.show_all_output = show_all_output
        self.spin_mode = spin_mode
    
    def run_test_file(self, test_file: Path, verbose: bool = False) -> bool:
        """
        Run a single test file.
        
        Args:
            test_file: Path to test YAML file
            verbose: Show detailed output
            
        Returns:
            True if test passed
        """
        print(f"\n{'='*50}")
        print(f"Test file: {test_file.name}")
        print('='*50)
        
        # Load test definition first to check for setup requirements
        try:
            with open(test_file, 'r') as f:
                test_def = yaml.safe_load(f)
        except Exception as e:
            print(f"✗ Failed to load test file: {e}")
            return False
        
        # Get character info from setup
        char_name = None
        char_pass = None
        char_level = 1
        if 'setup' in test_def and 'character' in test_def['setup']:
            char_name = test_def['setup']['character'].get('name', 'TestChar')
            char_pass = test_def['setup']['character'].get('password', 'test')
            char_level = test_def['setup']['character'].get('level', 1)
        
        # start_room is REQUIRED - all tests must specify where the character starts
        if 'setup' not in test_def or 'start_room' not in test_def['setup']:
            print(f"✗ Test error: 'start_room' is required in setup section")
            print(f"   Add 'start_room: <vnum>' to the setup section of your test")
            return False
        
        start_room = test_def['setup']['start_room']
        if not char_name:
            char_name = 'TestChar'
        if not char_pass:
            char_pass = 'test'
        
        try:
            self.server_manager.create_test_player(char_name, char_pass, start_room, char_level)
        except Exception as e:
            print(f"✗ Failed to create test player: {e}")
            return False
        
        # Start server
        try:
            port = self.server_manager.start()
            print(f"✓ Server started on port {port}")
        except Exception as e:
            print(f"✗ Failed to start server: {e}")
            return False
        
        try:
            # Connect client with spin mode enabled
            client = GameClient('localhost', port, spin_mode=self.spin_mode)
            try:
                client.connect(char_name=char_name, char_pass=char_pass)
                print(f"✓ Connected to server")
                if char_name:
                    print(f"✓ Logged in as {char_name}")
            except Exception as e:
                print(f"✗ Failed to connect: {e}")
                return False
            
            # Execute test
            executor = TestExecutor(client, show_all_output=self.show_all_output)
            try:
                passed = executor.execute_test(test_def)
            except Exception as e:
                print(f"✗ Test execution failed: {e}")
                if verbose:
                    import traceback
                    traceback.print_exc()
                passed = False
            
            # Disconnect
            client.disconnect()
            
            return passed
            
        finally:
            # Stop server
            try:
                self.server_manager.stop()
                print(f"✓ Server stopped")
            except Exception as e:
                if verbose:
                    print(f"! Warning: Server stop had issues: {e}")
            
            self.server_manager.cleanup()
    
    def run_all_tests(self, test_dir: Path) -> Dict[str, Any]:
        """
        Run all tests in directory.
        
        Args:
            test_dir: Directory containing test files
            
        Returns:
            Summary of results
        """
        test_files = list(test_dir.rglob('*.yaml'))
        
        passed = 0
        failed = 0
        
        for test_file in test_files:
            if self.run_test_file(test_file):
                passed += 1
            else:
                failed += 1
        
        return {
            'total': len(test_files),
            'passed': passed,
            'failed': failed
        }
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test results summary."""
        print("\n" + "="*50)
        print("Test Results Summary")
        print("="*50)
        print(f"Total:  {results['total']}")
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")
        
        if results['failed'] == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ {results['failed']} test(s) failed")


def main():
    """Main entry point."""
    print("="*50)
    print("DikuMUD Integration Test Runner")
    print("="*50)
    
    # Parse arguments
    if len(sys.argv) < 3:
        print("\nUsage: python3 integration_test_runner.py [--show-all-output] <server_path> <test_file_or_dir>")
        print("       python3 integration_test_runner.py [--show-all-output] <server_path> --all <test_dir>")
        print("\nOptions:")
        print("  --show-all-output    Show all command output from the game server")
        print("\nExample:")
        print("  python3 integration_test_runner.py ./dmserver tests/integration/shops/bug_3003_nobles_waiter_list.yaml")
        print("  python3 integration_test_runner.py ./dmserver --all tests/integration/")
        print("  python3 integration_test_runner.py --show-all-output ./dmserver --all tests/integration/")
        sys.exit(1)
    
    # Check for --show-all-output flag
    show_all_output = False
    arg_offset = 1
    if sys.argv[1] == '--show-all-output':
        show_all_output = True
        arg_offset = 2
        if len(sys.argv) < 4:
            print("\n✗ Error: Not enough arguments")
            print("Usage: python3 integration_test_runner.py [--show-all-output] <server_path> <test_file_or_dir>")
            sys.exit(1)
    
    server_path = sys.argv[arg_offset]
    test_arg = sys.argv[arg_offset + 1]
    
    # Verify server exists
    if not os.path.exists(server_path):
        print(f"\n✗ Error: Server not found at {server_path}")
        print("  Please build the server first: cd dm-dist-alfa && make dmserver")
        sys.exit(1)
    
    # Determine lib path
    lib_path = os.path.join(os.path.dirname(server_path), 'lib')
    
    # Create test runner
    runner = TestRunner(server_path, lib_path, show_all_output=show_all_output)
    
    # Run tests
    if test_arg == '--all' and len(sys.argv) > arg_offset + 2:
        # Run all tests in directory
        test_dir = Path(sys.argv[arg_offset + 2])
        if not test_dir.exists():
            print(f"\n✗ Error: Test directory not found: {test_dir}")
            sys.exit(1)
        
        results = runner.run_all_tests(test_dir)
        runner.print_summary(results)
        sys.exit(0 if results['failed'] == 0 else 1)
    else:
        # Run single test
        test_file = Path(test_arg)
        if not test_file.exists():
            print(f"\n✗ Error: Test file not found: {test_file}")
            sys.exit(1)
        
        passed = runner.run_test_file(test_file)
        
        if passed:
            print("\n" + "="*50)
            print("✅ Test PASSED")
            print("="*50)
            sys.exit(0)
        else:
            print("\n" + "="*50)
            print("❌ Test FAILED")
            print("="*50)
            sys.exit(1)


if __name__ == '__main__':
    main()
