from ipykernel.kernelbase import Kernel
import pexpect
import os
import time

class KapKernel(Kernel):
    implementation = 'Kap'
    implementation_version = '1.0'
    language = 'kap'
    language_info = {
        'name': 'kap',
        'mimetype': 'text/x-apl',
        'file_extension': '.kap',
        'codemirror_mode': 'apl',
    }
    banner = "Kap Native CLI Kernel"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # --- PATH CONFIGURATION ---
        # Change this to your absolute project path
        wd = '/home/theb/Documents/kodaus/array/kap-jupyter-kernel' 
        
        # Construct absolute paths using the wd variable
        kap_executable = os.path.join(wd, 'bin', 'kap-cli')
        lib_path = os.path.join(wd, 'standard-lib')
        debug_log_path = os.path.join(wd, 'kap_debug.log')
        
        command = f'{kap_executable} --lib-path={lib_path}'
        # --------------------------

        # Start the process
        self.kap_process = pexpect.spawn(command, encoding='utf-8', timeout=None)
        
        # Write debug logs to the wd directory
        self.kap_process.logfile = open(debug_log_path, "w")
        
        # Wait for the prompt character you identified
        self.kap_process.expect('⊢') 


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [], 'user_expressions': {}}

        # 1. FLUSH: Clear out any leftover data from a previous crash or timeout
        try:
            while self.kap_process.expect(['.+', pexpect.TIMEOUT], timeout=0) == 0:
                pass
        except:
            pass

        # 2. PRE-PROCESS: Flatten multiline { } blocks with ⋄
        import re
        def flatten_block(match):
            content = match.group(0)[1:-1]
            lines = [l.split('⍝')[0].strip() for l in content.splitlines()]
            return f"{{ {' ⋄ '.join([l for l in lines if l])} }}"
        
        processed_code = re.sub(r'\{[^{}]*\}', flatten_block, code, flags=re.DOTALL)
        lines = processed_code.splitlines()
        
        full_output = []

        for line in lines:
            clean_raw = line.split('⍝')[0].strip()
            if not clean_raw:
                continue
            
            # Send the line
            self.kap_process.sendline(clean_raw)
            
            # Wait for the prompt ⊢
            # We use a regex to ensure it's a prompt at the start of a line
            index = self.kap_process.expect([r'\r?\n⊢', pexpect.TIMEOUT], timeout=5)
            
            if index == 0:
                # Capture everything between the command and the prompt
                raw_output = self.kap_process.before.strip()
                output_lines = raw_output.splitlines()
                
                # STRIP ECHO: Only keep the output if it's not the command itself
                # REPLs echo back your command; we skip that first line
                if output_lines and (clean_raw in output_lines[0] or output_lines[0] in clean_raw):
                    clean_output = "\n".join(output_lines[1:]).strip()
                else:
                    clean_output = raw_output.strip()

                # Don't collect the Zilde (⍬) or empty results
                if clean_output and clean_output != '⍬':
                    full_output.append(clean_output)
            else:
                full_output.append(f"TIMEOUT ERROR: Kap didn't respond to: {clean_raw}")

        # 3. DISPLAY: Join all collected outputs and send to Jupyter
        if not silent and full_output:
            final_display = "\n".join(full_output)
            stream_content = {'name': 'stdout', 'text': final_display}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=KapKernel)
