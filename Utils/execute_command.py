import re
import subprocess
import threading


class CommonProcess:
    def __init__(self):
        self.execute_file_path = None
        self.arguments = None
        self.error_flags = []
        self.errors = ""
        self.outputs = ""
        self.working_directory = None
        self.time_out = 300
        self.process = None
        self.process_thread = None

    def run(self, file_name=None, arguments=None, error_flags=None):
        if file_name:
            self.execute_file_path = file_name
        if arguments:
            self.arguments = arguments
        if error_flags:
            self.error_flags = error_flags

        if not self.execute_file_path:
            raise Exception("请设置要执行的程序文件路径")

        def read_output():
            while True:

                try:
                    output = self.process.stdout.readline().decode("utf-8")
                except Exception as e:
                    self.errors += str(e)
                    self.on_error_changed(str(e))

                if output == '' and self.process.poll() is not None:
                    break

                if error_flags in output and output != '':
                    self.errors += output
                    self.on_error_changed(output)
                else:
                    self.outputs += output
                    self.on_output_changed(output)

        def read_error():
            while True:
                try:
                    error = self.process.stderr.readline().decode("utf-8")
                except Exception as e:
                    self.errors += str(e)
                    self.on_error_changed(str(e))
                    error = "Error reading error output"

                if error == '' and self.process.poll() is not None:
                    break

                if error_flags in error and error != '' and error != b'':
                    self.errors += error
                    self.on_error_changed(error)
                else:
                    self.outputs += error
                    self.on_output_changed(error)

        try:
            if arguments is None or arguments == "":
                self.process = subprocess.Popen(self.execute_file_path,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                cwd=self.working_directory)
            else:
                self.process = subprocess.Popen([self.execute_file_path, self.arguments],
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                cwd=self.working_directory)

            stdout_thread = threading.Thread(target=read_output)
            stderr_thread = threading.Thread(target=read_error)

            stdout_thread.start()
            stderr_thread.start()

            stdout_thread.join()
            stderr_thread.join()

            self.process.wait(timeout=self.time_out)

            if self.process.returncode is None:
                self.process.kill()
                self.errors += f"超出最大允许的模拟时长：{self.time_out}秒"
                self.on_error_changed(f"超出最大允许的模拟时长：{self.time_out}秒")

        except Exception as e:
            self.errors += str(e)
            self.on_error_changed(str(e))

    def on_output_changed(self, output):
        # 打开文件以进行写入（如果文件不存在，则创建一个新文件）
        file = open("example.txt", "a")
        if str(output.strip()) != '' and output != b'':
            print("Output:", output.strip())
            # 将数据写入文件
            file.write(output.strip() + "\n")
        file.close()

    def on_error_changed(self, error):
        if str(error.strip()) != '' and error != b'':
            print("Error:", error.strip())
            # 发生错误时停止进程
            self.process.kill()

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.kill()
            self.process.wait()

    def wait(self):
        if self.process_thread:
            self.process_thread.join()
