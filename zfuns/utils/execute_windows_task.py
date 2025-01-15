import winrm


def execute_windows_task(cmd, ip, user, password):
    """Execute a task on a remote Windows machine.

    Args:
        cmd (str): The command to execute.
        ip (str): The IP address of the remote machine.
        user (str): The username that can log in.
        password (str): The password for the user.

    Returns:
        tuple: A tuple containing the standard output and standard error of the command.
    """
    session = winrm.Session(f"http://{ip}:5985/wsman", auth=(user, password))
    result = session.run_cmd(cmd)
    output = result.std_out.decode("gbk")
    error = result.std_err.decode("gbk")
    return output, error
