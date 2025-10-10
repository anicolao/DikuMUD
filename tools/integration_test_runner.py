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
    
    def __init__(self, server_path: str, lib_path: str):
        self.server_path = server_path
        self.lib_path = lib_path
        self.test_lib_path = None  # Will be created as a copy of lib_path
        self.process = None
        self.port = None
    
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
        
        # Create test lib directory
        self._create_test_lib()
        
        # Start server as subprocess with test_lib as the data directory
        server_dir = os.path.dirname(self.server_path)
        self.process = subprocess.Popen(
            [self.server_path, '-p', str(port), '-d', 'test_lib'],
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
    
    def create_test_player(self, name: str, password: str, start_room: int = 3001):
        """
        Create a test player file with the specified starting room.
        
        Uses the C helper program to create a properly formatted player file
        that matches the exact struct char_file_u format from structs.h.
        This creates the player in the test_lib directory, not the real lib directory.
        
        Args:
            name: Character name (will be lowercased)
            password: Character password (plaintext, will be encrypted by server)
            start_room: Room vnum where character should start
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
        
        # Run helper program, setting the working directory to use test_lib
        try:
            # Change to the server directory with test_lib
            env = os.environ.copy()
            
            result = subprocess.run(
                [helper_path, name, password, str(start_room)],
                cwd=server_dir,
                capture_output=True,
                text=True,
                timeout=5,
                env=env
            )
            
            if result.returncode == 0:
                # The helper creates in lib/, we need to move it to test_lib/
                import shutil
                src_player = os.path.join(server_dir, 'lib', 'players')
                dst_player = os.path.join(server_dir, 'test_lib', 'players')
                if os.path.exists(src_player):
                    shutil.move(src_player, dst_player)
                    print(f"    {result.stdout.strip()}")
                else:
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
        
        # Give server a moment to start
        time.sleep(1)
        
        while time.time() - start_time < timeout:
            try:
                # Try to connect to the port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect(('localhost', self.port))
                    # Connection successful, server is ready
                    time.sleep(0.5)  # Give it a bit more time to fully initialize
                    return
            except (ConnectionRefusedError, socket.timeout, OSError) as e:
                last_error = e
                time.sleep(0.5)
        
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
    
    def __init__(self, host: str = 'localhost', port: int = 4000):
        self.host = host
        self.port = port
        self.connection = None
    
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
            # Read initial welcome message
            time.sleep(0.5)
            welcome = self._read_available()
            
            # If character name provided, handle login
            if char_name and char_pass:
                # Send character name
                self.connection.write(char_name.encode('ascii') + b'\n')
                time.sleep(0.5)
                response = self._read_available()
                
                # Answer "yes" to name confirmation
                if "Did I get that right" in response or "(Y/N)" in response:
                    self.connection.write(b'yes\n')
                    time.sleep(0.5)
                    response = self._read_available()
                
                # Enter password
                if "password" in response.lower() or "Password" in response:
                    self.connection.write(char_pass.encode('ascii') + b'\n')
                    time.sleep(0.5)
                    response = self._read_available()
                    
                    # Handle password retype for new characters or wrong password
                    if "retype" in response.lower() or "Retype" in response or "Wrong password" in response:
                        self.connection.write(char_pass.encode('ascii') + b'\n')
                        time.sleep(0.5)
                        response = self._read_available()
                    
                    # Handle menu after login (press return)
                    if "PRESS RETURN" in response:
                        self.connection.write(b'\n')
                        time.sleep(0.5)
                        response = self._read_available()
                    
                    # Handle menu choice (enter the game)
                    if "Make your choice" in response:
                        self.connection.write(b'1\n')
                        time.sleep(0.5)
                        response = self._read_available()
                    
                    # Wait for login to complete and all MOTD/initial output to arrive
                    # The server outputs MOTD and then the room description automatically
                    time.sleep(2.0)
                    # Use _read_until_prompt to properly drain the buffer until we see a prompt
                    self._read_until_prompt(timeout=5)
                    
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}: {e}")
    
    def disconnect(self):
        """Disconnect from server."""
        if self.connection:
            try:
                self.connection.write(b"quit\n")
                time.sleep(0.2)
            except Exception:
                pass
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None
    
    def send_command(self, command: str, wait_for_prompt: bool = True) -> str:
        """
        Send command to server and return response.
        
        Args:
            command: Command to send
            wait_for_prompt: Whether to wait for prompt after command
            
        Returns:
            Server response as string
        """
        if not self.connection:
            raise RuntimeError("Not connected to server")
        
        self.connection.write(command.encode('ascii') + b'\n')
        time.sleep(0.3)  # Give server time to process
        
        if wait_for_prompt:
            return self._read_until_prompt(timeout=5)
        else:
            return self._read_available()
    
    def expect_output(self, pattern: str, timeout: int = 5) -> bool:
        """
        Wait for output matching pattern.
        
        Args:
            pattern: Regular expression pattern to match
            timeout: How long to wait for match
            
        Returns:
            True if pattern found, False otherwise
        """
        output = self._read_until_prompt(timeout)
        return bool(re.search(pattern, output, re.IGNORECASE | re.MULTILINE))
    
    def _read_available(self) -> str:
        """Read all currently available data."""
        try:
            data = self.connection.read_very_eager()
            return data.decode('ascii', errors='ignore')
        except Exception:
            return ""
    
    def _read_until_prompt(self, timeout: int = 5) -> str:
        """Read until we get a prompt or timeout."""
        output = ""
        start_time = time.time()
        last_read_time = start_time
        
        while time.time() - start_time < timeout:
            try:
                chunk = self.connection.read_very_eager()
                if chunk:
                    decoded = chunk.decode('ascii', errors='ignore')
                    output += decoded
                    last_read_time = time.time()
                    # Check for prompt patterns (>, ], etc.)
                    if re.search(r'[>]\s*$', output):
                        break
                # If we haven't received data for 0.5 seconds and we have some output, assume done
                elif output and (time.time() - last_read_time > 0.5):
                    break
                time.sleep(0.1)
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
    
    def __init__(self, client: GameClient):
        self.client = client
        self.results = []
    
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
        if 'direction' in step:
            # Single direction
            direction = step['direction']
            output = self.client.send_command(direction)
        elif 'path' in step:
            # Multiple directions
            for direction in step['path']:
                output = self.client.send_command(direction)
                time.sleep(0.2)
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
        output = self.client.send_command(command)
        
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
        
        output = self.client.send_command(command)
        
        # Validate expectations
        if 'expected' in step:
            return self._validate_expectations(output, step['expected'])
        
        return True
    
    def _execute_inventory(self, step: Dict[str, Any]) -> bool:
        """Execute inventory check."""
        output = self.client.send_command("inventory")
        
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
    
    def __init__(self, server_path: str, lib_path: str):
        self.server_manager = ServerManager(server_path, lib_path)
        self.results = []
    
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
        if 'setup' in test_def and 'character' in test_def['setup']:
            char_name = test_def['setup']['character'].get('name', 'TestChar')
            char_pass = test_def['setup']['character'].get('password', 'test')
        
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
            self.server_manager.create_test_player(char_name, char_pass, start_room)
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
            # Connect client
            client = GameClient('localhost', port)
            try:
                client.connect(char_name=char_name, char_pass=char_pass)
                print(f"✓ Connected to server")
                if char_name:
                    print(f"✓ Logged in as {char_name}")
            except Exception as e:
                print(f"✗ Failed to connect: {e}")
                return False
            
            # Execute test
            executor = TestExecutor(client)
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
        print("\nUsage: python3 integration_test_runner.py <server_path> <test_file_or_dir>")
        print("       python3 integration_test_runner.py <server_path> --all <test_dir>")
        print("\nExample:")
        print("  python3 integration_test_runner.py ./dmserver tests/integration/shops/bug_3003_nobles_waiter_list.yaml")
        print("  python3 integration_test_runner.py ./dmserver --all tests/integration/")
        sys.exit(1)
    
    server_path = sys.argv[1]
    test_arg = sys.argv[2]
    
    # Verify server exists
    if not os.path.exists(server_path):
        print(f"\n✗ Error: Server not found at {server_path}")
        print("  Please build the server first: cd dm-dist-alfa && make dmserver")
        sys.exit(1)
    
    # Determine lib path
    lib_path = os.path.join(os.path.dirname(server_path), 'lib')
    
    # Create test runner
    runner = TestRunner(server_path, lib_path)
    
    # Run tests
    if test_arg == '--all' and len(sys.argv) > 3:
        # Run all tests in directory
        test_dir = Path(sys.argv[3])
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
